-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Stores currently registered playes
CREATE TABLE Players(
        Id SERIAL PRIMARY KEY, 
        Name TEXT);

--Store information of matches of the tournament
CREATE TYPE Result as ENUM('win', 'lose');
CREATE TABLE Tournament(
        PLAYER1 Integer references Players(Id) ON DELETE CASCADE, 
        matches integer[], 
        results Result[]);

--Trigger function to invoke when a new player is added
CREATE OR REPLACE FUNCTION add_player_tournament()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO Tournament VALUES(NEW.Id, NULL, NULL);

    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

-- Trigger to register player for a tournament
CREATE TRIGGER add_play_tour
    AFTER INSERT
    ON Players
    FOR EACH ROW
    EXECUTE PROCEDURE add_player_tournament();



