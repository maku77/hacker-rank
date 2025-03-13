import numpy as np
import pandas as pd
import sys


def load_data():
    # Read the temperature data from stdin, skipping the first line
    f = sys.stdin
    df = pd.read_csv(f, skiprows=1, sep=r"\s+")
    # Replace with np.nan if the value starts with "Missing_"
    df['tmax_pred'] = df['tmax'].replace(to_replace="Missing_", value=np.nan, regex=True)
    df['tmin_pred'] = df['tmin'].replace(to_replace="Missing_", value=np.nan, regex=True)
    df['tmax_pred'] = df['tmax_pred'].astype(float)
    df['tmin_pred'] = df['tmin_pred'].astype(float)
    return df


def predict_by_interp(df):
    df['tmax_pred'] = df['tmax_pred'].interpolate()
    df['tmin_pred'] = df['tmin_pred'].interpolate()


#def seasonal_adjust(series):
#    from statsmodels.tsa.seasonal import seasonal_decompose
#
#    decomposed = seasonal_decompose(series, period=12, extrapolate_trend=10)
#    # Can we make accurate predictions using these results?
#    return decomposed.seasonal + decomposed.trend + decomposed.resid


def seasonal_adjust(series):
    from statsmodels.tsa.seasonal import STL

    stl = STL(series, period=12, robust=True).fit()
    return stl.trend + stl.seasonal


def predict_by_season(df):
    df['tmax_pred'] = seasonal_adjust(df['tmax_pred'])
    df['tmin_pred'] = seasonal_adjust(df['tmin_pred'])


def print_results(df):
    # Number of Missing_XXX values
    missing_tmax = df['tmax'].str.startswith("Missing_", na=False).sum()
    missing_tmin = df['tmin'].str.startswith("Missing_", na=False).sum()
    num_missing = missing_tmax + missing_tmin

    # Search missing values and print predicted values
    for i in range(1, num_missing + 1):
        label = "Missing_" + str(i)
        row = df[df["tmax"] == label]
        if not row.empty:
            print(row["tmax_pred"].values[0])
            continue
        row = df[df["tmin"] == label]
        if not row.empty:
            print(row["tmin_pred"].values[0])
            continue


if __name__ == "__main__":
    df = load_data()
    predict_by_interp(df)
    predict_by_season(df)
    print_results(df)
