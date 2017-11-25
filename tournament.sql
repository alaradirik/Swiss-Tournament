-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
    id SERIAL,
    player_name TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE tournament_matches (
    id SERIAL,
    player_one_id INTEGER REFERENCES players(id),
    player_one_points INTEGER,
    player_two_id INTEGER REFERENCES players(id),
    player_two_points INTEGER,
    PRIMARY KEY (id)
);

-- Function to calculate the Opponent Match Win Points. Used by the player standings function
CREATE OR REPLACE FUNCTION getOMWPoints(player_id int) returns NUMERIC as $$ 
    DECLARE opponents INT[];
    DECLARE p1Points NUMERIC;
    DECLARE p2Points NUMERIC;
    DECLARE total_points NUMERIC;
    BEGIN
        opponents := (SELECT ARRAY(SELECT (CASE WHEN player_one_id = player_id THEN player_two_id ELSE player_one_id END) as opponent_id
                     FROM tournament_matches 
                     WHERE (player_one_id = player_id OR player_two_id = player_id)));
        p1Points := (SELECT SUM(player_one_points)
                    FROM tournament_matches 
                    WHERE player_one_id = ANY(opponents));
        
        p2Points := (SELECT SUM(player_two_points)
                    FROM tournament_matches 
                    WHERE player_two_id = ANY(opponents));
        total_points = p1Points + p2Points;
        return total_points;
                   
    END;
$$ LANGUAGE plpgsql;

CREATE VIEW player_standings AS (
	SELECT players.id,
        players.player_name,
        (   SELECT count(id) 
            FROM tournament_matches 
            WHERE (
                player_one_points = 3 AND player_one_id = players.id
            )
            OR (
                  player_two_points = 3 AND player_two_id = players.id
            )
        )::int as wins,
      (   SELECT count(id) 
            FROM tournament_matches 
            WHERE (
                player_one_id = players.id OR player_two_id = players.id
            )
        )::int as matches,
        (   SELECT count(id) 
            FROM tournament_matches 
            WHERE (
                player_one_points = 1 AND player_one_id = players.id
            )
            OR (
                  player_two_points = 1 AND player_two_id = players.id
            )
        )::int as draws,
  
        getOMWPoints(players.id)::int as OMW
    FROM players
    ORDER BY wins DESC, OMW DESC
);



