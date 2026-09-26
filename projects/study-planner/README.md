# Study planner · Streamlit

A dashboard for fictional coursework. Add, edit, filter, search and delete tasks, and see progress counts. Each browser session uses its own temporary SQLite file; data can disappear on a server restart. No account or secrets are required.

## Run

From the repository root:

```bash
cd projects/study-planner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.address 127.0.0.1 --server.port 8502
```

Open http://127.0.0.1:8502/. Windows: activate with `.venv\Scripts\activate`. For checks, run `python -m unittest discover -s tests -v` from this directory. For Community Cloud select `main` and `projects/study-planner/app.py`. The delete button deletes the selected task. Session SQLite files are temporary and are not durable storage.
