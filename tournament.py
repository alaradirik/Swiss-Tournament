#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#


import psycopg2
import random
byes = []


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Unable to connect to database")


def deleteMatches():
    """Remove all the match records from the database."""
    byes = []
    db, cursor = connect()
    query = "DELETE FROM tournament_matches;"
    cursor.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    query = "DELETE FROM players;"
    cursor.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    query = "SELECT COUNT(*) FROM players;"
    cursor.execute(query)
    results = cursor.fetchone()
    db.close()
    player_count = results[0]
    return player_count


def getPlayers():
    """Returns a list of player names."""
    db, cursor = connect()
    query = "SELECT * FROM players;"
    cursor.execute(query)
    results = cursor.fetchall()
    rows = ({'player_name': str(row[1])} for row in results)
    db.close()
    return rows


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    query = "INSERT INTO players (player_name) VALUES (%s);"
    parameter = (name,)
    cursor.execute(query, parameter)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains:
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
        draws: the number of draws
        omw: the sum of Opponent Match Wins
    """
    standings = []
    db, cursor = connect()
    query = "SELECT * FROM player_standings;"
    cursor.execute(query)
    for row in cursor.fetchall():
        standings.append((row[0], str(row[1]), row[2], row[3], row[4], row[5]))
    db.close()
    return standings


def reportMatch(p_one_id, p_one_points, p_two_id, p_two_points):
    """Records the outcome of a single match between two players.

    Args:
      p_one_id:  the id number of player one
      p_one_points:  the points won by player one
      p_two_id:  the id number of player two
      p_two_points:  the points won by player two
    """

    db, cursor = connect()
    query = "INSERT INTO tournament_matches \
        (player_one_id, player_one_points, player_two_id, \
        player_two_points) VALUES (%s, %s, %s, %s) "
    parameters = (p_one_id, p_one_points, p_two_id, p_two_points, )
    cursor.execute(query, parameters)
    db.commit()
    db.close()


def tournamentRounds():
    """Returns the number of tournament rounds based on the player count

    Returns:
        rounds: an integer with the number of rounds in the tournament
    """
    player_count = countPlayers()
    rounds = (player_count + 7) / 5
    return rounds


def tournamentWinner():
    """Returns a statement advising of the tournament winner

    Uses the player_standings view to determine first placed based on the
    number of wins and the opponent match win points.

    Returns:
        winner_statement: a formatted string providing details on the winner
    """
    db, cursor = connect()
    query = "SELECT * FROM player_standings LIMIT 1;"
    cursor.execute(query)
    winner = cursor.fetchone()
    db.close()
    winner_statement = '''
        The winner of this tournament is {player_name}.
        With {wins} wins, {draws} draws and {omw} opponent match wins
        in {matches} rounds.
    '''
    return winner_statement.format(
        player_name=winner[1],
        wins=str(winner[2]),
        draws=str(winner[3]),
        matches=str(winner[4]),
        omw=str(winner[5])
    )
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    player_count = countPlayers()
    standings = playerStandings()
    pairings = []
    match_counter = 0
    """Check to see if there is an odd number of players.
    If there is an odd number of players then assign a bye to one at random.
    If a player has already had a bye then another player needs to be selected
    at random
    """
    if (player_count % 2 != 0):
        player_count = player_count - 1
        bye_player = random.choice(standings)
        while bye_player[0] in byes:
            bye_player = random.choice(standings)
        pairings.append((bye_player[0], bye_player[1], 0, ""))
        standings.remove(bye_player)
        byes.append(bye_player[0])
    while match_counter < player_count:
        pairings.append((standings[match_counter][0],
                        standings[match_counter][1],
                        standings[match_counter + 1][0],
                        standings[match_counter + 1][1]))
        match_counter += 2
    return pairings
