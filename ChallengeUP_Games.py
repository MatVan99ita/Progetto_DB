
import tkinter as tk
from tkinter import *
from tkinter import Listbox
from tkinter import messagebox as msg
import sqlite3 as lite
from sqlite3 import Error
from tkinter import ttk
import connessione_DB


window_main = tk.Tk()
window_main.title("ChallengeUP Games")
admin_log=False
screen_width = window_main.winfo_screenwidth()
screen_height = window_main.winfo_screenheight()

password_entry=tk.StringVar()
name_entry=tk.StringVar()
nomeFrame=Frame()


######################################## FUNZIONI APPLICAZIONE ####################################################

dataTorneo=tk.StringVar()
try:
    conn=lite.connect("./ChallengeUPGames_DB.db")
    cur=conn.cursor()
    print(cur)
except Error as e:
    msg.showerror(title="CONNESSIONE FALLITA", message="connessione fallita verso ChallengeUPGames_DB.db")

def Admin_login(log):#da perfezionare ma non indispensabile ai fini del programma
    if(log):
        print("si")#andranno mostrati i textbox per le credenziali e nascosto il tasto
        first_frame.pack_forget()
        admin_login_frame.pack(side=tk.TOP)
    else:
        #accesso utente senza log in e senza funzionalità aggiuntive
        program_start("user")

def calcolo_dimensioni_finestra(frame, alt=0, larg=1):
    GUI_altezza=(90*screen_height)/100
    GUI_larghezza=(80*screen_width)/100
    
    if(frame=="inizio"):
        nuova_altezza=(10*screen_height)/100
        nuova_larghezza=(20*screen_width)/100

    elif(frame=="GUI principale"):#finestra principale
        nuova_altezza=(90*screen_height)/100
        nuova_larghezza=(80*screen_width)/100

#################### Verranno usate le dimensioni della gui principale come metro di misura della tabella ##########################
    elif(frame=="frame tabella"):#frame tabella
        nuova_altezza=(60*GUI_altezza)/100
        nuova_larghezza=((50*GUI_larghezza)/2)/100

    #CALCOLO DELLE DIMENSIONI DELLE COLONNE IN BASE AL NUMERO
    elif(frame=="tabella"):
        #dimensione del frame della tabella
        nuova_altezza=(60*GUI_altezza)/100
        #nuova_larghezza=(((50*screen_width)/2)/100)/(larg*2)
        nuova_larghezza=(GUI_larghezza/larg)/2

    geometria="%dx%d" % (nuova_larghezza, nuova_altezza)

    return geometria

def clear_frame(frame):
   for widgets in frame.winfo_children():
        widgets.destroy()

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
############################## CREAZIONE DELLA TABELLA GRAFICA ####################################
def genera_tabella_query(tipo, records, colonne):
    total_rows=len(records)
    total_columns=len(records[0])
    
    print(str(total_rows)+" x "+str(total_columns))

    print("righe totali = " + str(total_rows))


    ############# CREAZIONE GEOMETRIE ##################
    geometria_tabella=calcolo_dimensioni_finestra("tabella", total_rows, colonne)
    geometria_frame=calcolo_dimensioni_finestra("frame tabella")
    geometria_finestra=calcolo_dimensioni_finestra("GUI principale")

    ############# SUDDIVISIONE GEOMETRIE #################
    dim_tabella=geometria_tabella.split("x")
    dim_frame=geometria_frame.split("x")
    dim_finestra=geometria_finestra.split("x")

    ############# VISTA GEOMETRIE #####################
    print("dimensioni_tabella")
    print(dim_tabella)
    print("dimensioni_frame")
    print(dim_frame)
    print("dimensioni_finestra")
    print(dim_finestra)


    if(tipo=="user"):
        frame=db_frame_user
    else:
        frame=db_frame_admin
    clear_frame(frame)
    #frame.grid(row=1, columnspan=2, padx=2, pady=2, sticky=tk.N+tk.E+tk.S+tk.W)

    # TODO: far funzionare lo scroll
    text_area = tk.Canvas(frame, background="black", width=dim_frame[0], height=dim_tabella[1], scrollregion=(0,0,1200,800))
    hscroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=text_area.xview)
    vscroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=text_area.yview)
    text_area['xscrollcommand'] = hscroll.set
    text_area['yscrollcommand'] = vscroll.set

    text_area.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
    hscroll.grid(row=1, column=0, sticky=tk.N+tk.E+tk.W)
    vscroll.grid(row=0, column=1, sticky=tk.W+tk.N+tk.S)
    i=2
    j=2
    _widgets = []

    print("##################################################### RECORD NELLA CREAZIONE TABELLA #####################################################")
    for row in range(total_rows):
        print(records[row])
    print("##########################################################################################################################################")

    larghezza_singolo_elemento=int( (int(dim_tabella[0])/total_columns)/2 )
    1
    print("Larghezza elemento: " + str(larghezza_singolo_elemento))
    for row in range(total_rows):
        current_row = []
        for column in range(total_columns):
            label = tk.Label(text_area, text=str(records[row][column]), borderwidth=0, height=1, width=larghezza_singolo_elemento)
            j=j+1
            label.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
        j=2
        i=i+1
        _widgets.append(current_row)

################################################################################################################################################


######################## FORMATTAZZIONE RISULTATO QUERY ##########################
def genera_matrice_query(records, colonne):
    tabella=[]
    index=0
    tabella.append(colonne)
    for i in records:
            tabella.append(i)
            index=index+1
    print(tabella)
    return tabella

