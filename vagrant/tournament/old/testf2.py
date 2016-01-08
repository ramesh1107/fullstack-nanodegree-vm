#!/usr/bin/env python
#This program is used to test python program tournament.py 
# Test cases for tournament.py

from tf2 import *

def testcreatetable():
    print "cursor created-table creation"
    createtable()


def testdroptbales():
    print "cursor drop table creation"
    droptable()


def testCount():
    deleteMatches()
    deletePlayers()
    deletetournament()
    tid=createTournament(1,"India Open")
    print "india open created"
    c = countplyr(tid)
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    
    print "3. After deleting, countPlayers() returns zero."
     

def testRegister():
    deleteMatches()    
    deletePlayers()
    deletetournament()
    tid=createTournament(1,"Indian Open")
    registerPlyr(1,"Chandra Nalaar",1)
    c = countplyr(tid)
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."
     

def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    deletetournament()
    tid=createTournament(1,"US Open")
    registerPlyr(1,"Markov Chaney",1)
    registerPlyr(2,"Joe Malik",1)
    registerPlyr(3,"Mao Tsu-hsi",3)
    registerPlyr(4,"Atlanta Hope",4)
    c = countplyr(tid)
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countplyr(tid)
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."
     


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    deletetournament()
    tid=createTournament(1,"AUS Open")
    registerPlyr(1,"Melpomene Murray",1)
    registerPlyr(2,"Randy Schwartz",1)
    standings = plyrStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, score1,matches1), (id2,name2, score2,matches2)] = standings
    if matches1 != 0 or matches2 != 0 or score1 != 0 or score2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    print "6. Newly registered players appear in the standings with no matches."
     
def testReportMatches():
    deleteMatches()
    deletePlayers()
    tid=createTournament(1,"Wimbeldon")
    registerPlyr(1,"Bruno Walton",1)
    registerPlyr(2,"Boots O'Neal",1)
    registerPlyr(3,"Cathy Burton",1)
    registerPlyr(4,"Diane Grant",1)
    standings = plyrStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    print "id1", id1
    print "id3" ,id3
    reportMatch(1,id1, id2,"false")
    reportMatch(1,id3, id4,"false")
    standings = plyrStandings()
    for (i, n, s, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and s != 3:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and s != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."

def testPairings():
    deleteMatches()
    deletePlayers()
    tid=createTournament(1,"frenchopen")
    registerPlyr(1,"Twilight Sparkle",1)
    registerPlyr(2,"Fluttershy",1)
    registerPlyr(3,"Applejack",1)
    registerPlyr(4,"Pinkie Pie",1)
    standings = plyrStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(1,id1, id2,"false")
    reportMatch(1,id3, id4,"false")
    pairings = swissPairings(2)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."
    print "testpairings- Tested successfully"
 
if __name__ == '__main__':
  #testcreatetable()
  #  testDeleteMatches()
  #  testDelete()
  testCount()
  testRegister()
  testRegisterCountDelete()
  testStandingsBeforeMatches()
  testReportMatches()
  testPairings()
  print "Success!  All tests pass!"
