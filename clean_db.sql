DROP VIEW IF EXISTS CURRENT_STANDINGS;
DROP FUNCTION IF EXISTS count_wins(Result[]);
DROP FUNCTION IF EXISTS count_matches(int[]);
DROP TABLE IF EXISTS tournament;
DROP type IF EXISTS result;
DROP Trigger IF EXISTS add_play_tour on players cascade;
DROP FUNCTION IF EXISTS add_player_tournament();
DROP TABLE IF EXISTS players;