######################## CONVERSIONE DATA DEL DATABASE ########################
def controlloData(giorno, mese, anno):
    g=len(giorno)
    m=len(mese)
    y=len(anno)
    if(g>2 and m>2 and y>4):
        msg.showerror(title="FORMATTAZIONE DATA ERRATA", message="Valori con troppi caratteri")
        return 1
    gg=int(giorno)
    mm=int(mese)
    yy=int(anno)
    
    if( (gg%2!=0 and gg%2!=1) and (mm%2!=0 and mm%2!=1) and (yy%2!=0 and yy%2!=1) ):
        msg.showerror(title="FORMATTAZIONE DATA ERRATA", message="Non esiste un valore numerico")
        return 1
    #formattazione della data secondo i database
    return giorno+"/"+mese+"/"+anno

###########################################################################################################



######################################## FUNZIONI USER ####################################################

def lista_partite_effettuate_torneo(conn, giorno, mese, anno, ruolo):
    if(controlloData(giorno, mese, anno) != 1):
        data=controlloData(giorno, mese, anno)
        print(data)
        sql="""SELECT T.IdTorneo, T.nomeTorneo, T.numeroSpettatori, T.numeroPartecipanti, T.codGioco, T.IdFiera, PU.IdMatch, PU.dataPartita, P.nomePadiglione
            FROM 	TORNEI T, PARTITE_UFFICIALI PU, DIPENDENTI D, PADIGLIONI P, BATTAGLIE B, CONCORRENTI C
            WHERE T.IdTorneo = PU.IdTorneo AND
            D.CodiceBadge = PU.IdGiudice AND
            P.CodPadiglione = PU.CodPadiglione AND
            PU.IdMatch = B.numeroMatch AND
            B.codConcorrente = C.codConcorrente AND
            T.dataTorneo=(?);"""

        colonne=("IdTorneo","nomeTorneo", "numeroSpettatori", "numeroPartecipanti", "codGioco", "IdFiera", "IdMatch", "dataPartita", "nomePadiglione" )
        cur.execute(sql, data)
        records=cur.fetchall()
        print(records)
        tabella=colonne
        tabella.append(records)
        print(tabella)
        genera_tabella_query(ruolo, records)

def top_giocatori(ruolo, IdGiocatore):
    sql=""" SELECT t.IdTorneo, nome, cognome, SUM(b.punteggio),
            (
                SELECT COUNT(esito) 
                FROM BATTAGLIE b, PARTITE_UFFICIALI pu1 
                WHERE pu1.IdMatch = b.numeroMatch AND 
                esito = "vittoria" AND
                pu1.IdTorneo = t.IdTorneo
            ) AS numVittorie,
            (
                SELECT COUNT(esito)
                FROM BATTAGLIE b ,PARTITE_UFFICIALI pu1
                WHERE pu1.IdMatch = b.numeroMatch AND
                esito = "sconfitta" AND
                pu1.IdTorneo = t.IdTorneo
            ) AS numSconfitte
            FROM GIOCHI_DA_TAVOLO g, TORNEI t, CONCORRENTI c, PARTITE_UFFICIALI pu, BATTAGLIE b
            WHERE t.CodGioco = g.CodGioco AND
            pu.IdTorneo = t.IdTorneo AND
            pu.IdMatch = b.numeroMatch AND 
            b.codConcorrente = c.codConcorrente
            GROUP BY c.codConcorrente; """

    colonne=["IdTorneo", "Nome", "Cognome", "Punteggio tot", "Vittorie tot", "Sconfitte tot"]
    cursor=conn.cursor()

    records=cursor.fetchall()
    index=0
    cursor=conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
        records=cursor.fetchall()
        tabella=genera_matrice_query(records, colonne)
        genera_tabella_query(ruolo, tabella, len(tabella))
    except Error as e:
        msg.showerror(title="ERRORE CARICAMENTO DATI", message="qualcosa è andato storto con la richiesta dei dati\n"+str(e))


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
    tabella=colonne
    tabella.append(records)
    genera_tabella_query(ruolo, tabella)

def lista_carte_mazzo(ruolo, mazzo):
    sql=""" SELECT codMazzo, colore_clan, codCarta, nome, tipo, descrizione, costoMana, attributo, attacco, difesa, effetto
            FROM MAZZI M, CARTE C, COMPOSTI CO
            WHERE CO.codiceMazzo = M.codiceMazzo AND
            C.codCarta = CO.codCarta AND
            codiceMazzo = (?)
            """

    colonne=("codMazzo", "Colore", "codCarta", "nome", "tipo", "descrizione", "Costo", "Attributo", "Attacco", "Difesa", "Effetto")
    cursor=conn.cursor()
    cursor.execute(sql, mazzo)
    records=cursor.fetchall()
    print(colonne)
    print(records)
    tabella=colonne
    tabella.append(records)
    genera_tabella_query(ruolo, tabella)


######################################## FUNZIONI ADMIN ####################################################

