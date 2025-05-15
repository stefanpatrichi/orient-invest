from datetime import datetime, timedelta
import pandas as pd
from investiny import historical_data, search_assets 
import os.path
import numpy as np

def log(msg):
    print(f"[INFO] {msg}")

def mdy_slash_format(date):
    return str(date.strftime("%m/%d/%Y"))

def ymd_dash_format(date):
    return str(date.strftime("%Y-%m-%d"))

def sort_indices_by_date(idx: pd.Index):
    if pd.api.types.is_integer_dtype(idx):
        return pd.to_datetime(idx, unit="ms")
    return pd.to_datetime(idx)

def search_etf(query_symbol):
    results = search_assets(query=query_symbol, limit=1, type="ETF")
    if not results or results[0]["symbol"] != query_symbol:
        raise LookupError(f"Could not find ETF with symbol {query_symbol}")
    return int(results[0]["ticker"])
    
def search_fx(query_symbol):
    results = search_assets(query=query_symbol, limit=1, type="FX")
    if not results or results[0]["symbol"] != query_symbol:
        raise LookupError(f"Could not find ETF with symbol {query_symbol}")
    return int(results[0]["ticker"])

def get_fx(currency, start, end):
    raw = historical_data(
        investing_id=search_fx(f"EUR/{currency}"),
        from_date=start,
        to_date=end,
    )
        
    fx = (
        pd.Series(dict(zip(raw["date"], raw["close"])), name=f"EUR_{currency}")
        .sort_index(key=sort_indices_by_date)
    )
    fx.index = sort_indices_by_date(fx.index)

    full_range = pd.date_range(fx.index.min(), fx.index.max(), freq="D")
    return fx.reindex(full_range).ffill()

def get_close_series(query_symbol, start, end):
    raw = historical_data(
        investing_id=search_etf(query_symbol["name"]),
        from_date=start,
        to_date=end,
    )

    closes = pd.Series(
        dict(zip(raw["date"], raw["close"])),
        name=f'{query_symbol["name"]}_close',
    )
    closes.index = sort_indices_by_date(closes.index).tz_localize(None)

    if query_symbol["currency"] != "EUR":
        fx = get_fx(query_symbol["currency"], start, end)
        fx = fx.reindex(closes.index) 
        closes = closes / fx.values

    return closes
    
SYMBOLS = [
    {"name": "TVBETETF", "currency": "RON"}, 
    {"name": "EPOL",     "currency": "USD"}, 
    {"name": "BGX",      "currency": "BGN"}, 
    {"name": "LEER",     "currency": "EUR"}, 
    {"name": "ESTEG",    "currency": "EUR"}, 
    {"name": "TUR",      "currency": "USD"}, 
    {"name": "GREK",     "currency": "USD"}, 
    {"name": "PLXG",     "currency": "EUR"}
]
TIME_WINDOW_DAYS = 4000

START_DATE = datetime.now() - timedelta(days=TIME_WINDOW_DAYS)
END_DATE = datetime.now()
DATA_PATH = os.path.abspath(f"../data/{ymd_dash_format(END_DATE)}_portfolio_data.json")

def fetch():
    if os.path.isfile(DATA_PATH):
        log(f"File {DATA_PATH} already exists; skipping download.")
        return

    log(f"Could not find file {DATA_PATH}; downloading data...")
    series_list = [get_close_series(sym, mdy_slash_format(START_DATE), mdy_slash_format(END_DATE)) for sym in SYMBOLS]
    df = (
        pd.concat(series_list, axis=1)
        .sort_index(key=sort_indices_by_date)
        .reset_index()
        .rename(columns={"index": "date"})
    )
    df["date"] = df["date"].apply(mdy_slash_format)
    df.to_json(DATA_PATH)
    log(f"Successfully wrote JSON data to {DATA_PATH}.")
