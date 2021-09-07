import connessione_DB as cDB
import sqlite3 as lite
import os

con=lite.connect("ChallengeUPGames_DB.db")
cur=con.cursor()
msg=""


for root, dirs, files in os.walk('SQL_TABELLE/'):
    for file in files:
        print(file)
        filename, extension = os.path.splitext(file)
        if extension == '.sql':
            script="SQL_TABELLE/"+filename+""+extension
            cDB.riempimento(script)