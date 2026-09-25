"""Interactive data cleaning and public-data explorer."""
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

from cleaning import clean, profile
from sources import ecb_exchange, weather, world_bank

st.set_page_config(page_title="Data cleaning studio", page_icon="◫", layout="wide")
st.title("Data cleaning studio")
st.caption("Explore a sample, upload CSV, or retrieve public data. Review transformations before downloading.")
today = date.today()
with st.sidebar:
    st.header("1 · Select data")
    source = st.selectbox("Data source", ["Sample CSV (offline)", "Upload CSV", "Open-Meteo weather", "ECB EUR/USD rate", "World Bank indicators"])
    uploaded = None
    settings = {}
    if source == "Upload CSV":
        uploaded = st.file_uploader("CSV file", type="csv")
    elif source == "Open-Meteo weather":
        settings["lat"] = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=28.61)
        settings["lon"] = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=77.21)
    elif source == "World Bank indicators":
        settings["country"] = st.text_input("ISO 3 country code", "IND").strip().upper()
        settings["indicator"] = st.selectbox("Indicator", ["NY.GDP.MKTP.CD", "NY.GDP.MKTP.KD.ZG", "FP.CPI.TOTL.ZG"], format_func=lambda x: {"NY.GDP.MKTP.CD": "GDP (current US$)", "NY.GDP.MKTP.KD.ZG": "GDP growth (%)", "FP.CPI.TOTL.ZG": "Inflation, consumer prices (%)"}[x])
        settings["start_year"] = st.number_input("From year", 1960, today.year, max(1960, today.year - 12))
        settings["end_year"] = st.number_input("To year", 1960, today.year, today.year)
    if source in ("Open-Meteo weather", "ECB EUR/USD rate"):
        settings["start"] = st.date_input("From date", today - timedelta(days=30))
        settings["end"] = st.date_input("To date", today - timedelta(days=2))
    if source in ("Open-Meteo weather", "ECB EUR/USD rate", "World Bank indicators") and st.button("Fetch public data", type="primary"):
        try:
            with st.spinner("Fetching data…"):
                if source == "Open-Meteo weather":
                    frame, url = weather(settings["lat"], settings["lon"], settings["start"], settings["end"])
                elif source == "ECB EUR/USD rate":
                    frame, url = ecb_exchange(settings["start"], settings["end"])
                else:
                    frame, url = world_bank(settings["country"], settings["indicator"], settings["start_year"], settings["end_year"])
            st.session_state["fetched_data"] = (source, settings.copy(), frame, url)
        except (requests.RequestException, ValueError, KeyError, pd.errors.ParserError) as exc:
            st.error(f"Could not load data: {exc}")

if source == "Sample CSV (offline)":
    raw = pd.read_csv(Path(__file__).parent / "samples" / "messy_sales.csv")
    provenance = "Bundled fictional sample data"
elif source == "Upload CSV":
    if uploaded is None:
        st.info("Upload a CSV file to start.")
        st.stop()
    if uploaded.size > 20 * 1024 * 1024:
        st.error("Upload a CSV smaller than 20 MB.")
        st.stop()
    try:
        raw = pd.read_csv(uploaded)
    except (UnicodeError, pd.errors.ParserError, ValueError) as exc:
        st.error(f"Could not read CSV: {exc}")
        st.stop()
    provenance = f"Your uploaded file: {uploaded.name}"
else:
    cached = st.session_state.get("fetched_data")
    if cached is None or cached[0] != source or cached[1] != settings:
        st.info("Choose the parameters, then select Fetch public data.")
        st.stop()
    raw, provenance = cached[2], cached[3]

if raw.empty:
    st.warning("This dataset has no rows.")
    st.stop()
st.caption(f"Source: {provenance}")
st.subheader("Original data")
st.dataframe(raw.head(500), hide_index=True, width="stretch")
st.write(f"{len(raw):,} rows · {len(raw.columns)} columns · {raw.isna().sum().sum():,} missing cells")

st.subheader("2 · Choose cleaning steps")
left, right = st.columns(2)
with left:
    trim = st.checkbox("Trim text and turn empty text into missing values", True)
    deduplicate = st.checkbox("Remove duplicate rows", True)
    normalize = st.checkbox("Normalize column names", False)
with right:
    numeric = st.multiselect("Convert columns to numbers", list(raw.columns))
    dates = st.multiselect("Parse columns as dates (UTC)", [x for x in raw.columns if x not in numeric])
    missing = st.selectbox("Missing values", ["Keep", "Drop incomplete rows", "Fill numeric medians"])
try:
    result = clean(raw, trim=trim, deduplicate=deduplicate, numeric=numeric, date_columns=dates, missing=missing, normalize_names=normalize)
except (ValueError, TypeError) as exc:
    st.error(f"Could not clean data: {exc}")
    st.stop()

st.subheader("3 · Inspect and export")
a, b, c = st.columns(3)
a.metric("Rows after cleaning", len(result), len(result) - len(raw))
b.metric("Missing cells", int(result.isna().sum().sum()), int(result.isna().sum().sum() - raw.isna().sum().sum()))
c.metric("Columns", len(result.columns))
st.dataframe(profile(result), hide_index=True, width="stretch")
st.dataframe(result.head(500), hide_index=True, width="stretch")
numbers = list(result.select_dtypes(include="number").columns)
if numbers and len(result):
    st.line_chart(result[numbers].head(500))
st.download_button("Download cleaned CSV", result.to_csv(index=False).encode("utf-8"), "cleaned_data.csv", "text/csv")
st.caption("Charts and previews show up to 500 rows; exports contain every cleaned row. Check provider terms before reuse.")
