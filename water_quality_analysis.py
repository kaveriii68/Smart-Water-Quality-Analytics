import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

# Generate simulated water-quality data
np.random.seed(42)

n = 1000

data = {
    "Reading_ID": range(1, n + 1),
    "Timestamp": pd.date_range(start="2026-01-01", periods=n, freq="h"),
    "pH": np.round(np.random.normal(7.2, 0.5, n), 2),
    "Turbidity_NTU": np.round(np.random.normal(18, 8, n).clip(1), 2),
    "Temperature_C": np.round(np.random.normal(25, 2.5, n), 2)
}

df = pd.DataFrame(data)

# Classify water quality
def water_status(row):
    if 6.5 <= row["pH"] <= 8.5 and row["Turbidity_NTU"] < 25:
        return "Good"
    elif 6.0 <= row["pH"] <= 9.0 and row["Turbidity_NTU"] < 50:
        return "Warning"
    else:
        return "Poor"

df["Status"] = df.apply(water_status, axis=1)

# Data cleaning checks
print(df.info())
print(df.isnull().sum())
print("Duplicates:", df.duplicated().sum())

df = df.drop_duplicates()

df["pH"] = df["pH"].fillna(df["pH"].median())
df["Turbidity_NTU"] = df["Turbidity_NTU"].fillna(df["Turbidity_NTU"].median())
df["Temperature_C"] = df["Temperature_C"].fillna(df["Temperature_C"].median())

# Basic analysis
print("Average pH:", df["pH"].mean())
print("Average turbidity:", df["Turbidity_NTU"].mean())
print("Average temperature:", df["Temperature_C"].mean())

print(df["Status"].value_counts())

# Save cleaned data
df.to_csv("water_quality_cleaned.csv", index=False)

print("Cleaned dataset saved successfully.")