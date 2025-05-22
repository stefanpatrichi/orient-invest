import matplotlib.pyplot as plt
import pandas as pd

def make_graph(df: pd.DataFrame):
    df = df.drop(columns=["Date", "EURRON=X", "EURUSD=X"])
    for col in df.columns:
        df[col] = df[col].interpolate()

    for col in df.columns:
        ypoints = df[col]

        plt.plot(ypoints)
        plt.title(f"{col} Price History")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.grid(True)

        plt.savefig(f"../images/{col}.png", dpi=300, bbox_inches="tight")
        plt.close()
