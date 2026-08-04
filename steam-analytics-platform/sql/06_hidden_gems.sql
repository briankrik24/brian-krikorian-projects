SELECT
    game_name,
    positive_review_percentage,
    total_reviews,
    review_category,
    estimated_owner_bucket,
    price
FROM games_gold
WHERE
    review_category IN ('Excellent', 'Exceptional')
    AND estimated_owner_bucket IN ('Indie', 'Small')
    AND total_reviews >= 100
ORDER BY
    positive_review_percentage DESC,
    total_reviews DESC;