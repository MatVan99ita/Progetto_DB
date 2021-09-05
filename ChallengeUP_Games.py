
import tkinter as tk
from tkinter import *
from tkinter import Listbox
from tkinter import messagebox as msg
import lib_query
import sqlite3 as lite

window_main = tk.Tk()
window_main.title("ChallengeUP Games")
admin_log=False
screen_width = window_main.winfo_screenwidth()
screen_height = window_main.winfo_screenheight()

password_entry=tk.StringVar()
name_entry=tk.StringVar()

dataTorneo=tk.StringVar()

conn=lite.connect("ChallengeUPGames_DB.db")
cur=conn.cursor()


def Admin_login(log):
    if(log):
        print("si")#andranno mostrati i textbox per le credenziali e nascosto il tasto
        first_frame.pack_forget()
        admin_login_frame.pack(side=tk.TOP)
    else:
        #accesso utente senza log in e senza funzionalità aggiuntive
        program_start("user")
    

def calcolo_dimensioni_finestra(frame, alt=0, larg=0):

    if(frame=="inizio"):
        nuova_altezza=(10*screen_height)/100
        nuova_larghezza=(20*screen_width)/100

    elif(frame=="GUI principale"):#finestra principale
        nuova_altezza=(75*screen_height)/100
        nuova_larghezza=(80*screen_width)/100

    elif(frame=="frame tabella"):#frame tabella
        nuova_altezza=(75*screen_height)/100
        nuova_larghezza=((50*screen_width)/2)/100

    #CALCOLO DELLE DIMENSIONI DELLE COLONNE IN BASE AL NUMERO
    elif(frame=="tabella"):
        #dimensione del frame della tabella
        nuova_larghezza=((50*screen_width)/2)/100
        nuova_altezza=(75*screen_height)/100
        #suddivisione per la query
        nuova_larghezza=(nuova_larghezza/larg)/4
        return nuova_larghezza

    geometria="%dx%d" % (nuova_larghezza, nuova_altezza)

    return geometria


nomeFrame=Frame()

def program_start(tipologia_utente):
    
    if(tipologia_utente=="user"):
        top_welcome_frame.pack_forget()
        window_main.geometry(calcolo_dimensioni_finestra("GUI principale"))

        top_frame.pack(side=tk.TOP)
        

    elif(tipologia_utente=="admin"):
        print("acceso admin")
        top_welcome_frame.pack_forget()
    
        window_main.geometry(calcolo_dimensioni_finestra("GUI principale"))
        
        #if(nome=='mat' and passw=='123'):
        admin_frame.pack(side=tk.TOP)
        #else:
        #    print("errore user e/o password")
        #controllo sulle credenziali


def genera_tabella_query(tipo, ris):
    total_rows=len(ris)
    total_columns=len(ris[0])

    dimensione_colonna=calcolo_dimensioni_finestra("tabella", total_rows, total_columns)
    print(dimensione_colonna)
    if(tipo=="user"):
        for i in range(total_rows):
            for j in range(total_columns):
                e = Listbox(db_frame_user, width=int(dimensione_colonna), height=1)
                e.grid(row=i, column=j)
                e.insert(j, ris[i][j])
    else:
        for i in range(total_rows):
            for j in range(total_columns):
                e = Listbox(db_frame_admin, width=int(dimensione_colonna), height=1)
                e.grid(row=i, column=j)
                e.insert(ris[i][j], ris[i][j])


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

    return 0
    
