#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""DELETE FROM Tournament;""")
        conn.commit()
        cur.close()
        conn.close()
    except:
        print 'Unable to connect to the database'


def deletePlayers():
    """Remove all the player records from the database."""
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""DELETE FROM Players;""")
        conn.commit()
        cur.close()
        conn.close()
    except:
        print 'Unable to connect to the database'


def countPlayers():
    """Returns the number of players currently registered."""
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""SELECT COUNT(*) FROM Players;""")
        result = cur.fetchone()
        count = result[0]
        cur.close()
        conn.close()
        return count
    except:
        print 'Unable to connect to the database'
	

def registerPlayer(name):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""INSERT INTO Players(Name) Values (%s)""", (bleach.clean(name), ))
        conn.commit()
        cur.close()
        conn.close()
    except:
        print 'Unable to connect to the database'

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""SELECT * FROM CURRENT_STANDINGS;""");
        result = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return result
    except:
        print 'Unable to connect to the database'


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""UPDATE Tournament SET matches=array_append(matches, %s),
                                             results=array_append(results, 'win') where Player1=%s""",
                                             (loser, winner));
        cur.execute("""UPDATE Tournament SET matches=array_append(matches, %s),
                                             results=array_append(results, 'lose') where Player1=%s""",
                                             (winner, loser));
        conn.commit()
        cur.close()
        conn.close()
    except:
        print 'Unable to connect to the database'
    
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match."""
    standings = playerStandings()
    size = len(standings)
    l = []
    i = 0
    while(i < size-1):
        l.append([standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1]])
        i += 2
    return l
