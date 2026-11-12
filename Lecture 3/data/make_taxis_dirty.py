"""Build taxis_dirty.csv, the practice dataset of Session 3 (Data Quality Assessment).

Source: seaborn sample data `taxis` (6,433 NYC taxi rides, March 2019),
derived from NYC TLC trip records:
https://raw.githubusercontent.com/mwaskom/seaborn-data/master/taxis.csv

The real file already contains quality problems (missing zones and payments,
rides with 0 passengers or 0 distance, totals that do not add up, one ride
picked up in February). This script ADDS a small, documented set of problems so
that all four dimensions of the session appear. Everything is seeded: running
the script again gives exactly the same file.

Usage:  python make_taxis_dirty.py          (reads taxis.csv, writes taxis_dirty.csv)
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SRC = HERE / "taxis.csv"
URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/taxis.csv"
OUT = HERE / "taxis_dirty.csv"

rng = np.random.default_rng(3)

df = pd.read_csv(SRC if SRC.exists() else URL)
df.insert(0, "ride_id", np.arange(1, len(df) + 1))   # a key: one id per ride

# --- 1. Inconsistency: payment written in several ways (120 rows) -------------
variants = {"cash": ["Cash", "CASH", " cash"],
            "credit card": ["Credit card", "credit card ", "CREDIT CARD"]}
rows = rng.choice(df.index[df["payment"].notna()], size=120, replace=False)
for i in rows:
    df.loc[i, "payment"] = rng.choice(variants[df.loc[i, "payment"]])

# --- 2. Inconsistency: borough in lower case (25 rows) --------------------------
rows = rng.choice(df.index[df["pickup_borough"] == "Manhattan"], size=25, replace=False)
df.loc[rows, "pickup_borough"] = "manhattan"

# --- 3. Disguised missing value: payment = "unknown" (30 rows) ------------------
rows = rng.choice(df.index[df["payment"].isin(["cash", "credit card"])], size=30, replace=False)
df.loc[rows, "payment"] = "unknown"

# --- 4. Accuracy: negative fares (8 rows) ---------------------------------------
rows = rng.choice(df.index[df["fare"] > 0], size=8, replace=False)
df.loc[rows, "fare"] = -df.loc[rows, "fare"]

# --- 5. Accuracy: impossible passenger count 9 (5 rows) -------------------------
rows = rng.choice(df.index[df["passengers"].between(1, 6)], size=5, replace=False)
df.loc[rows, "passengers"] = 9

# --- 6. Accuracy / consistency: dropoff before pickup (6 rows, times swapped) ---
rows = rng.choice(df.index[df["dropoff"] > df["pickup"]], size=6, replace=False)
df.loc[rows, ["pickup", "dropoff"]] = df.loc[rows, ["dropoff", "pickup"]].to_numpy()

# --- 7. Duplication: 40 exact copies --------------------------------------------
exact = df.loc[rng.choice(df.index, size=40, replace=False)].copy()

# --- 8. Duplication: 10 rides recorded twice with a different tip and total -----
pool = df.index.difference(exact.index)
key_dup = df.loc[rng.choice(pool, size=10, replace=False)].copy()
extra_tip = rng.choice([1.0, 2.0, 3.0], size=10)
key_dup["tip"] = (key_dup["tip"] + extra_tip).round(2)
key_dup["total"] = (key_dup["total"] + extra_tip).round(2)

# --- Assemble and shuffle --------------------------------------------------------
dirty = (pd.concat([df, exact, key_dup], ignore_index=True)
           .sample(frac=1, random_state=3)
           .reset_index(drop=True))
dirty.to_csv(OUT, index=False)
print(f"wrote {OUT.name}: {dirty.shape[0]} rows x {dirty.shape[1]} columns")
