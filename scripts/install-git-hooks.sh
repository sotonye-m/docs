#!/usr/bin/env bash
# install-git-hooks.sh — Install a post-push git hook that automatically syncs
# changed MDX files to the AI knowledge base after every `git push`.
#
# Run this once per machine:
#   ./scripts/install-git-hooks.sh

set -euo pipefail

DOCS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HOOK_PATH="$DOCS_DIR/.git/hooks/post-push"

cat > "$HOOK_PATH" << 'HOOK'
#!/usr/bin/env bash
# Auto-sync changed MDX files to the AI knowledge base after push.
# Installed by scripts/install-git-hooks.sh

DOCS_DIR="$(git rev-parse --show-toplevel)"
SYNC_SCRIPT="$DOCS_DIR/scripts/sync-ai.sh"

if [ ! -f "$SYNC_SCRIPT" ]; then exit 0; fi

CHANGED=$(git diff --name-only HEAD~1 HEAD 2>/dev/null | grep '\.mdx$' || true)
if [ -z "$CHANGED" ]; then exit 0; fi

echo ""
echo "[AI Sync] $(echo "$CHANGED" | wc -l | tr -d ' ') MDX file(s) changed — syncing to knowledge base..."
bash "$SYNC_SCRIPT" || echo "[AI Sync] Sync failed — run ./scripts/sync-ai.sh manually"
echo "[AI Sync] Done"
HOOK

chmod +x "$HOOK_PATH"

echo "Git hook installed at: $HOOK_PATH"
echo ""
echo "From now on, changed MDX files will automatically sync to MongoDB after every push."
echo "To sync manually: ./scripts/sync-ai.sh"
echo "To force a full rescan: ./scripts/sync-ai.sh --all"
