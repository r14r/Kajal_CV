# Job application tracker · Streamlit

A single-user local dashboard to create, edit, filter, search and delete job applications. It persists to a local SQLite database. No account or internet access is required after installation.

## Run

From the repository root:

```bash
cd projects/job-application-tracker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Open http://127.0.0.1:8501/. Windows: activate with `.venv\Scripts\activate`. For checks, run `python -m unittest discover -s tests -v` from this directory. Storage is in `data.sqlite3` beside the app; back it up to retain your records. The delete button deletes the selected record. This is a local learning app without sign-in or multi-user access.
