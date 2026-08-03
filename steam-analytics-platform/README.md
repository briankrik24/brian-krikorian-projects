# 🎮 Steam Analytics Platform

An end-to-end analytics engineering project that transforms raw Steam game data into an analytics-ready dataset using a Medallion Architecture (Bronze → Silver → Gold), with automated profiling, data validation, and business-focused transformations.

The finished dataset is designed for SQL analytics and an interactive Power BI game discovery dashboard.

---

## Project Goals

- Build a production-style ETL pipeline using Python and Pandas
- Implement a Medallion Architecture
- Validate data quality at every stage
- Create an analytics-ready semantic layer
- Load curated data into DuckDB
- Build an interactive Power BI dashboard for exploring Steam games

---

## Project Architecture

```
Steam Dataset
      │
      ▼
download_dataset.py
      │
      ▼
Bronze Layer
      │
      ├── profile_bronze.py
      ▼
Silver Layer
      │
      ├── profile_silver.py
      ▼
Gold Layer
      │
      ├── profile_gold.py
      ▼
DuckDB
      ▼
Power BI Dashboard
```

---

# Repository Structure

```
steam-analytics-platform/
│
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── docs/
│   ├── silver_schema.md
│   └── gold_schema.md
│
├── src/
│   ├── extract/
│   │   └── download_dataset.py
│   │
│   ├── transform/
│   │   ├── build_silver.py
│   │   └── build_gold.py
│   │
│   ├── analysis/
│   │   ├── profile_bronze.py
│   │   ├── profile_silver.py
│   │   └── profile_gold.py
│   │
│   └── load/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ETL Pipeline

## Bronze Layer

Purpose:

- Preserve the raw source dataset
- Perform initial profiling
- Detect missing values, duplicates, and schema issues

Outputs:

- Bronze dataset
- Bronze profiling report

---

## Silver Layer

Purpose:

- Select required columns
- Rename fields for consistency
- Standardize data types
- Validate cleaned data

Outputs:

- Clean analytics dataset
- Silver profiling report

---

## Gold Layer

Purpose:

Create business-friendly features for analytics and reporting.

Derived columns include:

- Release Year
- Release Month
- Release Decade
- Price Bucket
- Review Category
- Positive Review Percentage
- Estimated Owner Midpoint
- Estimated Owner Bucket
- Average Playtime (Hours)
- Playtime Bucket
- Has Metacritic
- Has Achievements

Outputs:

- Analytics-ready dataset
- Gold profiling report

---

# Technologies

- Python
- Pandas
- DuckDB *(coming next)*
- SQL *(coming next)*
- Power BI *(coming next)*

---

# Current Status

## ✅ Complete

- Dataset ingestion
- Bronze layer
- Bronze profiling
- Silver transformation
- Silver profiling
- Gold transformation
- Gold profiling
- Documentation
- Git version control

## 🚧 In Progress

- DuckDB loading
- SQL analytics
- Power BI dashboard

---

# Future Dashboard

The final Power BI dashboard will function as a Steam game discovery tool.

Users will be able to filter games by attributes such as:

- Platform (Windows / Mac / Linux)
- Price Bucket
- Review Category
- Genres
- Categories
- Release Year
- Release Decade
- Estimated Owners
- Playtime Bucket
- Metacritic Availability
- Achievements

The goal is to make discovering games as intuitive as querying an analytics model.

---

# Author

**Brian Krikorian**

Built as a portfolio project to demonstrate analytics engineering, ETL development, data validation, and business intelligence workflows.