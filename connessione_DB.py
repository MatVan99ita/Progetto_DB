import sqlite3 as lite
con=lite.connect("ChallengeUPGames_DB.db")
cur=con.cursor()
sql=[]

####################################### CREAZIONE TABELLE ################################################

########## Nazione #############
sql.append(""" CREATE TABLE IF NOT EXISTS NAZIONI(
    IdNazione int PRIMARY KEY,
    nomeNazione char(50) NOT NULL
);""")

########## Città #############
sql.append(""" CREATE TABLE IF NOT EXISTS CITTA(
    IdCittà int PRIMARY KEY,
    nomeCittà char(60) NOT NULL,
    FOREIGN KEY (IdNazione) references NAZIONI
);""")

########## Nazione #############
sql.append(""" CREATE TABLE IF NOT EXISTS FIERE(
    IdFiera int PRIMARY KEY,
    via char(10),
    numeroCivico int,
    nomeFiera char(20) NOT NULL,
    dataInzioFiera DATETIME NOT NULL,
    dataFineFiera DATETIME NOT NULL,
    FOREIGN KEY (IdNazione) references CITTA,
    FOREIGN KEY (IdCittà) references CITTA
);""")

########## Vendite #############
sql.append(""" CREATE TABLE IF NOT EXISTS VENDITE(
    CodVendita int NOT NULL AUTO_INCRMENT,
    prodotto char(20) NOT NULL,
    quantità int NOT NULL,
    dataVendita DATETIME NOT NULL,
    prezzoVendita MONEY NOT NULL,
    PRIMARY KEY (CodVendita, prodotto, quantità),
    FOREIGN KEY (IdStand) REFERENCES STANDS
);""")

########## Stands #############
sql.append(""" CREATE TABLE IF NOT EXISTS STANDS(
    codStand int PRIMARY KEY,
    nome char(10) NOT NULL,
    FOREIGN KEY (IdFiera) REFERENCES FIERE,
    FOREIGN KEY (CodiceBadge) REFERENCES DIPENDENTI
);""")

########## Contenuti #############
sql.append(""" CREATE TABLE IF NOT EXISTS CONTENUTI(
    quantitàGiochi int NOT NULL,
    codStand INT NOT NULL FOREIGN KEY REFERENCES STAND,
    codGioco INT NOT NULL FOREIGN KEY REFERENCES GIOCHI_DA_TAVOLO,
    PRIMARY KEY(codStand, codGioco)
);""")

########## Immagazzinati #############
sql.append(""" CREATE TABLE IF NOT EXISTS IMMAGAZZINATI(
    quantitàMateriale int NOT NULL,
    codStand INT NOT NULL FOREIGN KEY REFERENCES STAND,
    codMateriale INT NOT NULL FOREIGN KEY REFERENCES MATERIALI_DA_GIOCO,
    PRIMARY KEY (codStand, codMateriale)
);""")

########## Giochi da tavolo #############
sql.append(""" CREATE TABLE IF NOT EXISTS GIOCHI_DA_TAVOLO(
    codGioco int PRIMARY KEY,
    nomeGioco char(30) NOT NULL,
    descrizione char(200) NOT NULL,
    regolamento char(300) NOT NULL
);""")

########## Formati #############
sql.append(""" CREATE TABLE IF NOT EXISTS FORMATI(
    dataInizio DATETIME NOT NULL,
    dataFine DATETIME NOT NULL,
    listaCarteBandite varchar(1000) NOT NULL,
    PRIMARY KEY (dataInzio, dataFine),
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO
);""")

########## Situati #############
sql.append(""" CREATE TABLE IF NOT EXISTS SITUATI(
    codGioco INT NOT NULL FOREIGN KEY REFERENCES GIOCHI_DA_TAVOLO,
    codTerreno INT NOT NULL FOREIGN KEY REFERENCES TERRENO,
    PRIMARY KEY (codGioco, codTerreno)
);""")

########## Terreni #############
sql.append(""" CREATE TABLE IF NOT EXISTS TERRENI(
    codTerreno int PRIMARY KEY,
    descrizione char(30)
);""")

########## Tornei #############
sql.append(""" CREATE TABLE IF NOT EXISTS TORNEI(
    IdTorneo int PRIMARY KEY,
    dataTorneo DATETIME NOT NULL,
    nomeTorneo char(20) NOT NULL,
    numeroSpettatori int NOT NULL,
    numeroPartecipanti int NOT NULL CHECK(numeroPartecipanti >= 2)
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO,
    FOREIGN KEY (IdFiera) REFERENCES FIERA,
);""")

########## Sorvegliano #############
sql.append(""" CREATE TABLE IF NOT EXISTS SORVEGLIANO(
    turnoDiLavoro DATETIME PRIMARY KEY,
    FOREIGN KEY (IdFiera) REFERENCES FIERA,
    FOREIGN KEY (CodiceBadge) REFERENCES DIEPENDENTI
);""")

########## Dipendenti #############
sql.append(""" CREATE TABLE IF NOT EXISTS DIPENDENTI(
    CodiceBadge int PRIMARY KEY,
    nome char(30) NOT NULL,
    cognome char(30) NOT NULL,
    dataDiNascita DATETIME NOT NULL,
    ruolo char(10) NOT NULL
);""")

########## Partecipanti #############
sql.append(""" CREATE TABLE IF NOT EXISTS PARTECIPANTI(
    codPartecipante int PRIMARY KEY,
    nome char(30) NOT NULL,
    cognome char(30) NOT NULL,
    dataDiNascita DATETIME NOT NULL,
    FOREIGN KEY (IdFiera) REFERENCES FIERA,
    FOREIGN KEY (CodiceBadge) REFERENCES DIPENDENTI
);""")

