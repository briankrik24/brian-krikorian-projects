SELECT
    game_name,
    positive_review_percentage,
    estimated_owner_midpoint
FROM games_gold
ORDER BY positive_review_percentage DESC
LIMIT 25;