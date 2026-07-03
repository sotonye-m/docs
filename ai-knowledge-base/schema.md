# Yativo AI Knowledge Base — MongoDB Schema

## Purpose

This knowledge base powers a RAG (retrieval-augmented generation) AI chatbot that answers questions from API integrators and developers about the Yativo platform. It is **not** for internal staff or dashboard users.

When a user asks the AI a question, the pipeline:
1. Embeds the user's question (e.g. via OpenAI `text-embedding-3-small`)
2. Does a vector similarity search against the `content` field embeddings
3. Retrieves the top-K most relevant documents
4. Injects them as context into the LLM prompt
5. The LLM answers grounded in real documentation — no hallucination

---

## Collections

### `knowledge_docs`

Primary collection. All API docs, guides, error references, and support Q&A.

```javascript
{
  _id: "unique-kebab-case-slug",          // e.g. "crypto-auth-token"
  source: "docs" | "support_qa",         // origin of the document
  product: "crypto" | "fiat" | "general",
  version: "v1",
  type: "endpoint" | "concept" | "guide" | "error" | "authentication" | "webhook" | "support_qa",
  category: String,                       // e.g. "transactions", "cards", "iban"
  title: String,                          // human-readable title
  method: "GET" | "POST" | "PUT" | "DELETE" | "PATCH" | null,
  path: String | null,                    // e.g. "/v1/transactions/send-funds"
  baseUrl: String | null,                 // "https://crypto-api.yativo.com/api/v1"
  description: String,                    // markdown-safe description
  auth_required: Boolean,
  auth_type: "bearer" | "api_key" | null,
  request_params: Object | null,          // query params
  request_body: Object | null,            // body fields with types and descriptions
  response_example: Object | null,        // example success response
  errors: Array,                          // [{code, status, description}]
  related: Array,                         // _id slugs of related documents
  tags: Array,                            // semantic tags for filtering
  verified: Boolean,                      // true = confirmed accurate, false = needs review
  content: String,                        // DENSE TEXT FOR EMBEDDING — see below

  // Support Q&A fields (type: "support_qa")
  problem: String,                        // the client's problem description
  resolution: String,                     // what fixed it
  api_endpoints_mentioned: Array,         // endpoint paths that came up
  resolved_at: Date,

  // Metadata
  created_at: Date,
  updated_at: Date,
}
```

---

## The `content` Field (Embedding Target)

The `content` field is concatenated plain text that gets embedded into a vector. It should be dense with:
- Title and category
- Full description
- All parameter names and their descriptions
- Request/response field names and types
- Example values
- Related concept names

**Example**:
```
Send Funds — Transactions — Crypto API
POST /v1/transactions/send-funds
Initiate an outbound crypto transfer. Sends crypto from a wallet to an external address.
Required fields: account (MongoDB ObjectId of the account), assets (MongoDB ObjectId of the source wallet), receiving_address (recipient blockchain address), amount (number in token units), type (token ticker e.g. USDC ETH SOL), chain (blockchain e.g. ethereum solana polygon), category (payment business personal).
Optional: priority (low medium high, default medium), description (note), use_self_funding (boolean for native token gas), idempotency_key.
Response: transaction_id, transaction_hash, gas_amount, platform_fee, gas_funding_markup, total_fee.
Errors: 422 insufficient_balance if wallet balance is too low. 409 conflict if idempotency key was already used — returns existing_transaction_id.
Gas: token assets (USDC USDT) need native gas. Yativo auto-funds from your gas station or platform fallback with 20% markup.
Idempotency: use Idempotency-Key header to prevent duplicates. Keys expire after 24 hours.
```

---

## MongoDB Indexes

```javascript
// Text index (fallback keyword search)
db.knowledge_docs.createIndex(
  { content: "text", title: "text", description: "text" },
  { weights: { title: 10, description: 5, content: 1 } }
)

// Vector search index (Atlas Vector Search)
// Field: "embedding" — 1536-dim float32 array (OpenAI text-embedding-3-small)
// Run once after embeddings are generated:
db.knowledge_docs.createSearchIndex({
  name: "vector_index",
  type: "vectorSearch",
  definition: {
    fields: [{
      type: "vector",
      path: "embedding",
      numDimensions: 1536,
      similarity: "cosine"
    }]
  }
})

// Compound indexes for filtered queries
db.knowledge_docs.createIndex({ product: 1, category: 1 })
db.knowledge_docs.createIndex({ product: 1, type: 1 })
db.knowledge_docs.createIndex({ tags: 1 })
db.knowledge_docs.createIndex({ source: 1, verified: 1 })
```

---

## RAG Query Pattern

