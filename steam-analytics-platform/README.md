# Steam Analytics Platform

An end-to-end Analytics Engineering project that transforms raw Steam game data into an analytics-ready dataset for SQL and Power BI reporting.

## Project Overview

This project demonstrates a modern ELT pipeline using a Medallion Architecture (Bronze → Silver → Gold).

The pipeline:

- Downloads the latest Steam dataset from Kaggle
- Stores raw source data in a Bronze layer
- Profiles and validates raw data quality
- Cleans and standardizes the dataset into a Silver layer
- Validates transformation results
- Builds an analytics-ready Gold layer *(in progress)*
- Loads the final dataset into DuckDB for SQL analytics
- Visualizes insights in Power BI

---

# Architecture

```
Kaggle Dataset
      │
      ▼
download_dataset.py
      │
      ▼
Bronze Layer
      │
      ▼
profile_bronze.py
      │
      ▼
build_silver.py
      │
      ▼
Silver Layer
      │
      ▼
profile_silver.py
      │
      ▼
Gold Layer (In Progress)
      │
      ▼
DuckDB
      │
      ▼
Power BI
```

---

# Current Status

## ✅ Bronze Layer

- Download Steam dataset from Kaggle
- Store raw dataset
- Profile data quality
- Validate raw data integrity

## ✅ Silver Layer

- Remove unnecessary columns
- Standardize schema
- Rename analytics fields
- Convert data types
- Validate transformation
- Profile transformed dataset

## 🚧 Gold Layer

Planned features:

- Business-friendly metrics
- Derived analytics columns
- DuckDB warehouse
- SQL analysis
- Power BI dashboard

---

# Pipeline Results

| Layer | Rows | Columns | Memory |
|-------|------:|--------:|-------:|
| Bronze | 89,618 | 47 | 675 MB |
| Silver | 89,618 | 30 | 59 MB |

The Silver transformation preserves all game records while reducing memory usage by approximately **91%** through the removal of unnecessary text, URL, and metadata fields.

---

# Repository Structure

```
steam-analytics-platform/

├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── docs/
│   ├── data_dictionary.md
│   └── silver_schema.md
│
├── src/
│   ├── analysis/
│   │   ├── profile_bronze.py
│   │   └── profile_silver.py
│   │
│   ├── extract/
│   │   └── download_dataset.py
│   │
│   └── transform/
│       └── build_silver.py
│
├── requirements.txt
└── README.md
```

---

# Technologies

- Python
- Pandas
- KaggleHub
- DuckDB *(planned)*
- SQL *(planned)*
- Power BI *(planned)*

---

# Project Progress

- ✅ Bronze Layer
- ✅ Bronze Profiling
- ✅ Silver Layer
- ✅ Silver Profiling
- ⬜ Gold Layer
- ⬜ Gold Profiling
- ⬜ DuckDB Warehouse
- ⬜ SQL Analytics
- ⬜ Power BI Dashboard

---

# Future Enhancements

- Gold analytics layer
- DuckDB warehouse
- SQL reporting queries
- Interactive Power BI dashboard
- Additional data quality validation