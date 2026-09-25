import unittest
from datetime import date
from unittest.mock import Mock, patch

import pandas as pd

from cleaning import clean, profile
from sources import ecb_exchange, weather, world_bank


class CleaningTests(unittest.TestCase):
    def test_transform_keeps_input_and_handles_duplicates_missing_numbers_dates(self):
        original = pd.DataFrame({" Date ": ["2026-01-01", "2026-01-01", "bad"], " Amount ": [" 10 ", " 10 ", "oops"], " Notes ": [" hi ", " hi ", "  "]})
        result = clean(original, numeric=[" Amount "], date_columns=[" Date "], missing="Fill numeric medians", normalize_names=True)
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result.columns), ["date", "amount", "notes"])
        self.assertEqual(result.loc[1, "amount"], 10)
        self.assertTrue(pd.isna(result.loc[1, "date"]))
        self.assertEqual(result.loc[0, "notes"], "hi")
        self.assertEqual(original.loc[0, " Amount "], " 10 ")
        self.assertEqual(profile(result).loc[1, "missing"], 0)

    def test_reject_colliding_normalized_columns(self):
        with self.assertRaisesRegex(ValueError, "unique"):
            clean(pd.DataFrame({"My Key": [1], "my_key": [2]}), normalize_names=True)

    def test_drop_incomplete(self):
        result = clean(pd.DataFrame({"a": [1, None], "b": [" x ", " y "]}), missing="Drop incomplete rows")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.loc[0, "b"], "x")


class SourcesTests(unittest.TestCase):
    @patch("sources.requests.get")
    def test_world_bank_parses_json_and_validates_input(self, get):
        get.return_value = Mock(url="https://api.worldbank.org/test", json=lambda: [{"total": 1}, [{"date": "2024", "country": {"value": "India"}, "value": 123}]])
        data, _ = world_bank("IND", "NY.GDP.MKTP.CD", 2020, 2024)
        self.assertEqual(data.iloc[0]["value"], 123)
        with self.assertRaises(ValueError):
            world_bank("IND/../../foo", "NY.GDP.MKTP.CD", 2020, 2024)
        self.assertEqual(get.call_count, 1)

    @patch("sources.requests.get")
    def test_weather_parses_daily_data(self, get):
        get.return_value = Mock(url="https://archive-api.open-meteo.com/test", json=lambda: {"daily": {"time": ["2024-01-01"], "precipitation_sum": [2]}})
        data, _ = weather(28.61, 77.21, date(2024, 1, 1), date(2024, 1, 2))
        self.assertEqual(data.iloc[0]["precipitation_sum"], 2)
        self.assertEqual(get.call_args.kwargs["timeout"], 20)

    @patch("sources.requests.get")
    def test_ecb_parses_time_and_value(self, get):
        get.return_value = Mock(url="https://data-api.ecb.europa.eu/test", text="TIME_PERIOD,OBS_VALUE,COMMENT\n2024-01-02,1.09,\n")
        data, _ = ecb_exchange(date(2024, 1, 1), date(2024, 1, 3))
        self.assertEqual(list(data.columns), ["date", "usd_per_eur"])
        self.assertEqual(data.iloc[0]["usd_per_eur"], 1.09)
