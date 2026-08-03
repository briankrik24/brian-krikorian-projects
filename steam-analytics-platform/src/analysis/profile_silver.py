"""
profile_silver.py

Profiles the Silver layer dataset by reporting dataset
statistics and validating that the Silver transformation
completed successfully.
"""

from pathlib import Path

import pandas as pd


SILVER_FILE = Path("data/silver/games_clean.csv")

EXPECTED_COLUMNS = [
    "appid",
    "game_name",
    "release_date",
    "required_age",
    "price",
    "dlc_count",
    "windows",
    "mac",
    "linux",
    "metacritic_score",
    "achievements",
    "recommendations",
    "developers",
    "publishers",
    "categories",
    "genres",
    "user_score",
    "positive_reviews",
    "negative_reviews",
    "estimated_owners",
    "average_playtime_forever",
    "average_playtime_2weeks",
    "median_playtime_forever",
    "median_playtime_2weeks",
    "discount",
    "peak_ccu",
    "pct_positive_reviews",
    "total_reviews",
    "pct_positive_recent",
    "recent_reviews",
]

RENAMED_COLUMNS = [
    "game_name",
    "positive_reviews",
    "negative_reviews",
    "pct_positive_reviews",
    "total_reviews",
    "pct_positive_recent",
    "recent_reviews",
]

REMOVED_COLUMNS = [
    "name",
    "positive",
    "negative",
    "pct_pos_total",
    "num_reviews_total",
    "pct_pos_recent",
    "num_reviews_recent",
    "website",
    "reviews",
    "support_url",
    "support_email",
]


def load_data():
    """Load the Silver dataset."""

    if not SILVER_FILE.exists():
        raise FileNotFoundError(
            f"Silver dataset not found:\n{SILVER_FILE.resolve()}"
        )

    return pd.read_csv(
        SILVER_FILE,
        parse_dates=["release_date"]
    )


def main():

    df = load_data()

    print("=" * 50)
    print("Silver Layer Profile")
    print("=" * 50)

    print(f"Rows:    {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Memory:  {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")

    print("\nColumn Types")
    print("-" * 50)

    type_counts = (
        df.dtypes.astype(str)
        .replace({
            "object": "Object",
            "int64": "Integer",
            "float64": "Float",
            "bool": "Boolean",
            "datetime64[ns]": "Datetime",
        })
        .value_counts()
    )

    print(type_counts)

    print("\nTop Missing Values")
    print("-" * 50)

    missing = df.isnull().mean() * 100
    missing = missing[missing > 0].sort_values(ascending=False)

    if missing.empty:
        print("No missing values found. ✅")
    else:
        print(
            missing.head(10)
            .round(1)
            .astype(str)
            + "%"
        )

    print("\nDuplicate App IDs")
    print("-" * 50)

    duplicates = df["appid"].duplicated().sum()

    print(f"{duplicates:,} duplicates ({duplicates / len(df):.2%})")

    print("\nRelease Date Range")
    print("-" * 50)

    print(f"Earliest: {df['release_date'].min().date()}")
    print(f"Latest:   {df['release_date'].max().date()}")

    print("\nKey Metrics Summary")
    print("-" * 50)

    metrics = [
        "price",
        "positive_reviews",
        "negative_reviews",
        "peak_ccu",
        "average_playtime_forever",
    ]

    print(df[metrics].describe())

    print("-" * 50)

    print("\nTransformation Validation")
    print("=" * 50)

    checks = []

    checks.append((
        "Expected Column Count",
        len(df.columns) == len(EXPECTED_COLUMNS)
    ))

    checks.append((
        "Expected Schema",
        set(df.columns) == set(EXPECTED_COLUMNS)
    ))

    checks.append((
        "Renamed Columns",
        all(col in df.columns for col in RENAMED_COLUMNS)
    ))

    checks.append((
        "Bronze Columns Removed",
        all(col not in df.columns for col in REMOVED_COLUMNS)
    ))

    checks.append((
        "Duplicate App IDs",
        duplicates == 0
    ))

    checks.append((
        "Missing App IDs",
        df["appid"].isnull().sum() == 0
    ))

    checks.append((
        "Future Release Dates",
        (df["release_date"] <= pd.Timestamp.today()).all()
    ))

    checks.append((
        "Release Date Parsed",
        pd.api.types.is_datetime64_any_dtype(df["release_date"])
    ))

    passed = 0

    for name, result in checks:

        icon = "✅" if result else "❌"
        status = "PASS" if result else "FAIL"

        print(f"{icon} {name:<30} {status}")

        if result:
            passed += 1

    print("\nSilver Health Summary")
    print("=" * 50)

    overall = "HEALTHY ✅" if passed == len(checks) else "ISSUES DETECTED ❌"

    print(f"Overall Status: {overall}")
    print(f"Checks Passed:  {passed}/{len(checks)}")

    print("\nSilver Layer Ready for Gold " +
          ("✅" if passed == len(checks) else "❌"))
    
    
if __name__ == "__main__":
    main()