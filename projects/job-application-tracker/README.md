# Job application tracker · Streamlit

A dashboard to create, edit, filter, search and delete fictional job applications. Each browser session uses its own temporary SQLite file. It can run on Streamlit Community Cloud without accounts or secrets, but the data can disappear on restart. Do not use this public demo for a real job search.

## Run

From the repository root:

```bash
cd projects/job-application-tracker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Open http://127.0.0.1:8501/. Windows: activate with `.venv\Scripts\activate`. For checks, run `python -m unittest discover -s tests -v` from this directory. For Community Cloud select `main` and `projects/job-application-tracker/app.py`. The delete button deletes the selected record. The SQLite files are session-specific and temporary; this is a learning app without durable storage.
