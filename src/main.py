from fetch import fetch, DATA_PATH
from model import Model
import pandas as pd
import os

# executa din folderul src!!

if __name__ == "__main__":
    #fetch()
    # tot nu-mi merge fetch-ul 😭😭

    # s-ar putea sa fie un pic belite folderele nu stiu sigur
    df = pd.read_json(DATA_PATH)
    
    # df preprocessing: drop date column, interpolate missing values
    df = df.drop(columns="date")
    for col in df.columns:
        df[col] = df[col].interpolate()
    df.fillna(1e-6, inplace=True)
    print(df)

    model = Model(window_size=200, step=100)

    allocations, roi, sharpe = model.fit_predict(df)

    print(allocations)
    print(roi)
    print(f"Return on investment for the last window: {roi.sum()}")
    print(f"Sharpe for the last window: {sharpe}")