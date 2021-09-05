
import tkinter as tk
from tkinter import *
from tkinter import Listbox
from tkinter import messagebox as msg
import sqlite3 as lite
from sqlite3 import Error
import connessione_DB


window_main = tk.Tk()
window_main.title("ChallengeUP Games")
admin_log=False
screen_width = window_main.winfo_screenwidth()
screen_height = window_main.winfo_screenheight()

password_entry=tk.StringVar()
name_entry=tk.StringVar()
nomeFrame=Frame()

dataTorneo=tk.StringVar()

connessione_DB.creazione_tabelle()

conn=lite.connect("ChallengeUPGames_DB.db")
cur=conn.cursor()

def Admin_login(log):#da perfezionare ma non indispensabile ai fini del programma
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

    #formattazione della data secondo i database
    return anno + "-" + mese + "-" + giorno

def lista_partite_effettuate_torneo(conn, giorno, mese, anno, ruolo):
    if(controlloData(giorno, mese, anno) != 1):
        data=controlloData(giorno, mese, anno)

        sql="""SELECT *
            FROM 	TORNEI T, PARTITE_UFFICIALI PU, DIPENDENTI D, PADIGLIONI P, VINCITORI V, PERDENTI PE, CONCORRENTI C
            WHERE T.IdTorneo = PU.IdTorneo AND
            D.CodiceBadge = PU.IdGiudice AND
            P.CodPadiglione = PU.CodPadiglione AND
            PU.IdMatch = V.IdMatch AND
            PU.IdMatch = PE.IdMatch AND
            PE.codConcorrente = C. codConcorrente AND
            V.codConcorrente = C. codConcorrente AND
            T.dataTorneo=(?);"""

        colonne=["IdTorneo","nomeTorneo", "numeroSpettatori", "numeroPartecipanti", "codGioco", "IdFiera", "IdMatch", "dataPartita", "nomePadiglione", ]
        cursor=conn.cursor()
        cursor.execute(sql, data)
        records=cursor.fetchall()
        tabella=colonne
        tabella.append(records)
        genera_tabella_query(ruolo, tabella)

def top_giocatori(ruolo, IdGiocatore):
    sql=""" SELECT ( (SELECT SUM(punteggioVittoria)
        FROM )) + ()) AS punteggio totale, COUNT(punteggioVittoria) AS numeroVittorie, COUNT(punteggioSconfitte) AS numeroSconfitte
        FROM TORNEI T, PARTITE_UFFICIALI PU, VINCITORE V, PERDENTE P, CONCORRENTE C
        WHERE PU.IdTorneo = T.IdTorneo AND
        V.IdMatch = PU.IdMatch AND
        P.IdMatch = PU.IdMatch AND
        C.codConcorrente = V.codConcorrente AND
        C.codConcorrente = P.codConcorrente AND
        CodConcorrente = (?)
        GROUP BY IdTorneo;"""

    colonne=["IdGiocatore", "Punteggio totale"]
    cursor=conn.cursor()
    cursor.execute(sql, IdGiocatore)
    records=cursor.fetchall()
    tabella=colonne
    tabella.append(records)
    genera_tabella_query(ruolo, tabella)

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

    colonne=["codMazzo", "Colore", "codCarta", "nome", "tipo", "descrizione", "Costo", "Attributo", "Attacco", "Difesa", "Effetto"]
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

        sql=""" INSERT INTO FIERE(via, numeroCivico, Idcittà, Idnazione, nomeFiera, dataInizioFiera, dataFineFiera) 
        VALUES((?), (?), (?), (?), (?), (?), (?));"""
        print(dataInizio)
        print(dataFine)
        cursor=conn.cursor()
        dati=(via, numeroCivico, int(IdCittà), id(IdNazione), nomeFiera, dataInizio, dataFine)
        try:
            cursor.execute(sql, dati)
            conn.commit()
        except Error as e:
            msg.showerror(title="ERRORE INSERIMENTO", message="qualcosa è andato storto con l'inserimento della fiera\n"+str(e))

