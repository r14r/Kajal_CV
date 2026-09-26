# Kajal developer portfolio - learning package

Six independent, runnable Streamlit projects and a two-section CV portfolio in HTML and PDF. The PDF has one CV page followed by six technical project pages with architecture and data flow images. The original Django/HTMX, FastAPI and plain HTML implementations are retained as separate learning references.

The root `cv.yaml` is the editable source for the CV and the website. On every push or merge to `main`, GitHub Actions regenerates and deploys the Jekyll site from it. The `docs/` folder is a Jekyll portfolio website for GitHub Pages, with a home hero, animated sidebar navigation, and a detail page for every project. See `docs/README.md` for publishing instructions. The static site describes the backend projects; it does not host their Python servers.

## Contents

```text
cv.yaml             Edit this file to update CV and Jekyll site
cv/                 CV and six illustrated project pages, PDF and HTML
docs/               Jekyll source for GitHub Pages
projects/
  job-application-tracker/   Streamlit + SQLite
  study-planner/             Streamlit + SQLite
  animated-portfolio/        HTML + CSS + JavaScript; no install
  django-htmx-taskboard/     Django + SQLite + locally bundled HTMX
  fastapi-rag-chat/          FastAPI + SQLite + local retrieval + optional Ollama
  data-cleaning-studio/      Streamlit + Pandas + CSV and public APIs
```

Each project's README gives exact run and verification commands. To deploy on Streamlit Community Cloud, connect this GitHub repository and choose `main` with one of these entry points. Create six Cloud apps if you want six separate URLs. The dependency file in each app's folder is detected automatically; select Python 3.12. After deployment, put each actual URL into its `demo_url` in `cv.yaml` to display a launch button on the Jekyll project page.

| Project | Streamlit Cloud entry point |
| --- | --- |
| Animated portfolio | `projects/animated-portfolio/streamlit_app.py` |
| Django task board adaptation | `projects/django-htmx-taskboard/streamlit_app.py` |
| RAG chat adaptation | `projects/fastapi-rag-chat/streamlit_app.py` |
| Job application tracker | `projects/job-application-tracker/app.py` |
| Study planner | `projects/study-planner/app.py` |
| Data cleaning studio | `projects/data-cleaning-studio/app.py` |

The task board and chat use per-browser-session memory. The trackers use separate temporary SQLite files per browser session. Cloud data can disappear on restart and is intended for fictional demonstrations. Uploaded notes and CSVs are processed in the app session; avoid sensitive data on public demos. The RAG Cloud app returns cited retrieved excerpts without a language model. No API keys are needed.

## Important before applying

These are learning projects prepared for Kajal. Kajal should run, inspect, modify, and explain the code before presenting either as her work. The CV is explicitly a draft: add her verified email, college, graduation dates, actual skills, and her own GitHub URL before sending it. Do not describe generated starter code as independently authored. After personalising, she may publish each project as a separate GitHub repository and link her actual contributions.

## Suggested learning tasks

1. Add a due date to the study planner (database, form, and storage test).
2. Change the animated site's branding and artwork, and explain reduced-motion support.
3. Extend the Django board with editing and an end-to-end test.
4. Add citations highlighting to the RAG chat and explain how retrieval ranking works.
5. Add a new data source to the cleaning studio, documenting provenance and missing values.
6. Add screenshots and a brief screen recording to each published repository.

All sample data should be fictional. Keep `data.sqlite3` and `.env` files out of Git.
