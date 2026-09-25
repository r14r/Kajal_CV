---
layout: project
title: Data Cleaning Studio
description: Clean uploaded CSVs or explore public weather, financial and economic data in Streamlit.
permalink: /projects/data-cleaning-studio/
number: "06"
order: 6
category: Streamlit / Data
technology: Python, Streamlit, Pandas, public APIs
runtime: Local Streamlit app
source: data-cleaning-studio
---

## What it does

Start with a bundled fictional dataset, upload a CSV, or retrieve historical observations from Open-Meteo, the European Central Bank or the World Bank. Trim text, remove duplicates, convert dates and numbers, handle missing values, inspect a preview and chart, then download cleaned CSV data.

## What to explore

- Deterministic data transforms that leave the original table untouched.
- Fixed public API connectors with validation, error handling and source URLs.
- Column profiles, before-and-after metrics and CSV export.
- Offline sample data and focused transform and response tests.

## Run it

From `projects/data-cleaning-studio/`, install the requirements and run `streamlit run app.py --server.address 127.0.0.1 --server.port 8503`. Open `http://127.0.0.1:8503/`. The project README has setup commands, provider documentation and limitations.
