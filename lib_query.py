import sqlite3
from sqlite3 import Error
import tkinter as tk

window_main = tk.Tk()
window_main.title("Game Client")

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)



def select_all_from_single_table(conn, table):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table)

    rows = cur.fetchall()

    return rows


def inserisci(conn, istruzione_d_inserimento):
    try:
        c = conn.cursor()
        c.execute(istruzione_d_inserimento)
        conn.commit()
    except Error as e:
        print(e)

"""
1.	Inserimento di una nuova fiera						                (Admin)
2.	Inserimento di un nuovo torneo                      				(Admin)
3.	Lista partite effettuale in un torneo per uno specifico torneo		(User)	
4.	Gioco con più tornei basati su di esso 					            (User)
5.	Gioco da tavolo con più partite non ufficiali    				    (Admin)
6.	Top 10 giocatori con il punteggio più alto 					        (User)
7.	I due giochi più venduti 							                (User)
8.	Inserimento di un nuovo dipendente 					                (Admin)
9.	Lista vendite per uno stand 							            (Admin)
10.	Lista dell’attuale formato 							                (User)
11.	Aggiornamento di un formato 						                (Admin)



    istruzione_inserimento1 = INSERT INTO projects(name,begin_date,end_date) VALUES ('proggeto1','2001-01-01','2002-02-02')

"""

def inserimento_nuova_fiera(conn):
    print()
    istruzione = """ INSERT INTO Fiera(...) VALUES (...variabili da input...)"""

def inserimento_nuovo_torneo(conn):
    print()
    istruzione = """ INSERT INTO Fiera(...) VALUES (...variabili da input...)"""

def lista_partite_effettuate_torneo(conn, torneo):
    istruzione=""" SELECT <parametri> FROM Torneo WHERE CodTorneo=%s""" % torneo