########## Padiglioni #############
sql.append(""" CREATE TABLE IF NOT EXISTS PADIGLIONI(
    codPadiglione int PRIMARY KEY,
    tipologia char(8),
    nomePadiglione char(20) NOT NULL,
    capienzaMassima int NOT NULL CHECK(capienzaMassima >= 1),
    numeroTavoli int NOT NULL CHECK(numeroTavoli >=1),
    FOREIGN KEY (IdFiera) REFERENCES FIERA
);""")

########## Partite non ufficiali #############
sql.append(""" CREATE TABLE IF NOT EXISTS PARTITE_NON_UFFICIALI(
    numeroPartite int NOT NULL,
    codGioco INT NOT NULL FOREIGN KEY REFERENCES GIOCHI_DA_TAVOLO,
    codPadiglione INT NOT NULL FOREIGN KEY REFERENCES PADIGLIONI,
    PRIMARY KEY (codGioco, codPadiglione)
);""")

########## Partite ufficiali #############
sql.append(""" CREATE TABLE IF NOT EXISTS PARTITE_UFFICIALI(
    IdMatch int PRIMARY KEY,
    dataPartita DATETIME NOT NULL,
    FOREIGN KEY (IdGiudice) REFERENCES DIPENDENTI,
    FOREIGN KEY (CodPadiglione) REFERENCES PADIGLIONI,
    FOREIGN KEY (IdTorneo) REFERENCES TORNEI
);""")

########## Vincitori #############
sql.append(""" CREATE TABLE IF NOT EXISTS VINCITORI(
    IdMatch INT NOT NULL FOREIGN KEY REFERENCES PARTITE_UFFICIALI,
    codConcorrente INT NOT NULL FOREIGN KEY REFERENCES CONCORRENTI,
    PRIMARY KEY (numeroMatch, codConcorrente)
);""")

########## Perdenti #############
sql.append(""" CREATE TABLE IF NOT EXISTS PERDENTI(
    IdMatch INT NOT NULL FOREIGN KEY REFERENCES PARTITE_UFFICIALI,
    codConcorrente INT NOT NULL FOREIGN KEY REFERENCES CONCORRENTI,
    PRIMARY KEY (numeroMatch, codConcorrente)
);""")

########## Concorrenti #############
sql.append(""" CREATE TABLE IF NOT EXISTS CONCORRENTI(
    codConcorrente int PRIMARY KEY,
    punteggio int
);""")

########## Possiedono #############
sql.append(""" CREATE TABLE IF NOT EXISTS POSSIEDONO(
    codGioco INT NOT NULL FOREIGN KEY REFERENCES GIOCHI_DA_TAVOLO,
    codCarta INT NOT NULL FOREIGN KEY REFERENCES CARTE,
    PRIMARY KEY (codGioco, codCarta)
);""")

########## Composti #############
sql.append(""" CREATE TABLE IF NOT EXISTS COMPOSTI(
    codMazzo INT NOT NULL FOREIGN KEY REFERENCES MAZZI,
    codCarta INT NOT NULL FOREIGN KEY REFERENCES CARTE,
    PRIMARY KEY (codGioco, codCarta)
);""")

########## Set carte bandite #############
sql.append(""" CREATE TABLE IF NOT EXISTS SET_CARTE_BANDITE(
    dataInizio INT NOT NULL FOREIGN KEY REFERENCES FORMATI,
    dataFine INT NOT NULL FOREIGN KEY REFERENCES FORMATI,
    codCarta INT NOT NULL FOREIGN KEY REFERENCES CARTE,
    PRIMARY KEY (dataInizio, dataFine, codCarta)
);""")

########## Carte #############
sql.append(""" CREATE TABLE IF NOT EXISTS CARTE(
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

########## Mazzi #############
sql.append(""" CREATE TABLE IF NOT EXISTS MAZZI(
    codMazzo int PRIMARY KEY,
    colore_clan char(20) NOT NULL,
    dimensioni int NOT NULL CHECK(dimensioni >= 0)
);""")

########## Dadi #############
sql.append(""" CREATE TABLE IF NOT EXISTS DADI(
    codDado int PRIMARY KEY,
    numFacce int NOT NULL CHECK(numfacce >= 4),
    colore char(20) NOT NULL,
    materiale char(50) NOT NULL
);""")

########## Pedine #############
sql.append(""" CREATE TABLE IF NOT EXISTS PEDINE(
    codPedina int PRIMARY KEY,
    colore char(20) NOT NULL,
    materiale char(50) NOT NULL
);""")

########## Materiali da gioco #############
sql.append(""" CREATE TABLE IF NOT EXISTS MATERIALI_DA_GIOCO(
  codMateriale int NOT NULL,
  codDado int, codCarta INT, codPedina int,
  primary key (codMateriale) --,
--    CHECK(EXISTS( (SELECT * FROM DADI WHERE codDado IS NOT NULL AND DADI.codDado=codMateriale) OR 
--               (select * from PEDINE where codPedina IS NOT NULL AND PEDINE.codPedina=codMateriale) OR 
--               (select * from CARTE where codCarta IS NOT NULL AND CARTE.codCarta=codMateriale))
,
     foreign key (codDado) references DADI,
     foreign key (codPedina) references PEDINE,
     foreign key (codCarta) references CARTE);""")


for k in sql:
    cur.execute(k)
    risultato=cur.fetchall()
con.commit()

