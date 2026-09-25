"""Public read-only sources. Requests use fixed hosts and strict inputs."""
import io
import re

import pandas as pd
import requests

TIMEOUT = 20


def weather(latitude, longitude, start, end):
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180 or start > end:
        raise ValueError("Check coordinates and date range")
    url = "https://archive-api.open-meteo.com/v1/archive"
    response = requests.get(url, params={"latitude": latitude, "longitude": longitude, "start_date": start.isoformat(), "end_date": end.isoformat(), "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum", "timezone": "UTC"}, timeout=TIMEOUT)
    response.raise_for_status()
    body = response.json()
    if body.get("error") or "daily" not in body:
        raise ValueError(body.get("reason", "No daily weather data returned"))
    return pd.DataFrame(body["daily"]), response.url


def world_bank(country, indicator, start_year, end_year):
    if not re.fullmatch(r"[A-Z]{3}", country) or indicator not in ("NY.GDP.MKTP.CD", "NY.GDP.MKTP.KD.ZG", "FP.CPI.TOTL.ZG") or start_year > end_year:
        raise ValueError("Check country, indicator and date range")
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
    response = requests.get(url, params={"format": "json", "date": f"{start_year}:{end_year}", "per_page": 1000}, timeout=TIMEOUT)
    response.raise_for_status()
    body = response.json()
    if not isinstance(body, list) or len(body) < 2 or body[1] is None:
        raise ValueError("No World Bank observations returned")
    return pd.DataFrame([{"year": row["date"], "country": row["country"]["value"], "indicator": indicator, "value": row["value"]} for row in body[1]]), response.url


def ecb_exchange(start, end):
    if start > end:
        raise ValueError("Start date must precede end date")
    url = "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A"
    response = requests.get(url, params={"startPeriod": start.isoformat(), "endPeriod": end.isoformat(), "format": "csvdata"}, timeout=TIMEOUT)
    response.raise_for_status()
    frame = pd.read_csv(io.StringIO(response.text))
    if not {"TIME_PERIOD", "OBS_VALUE"}.issubset(frame.columns):
        raise ValueError("Unexpected ECB response columns")
    return frame[["TIME_PERIOD", "OBS_VALUE"]].rename(columns={"TIME_PERIOD": "date", "OBS_VALUE": "usd_per_eur"}), response.url
