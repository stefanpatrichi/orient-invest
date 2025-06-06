from fetch import fetch, DATA_PATH
from model import Model
from api import APIServer
import pandas as pd
import numpy as np
import uvicorn

# executa din folderul src!!

window_size = 200
step = 100


def process_request(etfs):
    fetch()
 
    df = pd.read_json(DATA_PATH)
   
    # df preprocessing: drop date column, interpolate missing values
    df = df.drop(columns=["Date", "EURRON=X", "EURUSD=X"])
    for col in df.columns:
        if col not in etfs:
            df = df.drop(columns=[col])
            continue
        df[col] = df[col].interpolate()
    df.bfill(inplace=True)
    print(df)

    model = Model(window_size=window_size, step=step)

    allocations, roi_individual, roi, sharpe = model.fit_predict(df)
    sharpe *= np.sqrt(252) # annualize	

    print([format(x, ".2%") for x in allocations])
    print(roi_individual)
    print(f"Return on investment for the last window: {roi:.2%}")
    print(f"Annualized sharpe: {sharpe:.2f}")

    allocations = list(allocations.astype(float))
    print(allocations)
    print(type(allocations))
    print(type(allocations[0]))

    return {"allocations": allocations, "roi": roi.numpy().astype(float), "sharpe": sharpe.numpy().astype(float)}

def get_etfs():
    df = pd.read_json(DATA_PATH)
    df = df.drop(columns=["Date", "EURRON=X", "EURUSD=X"])
    return list(df.columns)

def get_etf_history(etf):
    df = pd.read_json(DATA_PATH)
    return df[etf].interpolate().to_json()

server = APIServer(process_fn=process_request, get_etfs_fn=get_etfs, get_etf_history_fn=get_etf_history)
app = server.get_app()

if __name__ == "__main__":
    fetch()

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
