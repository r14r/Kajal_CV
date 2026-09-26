"""Run with streamlit run app.py."""
from pathlib import Path
import tempfile
import uuid

import streamlit as st
from application_store import STATUSES, delete, list_items, save

# Give each browser session its own temporary database on shared cloud instances.
if "application_db_path" not in st.session_state:
    st.session_state.application_db_path = str(Path(tempfile.gettempdir()) / f"kajal-applications-{uuid.uuid4().hex}.sqlite3")
DB_PATH = st.session_state.application_db_path

st.set_page_config(page_title="Application tracker", page_icon="↗", layout="wide")
st.title("Job application tracker")
st.caption("Practice with fictional entries. Data stays in this browser session and can disappear when the server restarts.")
items = list_items(DB_PATH)
c1, c2, c3 = st.columns(3)
c1.metric("Applications", len(items))
c2.metric("Interviews", sum(row["status"] == "Interview" for row in items))
c3.metric("Offers", sum(row["status"] == "Offer" for row in items))

with st.sidebar:
    st.header("Find applications")
    query = st.text_input("Search company, role or notes")
    status_filter = st.selectbox("Status", ("All", *STATUSES))

tab_list, tab_add, tab_edit = st.tabs(["Applications", "Add", "Edit or delete"])
with tab_list:
    filtered = [row for row in items if (status_filter == "All" or row["status"] == status_filter) and query.casefold() in (row["company"] + " " + row["role"] + " " + row["notes"]).casefold()]
    if filtered:
        st.dataframe(filtered, hide_index=True, width="stretch")
    else:
        st.info("No applications match your search. Add one in the next tab.")
with tab_add:
    with st.form("add_application", clear_on_submit=True):
        company = st.text_input("Company")
        role = st.text_input("Role")
        status = st.selectbox("Status", STATUSES)
        notes = st.text_area("Notes (optional)")
        if st.form_submit_button("Save application"):
            try:
                save(company, role, status, notes, path=DB_PATH)
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
with tab_edit:
    if items:
        selected = st.selectbox("Select application", items, format_func=lambda row: f"#{row['id']} · {row['company']} — {row['role']}")
        with st.form(f"edit_{selected['id']}"):
            company = st.text_input("Company", selected["company"])
            role = st.text_input("Role", selected["role"])
            status = st.selectbox("Status", STATUSES, index=STATUSES.index(selected["status"]))
            notes = st.text_area("Notes", selected["notes"])
            if st.form_submit_button("Update application"):
                try:
                    save(company, role, status, notes, selected["id"], path=DB_PATH)
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))
        if st.checkbox("Show delete button") and st.button("Delete selected application", type="secondary"):
            delete(selected["id"], DB_PATH)
            st.rerun()
    else:
        st.info("Add an application first.")