def inserimento_Torneo(dataTorneo, nomeTorneo, numeroSpettatori, numeroPatecipanti, IdFiera, codGioco):
    if(controlloData(dataTorneo[0], dataTorneo[1], dataTorneo[2]) != 1):
        
        #formattazione delle date
        dataT=controlloData(dataTorneo[0], dataTorneo[1], dataTorneo[2])
    
        sql=""" INSERT INTO TORNEI(dataTorneo, nomeTorneo, numeroSpettatori, numeroPartecipanti, IdFiera, codGioco) 
        VALUES((?), (?), (?), (?), (?), (?))"""
        
        dati=(dataT, nomeTorneo, int(numeroPatecipanti), int(numeroSpettatori), int(IdFiera), int(codGioco))
        cursor=conn.cursor()
        try:
            cursor.execute(sql, dati)
            conn.commit()
        except Error as e:
            msg.showerror(title="ERRORE INSERIMENTO", message="qualcosa è andato storto con l'inserimento del torneo\n"+str(e))

def gioco_partite_ufficiose():
    sql=""" SELECT TOP 1 WITH TIES nomeGioco, descrizione, regolamento, SUM(numeroPartite) AS partiteTotali
            FROM PARTITE NON UFFICIALI PNU, GIOCHI DA TAVOLO G
            WHERE PNU.CodGioco = G.CodGioco
            GROUP BY CodGioco
            ORDER BY 4
            """

    colonne=["Nome", "Descrizione", "Regolamento", "Partite totali"]
    cursor=conn.cursor()
    cursor.execute(sql)
    records=cursor.fetchall()
    print(colonne)
    print(records)
    tabella=colonne
    tabella.append(records)
    genera_tabella_query("admin", tabella)

