---
layout: project
title: Job Application Tracker
description: A compact local web app for recording and reviewing job applications.
permalink: /projects/job-application-tracker/
number: "04"
order: 4
category: Python / SQLite
technology: Python standard library, SQLite, HTML, JavaScript
runtime: Local Python server
source: job-application-tracker
---

## What it does

Add companies and roles, keep notes, update a status, and find entries through search or filtering. Data is stored in a local SQLite file and stays on the user's machine.

## What to explore

- A small JSON API built with Python's standard library.
- Create, update, delete, search and filter flows.
- Server-side validation and mobile-friendly browser controls.
- API tests that use a temporary database.

## Run it

From `projects/job-application-tracker/`, run `python3 server.py` and open `http://127.0.0.1:8761/`. The project README has the test command and API routes. It is intended for one local user, without authentication.
