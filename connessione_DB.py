import sqlite3 as lite
con=lite.connect("ChallengeUPGames_DB.db")
cur=con.cursor()
sql=[]

####################################### CREAZIONE TABELLE ################################################

########## Nazione #############
sql.append(""" CREATE TABLE IF NOT EXIST NAZIONI(
    IdNazione int PRIMARY KEY,
    nomeNazione char(50) NOT NULL
);""")

########## Città #############
sql.append(""" CREATE TABLE IF NOT EXIST CITTA(
    IdCittà int PRIMARY KEY,
    nomeCittà char(60) NOT NULL,
    FOREIGN KEY (IdNazione) references NAZIONI
);""")

sql.append(""" CREATE TABLE IF NOT EXIST FIERE(
    IdFiera int PRIMARY KEY,
    via char(10),
    numeroCivico int,
    nomeFiera char(20) NOT NULL,
    dataInzioFiera DATETIME NOT NULL,
    dataFineFiera DATETIME NOT NULL,
    FOREIGN KEY (IdNazione) references CITTA,
    FOREIGN KEY (IdCittà) references CITTA
);""")

sql.append(""" CREATE TABLE IF NOT EXIST VENDITE(
    CodVendita int NOT NULL AUTO_INCRMENT,
    prodotto char(20) NOT NULL,
    quantità int NOT NULL,
    dataVendita DATETIME NOT NULL,
    prezzoVendita MONEY NOT NULL,
    PRIMARY KEY (CodVendita, prodotto, quantità),
    FOREIGN KEY (IdStand) REFERENCES STANDS
);""")

sql.append(""" CREATE TABLE IF NOT EXIST STANDS(
    codStand int PRIMARY KEY,
    nome char(10) NOT NULL,
    FOREIGN KEY (IdFiera) REFERENCES FIERE,
    FOREIGN KEY (CodiceBadge) REFERENCES DIPENDENTI
);""")

sql.append(""" CREATE TABLE IF NOT EXIST CONTENUTI(
    quantitàGiochi int NOT NULL,
    codStand INT NOT NULL FOREIGN KEY REFERENCES STAND,
    codGioco INT NOT NULL FOREIGN KEY REFERENCES GIOCHI_DA_TAVOLO,
    PRIMARY KEY(codStand, codGioco)
);""")

sql.append(""" CREATE TABLE IF NOT EXIST IMMAGAZZINATI(
    quantitàMateriale int NOT NULL,
    codStand INT NOT NULL FOREIGN KEY REFERENCES STAND,
    codMateriale INT NOT NULL FOREIGN KEY REFERENCES MATERIALI_DA_GIOCO,
    PRIMARY KEY (codStand, codMateriale)
);""")

sql.append(""" CREATE TABLE IF NOT EXIST GIOCHI_DA_TAVOLO(
    codGioco int PRIMARY KEY,
    nomeGioco char(30) NOT NULL,
    descrizione char(200) NOT NULL,
    regolamento char(300) NOT NULL
);""")

sql.append(""" CREATE TABLE IF NOT EXIST FORMATI(
    dataInizio DATETIME NOT NULL,
    dataFine DATETIME NOT NULL,
    listaCarteBandite varchar(1000) NOT NULL,
    PRIMARY KEY (dataInzio, dataFine),
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO
);""")

sql.append(""" CREATE TABLE IF NOT EXIST SITUATI(
    codGioco INT NOT NULL FOREIGN KEY REFERENCES GIOCHI_DA_TAVOLO,
    codTerreno INT NOT NULL FOREIGN KEY REFERENCES TERRENO,
    PRIMARY KEY (codGioco, codTerreno)
);""")

sql.append(""" CREATE TABLE IF NOT EXIST TERRENI(
    codTerreno int PRIMARY KEY,
    descrizione char(30)
);""")

sql.append(""" CREATE TABLE IF NOT EXIST TORNEI(
    IdTorneo int PRIMARY KEY,
    dataTorneo DATETIME NOT NULL,
    nomeTorneo char(20) NOT NULL,
    numeroSpettatori int NOT NULL,
    numeroPartecipanti int NOT NULL CHECK(numeroPartecipanti >= 2)
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO,
    FOREIGN KEY (IdFiera) REFERENCES FIERA,
);""")

sql.append(""" CREATE TABLE IF NOT EXIST SORVEGLIANO(
    turnoDiLavoro DATETIME PRIMARY KEY,
    FOREIGN KEY (IdFiera) REFERENCES FIERA,
    FOREIGN KEY (CodiceBadge) REFERENCES DIEPENDENTI
);""")

sql.append(""" CREATE TABLE IF NOT EXIST DIPENDENTI(
    CodiceBadge int PRIMARY KEY,
    nome char(30) NOT NULL,
    cognome char(30) NOT NULL,
    dataDiNascita DATETIME NOT NULL,
    ruolo char(10) NOT NULL
);""")

sql.append(""" CREATE TABLE IF NOT EXIST PARTECIPANTI(
    codPartecipante int PRIMARY KEY,
    nome char(30) NOT NULL,
    cognome char(30) NOT NULL,
    dataDiNascita DATETIME NOT NULL,
    FOREIGN KEY (IdFiera) REFERENCES FIERA,
    FOREIGN KEY (CodiceBadge) REFERENCES DIPENDENTI
);""")

