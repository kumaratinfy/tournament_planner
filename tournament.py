#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach #Whitelist based HTML sanitization library


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
    """Registers a player for the tournament
    
    Arg: 
      Name of the player
    
    """
    try:
        conn = connect()
        cur = conn.cursor()
	''' Adding a player to the Players Table registers players for a tournament
	    by making an entry into tournament table through a trigger
	'''
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
        """Appends match and outcome of the match for the winner"""
        cur.execute("""UPDATE Tournament SET matches=array_append(matches, %s), 
                                             results=array_append(results, 'win') where PlayerId=%s""",
                                             (loser, winner));
                                             
        """Appends match and outcome of the match for the loser"""
        cur.execute("""UPDATE Tournament SET matches=array_append(matches, %s),
                                             results=array_append(results, 'lose') where PlayerId=%s""",
                                             (winner, loser));
        conn.commit()
        cur.close()
        conn.close()
    except:
        print 'Unable to connect to the database'
    
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    
    Returns:
      A list where each entry is a tuple where each tuple contains:
      First Player's Name
      First Player's Id
      Next Round Opponent's Name
      Next Round Opponent;s Id
    """
    standings = playerStandings()
    size = len(standings)
    l = [] 
    i = 0
    while(i < size-1):
    	"""Insert into the list a tuple containing the next round opponent names and ID's """
        l.append([standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1]])
        i += 2
    return l
