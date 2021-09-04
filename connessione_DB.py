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
    IdNazione INT NOT NULL, 
  	FOREIGN KEY (IdNazione) REFERENCES NAZIONI
);""")

########## Nazione #############
sql.append(""" CREATE TABLE IF NOT EXISTS FIERE(
    IdFiera int PRIMARY KEY,
    via char(10),
    numeroCivico int,
    nomeFiera char(20) NOT NULL,
    dataInzioFiera DATETIME NOT NULL,
    dataFineFiera DATETIME NOT NULL,
    IdNazione int NOT NULL,
    IdCittà int NOT NULL,
    FOREIGN KEY (IdNazione) references CITTA,
    FOREIGN KEY (IdCittà) references CITTA
);""")

########## Vendite #############
sql.append(""" CREATE TABLE IF NOT EXISTS VENDITE(
    CodVendita int NOT NULL,
    prodotto char(20) NOT NULL,
    quantità int NOT NULL,
    dataVendita DATETIME NOT NULL,
    prezzoVendita MONEY NOT NULL,
    IdStand int NOT NULL,
    PRIMARY KEY (CodVendita, prodotto, quantità),
    FOREIGN KEY (IdStand) REFERENCES STANDS
);""")

########## Stands #############
sql.append(""" CREATE TABLE IF NOT EXISTS STANDS(
    codStand int PRIMARY KEY,
    nome char(10) NOT NULL,
    IdFiera int NOT NULL,
    CodiceBadge int NOT NULL,
    FOREIGN KEY (IdFiera) REFERENCES FIERE,
    FOREIGN KEY (CodiceBadge) REFERENCES DIPENDENTI
);""")

########## Contenuti #############
sql.append(""" CREATE TABLE IF NOT EXISTS CONTENUTI(
    quantitàGiochi int NOT NULL,
    codStand INT NOT NULL,
    codGioco INT NOT NULL,
    PRIMARY KEY(codStand, codGioco),
    FOREIGN KEY (codStand) REFERENCES STAND,
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO
);""")

########## Immagazzinati #############
sql.append(""" CREATE TABLE IF NOT EXISTS IMMAGAZZINATI(
    quantitàMateriale int NOT NULL,
    codStand INT NOT NULL,
    codMateriale INT NOT NULL,
    PRIMARY KEY (codStand, codMateriale),
    FOREIGN KEY (codStand) REFERENCES STAND,
    FOREIGN KEY (codMateriale) REFERENCES MATERIALI_DA_GIOCO
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
    codGioco int NOT NULL,
    PRIMARY KEY (dataInizio, dataFine),
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO
);""")

########## Situati #############
sql.append(""" CREATE TABLE IF NOT EXISTS SITUATI(
    codGioco INT NOT NULL,
    codTerreno INT NOT NULL,
    PRIMARY KEY (codGioco, codTerreno),
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO,
    FOREIGN KEY (codTerreno) REFERENCES TERRENO
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
    numeroPartecipanti int NOT NULL CHECK(numeroPartecipanti >= 2),
    codGioco int NOT NULL,
    IdFiera int NOT NULL,
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO,
    FOREIGN KEY (IdFiera) REFERENCES FIERA
);""")

########## Sorvegliano #############
sql.append(""" CREATE TABLE IF NOT EXISTS SORVEGLIANO(
    turnoDiLavoro DATETIME PRIMARY KEY,
    IdFiera int NOT NULL,
    CodiceBadge int NOT NULL,
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
    IdFiera int NOT NULL,
    CodiceBadge int NOT NULL,
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
    IdFiera int NOT NULL,
    FOREIGN KEY (IdFiera) REFERENCES FIERA
);""")

########## Partite non ufficiali #############
sql.append(""" CREATE TABLE IF NOT EXISTS PARTITE_NON_UFFICIALI(
    numeroPartite int NOT NULL,
    codGioco INT NOT NULL,
    codPadiglione INT NOT NULL,
    PRIMARY KEY (codGioco, codPadiglione),
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO,
    FOREIGN KEY (codPadiglione) REFERENCES PADIGLIONI
);""")

########## Partite ufficiali #############
sql.append(""" CREATE TABLE IF NOT EXISTS PARTITE_UFFICIALI(
    IdMatch int PRIMARY KEY,
    dataPartita DATETIME NOT NULL,
    IdGiudice int NOT NULL,
    codPadiglione int NOT NULL,
    IdTorneo int NOT NULL,
    FOREIGN KEY (IdGiudice) REFERENCES DIPENDENTI,
    FOREIGN KEY (CodPadiglione) REFERENCES PADIGLIONI,
    FOREIGN KEY (IdTorneo) REFERENCES TORNEI
);""")

########## Vincitori #############
sql.append(""" CREATE TABLE IF NOT EXISTS VINCITORI(
    IdMatch INT NOT NULL,
    codConcorrente INT NOT NULL,
    PRIMARY KEY (IdMatch, codConcorrente),
    FOREIGN KEY (IdMatch) REFERENCES PARTITE_UFFICIALI,
    FOREIGN KEY (codConcorrente) REFERENCES CONCORRENTI
);""")

########## Perdenti #############
sql.append(""" CREATE TABLE IF NOT EXISTS PERDENTI(
    IdMatch INT NOT NULL,
    codConcorrente INT NOT NULL,
    PRIMARY KEY (IdMatch, codConcorrente),
    FOREIGN KEY (IdMatch) REFERENCES PARTITE_UFFICIALI,
    FOREIGN KEY (codConcorrente) REFERENCES CONCORRENTI
);""")

########## Concorrenti #############
sql.append(""" CREATE TABLE IF NOT EXISTS CONCORRENTI(
    codConcorrente int PRIMARY KEY,
    punteggio int
);""")

########## Possiedono #############
sql.append(""" CREATE TABLE IF NOT EXISTS POSSIEDONO(
    codGioco INT NOT NULL,
    codCarta INT NOT NULL,
    PRIMARY KEY (codGioco, codCarta),
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO,
    FOREIGN KEY (codCarta) REFERENCES CARTE
);""")

########## Composti #############
sql.append(""" CREATE TABLE IF NOT EXISTS COMPOSTI(
    codMazzo INT NOT NULL,
    codCarta INT NOT NULL,
    PRIMARY KEY (codMazzo, codCarta),
    FOREIGN KEY (codMazzo) REFERENCES MAZZI,
    FOREIGN KEY (codCarta) REFERENCES CARTE
);""")

########## Set di carte bandite #############
sql.append(""" CREATE TABLE IF NOT EXISTS SET_CARTE_BANDITE(
    dataInizio INT NOT NULL,
    dataFine INT NOT NULL,
    codCarta INT NOT NULL,
    PRIMARY KEY (dataInizio, dataFine, codCarta)
    FOREIGN KEY (dataInizio) REFERENCES FORMATI,
    FOREIGN KEY (dataFine) REFERENCES FORMATI,
    FOREIGN KEY (codCarta) REFERENCES CARTE
);""")

########## Carte #############
sql.append(""" CREATE TABLE IF NOT EXISTS CARTE(
    codCarta int PRIMARY KEY,
    nome char(50) NOT NULL,
    tipo char(10) NOT NULL CHECK(tipo = 'Mostro' OR tipo='Magia' OR tipo='Trappola'),
    descrizione char(100),
    costoMana int,
    attributo char(10),
    attacco int,
    difesa int,
    effetto char(20) NOT NULL
);
""")

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
  codDado int, 
  codCarta INT, 
  codPedina int,
  primary key (codMateriale) --,
--    CHECK(EXISTS( (SELECT * FROM DADI WHERE codDado IS NOT NULL AND DADI.codDado=codMateriale) OR 
--               (select * from PEDINE where codPedina IS NOT NULL AND PEDINE.codPedina=codMateriale) OR 
--               (select * from CARTE where codCarta IS NOT NULL AND CARTE.codCarta=codMateriale))
,
    foreign key (codDado) references DADI,
    foreign key (codPedina) references PEDINE,
    foreign key (codCarta) references CARTE
);""")

