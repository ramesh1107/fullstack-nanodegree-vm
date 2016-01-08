#!/usr/bin/env python
#This program is used to test python program tournament.py 
# Test cases for tournament.py

from tournament import *

def testcreatetable():
    print "cursor created-table creation"
    createtable()


def testdroptbales():
    print "cursor drop table creation"
    droptable()


def testCount():
    #deleteMatches()
    #deletePlayers()
    #deletetournament()
    tid=createTournament("India Open")
    print "india open created"
    cnt = countplyr(tid)
    if cnt == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if cnt != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    
    print "3. After deleting, countPlayers() returns zero."
     

def testRegister():
    deleteMatches()    
    deletePlayers()
    deletetournament()
    tid=createTournament("Indian Open")
    registerPlyr(tid,"Chandra Nalaar")
    c = countplyr(tid)
    print "count of player" , c
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."
     

def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    deletetournament()
    tid=createTournament("US Open")
    registerPlyr(tid,"Markov Chaney")
    registerPlyr(tid,"Joe Malik")
    registerPlyr(tid,"Mao Tsu-hsi")
    registerPlyr(tid,"Atlanta Hope")
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
    tid=createTournament("AUS Open")
    registerPlyr(tid,"Melpomene Murray")
    registerPlyr(tid,"Randy Schwartz")
    standings = plyrStandings(tid)
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
    tid=createTournament("Wimbeldon")
    registerPlyr(tid,"Bruno Walton")
    registerPlyr(tid,"Boots O'Neal")
    registerPlyr(tid,"Cathy Burton")
    registerPlyr(tid,"Diane Grant")
    standings = plyrStandings(tid)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    print "id1", id1
    print "id3" ,id3
    reportMatch(tid,id1, id2,"false")
    reportMatch(tid,id3, id4,"false")
    standings = plyrStandings(tid)
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
    tid=createTournament("frenchopen")
    registerPlyr(tid,"Twilight Sparkle")
    registerPlyr(tid,"Fluttershy")
    registerPlyr(tid,"Applejack")
    registerPlyr(tid,"Pinkie Pie")
    standings = plyrStandings(tid)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tid,id1, id2,"false")
    reportMatch(tid,id3, id4,"false")
    pairings = swissPairings(tid)
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
  testdroptbales()
  testcreatetable()
  #  testDeleteMatches()
  #  testDelete()
  testCount()
  testRegister()
  testRegisterCountDelete()
  testStandingsBeforeMatches()
  testReportMatches()
  testPairings()
  print "Success!  All tests pass!"