def inserimento_Fiera(via, numeroCivico, IdCittà, IdNazione, nomeFiera, dataInizioFiera, dataFineFiera):

    if(controlloData(dataInizioFiera[0], dataInizioFiera[1], dataInizioFiera[2]) != 1 and controlloData(dataFineFiera[0], dataFineFiera[1], dataFineFiera[2]) != 1):
        
        #formattazione delle date
        dataInizio=controlloData(dataInizioFiera[0], dataInizioFiera[1], dataInizioFiera[2])
        dataFine=controlloData(dataFineFiera[0], dataFineFiera[1], dataFineFiera[2])

        sql=""" INSERT INTO FIERE(IdFiera, via, numeroCivico, Idcittà, Idnazione, nomeFiera, dataInizioFiera, dataFineFiera) 
        VALUES((?), (?), (?), (?), (?), (?), (?), (?));"""
        print(dataInizio)
        print(dataFine)
        cursor=conn.cursor()
        id=cursor.execute("""SELECT MAX(IdFiera) FROM FIERE""")
        ID=id[0]+1
        dati=(ID, via, numeroCivico, int(IdCittà), id(IdNazione), nomeFiera, dataInizio, dataFine)
        try:
            cursor.execute(sql, dati)
            conn.commit()
        except Error as e:
            msg.showerror(title="ERRORE INSERIMENTO", message="qualcosa è andato storto con l'inserimento della fiera\n"+str(e))

def inserimento_Torneo(dataTorneo, nomeTorneo, numeroSpettatori, numeroPatecipanti, IdFiera, codGioco):
    if(controlloData(dataTorneo[0], dataTorneo[1], dataTorneo[2]) != 1):
        
        #formattazione delle date
        dataT=controlloData(dataTorneo[0], dataTorneo[1], dataTorneo[2])
    
        sql=""" INSERT INTO TORNEI(IdTorneo, dataTorneo, nomeTorneo, numeroSpettatori, numeroPartecipanti, IdFiera, codGioco) 
        VALUES((?), (?), (?), (?), (?), (?), (?))"""
        
        cursor=conn.cursor()
        id=cursor.execute("""SELECT MAX(IdTorneo) FROM TORNEI""")
        ID=id[0]+1
        dati=(ID, dataT, nomeTorneo, int(numeroPatecipanti), int(numeroSpettatori), int(IdFiera), int(codGioco))
        try:
            cursor.execute(sql, dati)
            conn.commit()
        except Error as e:
            msg.showerror(title="ERRORE INSERIMENTO", message="qualcosa è andato storto con l'inserimento del torneo\n"+str(e))

def gioco_partite_ufficiose():
    #sql="""SELECT nomeGioco, descrizione, regolamento, SUM(numeroPartite) AS partiteTotali
    #        FROM PARTITE_NON_UFFICIALI PNU, GIOCHI_DA_TAVOLO G
    #        WHERE PNU.CodGioco = G.CodGioco
    #        GROUP BY G.CodGioco
    #        ORDER BY 4
    #        LIMIT 2"""

    index=0
    #colonne=["Nome", "Descrizione", "Regolamento", "Partite totali"]
    colonne=("colonna1", "colonna2", "colonna3", "colonna4")
    sql="""SELECT * FROM BATTAGLIE"""
    tabella=[]
    cursor=conn.cursor()
    tabella.append(colonne)
    try:
        cursor.execute(sql, ())
        conn.commit()
        records=cursor.fetchall()
        tabella=genera_matrice_query(records, colonne)
        genera_tabella_query("admin", tabella, len(colonne))
    except Error as e:
        msg.showerror(title="ERRORE INSERIMENTO", message="qualcosa è andato storto con l'inserimento della fiera\n"+str(e))


def guadagni_stands():
    sql=""" SELECT V.codStand, SUM(prezzoTotale) AS guadagnoTotale, 
                (
                    SELECT AVG(prezzoTotale) 
                    FROM VENDITE V1, VEN_GIOCHI VG 
                    WHERE V1.codStand = VG.codStand AND V1.codVendita = VG.codVendita AND V1.codStand = V.codStand
                ) AS guadagnoMedioGiochiDaTavolo,
                (
                    SELECT AVG(prezzoTotale) 
                    FROM VENDITE V1, VEN_MATERIALI VM 
                    WHERE V1.codStand = VM.codStand AND V1.codVendita = VM.codVendita AND V1.codStand = V.codStand
                ) AS guadagnoMedioMaterialiDaGioco
            FROM VENDITE V
            GROUP BY V.codStand
        """

    colonne=["codStand", "Guadagno"]
    cursor=conn.cursor()
    cursor.execute(sql)
    records=cursor.fetchall()
    tabella=colonne
    tabella.append(records)
    genera_tabella_query("admin", tabella)

def inserimento_Dipendente(nome, cognome, ruolo, dataNascita):
    if(controlloData(dataNascita[0], dataNascita[1], dataNascita[2]) != 1):
        sql=""" INSERT INTO DIPENDENTI(CodiceBadge, nome, cognome, dataDiNascita, ruolo) 
        VALUES((?), (?), (?), (?), (?))"""
        #
        cursor=conn.cursor()
        id=cursor.execute("""SELECT MAX(CodiceBadge) FROM DIPENDENTI""")
        ID=id[0]+1
        dati=(ID, nome, cognome, ruolo, dataNascita)
        try:
            cursor.execute(sql, dati)
            conn.commit()
        except Error as e:
            msg.showerror(title="ERRORE INSERIMENTO", message="qualcosa è andato storto con l'inserimento del dipendente\n"+str(e))

