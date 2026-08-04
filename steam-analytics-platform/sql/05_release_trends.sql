SELECT
    release_year,
    COUNT(*) AS releases
FROM games_gold
GROUP BY release_year
ORDER BY release_year;