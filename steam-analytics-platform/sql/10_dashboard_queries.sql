-- Best Budget Games
SELECT
    game_name,
    price,
    positive_review_percentage
FROM games_gold
WHERE
    price_bucket = 'Budget'
ORDER BY positive_review_percentage DESC;

-- Best Mac Games
SELECT
    game_name,
    review_category,
    price
FROM games_gold
WHERE mac = TRUE
ORDER BY positive_review_percentage DESC;

-- Best Recent Games
SELECT
    game_name,
    release_year,
    positive_review_percentage
FROM games_gold
WHERE release_year >= 2020
ORDER BY positive_review_percentage DESC;