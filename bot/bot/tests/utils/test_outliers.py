import pandas as pd

from bot.utils import remove_outliers


def test_remove_no_outliers_from_small_array() -> None:
    data = {"amount": list(range(1, 11))}
    df = pd.DataFrame(data)

    df_filtered = remove_outliers(df, "amount", zscore_threshold=3)

    assert len(df_filtered) == 10


def test_remove_one_outlier_small_array() -> None:
    data = {"amount": list(range(1, 11)) + [100]}
    df = pd.DataFrame(data)

    df_filtered = remove_outliers(df, "amount", zscore_threshold=3)

    assert len(df_filtered) == 10


def test_remove_one_major_outlier() -> None:
    data = {"amount": [1] * 100 + [100]}
    df = pd.DataFrame(data)

    df_filtered = remove_outliers(df, "amount")

    assert len(df_filtered) == 100


def test_remove_multiple_major_outliers() -> None:
    data = {"amount": [1] * 100 + [100, 200, 300]}
    df = pd.DataFrame(data)

    df_filtered = remove_outliers(df, "amount", zscore_threshold=3)

    assert len(df_filtered) == 100


def test_remove_multiple_major_outliers_from_large_array() -> None:
    data = {"amount": [1] * 10_000 + [100, 200, 300]}
    df = pd.DataFrame(data)

    df_filtered = remove_outliers(df, "amount", zscore_threshold=3)

    assert len(df_filtered) == 10_000
