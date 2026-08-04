SELECT
    review_category,
    COUNT(*) AS games,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(AVG(average_playtime_hours), 1) AS average_playtime
FROM games_gold
GROUP BY review_category
ORDER BY average_price DESC;