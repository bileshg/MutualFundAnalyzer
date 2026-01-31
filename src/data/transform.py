from typing import List

import pandas as pd

from src.mfapi.model import NAVData


def nav_data_to_df(nav_data: List[NAVData]) -> pd.DataFrame:
    rows = [{"Date": item.date, "NAV": item.nav} for item in nav_data]

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
    df["NAV"] = pd.to_numeric(df["NAV"], errors="coerce")
    df = df.dropna(subset=["Date", "NAV"]).sort_values("Date")

    return df


def calculate_moving_average(df: pd.DataFrame, window: int) -> pd.DataFrame:
    if df.empty:
        return df

    if not isinstance(window, int) or window < 1:
        raise ValueError("window must be a positive integer")

    df[f"{window}_DMA"] = df["NAV"].rolling(window=window).mean()

    return df


def last_n_years_data(df: pd.DataFrame, years: int) -> pd.DataFrame:
    if df.empty:
        return df

    latest_date = df["Date"].max()

    ten_years_ago = latest_date - pd.DateOffset(years=years)
    mask = df["Date"] >= ten_years_ago
    filtered_df = df.loc[mask, :].copy()

    # Wrap in pd.DataFrame to satisfy the declared return type
    return pd.DataFrame(filtered_df)


def process_nav_data(nav_data: List[NAVData]) -> pd.DataFrame:
    df = nav_data_to_df(nav_data)
    if df.empty:
        return df

    df = last_n_years_data(df, years=7)
    df = calculate_moving_average(df, window=50)
    df = calculate_moving_average(df, window=200)
    df = last_n_years_data(df, years=5)

    return df
