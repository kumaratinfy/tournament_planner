-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

------------------------------------------------------------------        
-- Stores currently registered playes
CREATE TABLE Players(
        Id SERIAL PRIMARY KEY,
        Name TEXT);
------------------------------------------------------------------        

--Store information of matches of the tournament
CREATE TYPE Result as ENUM('win', 'lose'); --Represents possible outcomes of a match
CREATE TABLE Tournament(
        PLAYER1 Integer references Players(Id) ON DELETE CASCADE, --Makes sure player is present in Players Table 
        matches integer[], 
        results Result[]);
------------------------------------------------------------------        

--Trigger function to invoke when a new player is added
CREATE OR REPLACE FUNCTION add_player_tournament()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO Tournament VALUES(NEW.Id, NULL, NULL); --Initialize matches and results to NULL

    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';
------------------------------------------------------------------        

-- Trigger to register player for a tournament
CREATE TRIGGER add_play_tour
    AFTER INSERT
    ON Players
    FOR EACH ROW
    EXECUTE PROCEDURE add_player_tournament();
------------------------------------------------------------------        

--Calculate wins of a player
CREATE OR REPLACE FUNCTION count_wins(Result[]) returns int AS $$
DECLARE
    wins int := 0;
    x Result;
BEGIN
    FOREACH x in ARRAY $1 --Loop through results of a player
    LOOP
        IF x = 'win' THEN
            wins := wins + 1;
        END IF;
    END LOOP;
    RETURN wins;
EXCEPTION WHEN OTHERS THEN
    RETURN 0;
END;
$$ LANGUAGE 'plpgsql';

------------------------------------------------------------------

--Calculate matches of a player
CREATE OR REPLACE FUNCTION count_matches(int[]) returns int AS $$
DECLARE
    x int;
    matches int := 0;
BEGIN
    FOREACH x in ARRAY $1 --Loops through matches played by a player
    LOOP
        matches := matches + 1;
    END LOOP;
    RETURN matches;
EXCEPTION WHEN OTHERS THEN
    RETURN 0;
END;
$$ LANGUAGE 'plpgsql';

------------------------------------------------------------------

--View to give Current Standing of a player. It's Id, name wins and matches
CREATE VIEW Current_Standings as 
    select id, name, 
           count_wins(results) as wins,
           count_matches(matches) as matches
    from Players P, Tournament T
    where P.Id = T.PLAYER1
    ORDER BY wins DESC;

------------------------------------------------------------------        