def registro_vendite_stand(tipologia_prodotto, dataVendita, codStand, prezzoTotale, CODICE_PRODOTTO, quantità):
    if(controlloData(dataVendita[0], dataVendita[1], dataVendita[2]) != 1):
        
        #formattazione delle date
        dataV=controlloData(dataVendita[0], dataVendita[1], dataVendita[2])
    
        sql=""" INSERT INTO VENDITE(CodVendita, dataVendita, codStand, prezzoTotale) 
                    VALUES((?), (?), (?), (?))"""
        cursor=conn.cursor()
        id=cursor.execute("""SELECT MAX(CodVendita) FROM VENDITE""")
        codVendita=id[0]+1
        dati=(int(codVendita), dataV, int(codStand), prezzoTotale)
        try:
            cursor.execute(sql, dati)
            conn.commit()
        except Error as e:
            msg.showerror(title="ERRORE INSERIMENTO", message="qualcosa è andato storto con l'inserimento della vendita\n"+str(e))


        if(tipologia_prodotto=="Gioco da tavolo"):
            sql="""INSERT INTO VEN_GIOCHI(codVendita, codGioco, codStand, quantitàGiochiSelezionati) 
                        VALUES((?), (?), (?), (?))"""
            dati=(codVendita, CODICE_PRODOTTO, codStand, quantità)
            try:
                cursor.execute(sql, dati)
                conn.commit()
            except Error as e:
                msg.showerror(title="ERRORE INSERIMENTO", message="qualcosa è andato storto con l'inserimento dei giochi\n"+str(e))
        
        elif(tipologia_prodotto=="Materiale di gioco"):
            
            sql="""INSERT INTO VEN_MATERIALI(codVendita, codMateriale, codStand, quantitàMaterialiSelezionati) 
                        VALUES((?), (?), (?), (?));"""
            dati=(codVendita, CODICE_PRODOTTO, codStand, quantità)
            try:
                cursor.execute(sql, dati)
                conn.commit()
            except Error as e:
                msg.showerror(title="ERRORE INSERIMENTO", message="qualcosa è andato storto con l'inserimento dei matriali di gioco\n"+str(e))
            
            sql="""UPDATE IMMAGAZZINATI SET quantitàMateriali = quantitàMateriali - quantitàMaterialiSelezionati 
                         WHERE CodGioco = (?) AND codStand = (?)"""
            dati=(CODICE_PRODOTTO, codStand)
            try:
                cursor.execute(sql, dati)
                conn.commit()
            except Error as e:
                msg.showerror(title="ERRORE AGGIORNAMENTO", message="qualcosa è andato storto con l'aggiornamento del magazzino\n"+str(e))

def inserimento_Formato(dataInizio, dataFine, codGioco):
    if(controlloData(dataInizio[0], dataInizio[1], dataInizio[2]) != 1 and controlloData(dataFine[0], dataFine[1], dataFine[2]) != 1):
        
        #formattazione delle date
        dataI=controlloData(dataInizio[0], dataInizio[1], dataInizio[2])
        dataF=controlloData(dataFine[0], dataFine[1], dataFine[2])

        sql=""" INSERT INTO FORMATI(dataInizio, dataFine, codGioco) 
                VALUES((?), (?), (?))"""
        
        cursor=conn.cursor()
        dati=(dataI, dataF, int(codGioco))
        try:
            cursor.execute(sql, dati)
            conn.commit()
        except Error as e:
            msg.showerror(title="ERRORE INSERIMENTO", message="qualcosa è andato storto con l'inserimento della fiera\n"+str(e))

