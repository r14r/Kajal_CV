"""Pure table transforms; the original input is never changed."""
import pandas as pd


def clean(frame, *, trim=True, deduplicate=True, numeric=(), date_columns=(), missing="Keep", normalize_names=False):
    result = frame.copy(deep=True)
    if trim:
        for col in result.select_dtypes(include=["object", "string"]).columns:
            result[col] = result[col].map(lambda value: value.strip() if isinstance(value, str) else value)
            result[col] = result[col].replace("", pd.NA)
    for col in numeric:
        if col not in result:
            raise ValueError(f"Unknown numeric column: {col}")
        result[col] = pd.to_numeric(result[col], errors="coerce")
    for col in date_columns:
        if col not in result:
            raise ValueError(f"Unknown date column: {col}")
        result[col] = pd.to_datetime(result[col], errors="coerce", utc=True)
    if deduplicate:
        result = result.drop_duplicates().copy()
    if missing == "Drop incomplete rows":
        result = result.dropna().copy()
    elif missing == "Fill numeric medians":
        for col in result.select_dtypes(include="number"):
            result[col] = result[col].fillna(result[col].median())
    elif missing != "Keep":
        raise ValueError("Unknown missing-value policy")
    if normalize_names:
        result.columns = [str(col).strip().lower().replace(" ", "_") for col in result.columns]
        if not result.columns.is_unique:
            raise ValueError("Normalized column names must be unique")
    return result.reset_index(drop=True)


def profile(frame):
    return pd.DataFrame({"column": frame.columns, "type": [str(t) for t in frame.dtypes], "missing": frame.isna().sum().values, "unique": [frame[c].nunique(dropna=True) for c in frame.columns]})
