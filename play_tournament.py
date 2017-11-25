#!/usr/bin/env python
#
# play_tournament.py -- Plays out a tournament based on the Swiss-system
#

from tournament import *
import random


def register_players():
    """Sets up a dummy tournament with 16 players"""
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Fluttershy")
    registerPlayer("Jones")
    registerPlayer("Smith")
    registerPlayer("Homer")
    registerPlayer("Marge")
    registerPlayer("Ned")
    registerPlayer("Monty")
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")


def play_tournament():
    """Plays out the tournament by selecting a random winner or draw"""
    rounds = tournamentRounds()
    roundCounter = 0
    while roundCounter < rounds:
        pairs = swissPairings()
        for p in pairs:
            if (p[2] == 0):
                reportMatch(p[0], 3, p[0], 0)
            else:
                winner = random.randint(0, 2)
                if winner == 0:
                    """Player One won the match"""
                    reportMatch(p[0], 3, p[2], 0)
                elif winner == 1:
                    """Player Two won the match"""
                    reportMatch(p[0], 0, p[2], 3)
                else:
                    """Match resulted in a draw"""
                    reportMatch(p[0], 1, p[2], 1)
        roundCounter += 1
    winner = tournamentWinner()
    print winner

if __name__ == '__main__':
    register_players()
    play_tournament()
