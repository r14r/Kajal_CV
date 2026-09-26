# Data cleaning studio · Streamlit

Load a bundled fictional CSV, upload your own CSV (up to 20 MB), or retrieve historical data from one of three public sources. Preview columns and missing values, trim text, remove duplicate rows, convert dates and numbers, handle missing values, inspect charts, and download a cleaned CSV. The original data remains unchanged. The offline sample works without a network connection; public sources need internet access and may be unavailable or rate limited.

## Run

From the repository root:

```bash
cd projects/data-cleaning-studio
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.address 127.0.0.1 --server.port 8503
```

Open http://127.0.0.1:8503/. Windows: activate with `.venv\Scripts\activate`. Run `python -m unittest discover -s tests -v` from this directory for transform and response checks.

For Streamlit Community Cloud, select `main` and `projects/data-cleaning-studio/app.py` as the entry point. The sample works offline. Live sources require the Cloud server to reach their APIs. Uploads stay in the app session; use local execution for sensitive files.

## Public data and provenance

| Category | Provider / documentation | Data retrieved |
| --- | --- | --- |
| Weather | [Open-Meteo historical weather API](https://open-meteo.com/en/docs/historical-weather-api) | Historical daily temperature and precipitation for entered coordinates and dates. |
| Financial | [ECB Data Portal API](https://data.ecb.europa.eu/help/api/data) | ECB euro foreign exchange reference rate, U.S. dollars per euro, daily series `EXR.D.USD.EUR.SP00.A`. Informational historical reference rates; not investment or trading advice. |
| Global economic | [World Bank Indicators API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures) | Annual GDP in current U.S. dollars, GDP growth, or consumer price inflation for a selected ISO 3 country. Some years have missing observations. |

The original dataset URL is shown above the preview. Provider data may change or be revised. Check each provider's attribution and reuse requirements before publication. Uploaded CSVs are processed in the running Streamlit process; run locally for sensitive data. This app does not store uploaded files or make outbound requests to arbitrary user-entered URLs.

## Data-processing choices

Invalid numeric/date cells become missing values. “Fill numeric medians” leaves missing text and entirely empty numeric columns unchanged. Dropping incomplete rows can remove many records. The preview and chart are capped at 500 rows, but the exported CSV contains all cleaned rows. No code is executed from uploaded CSVs. Review spreadsheet formula injection risks if you later open untrusted exported cells in spreadsheet software.
