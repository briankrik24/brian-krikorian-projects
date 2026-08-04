"""
load_duckdb.py

Loads the Gold dataset into a DuckDB database
for SQL analytics and Power BI reporting.
"""

from pathlib import Path

import duckdb
import pandas as pd


GOLD_FILE = Path("data/gold/games_gold.csv")
DATABASE_FILE = Path("database/steam.db")

TABLE_NAME = "games_gold"


def load_gold():
    """Load the Gold dataset."""

    if not GOLD_FILE.exists():
        raise FileNotFoundError(
            f"Gold dataset not found:\n{GOLD_FILE.resolve()}"
        )

    return pd.read_csv(
        GOLD_FILE,
        parse_dates=["release_date"],
    )


def connect_database():
    """Create or connect to the DuckDB database."""

    DATABASE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    return duckdb.connect(DATABASE_FILE)


def load_table(conn, df):
    """Load the Gold dataset into DuckDB."""

    conn.register("gold_df", df)

    conn.execute(
        f"""
        CREATE OR REPLACE TABLE {TABLE_NAME} AS
        SELECT *
        FROM gold_df
        """
    )


def validate_load(conn, df):
    """Validate that all rows were loaded."""

    database_rows = conn.execute(
        f"""
        SELECT COUNT(*)
        FROM {TABLE_NAME}
        """
    ).fetchone()[0]

    csv_rows = len(df)

    if database_rows != csv_rows:
        raise ValueError(
            f"""
Loaded row count does not match.

CSV Rows:      {csv_rows:,}
Database Rows: {database_rows:,}
"""
        )

    print("\nDuckDB validation passed.")


def print_summary(conn):
    """Print database summary."""

    row_count = conn.execute(
        f"""
        SELECT COUNT(*)
        FROM {TABLE_NAME}
        """
    ).fetchone()[0]

    column_count = conn.execute(
        f"""
        SELECT COUNT(*)
        FROM information_schema.columns
        WHERE table_name = '{TABLE_NAME}'
        """
    ).fetchone()[0]

    print("\nDuckDB database successfully updated.")
    print(f"Database: {DATABASE_FILE.resolve()}")
    print(f"Table:    {TABLE_NAME}")
    print(f"Rows:     {row_count:,}")
    print(f"Columns:  {column_count}")


def main():

    df = load_gold()

    conn = connect_database()

    load_table(conn, df)

    validate_load(conn, df)

    print_summary(conn)

    conn.close()


if __name__ == "__main__":
    main()