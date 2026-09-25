"""Run with streamlit run app.py."""
from pathlib import Path

import streamlit as st
from storage import STATUSES, delete, list_items, save

DB_PATH = str(Path(__file__).with_name("data.sqlite3"))

st.set_page_config(page_title="Study planner", page_icon="◎", layout="wide")
st.title("Study planner")
st.caption("A local dashboard for coursework and progress.")
items = list_items(DB_PATH)
c1, c2, c3 = st.columns(3)
c1.metric("Tasks", len(items))
c2.metric("In progress", sum(row["status"] == "In progress" for row in items))
c3.metric("Done", sum(row["status"] == "Done" for row in items))

with st.sidebar:
    st.header("Find tasks")
    query = st.text_input("Search title, course or notes")
    status_filter = st.selectbox("Status", ("All", *STATUSES))

tab_list, tab_add, tab_edit = st.tabs(["Tasks", "Add", "Edit or delete"])
with tab_list:
    filtered = [row for row in items if (status_filter == "All" or row["status"] == status_filter) and query.casefold() in (row["title"] + " " + row["course"] + " " + row["notes"]).casefold()]
    if filtered:
        st.dataframe(filtered, hide_index=True, width="stretch")
    else:
        st.info("No tasks match your search. Add one in the next tab.")
with tab_add:
    with st.form("add_task", clear_on_submit=True):
        title = st.text_input("Task title")
        course = st.text_input("Course")
        status = st.selectbox("Status", STATUSES)
        notes = st.text_area("Notes (optional)")
        if st.form_submit_button("Save task"):
            try:
                save(title, course, status, notes, path=DB_PATH)
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
with tab_edit:
    if items:
        selected = st.selectbox("Select task", items, format_func=lambda row: f"#{row['id']} · {row['course']} — {row['title']}")
        with st.form(f"edit_{selected['id']}"):
            title = st.text_input("Task title", selected["title"])
            course = st.text_input("Course", selected["course"])
            status = st.selectbox("Status", STATUSES, index=STATUSES.index(selected["status"]))
            notes = st.text_area("Notes", selected["notes"])
            if st.form_submit_button("Update task"):
                try:
                    save(title, course, status, notes, selected["id"], path=DB_PATH)
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))
        if st.checkbox("Show delete button") and st.button("Delete selected task", type="secondary"):
            delete(selected["id"], DB_PATH)
            st.rerun()
    else:
        st.info("Add a task first.")
