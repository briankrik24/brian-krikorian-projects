"""
profile_bronze.py

Profiles the Bronze layer dataset by reporting
basic dataset statistics and data quality metrics.
"""

from pathlib import Path

import pandas as pd


BRONZE_FILE = Path("data/bronze/games_march2025_cleaned.csv")


def load_data():
    """Load the Bronze dataset."""
    return pd.read_csv(BRONZE_FILE)


def dataset_overview(df):
    """Display basic information about the dataset."""
    print("=" * 50)
    print("Bronze Layer Profile")
    print("=" * 50)
    print(f"Rows:    {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    memory = df.memory_usage(deep=True).sum() / 1024**2
    print(f"Memory:  {memory:.1f} MB")


def data_types(df):
    """Display the number of columns by data type."""
    print("\nColumn Types")
    print("-" * 50)

    counts = df.dtypes.value_counts()

    labels = {
        "object": "Object",
        "int64": "Integer",
        "float64": "Float",
        "bool": "Boolean",
    }

    for dtype, count in counts.items():
        label = labels.get(str(dtype), str(dtype))
        print(f"{label:<10} {count}")


def missing_values(df):
    """Display the columns with the highest percentage of missing values."""
    print("\nTop Missing Values")
    print("-" * 50)

    missing = (
        df.isnull()
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )

    missing = missing[missing > 0].head(10)

    for column, pct in missing.items():
        print(f"{column:<25} {pct:.1f}%")


def duplicate_check(df):
    """Check for duplicate primary keys."""
    print("\nDuplicate App IDs")
    print("-" * 50)

    duplicates = df["appid"].duplicated().sum()
    pct = duplicates / len(df) * 100

    print(f"{duplicates:,} duplicates ({pct:.2f}%)")


def release_dates(df):
    """Display the release date range."""
    print("\nRelease Date Range")
    print("-" * 50)

    dates = pd.to_datetime(df["release_date"], errors="coerce")

    print(f"Earliest: {dates.min().date()}")
    print(f"Latest:   {dates.max().date()}")


def numeric_summary(df):
    """Display summary statistics for key business metrics."""
    print("\nKey Metrics Summary")
    print("-" * 50)

    columns = [
        "price",
        "positive",
        "negative",
        "peak_ccu",
        "average_playtime_forever",
    ]

    print(df[columns].describe())

    print("-" * 50)


def health_summary(df):
    """Run basic data quality checks."""
    print("\nBronze Health Summary")
    print("=" * 50)

    duplicate_count = df["appid"].duplicated().sum()

    dates = pd.to_datetime(df["release_date"], errors="coerce")
    future_dates = (dates > pd.Timestamp.today()).sum()

    missing = df.isnull().mean().mul(100)

    checks = [
        (
            "Duplicate App IDs",
            duplicate_count == 0,
            f"{duplicate_count} duplicates found"
        ),
        (
            "Future Release Dates",
            future_dates == 0,
            f"{future_dates} future dates found"
        ),
        (
            "Dataset Loaded",
            len(df) > 0,
            f"{len(df):,} rows loaded"
        ),
    ]

    warning_columns = [
        "website",
        "support_url",
        "support_email",
        "metacritic_url",
        "reviews",
        "notes",
    ]

    warning_count = sum(missing[column] > 0 for column in warning_columns)
    passed = sum(check[1] for check in checks)

    overall = "HEALTHY ✅" if passed == len(checks) else "ISSUES DETECTED ❌"

    print(f"Overall Status: {overall}")
    print(f"Checks Passed: {passed}/{len(checks)}")
    print(f"Warnings:      {warning_count}")

    print("\nValidation Checks")
    print("-" * 50)

    for name, success, detail in checks:
        icon = "✅" if success else "❌"
        status = "PASS" if success else "FAIL"
        print(f"{icon} {name:<25} {status:<5} ({detail})")

    print("\nInformational Warnings")
    print("-" * 50)

    for column in warning_columns:
        pct = missing[column]
        if pct > 0:
            print(f"⚠️  {column:<20} {pct:.1f}% missing")


def main():
    df = load_data()

    dataset_overview(df)
    data_types(df)
    missing_values(df)
    duplicate_check(df)
    release_dates(df)
    numeric_summary(df)
    health_summary(df)


if __name__ == "__main__":
    main()