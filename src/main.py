from fetch import fetch, DATA_PATH
from model import Model
import pandas as pd
import numpy as np

# executa din folderul src!!

window_size = 200
step = 100

if __name__ == "__main__":
    fetch()
 
    df = pd.read_json(DATA_PATH)
   
    # df preprocessing: drop date column, interpolate missing values
    df = df.drop(columns="Date")
    for col in df.columns:
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