def guadagni_stands():
    sql=""" SELECT V.codStand, SUM(prezzoTotale) AS guadagnoTotale, 
                (
                    SELECT AVG(prezzoTotale) 
                    FROM VENDITE V1, VEN_GIOCO VG 
                    WHERE V1.codStand = VG.codStand AND V1.codVendita = VG.codVendita AND V1.codStand = V.codStand
                ) AS guadagnoMedioGiochiDaTavolo,
                (
                    SELECT AVG(prezzoTotale) 
                    FROM VENDITE V1, VEN_MAT VM 
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
        sql=""" INSERT INTO DIPENDENTI(nome, cognome, dataDiNascita, ruolo) 
        VALUES((?), (?), (?), (?))"""
        
        dati=(nome, cognome, ruolo, dataNascita)
        cursor=conn.cursor()
        try:
            cursor.execute(sql, dati)
            conn.commit()
        except Error as e:
            msg.showerror(title="ERRORE INSERIMENTO", message="qualcosa è andato storto con l'inserimento del dipendente\n"+str(e))

def registro_vendite_stand(tipologia_prodotto, codVendita, dataVendita, codStand, prezzoTotale, CODICE_PRODOTTO, quantità):
    if(controlloData(dataVendita[0], dataVendita[1], dataVendita[2]) != 1):
        
        #formattazione delle date
        dataV=controlloData(dataVendita[0], dataVendita[1], dataVendita[2])
    
        sql=""" INSERT INTO VENDITE(CodVendita, dataVendita, codStand, prezzoTotale) 
                    VALUES((?), (?), (?), (?))"""
        dati=(int(codVendita), dataV, int(codStand), prezzoTotale)
        cursor=conn.cursor()
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
        
        dati=(dataI, dataF, int(codGioco))
        cursor=conn.cursor()
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
    
        if(azione=="U1"):#Lista delle partite effettuate in un torneo svolto in una data specificata
            giorno_var=tk.StringVar()
            mese_var=tk.StringVar()
            anno_var=tk.StringVar()
            lbl_dataTorneo = tk.Label(nomeFrame, text="Inserire data GIORNO(gg)/MESE(mm)/ANNO(yyyy)").grid(row=0, column=0)
            ent_giorno = tk.Entry(nomeFrame, textvariable=giorno_var).grid(row=0, column=1)
            ent_mese = tk.Entry(nomeFrame, textvariable=mese_var).grid(row=0, column=2)
            ent_anno = tk.Entry(nomeFrame, textvariable=anno_var).grid(row=0, column=3)
            btn_calcoloQuery = tk.Button(nomeFrame, text="Controlla", command=lambda : lista_partite_effettuate_torneo(conn, giorno_var.get(), mese_var.get(), anno_var.get(), ruolo)).grid(row=1, column=0)

        elif(azione=="U2"):#Dato un concorrente ritornare il punteggio totale, numero vittorie e numero sconfitte per ogni torneo in cui ha partecipato
            giocatore_var=tk.StringVar()
            lbl_IdGiocatore = tk.Label(nomeFrame, text="Inserire IdGiocatore:").grid(row=0, column=0)
            ent_Giocatore = tk.Entry(nomeFrame, textvariable=giocatore_var).grid(row=0, column=1)
            btn_calcoloQuery = tk.Button(nomeFrame, text="Controlla", command=lambda : top_giocatori(ruolo, giocatore_var.get())).grid(row=1, column=0)
        
        elif(azione=="U3"):#Lista delle carte bandite dall'attuale formato
            #questa richiede solo la data attuale presa direttamente da sistema
            print()
        
        elif(azione=="U4"):#Lista delle carte di un mazzo specificato
            mazzo_var=tk.StringVar()
            lbl_Mazzo = tk.Label(nomeFrame, text="Inserire codice mazzo:").grid(row=0, column=0)
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

            lbl_via = tk.Label(db_param_frame_admin, text="Inserire via(opzionale):").grid(row=0, column=0)
            ent_via = tk.Entry(db_param_frame_admin, textvariable=via_var).grid(row=0, column=1)

            lbl_numero = tk.Label(db_param_frame_admin, text="Inserire numero civico(opzionale):").grid(row=0, column=2)
            ent_numero = tk.Entry(db_param_frame_admin, textvariable=numero_var).grid(row=0, column=3)

            lbl_city = tk.Label(db_param_frame_admin, text="Inserire codice città(opzionale):").grid(row=1, column=0)
            ent_city = tk.Entry(db_param_frame_admin, textvariable=city_var).grid(row=1, column=1)

            lbl_nazion = tk.Label(db_param_frame_admin, text="Inserire codice nazione(opzionale):").grid(row=1, column=2)
            ent_naizon = tk.Entry(db_param_frame_admin, textvariable=nazion_var).grid(row=1, column=3)

            lbl_fiera = tk.Label(db_param_frame_admin, text="Inserire nome della fiera:").grid(row=1, column=4)
            ent_fiera = tk.Entry(db_param_frame_admin, textvariable=fiera_var).grid(row=1, column=5)

            lbl_dataInitFiera = tk.Label(db_param_frame_admin, text="Inserire data inizio fiera GG/MM/YYYY:").grid(row=2, column=0)
            ent_GiornoInitFiera = tk.Entry(db_param_frame_admin, textvariable=GiornoInizioFiera_var).grid(row=2, column=1)
            ent_MeseInitFiera = tk.Entry(db_param_frame_admin, textvariable=MeseInizioFiera_var).grid(row=2, column=2)
            ent_AnnoInitFiera = tk.Entry(db_param_frame_admin, textvariable=AnnoInizioFiera_var).grid(row=2, column=3)

            lbl_dataEndFiera = tk.Label(db_param_frame_admin, text="Inserire data fine fiera GG/MM/YYYY:").grid(row=3, column=0)
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


            lbl_torneo = tk.Label(db_param_frame_admin, text="Inserire nome del torneo:").grid(row=0, column=0)
            ent_torneo = tk.Entry(db_param_frame_admin, textvariable=torneo_var).grid(row=0, column=1)

            lbl_part = tk.Label(db_param_frame_admin, text="Inserire numero spettatori:").grid(row=0, column=2)
            ent_part = tk.Entry(db_param_frame_admin, textvariable=partecipanti_var).grid(row=0, column=3)

            lbl_spett = tk.Label(db_param_frame_admin, text="Inserire numeroPartecipanti:").grid(row=1, column=0)
            ent_spett = tk.Entry(db_param_frame_admin, textvariable=spettatori_var).grid(row=1, column=1)

            lbl_gioco = tk.Label(db_param_frame_admin, text="Inserire codice gioco:").grid(row=1, column=2)
            ent_gioco = tk.Entry(db_param_frame_admin, textvariable=gioco_var).grid(row=1, column=3)

            lbl_fiera = tk.Label(db_param_frame_admin, text="Inserire codice fiera:").grid(row=1, column=4)
            ent_fiera = tk.Entry(db_param_frame_admin, textvariable=fiera_var).grid(row=1, column=5)

            lbl_dataTorneo = tk.Label(db_param_frame_admin, text="Inserire data del torneo GG/MM/YYYY:").grid(row=2, column=0)
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

            lbl_nome = tk.Label(db_param_frame_admin, text="Inserire nome del torneo:").grid(row=0, column=0)
            ent_nome = tk.Entry(db_param_frame_admin, textvariable=nome_var).grid(row=0, column=1)

            lbl_cognome = tk.Label(db_param_frame_admin, text="Inserire numero spettatori:").grid(row=0, column=2)
            ent_cognome = tk.Entry(db_param_frame_admin, textvariable=cognome_var).grid(row=0, column=3)

            lbl_ruolo = tk.Label(db_param_frame_admin, text="Inserire numeroPartecipanti:").grid(row=1, column=0)
            ent_ruolo = OptionMenu(db_param_frame_admin, ruolo_var, *ruolo).grid(row=1, column=1)#menù a tendina

            lbl_dataTorneo = tk.Label(db_param_frame_admin, text="Inserire data del torneo GG/MM/YYYY:").grid(row=2, column=0)
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

            lbl_dataInizio = tk.Label(db_param_frame_admin, text="Inserire data di inizio del formato GG/MM/YYYY:").grid(row=0, column=0)
            ent_GiornoInizio = tk.Entry(db_param_frame_admin, textvariable=GiornoInizio_var).grid(row=0, column=1)
            ent_MeseInizio = tk.Entry(db_param_frame_admin, textvariable=MeseInizio_var).grid(row=0, column=2)
            ent_AnnoInizio = tk.Entry(db_param_frame_admin, textvariable=AnnoInizio_var).grid(row=0, column=3)

            lbl_dataFine = tk.Label(db_param_frame_admin, text="Inserire data di fine del formato GG/MM/YYYY:").grid(row=1, column=0)
            ent_GiornoFine = tk.Entry(db_param_frame_admin, textvariable=GiornoFine_var).grid(row=1, column=1)
            ent_MeseFine = tk.Entry(db_param_frame_admin, textvariable=MeseFine_var).grid(row=1, column=2)
            ent_AnnoFine = tk.Entry(db_param_frame_admin, textvariable=AnnoFine_var).grid(row=1, column=3)

            lbl_gioco = tk.Label(db_param_frame_admin, text="Inserire codice gioco a cui corrisponde il formato:").grid(row=2, column=0)
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

            tipo_var.set(tipologia[0])#valore di partenza
            lbl_tipo = tk.Label(db_param_frame_admin, text="Scegliere tipo di prodotto:").grid(row=0, column=0)
            menu_tipo = OptionMenu(db_param_frame_admin, tipo_var, *tipologia).grid(row=0, column=1)#menù a tendina

            lbl_vendita = tk.Label(db_param_frame_admin, text="Inserire codice vendita:").grid(row=1, column=0)
            ent_vendita = tk.Entry(db_param_frame_admin, textvariable=vendita_var).grid(row=1, column=1)

            lbl_stand = tk.Label(db_param_frame_admin, text="Inserire codice dello stand:").grid(row=1, column=2)
            ent_stand = tk.Entry(db_param_frame_admin, textvariable=stand_var).grid(row=1, column=3)

            lbl_prezzo = tk.Label(db_param_frame_admin, text="Inserire prezzo del prodotto:").grid(row=2, column=0)
            ent_prezzo = tk.Entry(db_param_frame_admin, textvariable=prezzo_var).grid(row=2, column=1)

            lbl_prodotto = tk.Label(db_param_frame_admin, text="Inserire codice del prodotto:").grid(row=2, column=2)
            ent_prodotto = tk.Entry(db_param_frame_admin, textvariable=codiceProdotto_var).grid(row=2, column=3)

            lbl_quantity = tk.Label(db_param_frame_admin, text="Inserire quantità:").grid(row=2, column=4)
            ent_quantity = tk.Entry(db_param_frame_admin, textvariable=quantity_var).grid(row=2, column=5)

            lbl_dataFine = tk.Label(db_param_frame_admin, text="Inserire data di fine del formato GG/MM/YYYY:").grid(row=3, column=0)
            ent_GiornoFine = tk.Entry(db_param_frame_admin, textvariable=GiornoVendita_var).grid(row=3, column=1)
            ent_MeseFine = tk.Entry(db_param_frame_admin, textvariable=MeseVendita_var).grid(row=3, column=2)
            ent_AnnoFine = tk.Entry(db_param_frame_admin, textvariable=AnnoVendita_var).grid(row=3, column=3)

            btn_calcoloQuery = tk.Button(db_param_frame_admin, text="Inserisci scontrino", 
                command=lambda : registro_vendite_stand(tipo_var.get(), vendita_var.get(), (GiornoVendita_var.get().get(), MeseVendita_var, AnnoVendita_var.get()), stand_var.get(), prezzo_var.get(), codiceProdotto_var.get(), quantity_var.get()) ).grid(row=3, column=0)
                #tipologia_prodotto, codVendita, dataVendita, codStand, prezzoTotale, CODICE_PRODOTTO, quantità)


        ################################ RICERCHE PER ADMIN ##################################################
        
        elif(azione=="A5"):#Gioco da tavolo con più partite non ufficiali
            gioco_partite_ufficiose()
        
        elif(azione=="A8"):#Guadagno di ogni stand
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


top_frame = tk.Frame(window_main)

lbl_line = tk.Label(top_frame, text="***********************************************************").pack()
lbl_line = tk.Label(top_frame, text="**** SESSIONE UTENTE ****", font = "Helvetica 13 bold", foreground="blue").pack()
lbl_line = tk.Label(top_frame, text="***********************************************************").pack()

#####################################
top_left_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)



btn_U1=tk.Button(top_left_frame, text="Lista delle partite effettuate in un torneo svolto in una data specificata", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U1", "user")).grid(row=0, column=0)
btn_U2=tk.Button(top_left_frame, text="Top 10 giocatori con il punteggio più alto", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U2", "user")).grid(row=1, column=0)
btn_U3=tk.Button(top_left_frame, text="Lista delle carte bandite dall'attuale formato", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U3", "user")).grid(row=2, column=0)
btn_U4=tk.Button(top_left_frame, text="Lista delle carte di un mazzo specificato", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U4", "user")).grid(row=3, column=0)

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
btn_U2_admin=tk.Button(final_frame, text="Top 10 giocatori con il punteggio più alto", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U2", "admin")).grid(row=1, column=0)
btn_U3_admin=tk.Button(final_frame, text="Lista delle carte bandite dall'attuale formato", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U3", "admin")).grid(row=2, column=0)
btn_U4_admin=tk.Button(final_frame, text="Lista delle carte di un mazzo specificato", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("U4", "admin")).grid(row=3, column=0)

btn_A1=tk.Button(final_frame, text="Inserimento nuova fiera", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("A1", "admin")).grid(row=5, column=0)
btn_A2=tk.Button(final_frame, text="Inserimento nuovo torneo", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("A2", "admin")).grid(row=6, column=0)
btn_A3=tk.Button(final_frame, text="Inserimento dipendente", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("A3", "admin")).grid(row=7, column=0)
btn_A4=tk.Button(final_frame, text="Inserimento nuovo formato", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("A4", "admin")).grid(row=8, column=0)
btn_A5=tk.Button(final_frame, text="Gioco da tavolo con più partite non ufficiali", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("A5", "admin")).grid(row=9, column=0)
btn_A7=tk.Button(final_frame, text="Registrazione vendita per stand", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("A7", "admin")).grid(row=10, column=0)
btn_A8=tk.Button(final_frame, text="Guadagni di ogni stand", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_parametri("A8", "admin")).grid(row=11, column=0)


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
