-- Show all tables
SHOW TABLES;

-- Preview the dataset
SELECT *
FROM games_gold
LIMIT 10;

-- Count rows
SELECT COUNT(*)
FROM games_gold;

-- Count columns
DESCRIBE games_gold;

-- Release year range
SELECT
    MIN(release_year),
    MAX(release_year)
FROM games_gold;