SELECT
    price_bucket,
    COUNT(*) AS games
FROM games_gold
GROUP BY price_bucket
ORDER BY games DESC;