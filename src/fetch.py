from datetime import datetime, timedelta
import pandas as pd
from investiny import historical_data, search_assets 

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

def main():
    symbols = ["TVBETETF", "EPOL", "BGX"]
    start_date = str((datetime.now() - timedelta(days=10)).strftime("%m/%d/%Y"))
    end_date = str(datetime.now().strftime("%m/%d/%Y"))

    series_list = [get_close_series(sym, start_date, end_date) for sym in symbols]
    df = (
        pd.concat(series_list, axis=1)
        .reset_index()
        .rename(columns={"index": "date"})
    )
    df.to_json("portfolio_data.json")

if __name__ == "__main__":
    main()