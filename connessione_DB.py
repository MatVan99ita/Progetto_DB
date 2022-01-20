import sqlite3 as lite
from sqlite3 import Error
import os
import time

db_file="DB/ChallengeUPGames_DB.db"
msg=""


####################################### CREAZIONE TABELLE ################################################
def creazione_tabelle():
    print(db_file)
    # Open and read the file as a single buffer
    try:
        con=lite.connect(db_file)
        fd = open("CreazioneTabelleProgettoDB.sql")
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')
    except Error as e:
        print(e)
        time.sleep(5)
    # all SQL commands (split on ';')
    # Execute every command from the input file
    for command in sqlCommands:
        try:
            con.execute(command)
            print("comando")
            print(command)
            con.commit()
            time.sleep(1)
        except Error as e :
            print("Command skipped\n"+str(e))


####################################### INSERIMENTO RECORD ################################################
def riempimento(scriptSQL):
    try:
        print("apertura in corso...")
        fd = open(scriptSQL, 'r')
        script = fd.read()
        fd.close()
        time.sleep(1)
        print("apertura completata")
    except Error as e:
        print("errore apertura file")

    try:
        con=lite.connect(db_file)
        cur=con.cursor()    
        cur.execute(script)
        con.commit()
    except Error as e:
        print("Command skipped\n"+str(e))
    print()

def stampaTutto():
    try:
        # Open and read the file as a single buffer
        fd = open('./selezionaTutto_COMPLETO.sql')
        sqlFile = fd.read()
        fd.close()
    except Error as e:
        print("errore apertura file")
    
    con=lite.connect(db_file)
    cur=con.cursor()
    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')
    for command in sqlCommands:
        try:
            risultato=con.execute(command)
            record=risultato.fetchall()
            con.commit()
            print(record)
            time.sleep(3)
        except Error as e :
            print("Command skipped\n"+str(e))

