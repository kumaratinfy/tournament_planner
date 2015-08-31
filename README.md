Project 2 - Tournament Planner

What is it?
This project implements a Python module that uses PostgreSQL database to keep track of players and matches in a game tournament.
The game tournament uses the Swiss system for pairing up players in each round: players are not eliminated, and each player are paired with another player with the same number of wins, or as close as possible.

What is included?
a) tournament.sql - Contains the SQL statements to create necessary tables, views, triggers etc to persistently store tournament information in a database
b) cleanup_db.sql - Delete all the database objects created in tournament.sql 
c) tournament.py - Module that interacts with the database and provides functionalities such as registering players, store match information, provide current standings
d) tournament_test.py - Module containing unit test cases for testing the necessary functionality

Running the program:
a) Login to a machine having postgres installed 
b) Login to the psql shell
c) Create a database names as tournament using the following commane "CREATE DATABASE tournament;"
d) Connect to the database using the following command \c tournament
e) Create the database objects by typing the following command \i tournament.sql
f) In a python shell, test the program using the following commans python tournament_test.py

Software Requirements:
1) Postgres Version 9.0.22 and above
2) Python version 2.7.9

Version
1.1

Change History:
08/31/2015 - Incorporated Review Comments

Contact Information
kumar.garg@gmail.com

