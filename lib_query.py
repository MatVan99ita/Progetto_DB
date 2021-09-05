import sqlite3
from sqlite3 import Error
import tkinter as tk
from tkinter import *
from tkinter import Listbox
from tkinter import messagebox as msg

dati=[]
db_file=(r'.\ChallengeUPGames_DB.db')
conn = None
try:
    conn = sqlite3.connect(db_file)
except Error as e:
    print(e)
    msg.showerror(message="ERRORE CONNESSIONE")



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


def controlloData(giorno, mese, anno):
    g=len(giorno)
    m=len(mese)
    y=len(anno)
    gg=int(giorno)
    mm=int(mese)
    yy=int(anno)
    if( (gg%2!=0 and gg%2!=1) and (mm%2!=0 and mm%2!=1) and (yy%2!=0 and yy%2!=1) ):
        msg.showerror(title="FORMATTAZIONE DATA ERRATA", message="Non esiste un valore numerico")
        return 1
    
    if(g>2 and m>2 and y>4):
        msg.showerror(title="FORMATTAZIONE DATA ERRATA", message="Valori con troppi caratteri")
        return 1

    #formattazione della data secondo i database
    return anno + "-" + mese + "-" + giorno





######################################## FUNZIONI ADMIN ####################################################

def inserimento_Fiera(via, numeroCivico, IdCittà, IdNazione, nomeFiera, dataInizioFiera, dataFineFiera):

    if(controlloData(dataInizioFiera[0], dataInizioFiera[1], dataInizioFiera[2]) != 1 and controlloData(dataFineFiera[0], dataFineFiera[1], dataFineFiera[2]) != 1):
        
        #formattazione delle date
        dataInizio=controlloData(dataInizioFiera[0], dataInizioFiera[1], dataInizioFiera[2])
        dataFine=controlloData(dataFineFiera[0], dataFineFiera[1], dataFineFiera[2])
        print(dataInizio)
        print(dataFine)
        sql=""" INSERT INTO FIERE (via, numeroCivico, IDcittà, IDnazione, nomeFiera, dataInizioFiera, dataFineFiera) 
        VALUES ( (?), (?), (?), (?), (?), (?), (?) )"""
        
        dati=(via, numeroCivico, IdCittà, IdNazione, nomeFiera, dataInizio, dataFine)
        cursor=con.cursor()
        try:
            cursor.execute(sql, dati)
            #conn.commit()
        except:
            msg.showerror(title="ERRORE INSERIMENTO", message="qualcosa è andato storto con l'inserimento della fiera")





######################################## FUNZIONI UTENTE ####################################################

def lista_partite_effettuate_torneo(conn, giorno, mese, anno):

    data=str(anno)+"-"+str(mese)+"-"+str(giorno)

    sql="""SELECT *
        FROM 	TORNEI T, PARTITE_UFFICIALI PU, DIPENDENTI D, PADIGLIONI P, VINCITORI V, PERDENTI PE, CONCORRENTI C
        WHERE T.IdTorneo = PU.IdTorneo AND
        D.CodiceBadge = PU.IdGiudice AND
        P.CodPadiglione = PU.CodPadiglione AND
    PU.IdMatch = V.IdMatch AND
    PU.IdMatch = PE.IdMatch AND
    PE.codConcorrente = C. codConcorrente AND
    V.codConcorrente = C. codConcorrente AND
    T.dataTorneo=%s;""" & data

    cursor=conn.cursor()
    cursor.execute(sql)
    records=cursor.fetchall()

    return records



def gioco_con_maggior_tornei(conn, gioco):
    sql = """ SELECT <parametri>, COUNT(*) AS NumeroTornei FROM Torneo T, Gioco da tavolo G WHERE nomeGioco=%s GROUP BY nomeGioco """ % gioco


def top_dieci_giocatori(conn):
    sql = """ SELECT TOP(10) <parametri> FROM GiocatoreWHERE MAX(punteggio) """


def giochi_più_venduti():
    sql = """ SELECT TOP(2) <parametri> FROM Vendita WHERE """


def formato_attuale(conn, data):
    sql = """ SELECT <parametri> FROM Formato WHERE periodo comprende %s """ % data