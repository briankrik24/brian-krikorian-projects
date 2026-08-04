SELECT
    game_name,
    average_playtime_hours,
    review_category,
    estimated_owner_bucket
FROM games_gold
ORDER BY average_playtime_hours DESC
LIMIT 25;