sql.append(""" CREATE TABLE IF NOT EXIST PADIGLIONI(
    codPadiglione int PRIMARY KEY,
    tipologia char(8),
    nomePadiglione char(20) NOT NULL,
    capienzaMassima int NOT NULL CHECK(capienzaMassima >= 1),
    numeroTavoli int NOT NULL CHECK(numeroTavoli >=1),
    FOREIGN KEY (IdFiera) REFERENCES FIERA
);""")

sql.append(""" CREATE TABLE IF NOT EXIST PARTITE_NON_UFFICIALI(
    numeroPartite int NOT NULL,
    codGioco INT NOT NULL FOREIGN KEY REFERENCES GIOCHI_DA_TAVOLO,
    codPadiglione INT NOT NULL FOREIGN KEY REFERENCES PADIGLIONI,
    PRIMARY KEY (codGioco, codPadiglione)
);""")

sql.append(""" CREATE TABLE IF NOT EXIST PARTITE_UFFICIALI(
    IdMatch int PRIMARY KEY,
    dataPartita DATETIME NOT NULL,
    FOREIGN KEY (IdGiudice) REFERENCES DIPENDENTI,
    FOREIGN KEY (CodPadiglione) REFERENCES PADIGLIONI,
    FOREIGN KEY (IdTorneo) REFERENCES TORNEI
);""")

sql.append(""" CREATE TABLE IF NOT EXIST VINCITORI(
    IdMatch INT NOT NULL FOREIGN KEY REFERENCES PARTITE_UFFICIALI,
    codConcorrente INT NOT NULL FOREIGN KEY REFERENCES CONCORRENTI,
    PRIMARY KEY (numeroMatch, codConcorrente)
);""")

sql.append(""" CREATE TABLE IF NOT EXIST PERDENTI(
    IdMatch INT NOT NULL FOREIGN KEY REFERENCES PARTITE_UFFICIALI,
    codConcorrente INT NOT NULL FOREIGN KEY REFERENCES CONCORRENTI,
    PRIMARY KEY (numeroMatch, codConcorrente)
);""")

sql.append(""" CREATE TABLE IF NOT EXIST CONCORRENTI(
    codConcorrente int PRIMARY KEY,
    punteggio int
);""")

sql.append(""" CREATE TABLE IF NOT EXIST POSSIEDONO(
    codGioco INT NOT NULL FOREIGN KEY REFERENCES GIOCHI_DA_TAVOLO,
    codCarta INT NOT NULL FOREIGN KEY REFERENCES CARTE,
    PRIMARY KEY (codGioco, codCarta)
);""")

sql.append(""" CREATE TABLE IF NOT EXIST COMPOSTI(
    codMazzo INT NOT NULL FOREIGN KEY REFERENCES MAZZI,
    codCarta INT NOT NULL FOREIGN KEY REFERENCES CARTE,
    PRIMARY KEY (codGioco, codCarta)
);""")

sql.append(""" CREATE TABLE IF NOT EXIST SET_CARTE_BANDITE(
    dataInizio INT NOT NULL FOREIGN KEY REFERENCES FORMATI,
    dataFine INT NOT NULL FOREIGN KEY REFERENCES FORMATI,
    codCarta INT NOT NULL FOREIGN KEY REFERENCES CARTE,
    PRIMARY KEY (dataInizio, dataFine, codCarta)
);""")

sql.append(""" CREATE TABLE IF NOT EXIST CARTE(
    codCarta int PRIMARY KEY,
    nome char(50) NOT NULL,
    tipo char(10) NOT NULL CHECH(tipo = 'Mostro' OR 'Magia' OR 'Trappola'),
    descrizione char(100),
    costoMana int,
    attributo char(10),
    attacco int,
    difesa int,
    effetto char(20) NOT NULL
);""")

sql.append(""" CREATE TABLE IF NOT EXIST MAZZI(
    codMazzo int PRIMARY KEY,
    colore_clan char(20) NOT NULL,
    dimensioni int NOT NULL CHECK(dimensioni >= 0)
);""")

sql.append(""" CREATE TABLE IF NOT EXIST DADI(
    codDado int PRIMARY KEY,
    numFacce int NOT NULL CHECK(numfacce >= 4),
    colore char(20) NOT NULL,
    materiale char(50) NOT NULL
);""")

sql.append(""" CREATE TABLE IF NOT EXIST PEDINE(
    codPedina int PRIMARY KEY,
    colore char(20) NOT NULL,
    materiale char(50) NOT NULL
);""")

sql.append(""" CREATE TABLE IF NOT EXIST MATERIALI_DA_GIOCO(
    codMateriale int PRIMARY KEY,
    codDado INT FOREIGN KEY REFERENCES DADI CHECK( (codDado IS NOT NULL) AND (codMateriale=DADI.codDado) ),
    codPedina INT FOREIGN KEY REFERENCES PEDINE CHECK( (codPedina IS NOT NULL) AND (codMateriale=PEDINE.codPedina) ),
    codCarta INT FOREIGN KEY REFERENCES CARTE CHECK( (codCarta IS NOT NULL) AND (codMateriale=CARTE.codCarta) )

    primary key (Codice_NPC) --,
--     check(exists(select * from VENDITA
--                  where VENDITA.Codice_NPC = Codice_NPC)) 

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")

sql.append(""" CREATE TABLE IF NOT EXIST (

);""")


for k in sql:
    cur.execute(k)
    risultato=cur.fetchall()
con.commit()

