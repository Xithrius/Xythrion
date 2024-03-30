import pandas as pd
from scipy.stats import zscore

# https://stackoverflow.com/a/23202269

ZSCORE_LIMIT = 4


def remove_outliers(
    df: pd.DataFrame,
    key: str,
    *,
    zscore_threshold: int | None = ZSCORE_LIMIT,
) -> pd.DataFrame:
    while True:
        # Calculate the z-scores
        z_scores = zscore(df[key])

        # Check if all z-scores are NaN
        if pd.notna(z_scores).any():
            # Identify outliers using the z-scores
            outliers_mask = abs(z_scores) <= zscore_threshold

            # Filter the DataFrame to exclude outliers
            df_filtered = df[outliers_mask]

            # Check if no more outliers are found
            if len(df_filtered) == len(df):
                break

            df = df_filtered
        else:
            break

    return df_filtered
