# Silver Layer Schema

## Purpose

The Silver layer contains **cleaned, standardized, and analytics-ready source data**.

Unlike the Bronze layer, the Silver layer:

- Removes unnecessary columns
- Standardizes data types
- Renames columns for clarity
- Preserves one row per game
- Does **not** contain derived business metrics

Business calculations (review percentages, release year, price buckets, etc.) belong in the Gold layer.

---

## Pipeline

**Input**

```
data/bronze/games_march2025_cleaned.csv
```

↓

**Transformation**

```
src/transform/build_silver.py
```

↓

**Output**

```
data/silver/games_clean.csv
```

---

# Columns Retained

| Bronze Column | Silver Column | Action |
|---------------|---------------|--------|
| appid | appid | Keep |
| name | game_name | Rename |
| release_date | release_date | Convert to datetime |
| required_age | required_age | Keep |
| price | price | Keep |
| dlc_count | dlc_count | Keep |
| windows | windows | Keep |
| mac | mac | Keep |
| linux | linux | Keep |
| metacritic_score | metacritic_score | Keep |
| achievements | achievements | Keep |
| recommendations | recommendations | Keep |
| developers | developers | Keep |
| publishers | publishers | Keep |
| categories | categories | Keep |
| genres | genres | Keep |
| user_score | user_score | Keep |
| positive | positive_reviews | Rename |
| negative | negative_reviews | Rename |
| estimated_owners | estimated_owners | Keep |
| average_playtime_forever | average_playtime_forever | Keep |
| average_playtime_2weeks | average_playtime_2weeks | Keep |
| median_playtime_forever | median_playtime_forever | Keep |
| median_playtime_2weeks | median_playtime_2weeks | Keep |
| discount | discount | Keep |
| peak_ccu | peak_ccu | Keep |
| pct_pos_total | pct_positive_reviews | Rename |
| num_reviews_total | total_reviews | Rename |
| pct_pos_recent | pct_positive_recent | Rename |
| num_reviews_recent | recent_reviews | Rename |

---

# Columns Removed

| Bronze Column | Reason |
|---------------|--------|
| detailed_description | Large text field not used for analytics |
| about_the_game | Large text field not used for analytics |
| short_description | Large text field not used for analytics |
| reviews | 88% missing |
| header_image | Image URL not needed for reporting |
| website | 54% missing |
| support_url | Not relevant for analytics |
| support_email | Not relevant for analytics |
| metacritic_url | 96% missing |
| notes | 81% missing |
| supported_languages | Candidate for future normalization |
| full_audio_languages | Candidate for future normalization |
| packages | Nested data structure |
| screenshots | Image URLs |
| movies | Video URLs |
| score_rank | Nearly 100% missing |
| tags | Candidate for Version 2 normalization |

---

# Planned Transformations

- Convert `release_date` to datetime
- Rename columns for consistency
- Remove duplicate App IDs (if present)
- Preserve one row per game
- Preserve null values unless clearly invalid
- Export cleaned dataset to the Silver layer

---

# Gold Layer Preview

The Gold layer will build upon the Silver layer by adding business logic and derived metrics.

Planned additions include:

- review_percentage
- release_year
- release_month
- is_free_to_play
- owner_midpoint
- price_bucket

The Gold layer will remain **one row per game**, while providing analytics-ready data for SQL queries and Power BI dashboards.