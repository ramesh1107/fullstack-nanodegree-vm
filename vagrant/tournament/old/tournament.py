#!/usr/bin/env python
#
# tournament.py --
'''
This program is used for implementation of a Swiss-system tournament.
This program has code to creat required tables and drops these tables.
This program has cide to insert, update, delete data from tables.
There are 4 tables used in this program
plyr- Has the player information like id and name
tournament- This table is used to ensure this program can have matches across
            tournaments
match- This table is used to save match level data for each match in a given
            tournament.
score card- This table is used to list score of all scores across players in
            tournament

This program has options to give byes in case we have odd number of players


'''
import psycopg2



    

"""Connect to the PostgreSQL database.  Returns a database connection."""
 #def connect():
 #   return psycopg2.connect("dbname=tournament")
    
def connect(database_name="tournament"):
    try:
        DB = psycopg2.connect("dbname={}".format(database_name))
        c = DB.cursor()
        print "db connected"
        return DB, c
    except:
        print("unable to connect to database")


"""This procedure is to create the requred tables
This code is used to create tables called
    plyr
    tournament
    match
The player table has 5 columns which are
    ID (to uniquley identify a Player-assigned by the database)
    Name ( Name of the player)
    tid ( a serial number to uniquley identify any given
                tournament-assigned by the database)
    score  (score for match)
    matches (Number of matches)
    bye ( to indicate number of bye)
The tournament table has 2 columns which are
    ID (to uniquley identify a tournament-assigned by the database)
    Name ( Name of the tournament)
The match table has 5 columns which are
    tid ( a serial number to uniquley identify any given
          tournament-assigned by the database)
    winner  (to uniquley identify a Player-id)
    loser  (to uniquley identify a Player-id)
    draw (True in case of draw or false otherwise)
"""


def createtable():
    DB, c = connect()
   # c = DB.cursor()
    c.execute("create table  tournament\
        (tid SERIAL primary key ,\
        trnname TEXT Not Null );")

    c.execute("create table plyr (\
        pid   serial ,\
        pname TEXT Not Null,\
        tid int references tournament(tid) ON DELETE CASCADE,\
        score       Int Not Null DEFAULT 0,\
        matches      INT  Not Null DEFAULT 0,\
        bye      int Not Null DEFAULT 0);")
    
    c.execute("create table  match\
        (tid      INT  Not Null references tournament(tid) ON DELETE CASCADE ,\
        Winner     Int  Not Null ,\
        loser      INT    ,\
        draw      boolean Not Null);")
    DB.commit()
    DB.close()

'''
This procedure is used to drop tables when not required
'''


def droptable():
    DB, c = connect()
   
    c.execute("Drop TABLE  tournament cascade" )
    c.execute("Drop TABLE  plyr")    
    c.execute("Drop TABLE match")
    DB.commit()
    DB.close()

"""Remove all the match records from the database."""


def deleteMatches():
    DB, c = connect()
   # c = DB.cursor()
    c.execute("DELETE from match;")
    DB.commit()
    DB.close()


def deletePlayers():
    DB, c = connect()
 #   c = DB.cursor()
    c.execute("DELETE from plyr;")
    DB.commit()
    DB.close()


def deletetournament():
    DB, c = connect()
 #   c = DB.cursor()
    c.execute("DELETE from tournament;")
    DB.commit()
    DB.close()


"""Returns the number of players currently registered for a given tournament"""


def countplyr(tid):
    DB, c = connect()
  #  c = DB.cursor()
    c.execute("Select count(pid) from plyr")
    post = (c.fetchone())
    print "count of players", post
    return post[0]

"""Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
      Args:
      name: the player's full name (need not be unique).
"""


def createTournament(trname):
    """Create a new tournament.
    Args: Name of tournament
    """
    DB, c = connect()
   # c = DB.cursor()
    sql = "INSERT INTO tournament (trnname) VALUES (%s) RETURNING tid"
    c.execute(sql, (trname,))
    tid = c.fetchone()[0]
    DB.commit()
    DB.close()
    return tid

"""Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
      tid: id of tournament they are entering.
"""


def registerPlyr(tid, pname):
    DB, c = connect()
   # c = DB.cursor()
    print "inserting into plyr tournament id", tid
    plyr = "INSERT INTO plyr (pname,tid,score,matches,bye )\
            VALUES (%s,%s,0,0,0) RETURNING pid"
    c.execute(plyr, (pname, tid))
    pid = c.fetchone()[0]
    print "inserted player", tid, pname, pid
    DB.commit()
    DB.close()
    return pid