#U1
def lista_partite_effettuate_torneo(conn, giorno, mese, anno, ruolo):
    if(controlloData(giorno, mese, anno)==0):
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
            T.dataTorneo=%s;""" % data

        colonne=["IdTorneo","nomeTorneo", "numeroSpettatori", "numeroPartecipanti", "codGioco", "IdFiera", "IdMatch", "dataPartita", "nomePadiglione", ]
        cursor=conn.cursor()
        cursor.execute(sql)
        records=cursor.fetchall()
        v=[[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
        genera_tabella_query(ruolo, v)


def top_giocatori(ruolo, IdGiocatore):
    sql=""" SELECT ( (SELECT SUM(punteggioVittoria)
        FROM )) + ()) AS punteggio totale, COUNT(punteggioVittoria) AS numeroVittorie, COUNT(punteggioSconfitte) AS numeroSconfitte
        FROM TORNEI T, PARTITE_UFFICIALI PU, VINCITORE V, PERDENTE P, CONCORRENTE C
        WHERE PU.IdTorneo = T.IdTorneo AND
        V.IdMatch = PU.IdMatch AND
        P.IdMatch = PU.IdMatch AND
        C.codConcorrente = V.codConcorrente AND
        C.codConcorrente = P.codConcorrente AND
        CodConcorrente = %d
        GROUP BY IdTorneo;""" % IdGiocatore

    colonne=["IdGiocatore", "Punteggio totale"]
    cursor=conn.cursor()
    cursor.execute(sql)
    records=cursor.fetchall()
    v=[[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    genera_tabella_query(ruolo, v)


def lista_carte_bandite_formato(ruolo):
    sql=""" SELECT *
            FROM SET_CARTE_BANDITE S, FORMATI F
            WHERE F.dataInizio = S.dataInizio AND
            F.dataFine = S.dataFine AND
            dataInizio <= NOW() AND
            dataFine > NOW()"""


    colonne=["Data inizio", "Data Fine", "codCarta"]
    cursor=conn.cursor()
    cursor.execute(sql)
    records=cursor.fetchall()
    print(colonne)
    print(records)
    v=[[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    genera_tabella_query(ruolo, v)

def lista_carte_mazzo(ruolo, mazzo):
    sql=""" SELECT codMazzo, colore_clan, codCarta, nome, tipo, descrizione, costoMana, attributo, attacco, difesa, effetto
            FROM MAZZI M, CARTE C, COMPOSTI CO
            WHERE CO.codiceMazzo = M.codiceMazzo AND
            C.codCarta = CO.codCarta AND
            codiceMazzo = %d
            """ % mazzo

    colonne=["codMazzo", "Colore", "codCarta", "nome", "tipo", "descrizione", "Costo", "Attributo", "Attacco", "Difesa", "Effetto"]
    cursor=conn.cursor()
    cursor.execute(sql)
    records=cursor.fetchall()
    print(colonne)
    print(records)
    v=[[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    genera_tabella_query(ruolo, v)

def genera_parametri(azione, ruolo):
        nomeFrame=tk.Frame()
        if(ruolo=="user"):
            nomeFrame=db_param_frame_user
        else:
            nomeFrame=db_param_frame_admin
    
        if(azione=="U1"):#Lista delle partite effettuate in un torneo svolto in una data specificata
            giorno_var=tk.StringVar()
            mese_var=tk.StringVar()
            anno_var=tk.StringVar()
            lbl_dataTorneo = tk.Label(nomeFrame, text="Inserire data GIORNO(gg)/MESE(mm)/ANNO(yyyy)").grid(row=0, column=0)
            ent_giorno = tk.Entry(nomeFrame, textvariable=giorno_var).grid(row=0, column=1)
            ent_mese = tk.Entry(nomeFrame, textvariable=mese_var).grid(row=0, column=2)
            ent_anno = tk.Entry(nomeFrame, textvariable=anno_var).grid(row=0, column=3)
            btn_calcoloQuery = tk.Button(nomeFrame, text="Controlla", command=lambda : lista_partite_effettuate_torneo(conn, giorno_var.get(), mese_var.get(), anno_var.get(), ruolo)).grid(row=1, column=0)
        
        #U2: Dato un concorrente ritornare il punteggio totale, numero vittorie e numero sconfitte per ogni torneo in cui ha partecipato
        elif(azione=="U2"):
            giocatore_var=tk.StringVar()
            lbl_IdGiocatore = tk.Label(nomeFrame, text="Inserire IdGiocatore:").grid(row=0, column=0)
            ent_Giocatore = tk.Entry(nomeFrame, textvariable=giocatore_var).grid(row=0, column=1)
            btn_calcoloQuery = tk.Button(nomeFrame, text="Controlla", command=lambda : top_giocatori(ruolo, giocatore_var.get())).grid(row=1, column=0)
        
        #elif(azione=="U3"):#Lista delle carte bandite dall'attuale formato
        elif(azione=="U4"):#Lista delle carte di un mazzo specificato
            mazzo_var=tk.StringVar()
            lbl_Mazzo = tk.Label(nomeFrame, text="Inserire codice mazzo:").grid(row=0, column=0)
            ent_Mazzo = tk.Entry(nomeFrame, textvariable=mazzo_var).grid(row=0, column=1)
            btn_calcoloQuery = tk.Button(nomeFrame, text="Controlla", command=lambda : lista_carte_mazzo(ruolo, mazzo_var.get())).grid(row=1, column=0)
        
        elif(azione=="A1"):#
            print()
        elif(azione=="A2"):#
            print()
        elif(azione=="A3"):#
            print()
        elif(azione=="A4"):#
            print()
        elif(azione=="A5"):#
            print()
        elif(azione=="A6"):#
            print()
        elif(azione=="A7"):#
            print()


window_main.geometry(calcolo_dimensioni_finestra("inizio"))
dimensioni_frame_tabella=calcolo_dimensioni_finestra("GUI principale")
dimensioni_frame_tabella=dimensioni_frame_tabella.split("x")



##################################### FINESTRA LOG IN ####################################################

top_welcome_frame = tk.Frame(window_main)

#####################################
first_frame = tk.Frame(top_welcome_frame)

lbl_choice1 = tk.Label(first_frame, text = "Log in method:")
lbl_choice1.pack(side=tk.LEFT)
btn_Admin = tk.Button(first_frame, text="Admin", command=lambda : Admin_login(True))
btn_Admin.pack(side=tk.RIGHT)
btn_User = tk.Button(first_frame, text="User", command=lambda : Admin_login(False))
btn_User.pack(side=tk.RIGHT)

first_frame.pack(side=tk.TOP)
#####################################

#####################################
admin_login_frame = tk.Frame(top_welcome_frame)

lbl_admin_name = tk.Label(admin_login_frame, text = "Name:").grid(row=0, column=0)
ent_admin_name = tk.Entry(admin_login_frame, textvariable=name_entry).grid(row=0, column=1)

lbl_password = tk.Label(admin_login_frame, text = "Password:").grid(row=1, column=0)
ent_password = tk.Entry(admin_login_frame, textvariable=password_entry).grid(row=1, column=1)

btn_Log = tk.Button(admin_login_frame, text="Log-in", command=lambda : program_start("admin")).grid(row=2, column=0)

admin_login_frame.pack(side=tk.TOP)
admin_login_frame.pack_forget()
#####################################
top_welcome_frame.pack(side=tk.TOP)



##################################### FINESTRA PRINCIPALE ####################################################


top_frame = tk.Frame(window_main)

lbl_line = tk.Label(top_frame, text="***********************************************************").pack()
lbl_line = tk.Label(top_frame, text="**** SESSIONE UTENTE ****", font = "Helvetica 13 bold", foreground="blue").pack()
lbl_line = tk.Label(top_frame, text="***********************************************************").pack()

#####################################
top_left_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)



btn_U1=tk.Button(top_left_frame, text="Lista delle partite effettuate in un torneo svolto in una data specificata", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U1", "user")).grid(row=0, column=0)
btn_U2=tk.Button(top_left_frame, text="Top 10 giocatori con il punteggio più alto", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=1, column=0)
btn_U3=tk.Button(top_left_frame, text="Lista delle carte bandite dall'attuale formato", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=2, column=0)
btn_U4=tk.Button(top_left_frame, text="Lista delle carte di un mazzo specificato", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=3, column=0)

top_left_frame.pack(side=tk.LEFT)


################### DATABASE FRAME USER ##################

#parametri
db_param_frame_user = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
db_param_frame_user.pack(side=tk.BOTTOM)

#####################################
db_frame_user = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1, width=dimensioni_frame_tabella[0], height=dimensioni_frame_tabella[1])

db_frame_user.pack(side=tk.RIGHT)

top_frame.pack_forget()
#####################################




############################# SEZIONE ADMIN #############################################

admin_frame = tk.Frame(window_main)

lbl_line = tk.Label(admin_frame, text="***********************************************************").pack()
lbl_line = tk.Label(admin_frame, text="**** SESSIONE ADMIN ****", font = "Helvetica 13 bold", foreground="blue").pack()
lbl_line = tk.Label(admin_frame, text="***********************************************************").pack()


#####################################
final_frame = tk.Frame(admin_frame)
btn_U1_admin=tk.Button(final_frame, text="Lista delle partite effettuate in un torneo svolto in una data specificata", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U1", "admin")).grid(row=0, column=0)
btn_U2_admin=tk.Button(final_frame, text="Top 10 giocatori con il punteggio più alto", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=1, column=0)
btn_U3_admin=tk.Button(final_frame, text="Lista delle carte bandite dall'attuale formato", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=2, column=0)
btn_U4_admin=tk.Button(final_frame, text="Lista delle carte di un mazzo specificato", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=3, column=0)

btn_A1=tk.Button(final_frame, text="Inserimento nuova fiera", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=5, column=0)
btn_A2=tk.Button(final_frame, text="Inserimento nuovo torneo", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=6, column=0)
btn_A3=tk.Button(final_frame, text="Inserimento dipendente", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=7, column=0)
btn_A4=tk.Button(final_frame, text="Inserimento nuovo formato", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=8, column=0)
btn_A5=tk.Button(final_frame, text="Gioco da tavolo con più partite non ufficiali", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=9, column=0)
btn_A6=tk.Button(final_frame, text="Il gioco più venduto per ogni stand", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=10, column=0)
btn_A7=tk.Button(final_frame, text="Registrazione vendita per stand", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=11, column=0)


final_frame.pack(side=tk.LEFT)

#parametri
db_param_frame_admin = tk.Frame(admin_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
db_param_frame_admin.pack(side=tk.BOTTOM)


#####################################
db_frame_admin = tk.Frame(admin_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1, width=dimensioni_frame_tabella[0], height=dimensioni_frame_tabella[1])

db_frame_admin.pack(side=tk.RIGHT)

admin_frame.pack_forget()





################### DATABASE FRAME ##################



window_main.mainloop()


######################################################################################################
