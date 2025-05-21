from fetch import fetch
from model import Model
import pandas as pd
import os

if __name__ == "__main__":
    #fetch()
    # tot nu-mi merge fetch-ul 😭😭

    df = pd.read_json("orient-invest/data/" + os.listdir("orient-invest/data")[0])
    
    # df preprocessing: drop date column, interpolate missing values
    df = df.drop(columns="date")
    for col in df.columns:
        df[col] = df[col].interpolate()
    df.fillna(1e-6, inplace=True)
    print(df)

    model = Model(window_size=200, step=100)

    allocations, annual_stats = model.fit_predict(df)

    print(allocations)