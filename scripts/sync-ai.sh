#!/usr/bin/env bash
# sync-ai.sh — Push MDX doc changes into the MongoDB AI knowledge base.
#
# Usage:
#   ./scripts/sync-ai.sh              # sync files changed since last commit
#   ./scripts/sync-ai.sh --all        # full rescan (use after big doc restructures)
#   ./scripts/sync-ai.sh --embed      # sync + generate vector embeddings
#   ./scripts/sync-ai.sh --dry-run    # preview without writing to MongoDB
#
# Requirements:
#   MONGODB_URI must be set (loaded from ../cryptoyativo/yativo-crypto/.env if not in env)
#   JINA_API_KEY (optional, free at jina.ai) or OPENAI_EMBEDDING_KEY for vector search

set -euo pipefail

DOCS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CRYPTO_DIR="$(cd "$DOCS_DIR/../cryptoyativo/yativo-crypto" && pwd)"
SYNC_SCRIPT="$CRYPTO_DIR/scripts/sync-knowledge-base.js"

if [ ! -f "$SYNC_SCRIPT" ]; then
  echo "Error: sync script not found at $SYNC_SCRIPT"
  echo "Make sure yativo-crypto is checked out alongside this docs repo."
  exit 1
fi

# Load env from the crypto backend if MONGODB_URI is not already set
if [ -z "${MONGODB_URI:-}" ] && [ -f "$CRYPTO_DIR/.env" ]; then
  set -a; source "$CRYPTO_DIR/.env"; set +a
fi

if [ -z "${MONGODB_URI:-}" ]; then
  echo "Error: MONGODB_URI is not set. Add it to $CRYPTO_DIR/.env or export it."
  exit 1
fi

# Parse flags
MODE="changed"
EXTRA_FLAGS=""

for arg in "$@"; do
  case "$arg" in
    --all)      MODE="all" ;;
    --embed)    EXTRA_FLAGS="$EXTRA_FLAGS --embed" ;;
    --dry-run)  EXTRA_FLAGS="$EXTRA_FLAGS --dry-run" ;;
    *) echo "Unknown flag: $arg"; exit 1 ;;
  esac
done

if [ "$MODE" = "all" ]; then
  echo "Full MDX sync..."
  node "$SYNC_SCRIPT" --docs-dir "$DOCS_DIR" $EXTRA_FLAGS
else
  # Only files changed since the last commit
  CHANGED=$(git -C "$DOCS_DIR" diff --name-only HEAD~1 HEAD 2>/dev/null | grep '\.mdx$' || true)

  if [ -z "$CHANGED" ]; then
    echo "No MDX files changed since last commit. Run with --all to force a full rescan."
    exit 0
  fi

  echo "Changed: $(echo "$CHANGED" | wc -l | tr -d ' ') MDX file(s)"
  # Pass as space-separated list after --changed
  node "$SYNC_SCRIPT" --docs-dir "$DOCS_DIR" --changed $CHANGED $EXTRA_FLAGS
fi