"""Returns a list of the players and their win records, sorted by wins.
    The first entry in the list will be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
        A list of tuples, each of which contains (id, name, wins, matches,
        bye or not,score):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
        bye: if player got a bye or not boolean
        score: score for each player
"""


def plyrStandings(tid):

    DB, c = connect()
   # c = DB.cursor()
    c.execute("SELECT pid, pname ,score,matches\
                FROM plyr\
                WHERE tid = tid \
                ORDER BY score DESC, matches DESC""")
    ranks = []
    for row in c.fetchall():
        ranks.append(row)
    DB.close()
    print "current ranks", ranks
    return ranks
"""Records the outcome of a single match between two players.
    Args:
      tid: the id of the tournament match was in
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      draw:  if the match was a draw
"""


def reportMatch(tid, winner, loser, draw):

    if draw == 'true':
        w_points = 1
        l_points = 1
    else:
        w_points = 3
        l_points = 0

    DB, c = connect()
    #c = DB.cursor()
    ins = "INSERT INTO match (tid, winner, loser, draw) \
            VALUES (%s,%s,%s,%s)"
    win = "UPDATE plyr SET score = score+%s, matches = matches+1\
            WHERE pid = %s AND tid = %s"
    los = "UPDATE plyr SET score = score+%s, matches = matches+1 \
            WHERE pid = %s AND tid = %s"
    c.execute(ins, (tid, winner, loser, draw))
    c.execute(win, (w_points, winner, tid))
    c.execute(los, (l_points, loser, tid))
    DB.commit()
    DB.close()


"""Checks if player has bye.
    Args:
        id: id of player to check
    Returns true or false.
"""


def hasBye(pid, tid):
    DB, c = connect()
  #  c = DB.cursor()
    sql = """SELECT bye
             FROM plyr
             WHERE pid = %s
             AND tid = %s"""
    c.execute(sql, (pid, tid))
    bye = c.fetchone()[0]
    DB.close()
    if bye == 0:
        return True
    else:
        return False

"""Assign points for a bye.
    Args:
      player: id of player who receives a bye.
      tid: the id of the tournament
"""


def reportBye(pid, tid):
    DB, c = connect()
  #  c = DB.cursor()
    bye = "UPDATE plyr SET score = score+3, bye=bye+1 \
           WHERE pid = %s AND tid = %s"
    c.execute(bye, (pid, tid))
    DB.commit()
    DB.close()

"""Checks if players already have a bye
    Args:
        tid: tournament id
        ranks: list of current ranks from swissPairings()
        index: index to check
    Returns first id that is valid or original id if none are found.
"""


def checkByes(tid, ranks, index):
    if abs(index) > len(ranks):
        return -1
    elif not hasBye(ranks[index][0], tid):
        return index
    else:
        return checkByes(tid, ranks, (index - 1))
"""Checks if two players have already had a match against each other.
    If they have, recursively checks through the list until a valid match is
    found.
    Args:
        tid: id of tournament
        ranks: list of current ranks from swissPairings()
        id1: player needing a match
        id2: potential matched player
    Returns id of matched player or original match if none are found.
"""


def checkPairs(tid, ranks, id1, id2):
    if id2 >= len(ranks):
        return id1 + 1
    elif validPair(ranks[id1][0], ranks[id2][0], tid):
        return id2
    else:
        return checkPairs(tid, ranks, id1, (id2 + 1))

"""Checks if two players have already played against each other, if
    they play against each other row count will be more than zero.
    Also check for player1vs player2 and player2 vs player1
    Args:
        p1: the id number of first player to check
        p2: the id number of potentail paired player
        tid: the id of the tournament
    Return true if valid pair, false if not

"""


def validPair(p1, p2, tid):
    DB, c = connect()
 #   c = DB.cursor()
    sql = """SELECT winner, loser
             FROM match
             WHERE ((winner = %s AND loser = %s)
                    OR (winner = %s AND loser = %s))
             AND tid = %s"""
    c.execute(sql, (p1, p2, p2, p1, 1))
    matches = c.rowcount
    DB.close()
    if matches > 0:
        return False
    else:
        return True
"""Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Args:
        tid: id of tournament you are gettings standings for
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
"""


def swissPairings(tid):
    ranks = plyrStandings(tid)
    pairs = []
    numplyr = countplyr(tid)
    if numplyr % 2 != 0:
        bye = ranks.pop(checkByes(tid, ranks, -1))
        reportBye(tid, bye[0])
    while len(ranks) > 1:
        validMatch = checkPairs(tid, ranks, 0, 1)
        p1 = ranks.pop(0)
        p2 = ranks.pop(validMatch - 1)
        pairs.append((p1[0], p1[1], p2[0], p2[1]))
    return pairs
