import sqlite3
from sqlite3 import Error

dati=[]

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



######################################## FUNZIONI ADMIN ####################################################

def inserimento_nuova_fiera(conn):
    print()
    sql = """ INSERT INTO Fiera(...) VALUES (...variabili da input...)"""

def inserimento_nuovo_torneo(conn):
    print()
    sql = """ INSERT INTO Fiera(...) VALUES (...variabili da input...)"""


def gioco_con_maggior_partite_unofficial(conn):
    sql = """ SELECT <parametri>, MAX(numeroPartite) AS NumeroPartiteNonUfficiali FROM Gioco non ufficiale Gnu, Gioco da tavolo Gdt WHERE Gnu.codGioco = Gdt.codGioco """


def aggiornamento_dipendenti(conn):
    if(True):
        sql = """ UPDATE """
    else:
        sql = """ INSERT INTO """


def lista_vendite_stand(conn, stand):
    sql = """ SELECT * FROM Vendite WHERE codStand=%s """ % stand


def aggiornamento_formato(conn, formato):
    sql = """ UPDATE Formato SET <parametri> WHERE IdFormato=%s """ % formato





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