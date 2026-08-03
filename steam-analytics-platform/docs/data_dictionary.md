# Steam Analytics Platform

## Data Dictionary

This document describes the fields used throughout the analytics pipeline.

| Column | Data Type | Purpose |
|---------|-----------|-------|
| appid | Integer | Primary key for each game |
| name | String | Game title |
| release_date | Date | Used for time-based analysis |
| price | Decimal | Pricing analysis |
| developers | String | Developer dimension |
| publishers | String | Publisher dimension |
| genres | String | Genre dimension |
| categories | String | Future analysis |
| positive | Integer | Positive review count |
| negative | Integer | Negative review count |
| pct_pos_total | Integer | Overall review score |
| recommendations | Integer | Number of recommendations |
| estimated_owners | String | Popularity estimate |
| peak_ccu | Integer | Peak concurrent users |
| average_playtime_forever | Integer | Engagement metric |
| metacritic_score | Integer | External review metric |
