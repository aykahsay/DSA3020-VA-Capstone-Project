import pandas as pd
import numpy as np

def add_time_features(df, date_col='Date'):
    """
    Adds Year, Month, WeekofYear columns for modeling.
    """
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df['Year'] = df[date_col].dt.year
    df['Month'] = df[date_col].dt.month
    df['WeekofYear'] = df[date_col].dt.isocalendar().week
    df['Year_Week'] = df['Year'].astype(str) + "-" + df['WeekofYear'].astype(str)
    return df

def log_transform_columns(df, cols):
    """
    Applies log transformation to numeric columns to reduce skewness.
    """
    for col in cols:
        df[col + "_log"] = np.log1p(df[col])
    return df