def genera_parametri(azione, ruolo):
        nomeFrame=tk.Frame()
        if(ruolo=="user"):
            nomeFrame=db_param_frame_user
        else:
            nomeFrame=db_param_frame_admin
        
        #pulizia della grafica per evitare elementi sovrapposti
        clear_frame(nomeFrame)


        if(azione=="U1"):#Lista delle partite effettuate in un torneo svolto in una data specificata
            giorno_var=tk.StringVar()
            mese_var=tk.StringVar()
            anno_var=tk.StringVar()
            nomeFrame.pack()
            lbl_dataTorneo = tk.Label(nomeFrame, bg='#c7c7c7', text="Inserire data GIORNO(gg)/MESE(mm)/ANNO(yyyy)").grid(row=0, column=0)
            ent_giorno = tk.Entry(nomeFrame, textvariable=giorno_var).grid(row=0, column=1)
            ent_mese = tk.Entry(nomeFrame, textvariable=mese_var).grid(row=0, column=2)
            ent_anno = tk.Entry(nomeFrame, textvariable=anno_var).grid(row=0, column=3)
            btn_calcoloQuery = tk.Button(nomeFrame, text="Controlla", command=lambda : lista_partite_effettuate_torneo(conn, giorno_var.get(), mese_var.get(), anno_var.get(), ruolo)).grid(row=1, column=0)

        elif(azione=="U2"):#Dato un concorrente ritornare il punteggio totale, numero vittorie e numero sconfitte per ogni torneo in cui ha partecipato
            giocatore_var=tk.StringVar()
            nomeFrame.pack()
            lbl_IdGiocatore = tk.Label(nomeFrame, bg='#c7c7c7', text="Inserire IdGiocatore:").grid(row=0, column=0)
            ent_Giocatore = tk.Entry(nomeFrame, textvariable=giocatore_var).grid(row=0, column=1)
            btn_calcoloQuery = tk.Button(nomeFrame, text="Controlla", command=lambda : top_giocatori( ruolo, giocatore_var.get()) ).grid(row=1, column=0)
        
        elif(azione=="U3"):#Lista delle carte bandite dall'attuale formato
            #questa richiede solo la data attuale presa direttamente da sistema
            nomeFrame.pack_forget()
        
        elif(azione=="U4"):#Lista delle carte di un mazzo specificato
            mazzo_var=tk.StringVar()
            nomeFrame.pack()
            lbl_Mazzo = tk.Label(nomeFrame, bg='#c7c7c7', text="Inserire codice mazzo:").grid(row=0, column=0)
            ent_Mazzo = tk.Entry(nomeFrame, textvariable=mazzo_var).grid(row=0, column=1)
            btn_calcoloQuery = tk.Button(nomeFrame, text="Controlla", command=lambda : lista_carte_mazzo(ruolo, mazzo_var.get())).grid(row=1, column=0)

        ################################ INSERIMENTO DATI ##################################################

        elif(azione=="A1"):#Inserimento nuova fiera
            #INSERT INTO FIERE (via, numeroCivico, IDcittà, IDnazione, nomeFiera, dataInizioFiera, dataFineFiera) 
            via_var=tk.StringVar()
            numero_var=tk.StringVar()
            city_var=tk.StringVar()
            nazion_var=tk.StringVar()
            fiera_var=tk.StringVar()

            GiornoInizioFiera_var=tk.StringVar()
            MeseInizioFiera_var=tk.StringVar()
            AnnoInizioFiera_var=tk.StringVar()
            
            GiornoFineFiera_var=tk.StringVar()
            MeseFineFiera_var=tk.StringVar()
            AnnoFineFiera_var=tk.StringVar()
            
            db_param_frame_admin.pack()
            lbl_via = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire via(opzionale):").grid(row=0, column=0)
            ent_via = tk.Entry(db_param_frame_admin, textvariable=via_var).grid(row=0, column=1)

            lbl_numero = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire numero civico(opzionale):").grid(row=0, column=2)
            ent_numero = tk.Entry(db_param_frame_admin, textvariable=numero_var).grid(row=0, column=3)

            lbl_city = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire codice città(opzionale):").grid(row=1, column=0)
            ent_city = tk.Entry(db_param_frame_admin, textvariable=city_var).grid(row=1, column=1)

            lbl_nazion = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire codice nazione(opzionale):").grid(row=1, column=2)
            ent_naizon = tk.Entry(db_param_frame_admin, textvariable=nazion_var).grid(row=1, column=3)

            lbl_fiera = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire nome della fiera:").grid(row=1, column=4)
            ent_fiera = tk.Entry(db_param_frame_admin, textvariable=fiera_var).grid(row=1, column=5)

            lbl_dataInitFiera = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire data inizio fiera GG/MM/YYYY:").grid(row=2, column=0)
            ent_GiornoInitFiera = tk.Entry(db_param_frame_admin, textvariable=GiornoInizioFiera_var).grid(row=2, column=1)
            ent_MeseInitFiera = tk.Entry(db_param_frame_admin, textvariable=MeseInizioFiera_var).grid(row=2, column=2)
            ent_AnnoInitFiera = tk.Entry(db_param_frame_admin, textvariable=AnnoInizioFiera_var).grid(row=2, column=3)

            lbl_dataEndFiera = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire data fine fiera GG/MM/YYYY:").grid(row=3, column=0)
            ent_GiornoEndFiera = tk.Entry(db_param_frame_admin, textvariable=GiornoFineFiera_var).grid(row=3, column=1)
            ent_MeseEndFiera = tk.Entry(db_param_frame_admin, textvariable=MeseFineFiera_var).grid(row=3, column=2)
            ent_AnnoEndFiera = tk.Entry(db_param_frame_admin, textvariable=AnnoFineFiera_var).grid(row=3, column=3)

            btn_calcoloQuery = tk.Button(db_param_frame_admin, text="Inserisci Fiera", 
                command=lambda : inserimento_Fiera(via_var.get(), numero_var.get(), city_var.get(), nazion_var.get(), fiera_var.get(), (GiornoInizioFiera_var.get(), MeseInizioFiera_var.get(), AnnoInizioFiera_var.get()), (GiornoFineFiera_var.get(), MeseFineFiera_var.get(), AnnoFineFiera_var.get()) ) ).grid(row=4, column=0)
            
        elif(azione=="A2"):#Inserimento nuovo torneo
            torneo_var=tk.StringVar()
            partecipanti_var=tk.StringVar()
            spettatori_var=tk.StringVar()
            fiera_var=tk.StringVar()
            gioco_var=tk.StringVar()
        
            GiornoTorneo_var=tk.StringVar()
            MeseTorneo_var=tk.StringVar()
            AnnoTorneo_var=tk.StringVar()

            
            db_param_frame_admin.pack()
            lbl_torneo = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire nome del torneo:").grid(row=0, column=0)
            ent_torneo = tk.Entry(db_param_frame_admin, textvariable=torneo_var).grid(row=0, column=1)

            lbl_part = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire numero spettatori:").grid(row=0, column=2)
            ent_part = tk.Entry(db_param_frame_admin, textvariable=partecipanti_var).grid(row=0, column=3)

            lbl_spett = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire numeroPartecipanti:").grid(row=1, column=0)
            ent_spett = tk.Entry(db_param_frame_admin, textvariable=spettatori_var).grid(row=1, column=1)

            lbl_gioco = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire codice gioco:").grid(row=1, column=2)
            ent_gioco = tk.Entry(db_param_frame_admin, textvariable=gioco_var).grid(row=1, column=3)

            lbl_fiera = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire codice fiera:").grid(row=1, column=4)
            ent_fiera = tk.Entry(db_param_frame_admin, textvariable=fiera_var).grid(row=1, column=5)

            lbl_dataTorneo = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire data del torneo GG/MM/YYYY:").grid(row=2, column=0)
            ent_GiornoTorneo = tk.Entry(db_param_frame_admin, textvariable=GiornoTorneo_var).grid(row=2, column=1)
            ent_MeseTorneo = tk.Entry(db_param_frame_admin, textvariable=MeseTorneo_var).grid(row=2, column=2)
            ent_AnnoTorneo = tk.Entry(db_param_frame_admin, textvariable=AnnoTorneo_var).grid(row=2, column=3)

            btn_calcoloQuery = tk.Button(db_param_frame_admin, text="Inserisci Torneo", 
                command=lambda : inserimento_Fiera( (GiornoTorneo_var.get(), MeseTorneo_var.get(), AnnoTorneo_var.get()), torneo_var.get(), int(spettatori_var.get()), int(partecipanti_var.get()), fiera_var.get(), gioco_var.get() ) ).grid(row=3, column=0)
        
        elif(azione=="A3"):#Inserimento dipendente

            nome_var=tk.StringVar()
            cognome_var=tk.StringVar()
            ruolo_var=tk.StringVar()
        
            Giorno_var=tk.StringVar()
            Mese_var=tk.StringVar()
            Anno_var=tk.StringVar()

            ruolo=["Giudice", "Addetto sicurezza", "Addetto receptionist", "Negoziante"]
            ruolo_var.set(ruolo)
            
            db_param_frame_admin.pack()
            lbl_nome = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire nome del torneo:").grid(row=0, column=0)
            ent_nome = tk.Entry(db_param_frame_admin, textvariable=nome_var).grid(row=0, column=1)

            lbl_cognome = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire numero spettatori:").grid(row=0, column=2)
            ent_cognome = tk.Entry(db_param_frame_admin, textvariable=cognome_var).grid(row=0, column=3)

            lbl_ruolo = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire numeroPartecipanti:").grid(row=1, column=0)
            ent_ruolo = OptionMenu(db_param_frame_admin, ruolo_var, *ruolo).grid(row=1, column=1)#menù a tendina

            lbl_dataTorneo = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire data del torneo GG/MM/YYYY:").grid(row=2, column=0)
            ent_GiornoTorneo = tk.Entry(db_param_frame_admin, textvariable=Giorno_var).grid(row=2, column=1)
            ent_MeseTorneo = tk.Entry(db_param_frame_admin, textvariable=Mese_var).grid(row=2, column=2)
            ent_AnnoTorneo = tk.Entry(db_param_frame_admin, textvariable=Anno_var).grid(row=2, column=3)

            #inserimento_Dipendente(nome, cognome, ruolo, dataNascita):
            #sql=""" INSERT INTO DIPENDENTI(nome, cognome, dataDiNascita, ruolo) 
            btn_calcoloQuery = tk.Button(db_param_frame_admin, text="Inserisci Torneo", 
                command=lambda : inserimento_Dipendente(nome_var.get(), cognome_var.get(), (Giorno_var.get(), Mese_var.get(), Anno_var.get()), ruolo_var.get() ) ).grid(row=3, column=0)
        
        elif(azione=="A4"):#Inserimento nuovo formato
            #inserimento_Formato(dataInizio, dataFine, codGioco):
            
            gioco_var=tk.StringVar()

            GiornoInizio_var=tk.StringVar()
            MeseInizio_var=tk.StringVar()
            AnnoInizio_var=tk.StringVar()

            GiornoFine_var=tk.StringVar()
            MeseFine_var=tk.StringVar()
            AnnoFine_var=tk.StringVar()
            
            db_param_frame_admin.pack()
            lbl_dataInizio = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire data di inizio del formato GG/MM/YYYY:").grid(row=0, column=0)
            ent_GiornoInizio = tk.Entry(db_param_frame_admin, textvariable=GiornoInizio_var).grid(row=0, column=1)
            ent_MeseInizio = tk.Entry(db_param_frame_admin, textvariable=MeseInizio_var).grid(row=0, column=2)
            ent_AnnoInizio = tk.Entry(db_param_frame_admin, textvariable=AnnoInizio_var).grid(row=0, column=3)

            lbl_dataFine = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire data di fine del formato GG/MM/YYYY:").grid(row=1, column=0)
            ent_GiornoFine = tk.Entry(db_param_frame_admin, textvariable=GiornoFine_var).grid(row=1, column=1)
            ent_MeseFine = tk.Entry(db_param_frame_admin, textvariable=MeseFine_var).grid(row=1, column=2)
            ent_AnnoFine = tk.Entry(db_param_frame_admin, textvariable=AnnoFine_var).grid(row=1, column=3)

            lbl_gioco = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire codice gioco a cui corrisponde il formato:").grid(row=2, column=0)
            ent_gioco = tk.Entry(db_param_frame_admin, textvariable=gioco_var).grid(row=2, column=1)
            #inserimento_Dipendente(nome, cognome, ruolo, dataNascita):
            #sql=""" INSERT INTO DIPENDENTI(nome, cognome, dataDiNascita, ruolo) 

            btn_calcoloQuery = tk.Button(db_param_frame_admin, text="Inserisci Formato", 
                command=lambda : inserimento_Formato( (GiornoInizio_var.get(), MeseInizio_var.get(), AnnoInizio_var.get()), (GiornoFine_var.get(), MeseFine_var.get(), AnnoFine_var.get()), gioco_var.get() ) ).grid(row=3, column=0)
        
        elif(azione=="A7"):#Registrazione vendita per stand
            #registro_vendite_stand(tipologia_prodotto, codVendita, dataVendita, codStand, prezzoTotale, CODICE_PRODOTTO, quantità)
            
            tipologia=["Gioco da tavolo", "Materiale di gioco"]
            tipo_var=tk.StringVar()
            vendita_var=tk.StringVar()
            stand_var=tk.StringVar()
            prezzo_var=tk.StringVar()
            codiceProdotto_var=tk.StringVar()
            quantity_var=tk.StringVar()

            GiornoVendita_var=tk.StringVar()
            MeseVendita_var=tk.StringVar()
            AnnoVendita_var=tk.StringVar()
            db_param_frame_admin.pack()
            tipo_var.set(tipologia[0])#valore di partenza
            lbl_tipo = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Scegliere tipo di prodotto:").grid(row=0, column=0)
            menu_tipo = OptionMenu(db_param_frame_admin, tipo_var, *tipologia).grid(row=0, column=1)#menù a tendina

            lbl_stand = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire codice dello stand:").grid(row=0, column=2)
            ent_stand = tk.Entry(db_param_frame_admin, textvariable=stand_var).grid(row=0, column=3)

            lbl_prezzo = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire prezzo del prodotto:").grid(row=2, column=0)
            ent_prezzo = tk.Entry(db_param_frame_admin, textvariable=prezzo_var).grid(row=2, column=1)

            lbl_prodotto = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire codice del prodotto:").grid(row=2, column=2)
            ent_prodotto = tk.Entry(db_param_frame_admin, textvariable=codiceProdotto_var).grid(row=2, column=3)

            lbl_quantity = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire quantità:").grid(row=2, column=4)
            ent_quantity = tk.Entry(db_param_frame_admin, textvariable=quantity_var).grid(row=2, column=5)

            lbl_dataFine = tk.Label(db_param_frame_admin, bg='#c7c7c7', text="Inserire data di fine del formato GG/MM/YYYY:").grid(row=3, column=0)
            ent_GiornoFine = tk.Entry(db_param_frame_admin, textvariable=GiornoVendita_var).grid(row=3, column=1)
            ent_MeseFine = tk.Entry(db_param_frame_admin, textvariable=MeseVendita_var).grid(row=3, column=2)
            ent_AnnoFine = tk.Entry(db_param_frame_admin, textvariable=AnnoVendita_var).grid(row=3, column=3)

            btn_calcoloQuery = tk.Button(db_param_frame_admin, text="Inserisci scontrino", 
                command=lambda : registro_vendite_stand(tipo_var.get(), vendita_var.get(), (GiornoVendita_var.get().get(), MeseVendita_var, AnnoVendita_var.get()), stand_var.get(), prezzo_var.get(), codiceProdotto_var.get(), quantity_var.get()) ).grid(row=4, column=0)
                #tipologia_prodotto, codVendita, dataVendita, codStand, prezzoTotale, CODICE_PRODOTTO, quantità)


        ################################ RICERCHE PER ADMIN ##################################################
        
        elif(azione=="A5"):#Gioco da tavolo con più partite non ufficiali
            db_param_frame_admin.pack_forget()
            gioco_partite_ufficiose()
        
        elif(azione=="A8"):#Guadagno di ogni stand
            db_param_frame_admin.pack_forget()
            guadagni_stands()


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


