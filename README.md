# AI Study Assistant

Capstone project for week 17: build the full Study Assistant backend the lesson walks through, then extend it with two endpoints that exercise the data model from new angles.

The repo ships the same Docker + Django + pgvector infrastructure you've been using all week so the work today is the **integration** — making document management, embeddings, RAG, and conversation history all play nicely in one project.

## Setup

```bash
cp .env.example .env
# Put your AI_API_KEY in .env (or use Ollama — see the lesson)
docker compose up -d
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Then scaffold a fresh Django project — don't bring yesterday's code over, start clean:

```bash
django-admin startproject config .
python manage.py startapp assistant
```

Wire `"assistant"` into `INSTALLED_APPS`, point `DATABASES` at the pgvector container, and follow the lesson to build out `chunking.py`, `embeddings.py`, `rag.py`, models, serializers, views, and URLs.

## Assignment 1 — Get the full lesson project working

Implement every endpoint from the lesson's "Project Overview" table:

| Method | Endpoint | Verifies |
|---|---|---|
| `POST` | `/api/documents/` | Upload → auto-chunk → batch-embed → save chunks |
| `GET`  | `/api/documents/` | List with `chunk_count` per document |
| `POST` | `/api/conversations/` | Create a new conversation with a title |
| `GET`  | `/api/conversations/<id>/` | Full conversation with messages |
| `POST` | `/api/conversations/<id>/ask/` | RAG: retrieve → build prompt → LLM → save messages |

### Verify the full loop with curl

```bash
# 1. Upload a study doc
curl -X POST http://localhost:8000/api/documents/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Python Data Types", "content": "<paste a multi-paragraph explanation>"}'

# 2. Start a conversation
curl -X POST http://localhost:8000/api/conversations/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Python Basics Study Session"}'

# 3. Ask
curl -X POST http://localhost:8000/api/conversations/1/ask/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the difference between a list and a tuple?"}'

# 4. Follow-up — must use conversation context, not just RAG
curl -X POST http://localhost:8000/api/conversations/1/ask/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Can you give me an example of when I would use one instead?"}'
```

The follow-up matters: the LLM should know "one" refers to a tuple because of the previous exchange.  If you ask the same follow-up against a fresh conversation, the answer should be noticeably worse — try it.

## Assignment 2 — `DELETE /api/documents/<id>/`

Remove a document **and** all its chunks/embeddings.

### Requirements
- Returns `204 No Content` on success
- Returns `404` if the document doesn't exist
- Because `DocumentChunk.document` uses `on_delete=models.CASCADE`, the chunks go with the document automatically — your view just calls `.delete()`

### Verify
```bash
curl -X DELETE -i http://localhost:8000/api/documents/1/
# expect: HTTP/1.1 204 No Content

# Now ask a question — answer should fall back to "no materials" message
curl -X POST http://localhost:8000/api/conversations/1/ask/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a list?"}'
```

## Assignment 3 — `GET /api/documents/<id>/chunks/`

Return all chunks for a document with a `text_preview` of each chunk (first 200 chars).  Useful for debugging when an answer is surprising — you can see exactly what the chunker produced.

### Response shape

```json
{
  "document": {"id": 1, "title": "Python Data Types", "chunk_count": 4},
  "chunks": [
    {"index": 0, "text_preview": "Python has several built-in data types...", "length": 412},
    {"index": 1, "text_preview": "Strings are sequences of characters...", "length": 587}
  ]
}
```

### Requirements
- Order chunks by `chunk_index` ascending
- `length` is the full chunk length, not the preview length
- `text_preview` is `chunk_text[:200] + "..."` only when the chunk is longer than 200 chars

### Verify
```bash
curl http://localhost:8000/api/documents/1/chunks/ | jq
```

Look at the chunk boundaries.  Do they break in the middle of sentences?  At paragraph boundaries?  Use this to reason about whether your chunker is doing the right thing.

## Things to think about
- The lesson limits conversation history to **20 messages** to stay under the context window.  At what conversation length would you start needing summarization (lesson day 2 mentioned this)?
- `chunk_count` on the document list endpoint runs a separate query per document (an N+1).  How would you fix that with `annotate(Count("chunks"))`?  Try it.
- The `ask_with_rag` flow saves the user message **after** the LLM call.  What happens if the LLM call fails halfway?  Should you save the user message before, or after, or both with a transaction?
- Right now any user can ask questions against any conversation.  What's the simplest auth model that would change that (per-user conversations)?

## Stretch
- **Summarize old turns**: once a conversation exceeds 20 messages, replace the oldest half with a single LLM-generated "Earlier the student asked about X, Y, Z" summary message — like the lesson day 2 stretch.
- **Re-ranking** the retrieved chunks before they go into the prompt (the lesson day 2 `rerank_chunks` function).  Does it help here?
- **Streaming** the LLM answer back via SSE so the frontend can render word-by-word.
- **HNSW index** on the chunk embedding column.  Measure search time before/after with `EXPLAIN ANALYZE`.
- **Per-conversation document filter**: let users scope `ask` to a specific document (`?document_id=`) so the RAG retrieval only pulls chunks from one source.

> Stuck? Have a code error? Use the ["4 Before Me"](https://docs.google.com/document/d/1nseOs5oabYBKNHfwJZNAR7GlU0zkZxNagsw63AD7XV0/edit) debugging checklist to help you solve it!
