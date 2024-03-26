import numpy as np
import pandas as pd
from scipy import stats


def remove_outliers(df: pd.DataFrame, key: str) -> pd.DataFrame:
    """
    Removes outliers from a dataframe.

    Source: https://stackoverflow.com/a/23202269
    """
    return pd.DataFrame(df[np.abs(stats.zscore(df[key])) < 3])
