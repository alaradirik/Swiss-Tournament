# Swiss Tournament Project
Swiss Tournament Project for completion of [Udacity's Fullstack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

This project is based on the Swiss style tournament methods. In a Swiss style tournament, players don't get eliminated, instead they are paired with players that are equally (same number of wins) or nearly equal (closest number of wins) to each other in each round. 

Games and mathces are worth the following points during Swiss rounds:

  - 3 points for a win
  - 1 point for a draw
  - 0 points for a loss

In the event that there are an odd number of players a bye will be assigned to one of the players in the round. At the end of the tournament, player with the highest score wins.

Further information on the Swiss system can be found [here](https://www.wizards.com/dci/downloads/swiss_pairings.pdf)

'Python 2.7' & 'PostgreSQL' are used to build the project.

## Project Description
- tournament.sql - contains the list of the players, updates the database as the tournament proceeds
- tournament.py - contains the functions to implement the Swiss pairing system
- tournament_test.py - contains the tests for tournament.py
- play_tournament.py - runs a dummy tournament to randomly select the winners of each match

## Instructions

Creating the Database:
To create the database, tables, views and functions use the following command:

        psql -f tournament.sql

Running tournament_test.py:
To run the tournament_test.py script run the following command:

        python tournament_test.py

Running play_tournament.py:
To see a simulated tournament run the following command:
        
        python play_tournament.py
