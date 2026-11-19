"""MEMBER 1 - Built-in demo data. Timestamps are generated fresh every time."""
import numpy as np
import pandas as pd


def make_sample(dirty=False, n=1000, seed=42):
    rng = np.random.default_rng(seed)
    now = pd.Timestamp.now().floor("min")
    df = pd.DataFrame({
        "order_id": np.arange(n),
        "order_date": now - pd.to_timedelta(rng.integers(0, 48, n), unit="h"),
        "customer_age": rng.normal(35, 8, n).round(),
        "amount": rng.normal(500, 100, n).round(2),
        "region": rng.choice(["North", "South", "East", "West"], n),
    })
    if dirty:
        df["amount"] = df["amount"] * 1.6                                   # drift
        df.loc[rng.choice(n, 150, replace=False), "customer_age"] = np.nan  # missing
        df.loc[rng.choice(n, 30, replace=False), "amount"] = 99999          # outliers
        df = pd.concat([df, df.sample(60, random_state=1)], ignore_index=True)  # duplicates
        df["order_date"] = df["order_date"] - pd.Timedelta(hours=60)        # stale data
        df["coupon"] = "X1"                                                 # new column
    return df
