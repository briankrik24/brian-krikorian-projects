# Gold Layer Schema

## Purpose

The Gold layer contains an **analytics-ready dataset** built from the Silver layer.

Unlike the Silver layer, which focuses on standardized source data, the Gold layer introduces business logic and derived metrics that simplify SQL analysis and Power BI reporting.

The Gold dataset is designed to support interactive exploration of the Steam catalog, allowing users to search, filter, and compare games based on meaningful business metrics.

---

# Pipeline

**Input**

```
data/silver/games_clean.csv
```

↓

**Transformation**

```
src/transform/build_gold.py
```

↓

**Output**

```
data/gold/games_gold.csv
```

---

# Design Principles

The Gold layer should:

- Preserve one row per game
- Preserve all Silver columns
- Add analytics-friendly derived columns
- Avoid recalculating common business metrics in SQL or Power BI
- Support interactive filtering and game discovery

---

# Planned Derived Columns

| Gold Column | Source | Business Purpose | Example |
|-------------|--------|------------------|---------|
| release_year | release_date | Trend analysis | 2023 |
| release_month | release_date | Seasonality | March |
| release_decade | release_date | Long-term trends | 2020s |
| is_free_to_play | price | Simple filtering | True |
| price_bucket | price | Price segmentation | Budget |
| review_percentage | positive_reviews / total_reviews | Simplify reporting | 94.7 |
| review_category | review_percentage | Steam-style review labels | Very Positive |
| owner_min | estimated_owners | Lower ownership estimate | 200000 |
| owner_max | estimated_owners | Upper ownership estimate | 500000 |
| owner_midpoint | owner_min / owner_max | Numeric ownership estimate | 350000 |
| owner_bucket | owner_midpoint | Simplify grouping | Large |
| average_playtime_hours | average_playtime_forever | Easier interpretation | 42.5 |
| playtime_bucket | average_playtime_hours | Engagement segmentation | Hardcore |
| has_metacritic_score | metacritic_score | Quick filtering | True |
| has_achievements | achievements | Quick filtering | True |

---

# Business Rules

## Price Buckets

| Price | Bucket |
|--------|--------|
| $0.00 | Free to Play |
| <$10 | Budget |
| $10–30 | Mid-Range |
| $30–60 | Premium |
| >$60 | Deluxe |

---

## Review Categories

| Review % | Category |
|-----------|----------|
| 95–100 | Overwhelmingly Positive |
| 90–94 | Very Positive |
| 80–89 | Positive |
| 70–79 | Mostly Positive |
| 40–69 | Mixed |
| 20–39 | Mostly Negative |
| 0–19 | Overwhelmingly Negative |

---

## Ownership Buckets

| Estimated Owners | Bucket |
|-----------------|--------|
| <10,000 | Indie |
| 10k–100k | Small |
| 100k–1M | Medium |
| 1M–10M | Large |
| >10M | Massive |

---

## Playtime Buckets

| Average Hours | Bucket |
|---------------|--------|
| <5 | Very Casual |
| 5–20 | Casual |
| 20–100 | Dedicated |
| >100 | Hardcore |

---

# Intended Dashboard Experience

The Gold layer is designed to power an interactive game discovery dashboard.

Example filters include:

- Genre
- Price Bucket
- Free to Play
- Review Category
- Review Percentage
- Release Year
- Release Decade
- Estimated Owners
- Owner Bucket
- Average Playtime
- Playtime Bucket
- Windows
- Mac
- Linux
- Metacritic Available
- Has Achievements

The resulting dashboard should allow users to quickly identify highly rated games matching their preferred genres, price range, popularity, and engagement level.

---

# Planned Validation

The Gold profiling script will verify:

- All Silver rows preserved
- All Silver columns preserved
- Derived columns created successfully
- No duplicate App IDs
- No missing App IDs
- Review percentage between 0–100
- Owner midpoint calculated correctly
- Playtime hours calculated correctly

---

# Future Enhancements

Potential future additions include:

- Genre bridge table
- Developer bridge table
- Publisher bridge table
- Language dimension
- Platform dimension
- Recommendation score
- Bayesian review ranking
- Trending games metric