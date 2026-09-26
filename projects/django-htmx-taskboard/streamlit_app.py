"""Session-isolated Streamlit adaptation of the Django task board."""
from datetime import datetime, timezone
import streamlit as st

st.set_page_config(page_title="Momentum · Task board", page_icon="▦", layout="wide")
st.title("▦ Momentum task board")
st.caption("A Streamlit edition of the Django/HTMX board. Tasks exist only in this browser session.")

if "board_tasks" not in st.session_state:
    st.session_state.board_tasks = []
    st.session_state.board_next_id = 1

with st.form("new_task", clear_on_submit=True):
    title = st.text_input("Task title", max_chars=120)
    note = st.text_area("Details (optional)", max_chars=500)
    if st.form_submit_button("Add task", type="primary"):
        if not title.strip():
            st.error("Please enter a task title.")
        else:
            st.session_state.board_tasks.insert(0, {"id": st.session_state.board_next_id, "title": title.strip(), "note": note.strip(), "done": False, "created": datetime.now(timezone.utc).isoformat(timespec="seconds")})
            st.session_state.board_next_id += 1
            st.rerun()

tasks = st.session_state.board_tasks
a, b = st.columns(2)
a.metric("Open", sum(not item["done"] for item in tasks))
b.metric("All", len(tasks))
filter_by = st.segmented_control("Show", ["All", "Open", "Done"], default="All")
visible = [item for item in tasks if filter_by == "All" or item["done"] == (filter_by == "Done")]
if not visible:
    st.info("No tasks in this view. Add one above.")
for item in visible:
    with st.container(border=True):
        left, middle, right = st.columns([6, 1, 1], vertical_alignment="center")
        left.write(item["title"])
        if item["note"]:
            left.write(item["note"])
        left.caption("Done" if item["done"] else "Open")
        if middle.button("Reopen" if item["done"] else "Done", key=f"toggle_{item['id']}"):
            item["done"] = not item["done"]
            st.rerun()
        if right.button("Delete", key=f"delete_{item['id']}"):
            tasks.remove(item)
            st.rerun()

st.caption("The original Django models, HTMX views, and tests remain in this folder as a separate local implementation.")