##########################################################################################################

####################################### INSERIMENTO RECORD ################################################

sql.append(""" INSERT INTO NAZIONI(nomeNazione) 
VALUES(?),(?)
;""")

sql.append(""" INSERT INTO CITTA(nomeCittà, IdNazione) 
VALUES(?, ?)
;""")

sql.append(""" INSERT INTO FIERE(via, numeroCivico, nomeFiera, dataInzioFiera, dataFineFiera, IdNazione, IdCittà) 
VALUES(?, ?, ?, ?, ?, ?, ?)
;""")

sql.append(""" INSERT INTO VENDITE(CodVendita, prodotto, quantità, dataVendita, prezzoVendita, IdStand)
VALUES(?, ?, ?, ?, ?, ?)
;""")

sql.append(""" INSERT INTO STANDS(nome, IdFiera, CodiceBadge) 
VALUES(?, ?, ?)
;""")

sql.append(""" INSERT INTO CONTENUTI(quantitàGiochi, codStand, codGioco)
VALUES(?, ?, ?)
;""")

sql.append(""" INSERT INTO IMMAGAZZINATI(quantitàMateriale, codStand, codMateriale)
VALUES(?, ?, ?)
;""")

sql.append(""" INSERT INTO GIOCHI_DA_TAVOLO(nomeGioco, descrizione, regolamento)
VALUES(?, ?, ?)
;""")

