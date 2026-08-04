SELECT
    SUM(CAST(windows AS INTEGER)) AS windows_games,
    SUM(CAST(mac AS INTEGER)) AS mac_games,
    SUM(CAST(linux AS INTEGER)) AS linux_games
FROM games_gold;