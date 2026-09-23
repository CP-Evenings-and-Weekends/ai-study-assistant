# AI Study Assistant

Capstone assignment for week 17: **complete the Study Assistant** by finishing everything from Part 1 of Saturday's [lesson](https://github.com/CP-Evenings-and-Weekends/curriculum/blob/main/Module_06_AI_LLMs/week17/day4/README.md), then extend it with a delete endpoint.

**Work in the same `study_assistant` codebase you started Tuesday.** Do not start a fresh project. Tuesday gave you documents, chunking, and embeddings; Thursday gave you the one-off `/api/ask/` endpoint; today adds conversations and history. If either earlier build isn't working yet, fix that first (the RAG Document Q&A assignment repo and the lessons have everything you need).

The `docker-compose.yml`, `requirements.txt`, and `.env.example` in this repo are the same ones from Tuesday, included only as a fallback if your environment broke.

## Assignment 1 — Get all six endpoints working

Implement every endpoint from the lesson's overview table:

| Method | Endpoint | Verifies |
|---|---|---|
| `POST` | `/api/documents/` | Upload → auto-chunk → batch-embed → save chunks (Tuesday) |
| `GET`  | `/api/documents/` | List with `chunk_count` per document (Tuesday) |
| `POST` | `/api/ask/` | One-off RAG answer, no history (Thursday) |
| `POST` | `/api/conversations/` | Create a new conversation with a title |
| `GET`  | `/api/conversations/<id>/` | Full conversation with messages |
| `POST` | `/api/conversations/<id>/ask/` | RAG: retrieve → prompt with history → LLM → save both messages |

### Verify the full loop with curl

```bash
# 1. Upload a study doc (skip if your Tuesday data is still there)
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

The follow-up matters: the LLM should know "one" refers to a tuple because of the previous exchange. Now send the **same follow-up** to the history-free `POST /api/ask/` endpoint and compare. The difference you see is exactly what conversation history buys you — that comparison is the proof that today's work works.

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

## Things to think about
- The lesson limits conversation history to **20 messages** to stay under the context window. At what conversation length would you start needing the smarter truncation the lesson mentions (summarizing old turns)?
- `chunk_count` on the document list endpoint runs a separate query per document (an N+1). How would you fix that with `annotate(Count("chunks"))`? Try it.
- The `ask_with_rag` flow saves the user message **after** the LLM call. What happens if the LLM call fails halfway? Should you save the user message before, or after, or both with a transaction?
- Right now any user can ask questions against any conversation. What's the simplest auth model that would change that (per-user conversations)?

## Stretch

- **`GET /api/documents/<id>/chunks/`**: return all chunks for a document, ordered by `chunk_index`, each with `{"index", "text_preview", "length"}` (preview = first 200 chars, length = full chunk length). Then look at the chunk boundaries: do they break mid-sentence? At paragraph boundaries? This endpoint is the best debugging tool you can have when an answer is surprising.
- **Summarize old turns**: once a conversation exceeds 20 messages, replace the oldest half with a single LLM-generated "Earlier the student asked about X, Y, Z" summary message.
- **Per-conversation document filter**: let users scope `ask` to a specific document (`?document_id=`) so retrieval only pulls chunks from one source.
- **HNSW index** on the chunk embedding column. Measure search time before/after with `EXPLAIN ANALYZE`.
- **Streaming** the LLM answer back via SSE so a frontend could render word-by-word.

> Stuck? Have a code error? Use the ["4 Before Me"](https://docs.google.com/document/d/1nseOs5oabYBKNHfwJZNAR7GlU0zkZxNagsw63AD7XV0/edit) debugging checklist to help you solve it!
