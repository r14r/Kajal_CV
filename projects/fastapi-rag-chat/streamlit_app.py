"""Streamlit Community Cloud RAG demo with cited, session-scoped documents."""
from pathlib import Path

import streamlit as st
from retrieval import chunks, retrieve

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Notebook Chat · RAG", page_icon="◈", layout="wide")
st.title("◈ Notebook Chat")
st.caption("Ask questions about your notes. Retrieval shows matching passages with citations; no model or API key is required.")

if "rag_documents" not in st.session_state:
    st.session_state.rag_documents = [
        {"title": p.name, "content": p.read_text(encoding="utf-8")}
        for p in sorted((ROOT / "knowledge").glob("*.md"))
    ]
if "rag_messages" not in st.session_state:
    st.session_state.rag_messages = []

with st.sidebar:
    st.header("Knowledge library")
    st.caption("Private to this browser session. Do not upload sensitive information to a public demo.")
    with st.form("add_note", clear_on_submit=True):
        title = st.text_input("Document title", max_chars=120)
        content = st.text_area("Paste a note", height=130)
        submitted = st.form_submit_button("Add note")
        if submitted:
            if not title.strip() or not (20 <= len(content.strip()) <= 65536):
                st.error("Add a title and 20–65,536 characters of text.")
            else:
                st.session_state.rag_documents.append({"title": title.strip(), "content": content.strip()})
                st.rerun()
    uploaded = st.file_uploader("Or upload .txt / .md", type=["txt", "md"], max_upload_size=1)
    if uploaded and st.button("Add uploaded note"):
        try:
            content = uploaded.getvalue().decode("utf-8")
            if not (20 <= len(content.strip()) <= 65536):
                raise ValueError("Use a text file between 20 and 65,536 characters.")
            st.session_state.rag_documents.append({"title": uploaded.name[:120], "content": content.strip()})
            st.rerun()
        except (UnicodeDecodeError, ValueError) as exc:
            st.error(str(exc))
    for i, doc in enumerate(st.session_state.rag_documents):
        col, action = st.columns([4, 1], vertical_alignment="center")
        col.write(doc["title"])
        if action.button("✕", key=f"remove_{i}", help=f"Remove {doc['title']}"):
            del st.session_state.rag_documents[i]
            st.rerun()
    if st.button("Clear conversation"):
        st.session_state.rag_messages = []
        st.rerun()

for message in st.session_state.rag_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message.get("citations"):
            with st.expander("Retrieved sources"):
                for n, source in enumerate(message["citations"], 1):
                    st.write(f"[{n}] {source['title']} · passage {source['position']}")
                    st.caption(source["content"])

question = st.chat_input("Ask about the notes", max_chars=2000)
if question:
    passages = []
    for doc in st.session_state.rag_documents:
        for position, passage in enumerate(chunks(doc["content"]), 1):
            passages.append({"id": len(passages) + 1, "position": position, "title": doc["title"], "content": passage})
    sources = retrieve(question, passages)
    if sources:
        answer = "Matching passages from your notes (retrieved excerpts, not a generated answer):\n\n" + "\n\n".join(
            f"[{n}] {source['content'][:400]}" for n, source in enumerate(sources, 1)
        )
    else:
        answer = "I couldn't find a relevant passage. Try different words or add a note."
    st.session_state.rag_messages.extend([
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer, "citations": sources},
    ])
    st.rerun()

st.caption("Lexical retrieval may miss synonyms. The original FastAPI version also supports an optional local Ollama model; this Cloud edition deliberately uses cited excerpts.")
