# Steam Analytics Platform

## Star Schema

### FactGames

One record per Steam game.

| Column |
|---------|
| appid (PK) |
| release_date_key |
| developer_key |
| publisher_key |
| genre_key |
| price |
| recommendations |
| positive_reviews |
| negative_reviews |
| pct_positive |
| estimated_owners |
| peak_ccu |
| average_playtime |
| metacritic_score |

---

### DimDate

| Column |
|---------|
| date_key |
| release_date |
| year |
| quarter |
| month |
| month_name |

---

### DimDeveloper

| Column |
|---------|
| developer_key |
| developer_name |

---

### DimPublisher

| Column |
|---------|
| publisher_key |
| publisher_name |

---

### DimGenre

| Column |
|---------|
| genre_key |
| genre_name |
