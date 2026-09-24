# Kajal developer portfolio - learning package

Five independent, fully runnable projects and a draft CV in HTML and PDF.

The `docs/` folder is a Jekyll portfolio website for GitHub Pages, with a home hero, animated sidebar navigation, and a detail page for every project. See `docs/README.md` for publishing instructions. The static site describes the backend projects; it does not host their Python servers.

## Contents

```text
cv/                 One-page draft CV and HTML website
docs/               Jekyll source for GitHub Pages
projects/
  job-application-tracker/   Python + SQLite + browser UI
  study-planner/             Python + SQLite + browser UI
  animated-portfolio/        HTML + CSS + JavaScript; no install
  django-htmx-taskboard/     Django + SQLite + locally bundled HTMX
  fastapi-rag-chat/          FastAPI + SQLite + local retrieval + optional Ollama
```

Each project's README gives exact run and verification commands. The first two Python apps use only the standard library and run on ports 8761 and 8762. The animated site opens directly as an HTML file. The Django board and FastAPI chat use the dependencies listed in their own `requirements.txt` files and run on ports 8000 and 8001.

## Important before applying

These are learning projects prepared for Kajal. Kajal should run, inspect, modify, and explain the code before presenting either as her work. The CV is explicitly a draft: add her verified email, college, graduation dates, actual skills, and her own GitHub URL before sending it. Do not describe generated starter code as independently authored. After personalising, she may publish each project as a separate GitHub repository and link her actual contributions.

## Suggested learning tasks

1. Add a date field end-to-end to one task tracker (database, API, form, and test).
2. Change the animated site's branding and artwork, and explain reduced-motion support.
3. Extend the Django board with editing and an end-to-end test.
4. Add citations highlighting to the RAG chat and explain how retrieval ranking works.
5. Add screenshots and a brief screen recording to each published repository.

All sample data should be fictional. Keep `data.sqlite3` and `.env` files out of Git.