```javascript
async function ragQuery(userQuestion, options = {}) {
  const { product, category, topK = 5 } = options;

  // 1. Embed the question
  const embedding = await openai.embeddings.create({
    model: "text-embedding-3-small",
    input: userQuestion,
  });

  // 2. Vector search with optional product filter
  const pipeline = [
    {
      $vectorSearch: {
        index: "vector_index",
        path: "embedding",
        queryVector: embedding.data[0].embedding,
        numCandidates: 50,
        limit: topK,
        filter: {
          ...(product && { product }),
          ...(category && { category }),
          source: { $in: ["docs", "support_qa"] },
          verified: true,
        },
      },
    },
    {
      $project: {
        _id: 1, title: 1, description: 1, method: 1, path: 1,
        baseUrl: 1, request_body: 1, response_example: 1,
        errors: 1, content: 1, score: { $meta: "vectorSearchScore" },
      },
    },
  ];

  const results = await db.collection("knowledge_docs").aggregate(pipeline).toArray();

  // 3. Build context string
  const context = results
    .map(doc => `## ${doc.title}\n${doc.content}`)
    .join("\n\n---\n\n");

  // 4. Prompt the LLM
  const response = await openai.chat.completions.create({
    model: "claude-sonnet-5",   // or gpt-4o, etc.
    messages: [
      {
        role: "system",
        content: `You are the Yativo developer support AI. Answer questions about integrating the Yativo API using ONLY the context below. If the answer is not in the context, say so — do not invent endpoints or parameters.\n\nContext:\n${context}`,
      },
      { role: "user", content: userQuestion },
    ],
  });

  return response.choices[0].message.content;
}
```

---

## Embedding Pipeline

Run this after inserting or updating documents:

```javascript
async function embedDocuments(filter = {}) {
  const docs = await db.collection("knowledge_docs")
    .find({ ...filter, embedding: { $exists: false } })
    .toArray();

  for (const doc of docs) {
    const { data } = await openai.embeddings.create({
      model: "text-embedding-3-small",
      input: doc.content.slice(0, 8191), // token limit
    });

    await db.collection("knowledge_docs").updateOne(
      { _id: doc._id },
      { $set: { embedding: data[0].embedding, updated_at: new Date() } }
    );
  }
}
```

---

## WhatsApp Support Q&A Integration

When a support conversation is resolved via WhatsApp:

```javascript
// Schema for support Q&A documents
{
  _id: "support-qa-" + nanoid(),
  source: "support_qa",
  product: "crypto" | "fiat",
  type: "support_qa",
  category: "derived from problem",  // e.g. "transactions", "kyc", "webhooks"
  title: "Short description of the problem",
  description: "Full problem and resolution description",
  problem: "Original client problem in natural language",
  resolution: "Step-by-step resolution that worked",
  api_endpoints_mentioned: ["/transactions/send-funds"],
  tags: ["error", "USDC", "ethereum"],
  verified: true,                    // set to true after human review
  content: "problem + resolution + endpoints mentioned as dense text",
  resolved_at: new Date(),
  created_at: new Date(),
  updated_at: new Date(),
}
```

### WhatsApp export processing script (Node.js):

```javascript
// whatsapp-chat-to-kb.js
// Process WhatsApp .txt exports into knowledge_docs entries

const fs = require('fs');

function parseWhatsAppExport(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const lines = raw.split('\n');
  const messages = [];

  for (const line of lines) {
    // Format: [DD/MM/YYYY, HH:MM:SS] Sender: Message
    const match = line.match(/^\[(\d{2}\/\d{2}\/\d{4}, \d{2}:\d{2}:\d{2})\] ([^:]+): (.+)$/);
    if (match) {
      messages.push({ timestamp: match[1], sender: match[2].trim(), text: match[3].trim() });
    }
  }
  return messages;
}

// Group into conversations by time gaps > 4 hours
function groupIntoConversations(messages) { /* ... */ }

// Use an LLM to extract problem/resolution/endpoints
async function extractQA(conversation) {
  const prompt = `Extract from this support conversation:
1. problem: what was the client's issue (1-2 sentences)
2. resolution: what fixed it (step by step)
3. api_endpoints_mentioned: list of Yativo API paths mentioned
4. category: one of [authentication, transactions, cards, iban, webhooks, kyc, wallets, swap, payments, other]
5. product: "crypto" or "fiat"

Conversation:
${conversation.map(m => `${m.sender}: ${m.text}`).join('\n')}

Return JSON only.`;

  // ... call LLM
}
```

---

## Files in this directory

| File | Contents |
|------|----------|
| `schema.md` | This file — collection design, indexes, RAG pattern |
| `crypto-knowledge.json` | Crypto API endpoint + concept documents |
| `fiat-knowledge.json` | Fiat API endpoint + concept documents |
| `guides-knowledge.json` | Tutorial and guide documents |
| `errors-knowledge.json` | Error codes and troubleshooting documents |

Seed the database:
```bash
mongoimport --db yativo_ai --collection knowledge_docs --file crypto-knowledge.json --jsonArray
mongoimport --db yativo_ai --collection knowledge_docs --file fiat-knowledge.json --jsonArray
mongoimport --db yativo_ai --collection knowledge_docs --file guides-knowledge.json --jsonArray
mongoimport --db yativo_ai --collection knowledge_docs --file errors-knowledge.json --jsonArray
```
