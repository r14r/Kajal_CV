---
layout: project
title: Django Task Board
description: A responsive task board with Django forms, SQLite persistence and HTMX partial updates.
permalink: /projects/django-htmx-taskboard/
number: "02"
order: 2
category: Django / HTMX
technology: Python, Django, HTMX, SQLite
runtime: Local Python server
source: django-htmx-taskboard
---

## What it does

Create tasks, mark them complete, filter by progress and remove them without a full-page refresh. Django renders the task list and HTMX replaces only the changed section. The HTMX script is bundled locally.

## What to explore

- Model, form, migration and server-rendered templates.
- HTMX requests and HTML fragment responses.
- CSRF protection, form validation and escaped user content.
- Tests for task flows and invalid input.

## Run it

From `projects/django-htmx-taskboard/`, create a virtual environment and run:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

Open `http://127.0.0.1:8000/`. Full instructions and test commands are in the project README. The local development configuration is not intended for a public server.
