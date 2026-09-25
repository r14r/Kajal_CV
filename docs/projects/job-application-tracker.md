---
layout: project
title: Job Application Tracker
description: A local Streamlit dashboard for recording and reviewing job applications.
permalink: /projects/job-application-tracker/
number: "04"
order: 4
category: Streamlit / SQLite
technology: Python, Streamlit, SQLite
runtime: Local Streamlit app
source: job-application-tracker
---

## What it does

Add companies and roles, keep notes, update a status, and find entries through search or filtering. Data stays in a local SQLite file.

## What to explore

- Streamlit forms, tabs and status metrics.
- Create, update, delete, search and filter flows.
- Parameterized SQLite queries and input validation.
- Storage tests using temporary databases.

## Run it

From `projects/job-application-tracker/`, install the requirements and run `streamlit run app.py --server.address 127.0.0.1 --server.port 8501`. Open `http://127.0.0.1:8501/`. The project README includes virtual-environment and test commands. The app is for one local user.
