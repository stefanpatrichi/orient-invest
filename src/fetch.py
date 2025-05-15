from datetime import datetime, timedelta
import pandas as pd
from investiny import historical_data, search_assets 
import os.path

def mdy_slash_format(date):
    return str(date.strftime("%m/%d/%Y"))

def ymd_dash_format(date):
    return str(date.strftime("%Y-%m-%d"))

def search_etf(query_symbol):
    results = search_assets(query=query_symbol, limit=1, type="ETF")
    if not results or results[0]["symbol"] != query_symbol:
        raise LookupError(f"Could not find ETF with symbol {query_symbol}")
    else:
        return int(results[0]["ticker"])

def get_close_series(query_symbol, start, end):
    raw_asset_data = historical_data(
        investing_id=search_etf(query_symbol),
        from_date=start,
        to_date=end,
    )
        
    date_to_close = dict(zip(raw_asset_data["date"], raw_asset_data["close"]))
    s = pd.Series(date_to_close, name=f"{query_symbol}_close")
    
    return s

def sort_indices_by_date(idx: pd.Index):
    if pd.api.types.is_integer_dtype(idx):
        return pd.to_datetime(idx, unit="ms")
    else:                                
        return pd.to_datetime(idx)
    
SYMBOLS = ["TVBETETF", "EPOL", "BGX"]
TIME_WINDOW_DAYS = 3100

START_DATE = datetime.now() - timedelta(days=TIME_WINDOW_DAYS)
END_DATE = datetime.now()
DATA_PATH = os.path.abspath(f"../data/{ymd_dash_format(END_DATE)}_portfolio_data.json")

def fetch():
    if not os.path.isfile(DATA_PATH):
        print(f"Could not find file {DATA_PATH}; downloading data...")
        series_list = [get_close_series(sym, mdy_slash_format(START_DATE), mdy_slash_format(END_DATE)) for sym in SYMBOLS]
        df = (
            pd.concat(series_list, axis=1)
            .sort_index(key=sort_indices_by_date)
            .reset_index()
            .rename(columns={"index": "date"})
        )
        df.to_json(DATA_PATH)
        print(f"Successfully dumped JSON data to {DATA_PATH}!")
    else:
        print(f"File {DATA_PATH} already exists; skipping download")
