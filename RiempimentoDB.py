import connessione_DB as cDB
import sqlite3 as lite
import os
import time
import tkinter
from tkinter import messagebox as msg

con=lite.connect("ChallengeUPGames_DB.db")
cur=con.cursor()



for root, dirs, files in os.walk('SQL_TABELLE/'):
    for file in files:
        print(file)
        filename, extension = os.path.splitext(file)
        if extension == '.sql':
            script="SQL_TABELLE/" + filename + "" + extension
            print(script)
            time.sleep(1)
            cDB.riempimento(script)

