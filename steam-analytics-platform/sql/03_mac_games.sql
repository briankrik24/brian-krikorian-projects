SELECT
    game_name,
    price_bucket,
    review_category
FROM games_gold
WHERE mac = TRUE;