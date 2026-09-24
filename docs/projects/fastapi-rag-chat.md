---
layout: project
title: Notebook Chat
description: A local-first chat UI that retrieves passages from notes, cites sources and optionally uses Ollama.
permalink: /projects/fastapi-rag-chat/
number: "03"
order: 3
category: FastAPI / RAG
technology: Python, FastAPI, SQLite, vanilla JavaScript
runtime: Local Python server; Ollama optional
source: fastapi-rag-chat
---

## What it does

Add Markdown or text notes, ask questions and inspect the passages used in each response. A lexical retriever scores local document chunks. With no language model installed, the app returns labelled source excerpts. A configured local Ollama model can generate an answer using those passages.

## What to explore

- Chunking and token-based TF-IDF retrieval.
- Persistent documents, conversations and cited responses in SQLite.
- FastAPI validation and a responsive chat interface.
- Grounded generation with a local Ollama model as an optional extension.

## Run it

From `projects/fastapi-rag-chat/`, create a virtual environment and run:

```bash
python -m pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8001
```

Open `http://127.0.0.1:8001/`. The project README explains optional Ollama setup and the limits of lexical retrieval. This is a local single-user demo and has no authentication.