sql.append(""" INSERT INTO FORMATI(dataInizio, dataFine, listaCarteBandite, codGioco)
VALUES(?, ?, ?, ?)
;""")

sql.append(""" INSERT INTO SITUATI(codGioco, codTerreno)
VALUES(?, ?)
;""")

sql.append(""" INSERT INTO TERRENI(codTerreno, descrizione)
VALUES(?, ?)
;""")

sql.append(""" INSERT INTO TORNEI(dataTorneo, nomeTorneo, numeroSpettatori, numeroPartecipanti, codGioco, IdFiera)
VALUES(?, ?, ?, ?, ?, ?)
;""")

sql.append(""" INSERT INTO SORVEGLIANO(turnoDiLavoro, IdFiera, CodiceBadge)
VALUES(?, ?, ?)
;""")

sql.append(""" INSERT INTO DIPENDENTI(nome, cognome, dataDiNascita, ruolo)
VALUES(?, ?, ?, ?)
;""")

sql.append(""" INSERT INTO PARTECIPANTI(nome, cognome, dataDiNascita, IdFiera, CodiceBadge)
VALUES(?, ?, ?, ?, ?)
;""")

sql.append(""" INSERT INTO PADIGLIIONI(tipologia, nomePadiglione, capienzaMassima, numeroTavoli, IdFiera)
VALUES(?, ?, ?, ?, ?)
;""")

sql.append(""" INSERT INTO PARTITE_NON_UFFICIALI(numeroPartite, codGioco, codPadiglione)
VALUES(?, ?, ?)
;""")

sql.append(""" INSERT INTO PARTITE_UFFICIALI(dataPartita, IdGiudice, codPadiglione, IdTorneo)
VALUES(?, ?, ?, ?)
;""")

sql.append(""" INSERT INTO VINCITORI(IdMatch, codConcorrente)
VALUES(?, ?)
;""")

sql.append(""" INSERT INTO PERDENTI(IdMatch, codConcorrente)
VALUES(?, ?)
;""")

sql.append(""" INSERT INTO CONCORRENTI(punteggio)
VALUES(?)
;""")

sql.append(""" INSERT INTO POSSIEDONO(codGioco, codCarta)
VALUES(?, ?)
;""")

sql.append(""" INSERT INTO COMPOSTI(codMazzo, codCarta)
VALUES(?, ?)
;""")

sql.append(""" INSERT INTO SET_CARTE_BANDITE(dataInizio, dataFine, codCarta)
VALUES(?, ?, ?)
;""")

sql.append(""" INSERT INTO CARTE(nome, tipo, descrizione, costoMana, attributo, attacco, difesa, effetto)
VALUES(?, ?, ?, ?, ?, ?, ?, ?)
;
""")

sql.append(""" INSERT INTO MAZZI(colore_clan, dimensioni)
VALUES(?, ?)
;""")

sql.append(""" INSERT INTO DADI(numFacce, colore, materiale)
VALUES(?, ?, ?)
;""")

sql.append(""" INSERT INTO PEDINE(colore, materiale)
VALUES(?, ?)
;""")

sql.append(""" INSERT INTO MATERIALI_DA_GIOCO(codMateriale, codDado, codCarta, codPedina)
VALUES(?, ?, ?, ?)
;""")

##########################################################################################################


for k in sql:
    cur.execute(k)
    risultato=cur.fetchall()
con.commit()

