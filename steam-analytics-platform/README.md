# Steam Analytics Platform

An end-to-end ELT analytics project built using modern data engineering principles inspired by Microsoft Fabric's Medallion Architecture.

The project ingests publicly available Steam game data, profiles raw datasets for quality, transforms the data into analytics-ready tables, and ultimately serves business intelligence dashboards for exploring the Steam marketplace.

---

## Project Goals

- Build an end-to-end ELT pipeline
- Implement a Bronze → Silver → Gold architecture
- Perform automated data profiling and validation
- Build an analytics-ready warehouse
- Visualize insights using Power BI
- Demonstrate production-style analytics engineering practices

---

## Project Architecture

```
Kaggle Dataset
        │
        ▼
Extract
(download_dataset.py)
        │
        ▼
Bronze Layer
Raw Source Data
        │
        ▼
Analysis
(profile_bronze.py)
        │
        ▼
Silver Layer
Cleaned & Standardized Data
        │
        ▼
Gold Layer
Analytics-Ready Tables
        │
        ▼
DuckDB Warehouse
        │
        ▼
Power BI Dashboard
```

---

## Repository Structure

```
steam-analytics-platform/

├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── docs/
│   ├── data_dictionary.md
│   └── star_schema.md
│
├── src/
│   ├── extract/
│   ├── transform/
│   └── analysis/
│
├── requirements.txt
└── README.md
```

---

## Current Progress

### ✅ Bronze Layer

- Download latest Steam dataset from Kaggle
- Populate Bronze layer
- Profile raw data
- Validate dataset health

### ⏳ Silver Layer

- Clean and standardize source data
- Convert data types
- Remove unnecessary columns
- Prepare analytics-ready dataset

### ⏳ Gold Layer

- Build fact table
- Generate business metrics
- Prepare warehouse for reporting

### ⏳ Reporting

- DuckDB warehouse
- Power BI dashboards
- Executive analytics

---

## Technologies

- Python
- Pandas
- KaggleHub
- DuckDB *(planned)*
- Power BI *(planned)*
- Git
- GitHub

---

## Getting Started

Clone the repository.

Create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Download the latest Steam dataset.

```bash
python src/extract/download_dataset.py
```

Profile the Bronze layer.

```bash
python src/analysis/profile_bronze.py
```

---

## Current Status

**Version:** v0.2

Completed:

- Bronze layer ingestion
- Bronze layer profiling
- Dataset validation

In Progress:

- Silver layer transformations

---

## Future Enhancements

- DuckDB warehouse
- Star schema implementation
- Power BI executive dashboard
- Automated Markdown profiling reports
- Data validation framework
- CI/CD with GitHub Actions

---

## License

This project is intended for educational and portfolio purposes. Steam game metadata is sourced from publicly available datasets hosted on Kaggle.