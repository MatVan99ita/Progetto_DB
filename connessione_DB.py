import sqlite3 as lite
from sqlite3 import OperationalError

con=lite.connect("ChallengeUPGames_DB.db")
cur=con.cursor()
msg=""

####################################### CREAZIONE TABELLE ################################################
# Open and read the file as a single buffer
fd = open('CreazioneTabelleProgettoDB.sql', 'r')
sqlFile = fd.read()
fd.close()

# all SQL commands (split on ';')
sqlCommands = sqlFile.split(';')

# Execute every command from the input file
for command in sqlCommands:
    # This will skip and report errors
    # For example, if the tables do not yet exist, this will skip over
    # the DROP TABLE commands
    try:
        con.execute(command)
    except OperationalError :
        print("Command skipped")



####################################### INSERIMENTO RECORD ################################################

# Open and read the file as a single buffer
fd = open('RiempimentoTabelle.sql', 'r')
sqlFile = fd.read()
fd.close()

# all SQL commands (split on ';')
sqlCommands = sqlFile.split(';')

# Execute every command from the input file
for command in sqlCommands:

    try:
        con.execute(command)
    except OperationalError :
        print("Command skipped")


