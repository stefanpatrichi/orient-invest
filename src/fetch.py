
import os.path
import numpy as np
import pandas as pd
import yfinance as yf
from constants import *

# ---------- helpers ---------------------------------------------------------

def log(msg: str) -> None:
    print(f"[INFO] {msg}")

def mdy_slash_format(date):
    return date.strftime("%m/%d/%Y")


def ymd_dash_format(date):
    return date.strftime("%Y-%m-%d")


def sort_indices_by_date(idx):
    if pd.api.types.is_integer_dtype(idx):
        return pd.to_datetime(idx, unit="ms")
    return pd.to_datetime(idx)


# ---------- market-data fetchers -------------------------------------------

def get_fx_series(currency, start, end):
    pair_ticker = f"EUR{currency}=X"
    fx = yf.download(pair_ticker, start=start, end=end, progress=False)["Close"]

    if fx.empty:
        raise LookupError(f"Could not fetch FX rate for pair {pair_ticker}")

    fx.index = fx.index.tz_localize(None)              # make timezone-naive
    fx.name = f"EUR_{currency}"

    full_range = pd.date_range(fx.index.min(), fx.index.max(), freq="D")
    return fx.reindex(full_range).ffill()              # fill weekends / holidays


def get_close_series(query_symbol, start, end):
    ticker = query_symbol["name"]
    closes = yf.download(ticker, start=start, end=end, progress=False)["Close"]

    if closes.empty:
        raise LookupError(f"Could not download price series for ticker {ticker}")

    closes.index = closes.index.tz_localize(None)
    closes.name = f"{ticker}_close"

    if query_symbol["currency"] != "EUR":
        fx = get_fx_series(query_symbol["currency"], start, end)
        fx = fx.reindex(closes.index)
        closes = closes / fx.values

    return closes


# ---------- portfolio definition -------------------------------------------

# SYMBOLS = [
#     {"name": "TVBETETF.RO", "currency": "RON"},
#     {"name": "EPOL",        "currency": "USD"},
#     {"name": "IPOL.L",      "currency": "USD"},
#     {"name": "BGX.DE",      "currency": "EUR"},
#     {"name": "CEC.PA",      "currency": "EUR"},
# #   {"name": "ESTEG",       "currency": "EUR"}, nu l am gasit pe yfinance...
#     {"name": "TUR",         "currency": "USD"}, 
#     {"name": "GREK",        "currency": "USD"},
#     {"name": "PLX.DE",      "currency": "EUR"},
# ]
# CURRENCIES_NONEUR = ["RON", "USD"]
# TIME_WINDOW_DAYS = 4000
# START_DATE = datetime.now() - timedelta(days=TIME_WINDOW_DAYS)
# END_DATE = datetime.now()

DATA_PATH = os.path.abspath(
    f"../data/{ymd_dash_format(END_DATE)}_portfolio_data.json"
)

def fetch():
    if os.path.isfile(DATA_PATH):
        log(f"File {DATA_PATH} already exists; skipping download.")
        return

    log(f"Could not find file {DATA_PATH}; downloading data...")
    series_list = [get_close_series(sym, START_DATE, END_DATE) for sym in SYMBOLS]
    series_list += [get_fx_series(crcy, START_DATE, END_DATE) for crcy in CURRENCIES_NONEUR]

    df = (
        pd.concat(series_list, axis=1)
        .sort_index(key=sort_indices_by_date)
        .reset_index()
        .rename(columns={"index": "Date"})
    )
    df["Date"] = df["Date"].apply(mdy_slash_format)

    df.to_json(DATA_PATH)
    log(f"Successfully wrote JSON data to {DATA_PATH}.")


if __name__ == "__main__":
    fetch()
