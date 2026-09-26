# Notebook Chat - FastAPI RAG demonstration

A locally hosted chat interface that retrieves relevant passages from Markdown or text notes. It stores knowledge, conversations, and citations in SQLite. It works without a language model: the default answer is an explicitly labelled collection of matching excerpts. Set `OLLAMA_MODEL` to enable optional, grounded answer generation with a local Ollama installation.

## Streamlit Community Cloud edition

Select `main` and `projects/fastapi-rag-chat/streamlit_app.py` as the entry point, or install `requirements.txt` and run `streamlit run streamlit_app.py` locally. This edition reuses `retrieval.py` and the bundled notes. Visitors can paste or upload text, ask questions, inspect citations and clear the conversation. Each visitor's notes and chat are session-scoped and disappear on restart. This edition does not run Ollama or generate answers; it labels retrieved source excerpts clearly. Do not upload sensitive notes to a public demonstration.

## Run (Python 3.10+)

```bash
cd projects/fastapi-rag-chat
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8001
```

Open <http://127.0.0.1:8001/>. Three example notes are loaded from `knowledge/` when the database is first created. Add your own `.txt` or `.md` document using the Knowledge library. Your text is stored in `data/chat.sqlite3` on this computer. Deleting a document removes it from future retrieval; existing chat citations remain as historical excerpts. Delete `data/` to reset everything.

### Optional Ollama generation

Install and start Ollama separately, download a model suitable for your hardware, then run the app with `OLLAMA_MODEL=<your-installed-model>` in the environment. The app calls `http://127.0.0.1:11434/api/generate` with up to three retrieved passages. If the model is missing or unreachable, it displays source excerpts. No remote API key is needed. Generated answers may still be wrong; inspect citations.

## Verify

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

Tests exercise chunking and ranking, seeded documents, chat persistence and citations, input validation, and deletion. An API explorer is available at <http://127.0.0.1:8001/docs>.

## Design and limits

- Documents are split into passages and scored with local lexical TF-IDF. This is real retrieval, but not semantic vector search. Queries using synonyms may miss useful passages.
- Source text is treated as untrusted context in the Ollama prompt. Prompt injection and inaccurate answers remain possible.
- The application is bound to `127.0.0.1` for single-user learning. It has no login or cross-user separation; add authentication and production security before exposing it to a network.
- Text is accepted via browser file reading or paste, max 64 KiB per document. The server does not fetch URLs or execute uploaded content.

This is a study project prepared for Kajal. She should inspect and extend it before describing her own contribution to an employer.