top_frame = tk.Frame(window_main, bg='#c7c7c7')

lbl_line = tk.Label(top_frame, bg='#c7c7c7', text="***********************************************************").pack()
lbl_line = tk.Label(top_frame, bg='#c7c7c7', text="**** SESSIONE UTENTE ****", font = "Helvetica 13 bold", foreground="blue").pack()
lbl_line = tk.Label(top_frame, bg='#c7c7c7', text="***********************************************************").pack()

#####################################
top_left_frame = tk.Frame(top_frame, bg='#c7c7c7', highlightbackground="green", highlightcolor="green", highlightthickness=1)



btn_U1=tk.Button(top_left_frame, text="Lista partite effettuate in un torneo in una data specificata", width=50, bg='#71da71', highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U1", "user")).grid(row=0, column=0)
lbl_spaziatore1=tk.Label(top_left_frame, bg='#c7c7c7').grid(row=1, column=0)
btn_U2=tk.Button(top_left_frame, text="Punteggio totale, numero di vittorie e sconfitte di un concorrente", highlightbackground="green", width=50, bg='#71da71', highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U2", "user")).grid(row=2, column=0)
lbl_spaziatore1=tk.Label(top_left_frame, bg='#c7c7c7').grid(row=3, column=0)
btn_U3=tk.Button(top_left_frame, text="Lista delle carte bandite dall'attuale formato", highlightbackground="green", width=50, bg='#71da71', highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U3", "user")).grid(row=4, column=0)
lbl_spaziatore1=tk.Label(top_left_frame, bg='#c7c7c7').grid(row=5, column=0)
btn_U4=tk.Button(top_left_frame, text="Lista delle carte di un mazzo specificato", highlightbackground="green", width=50, bg='#71da71', highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U4", "user")).grid(row=6, column=0)

top_left_frame.pack(side=tk.LEFT)


################### DATABASE FRAME USER ##################

#parametri
db_param_frame_user = tk.Frame(top_frame, highlightbackground="green", bg='#c7c7c7', highlightcolor="green", highlightthickness=1)
db_param_frame_user.pack(side=tk.BOTTOM)

#####################################
db_frame_user = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1, width=dimensioni_frame_tabella[0], height=dimensioni_frame_tabella[1])

db_frame_user.pack(side=tk.RIGHT)

top_frame.pack_forget()
#####################################




############################# SEZIONE ADMIN #############################################

admin_frame = tk.Frame(window_main, bg='#c7c7c7')

lbl_line = tk.Label(admin_frame, bg='#c7c7c7', text="***********************************************************").pack()
lbl_line = tk.Label(admin_frame, bg='#c7c7c7', text="**** SESSIONE ADMIN ****", font = "Helvetica 13 bold", foreground="blue").pack()
lbl_line = tk.Label(admin_frame, bg='#c7c7c7', text="***********************************************************").pack()


#####################################
final_frame = tk.Frame(admin_frame, bg='#c7c7c7')

##e60000 	#00ace6 #00e639
lbl_spaziatore1=tk.Label(final_frame, bg='#4dffff', text="Operazioni di ricerca").grid(row=0, column=0)

btn_U1_admin=tk.Button(final_frame, text="Lista partite effettuate in un torneo in una data specificata", bg='#71da71', width=50, highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U1", "admin")).grid(row=1, column=0)
lbl_spaziatore1=tk.Label(final_frame, bg='#c7c7c7').grid(row=2, column=0)
btn_U2_admin=tk.Button(final_frame, text="Punteggio totale, numero di vittorie e sconfitte di un concorrente", bg='#71da71', width=50, highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U2", "admin")).grid(row=3, column=0)
lbl_spaziatore1=tk.Label(final_frame, bg='#c7c7c7').grid(row=4, column=0)
btn_U3_admin=tk.Button(final_frame, text="Lista delle carte bandite dall'attuale formato", bg='#71da71', width=50, highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U3", "admin")).grid(row=5, column=0)
lbl_spaziatore1=tk.Label(final_frame, bg='#c7c7c7').grid(row=6, column=0)
btn_U4_admin=tk.Button(final_frame, text="Lista delle carte di un mazzo specificato", bg='#71da71', width=50, highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U4", "admin")).grid(row=7, column=0)
lbl_spaziatore1=tk.Label(final_frame, bg='#c7c7c7').grid(row=8, column=0)
btn_A5=tk.Button(final_frame, text="Gioco da tavolo con più partite non ufficiali", bg='#99f3ff', width=50, highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("A5", "admin")).grid(row=9, column=0)
lbl_spaziatore1=tk.Label(final_frame, bg='#c7c7c7').grid(row=10, column=0)
btn_A8=tk.Button(final_frame, text="Guadagni di ogni stand", bg='#99f3ff', width=50, highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("A8", "admin")).grid(row=11, column=0)

lbl_spaziatore1=tk.Label(final_frame, bg='#c7c7c7').grid(row=12, column=0)
lbl_spaziatore1=tk.Label(final_frame, bg='#4dffff', text="Operazioni d'inserimento").grid(row=13, column=0)

btn_A1=tk.Button(final_frame, text="Inserimento nuova fiera", bg='#f75e5e', width=50, highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("A1", "admin")).grid(row=14, column=0)
lbl_spaziatore1=tk.Label(final_frame, bg='#c7c7c7').grid(row=15, column=0)
btn_A2=tk.Button(final_frame, text="Inserimento nuovo torneo", bg='#f75e5e', width=50, highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("A2", "admin")).grid(row=16, column=0)
lbl_spaziatore1=tk.Label(final_frame, bg='#c7c7c7').grid(row=17, column=0)
btn_A3=tk.Button(final_frame, text="Inserimento dipendente", bg='#f75e5e', width=50, highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("A3", "admin")).grid(row=18, column=0)
lbl_spaziatore1=tk.Label(final_frame, bg='#c7c7c7').grid(row=19, column=0)
btn_A4=tk.Button(final_frame, text="Inserimento nuovo formato", bg='#f75e5e', width=50, highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("A4", "admin")).grid(row=20, column=0)
lbl_spaziatore1=tk.Label(final_frame, bg='#c7c7c7').grid(row=21, column=0)
btn_A7=tk.Button(final_frame, text="Registrazione vendita per stand", bg='#f75e5e', width=50, highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("A7", "admin")).grid(row=22, column=0)


final_frame.pack(side=tk.LEFT)

#parametri
db_param_frame_admin = tk.Frame(admin_frame, highlightbackground="green", bg='#c7c7c7', highlightcolor="green", highlightthickness=1)
db_param_frame_admin.pack(side=tk.BOTTOM)


#####################################
db_frame_admin = tk.Frame(admin_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1, width=dimensioni_frame_tabella[0], height=dimensioni_frame_tabella[1])

db_frame_admin.pack(side=tk.RIGHT, fill=BOTH, expand=FALSE)

admin_frame.pack_forget()





################### DATABASE FRAME ##################



window_main.mainloop()


######################################################################################################
