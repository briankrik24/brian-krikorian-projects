"""
profile_database.py

Profiles the DuckDB database by validating the
database, tables, schema, and row counts.
"""

from pathlib import Path

import duckdb


DATABASE_FILE = Path("database/steam.db")
TABLE_NAME = "games_gold"


def connect_database():
    """Connect to the DuckDB database."""

    if not DATABASE_FILE.exists():
        raise FileNotFoundError(
            f"Database not found:\n{DATABASE_FILE.resolve()}"
        )

    return duckdb.connect(DATABASE_FILE)


def database_overview(conn):
    """Print database information."""

    print("=" * 50)
    print("DuckDB Database Profile")
    print("=" * 50)

    print(f"Database: {DATABASE_FILE.resolve()}")

    print("\nTables")
    print("-" * 50)

    tables = conn.execute(
        """
        SHOW TABLES
        """
    ).fetchall()

    for table in tables:
        print(table[0])


def table_summary(conn):
    """Print table statistics."""

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

    print("\nTable Summary")
    print("-" * 50)

    print(f"Table:    {TABLE_NAME}")
    print(f"Rows:     {row_count:,}")
    print(f"Columns:  {column_count}")


def schema_summary(conn):
    """Display the table schema."""

    print("\nSchema")
    print("-" * 50)

    schema = conn.execute(
        f"""
        DESCRIBE {TABLE_NAME}
        """
    ).fetchall()

    for column_name, data_type, *_ in schema:
        print(f"{column_name:<35} {data_type}")


def validate_database(conn):
    """Validate the database."""

    print("\nDatabase Validation")
    print("=" * 50)

    checks = {
        "Database Exists":
            DATABASE_FILE.exists(),

        "games_gold Table Exists":
            conn.execute(
                f"""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_name = '{TABLE_NAME}'
                """
            ).fetchone()[0] == 1,

        "Table Contains Rows":
            conn.execute(
                f"""
                SELECT COUNT(*)
                FROM {TABLE_NAME}
                """
            ).fetchone()[0] > 0,
    }

    passed = 0

    for name, result in checks.items():

        status = "PASS" if result else "FAIL"

        print(
            f"{'✅' if result else '❌'} "
            f"{name:<30} {status}"
        )

        if result:
            passed += 1

    print("\nDatabase Health Summary")
    print("=" * 50)

    overall = (
        "HEALTHY ✅"
        if passed == len(checks)
        else "ISSUES FOUND ❌"
    )

    print(f"Overall Status: {overall}")
    print(f"Checks Passed:  {passed}/{len(checks)}")


def main():

    conn = connect_database()

    database_overview(conn)

    table_summary(conn)

    schema_summary(conn)

    validate_database(conn)

    conn.close()


if __name__ == "__main__":
    main()