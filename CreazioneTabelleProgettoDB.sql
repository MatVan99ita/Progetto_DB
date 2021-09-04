
CREATE TABLE IF NOT EXISTS NAZIONI(
    IdNazione int PRIMARY KEY,
    nomeNazione char(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS CITTA(
    IdCittà int PRIMARY KEY,
    nomeCittà char(60) NOT NULL,
    IdNazione INT NOT NULL, 
  	FOREIGN KEY (IdNazione) REFERENCES NAZIONI
);

CREATE TABLE IF NOT EXISTS FIERE(
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
);

CREATE TABLE IF NOT EXISTS VENDITE(
    CodVendita int NOT NULL,
    prodotto char(20) NOT NULL,
    quantità int NOT NULL,
    dataVendita DATETIME NOT NULL,
    prezzoVendita MONEY NOT NULL,
    IdStand int NOT NULL,
    PRIMARY KEY (CodVendita, prodotto, quantità),
    FOREIGN KEY (IdStand) REFERENCES STANDS
);

CREATE TABLE IF NOT EXISTS STANDS(
    codStand int PRIMARY KEY,
    nome char(10) NOT NULL,
    IdFiera int NOT NULL,
    CodiceBadge int NOT NULL,
    FOREIGN KEY (IdFiera) REFERENCES FIERE,
    FOREIGN KEY (CodiceBadge) REFERENCES DIPENDENTI
);

CREATE TABLE IF NOT EXISTS CONTENUTI(
    quantitàGiochi int NOT NULL,
    codStand INT NOT NULL,
    codGioco INT NOT NULL,
    PRIMARY KEY(codStand, codGioco),
    FOREIGN KEY (codStand) REFERENCES STAND,
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO
);

CREATE TABLE IF NOT EXISTS IMMAGAZZINATI(
    quantitàMateriale int NOT NULL,
    codStand INT NOT NULL,
    codMateriale INT NOT NULL,
    PRIMARY KEY (codStand, codMateriale),
    FOREIGN KEY (codStand) REFERENCES STAND,
    FOREIGN KEY (codMateriale) REFERENCES MATERIALI_DA_GIOCO
);

CREATE TABLE IF NOT EXISTS GIOCHI_DA_TAVOLO(
    codGioco int PRIMARY KEY,
    nomeGioco char(30) NOT NULL,
    descrizione char(200) NOT NULL,
    regolamento char(300) NOT NULL
);

CREATE TABLE IF NOT EXISTS FORMATI(
    dataInizio DATETIME NOT NULL,
    dataFine DATETIME NOT NULL,
    listaCarteBandite varchar(1000) NOT NULL,
    codGioco int NOT NULL,
    PRIMARY KEY (dataInizio, dataFine),
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO
);

CREATE TABLE IF NOT EXISTS SITUATI(
    codGioco INT NOT NULL,
    codTerreno INT NOT NULL,
    PRIMARY KEY (codGioco, codTerreno),
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO,
    FOREIGN KEY (codTerreno) REFERENCES TERRENO
);

CREATE TABLE IF NOT EXISTS TERRENI(
    codTerreno int PRIMARY KEY,
    descrizione char(30)
);

CREATE TABLE IF NOT EXISTS TORNEI(
    IdTorneo int PRIMARY KEY,
    dataTorneo DATETIME NOT NULL,
    nomeTorneo char(20) NOT NULL,
    numeroSpettatori int NOT NULL,
    numeroPartecipanti int NOT NULL CHECK(numeroPartecipanti >= 2),
    codGioco int NOT NULL,
    IdFiera int NOT NULL,
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO,
    FOREIGN KEY (IdFiera) REFERENCES FIERA
);

CREATE TABLE IF NOT EXISTS SORVEGLIANO(
    turnoDiLavoro DATETIME PRIMARY KEY,
    IdFiera int NOT NULL,
    CodiceBadge int NOT NULL,
    FOREIGN KEY (IdFiera) REFERENCES FIERA,
    FOREIGN KEY (CodiceBadge) REFERENCES DIEPENDENTI
);

CREATE TABLE IF NOT EXISTS DIPENDENTI(
    CodiceBadge int PRIMARY KEY,
    nome char(30) NOT NULL,
    cognome char(30) NOT NULL,
    dataDiNascita DATETIME NOT NULL,
    ruolo char(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS PARTECIPANTI(
    codPartecipante int PRIMARY KEY,
    nome char(30) NOT NULL,
    cognome char(30) NOT NULL,
    dataDiNascita DATETIME NOT NULL,
    IdFiera int NOT NULL,
    CodiceBadge int NOT NULL,
    FOREIGN KEY (IdFiera) REFERENCES FIERA,
    FOREIGN KEY (CodiceBadge) REFERENCES DIPENDENTI
);

CREATE TABLE IF NOT EXISTS PADIGLIONI(
    codPadiglione int PRIMARY KEY,
    tipologia char(8),
    nomePadiglione char(20) NOT NULL,
    capienzaMassima int NOT NULL CHECK(capienzaMassima >= 1),
    numeroTavoli int NOT NULL CHECK(numeroTavoli >=1),
    IdFiera int NOT NULL,
    FOREIGN KEY (IdFiera) REFERENCES FIERA
);

CREATE TABLE IF NOT EXISTS PARTITE_NON_UFFICIALI(
    numeroPartite int NOT NULL,
    codGioco INT NOT NULL,
    codPadiglione INT NOT NULL,
    PRIMARY KEY (codGioco, codPadiglione),
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO,
    FOREIGN KEY (codPadiglione) REFERENCES PADIGLIONI
);

CREATE TABLE IF NOT EXISTS PARTITE_UFFICIALI(
    IdMatch int PRIMARY KEY,
    dataPartita DATETIME NOT NULL,
    IdGiudice int NOT NULL,
    codPadiglione int NOT NULL,
    IdTorneo int NOT NULL,
    FOREIGN KEY (IdGiudice) REFERENCES DIPENDENTI(CodiceBadge),
    FOREIGN KEY (CodPadiglione) REFERENCES PADIGLIONI,
    FOREIGN KEY (IdTorneo) REFERENCES TORNEI
);

CREATE TABLE IF NOT EXISTS VINCITORI(
    IdMatch INT NOT NULL,
    codConcorrente INT NOT NULL,
    PRIMARY KEY (IdMatch, codConcorrente),
    FOREIGN KEY (IdMatch) REFERENCES PARTITE_UFFICIALI,
    FOREIGN KEY (codConcorrente) REFERENCES CONCORRENTI
);

CREATE TABLE IF NOT EXISTS PERDENTI(
    IdMatch INT NOT NULL,
    codConcorrente INT NOT NULL,
    PRIMARY KEY (IdMatch, codConcorrente),
    FOREIGN KEY (IdMatch) REFERENCES PARTITE_UFFICIALI,
    FOREIGN KEY (codConcorrente) REFERENCES CONCORRENTI
);

CREATE TABLE IF NOT EXISTS CONCORRENTI(
    codConcorrente int PRIMARY KEY,
    punteggio int
);

CREATE TABLE IF NOT EXISTS POSSIEDONO(
    codGioco INT NOT NULL,
    codCarta INT NOT NULL,
    PRIMARY KEY (codGioco, codCarta),
    FOREIGN KEY (codGioco) REFERENCES GIOCHI_DA_TAVOLO,
    FOREIGN KEY (codCarta) REFERENCES CARTE
);

CREATE TABLE IF NOT EXISTS COMPOSTI(
    codMazzo INT NOT NULL,
    codCarta INT NOT NULL,
    PRIMARY KEY (codMazzo, codCarta),
    FOREIGN KEY (codMazzo) REFERENCES MAZZI,
    FOREIGN KEY (codCarta) REFERENCES CARTE
);

CREATE TABLE IF NOT EXISTS SET_CARTE_BANDITE(
    dataInizio INT NOT NULL,
    dataFine INT NOT NULL,
    codCarta INT NOT NULL,
    PRIMARY KEY (dataInizio, dataFine, codCarta)
    FOREIGN KEY (dataInizio) REFERENCES FORMATI,
    FOREIGN KEY (dataFine) REFERENCES FORMATI,
    FOREIGN KEY (codCarta) REFERENCES CARTE
);

CREATE TABLE IF NOT EXISTS CARTE(
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

CREATE TABLE IF NOT EXISTS MAZZI(
    codMazzo int PRIMARY KEY,
    colore_clan char(20) NOT NULL,
    dimensioni int NOT NULL CHECK(dimensioni >= 0)
);

CREATE TABLE IF NOT EXISTS DADI(
    codDado int PRIMARY KEY,
    numFacce int NOT NULL CHECK(numfacce >= 4),
    colore char(20) NOT NULL,
    materiale char(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS PEDINE(
    codPedina int PRIMARY KEY,
    colore char(20) NOT NULL,
    materiale char(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS MATERIALI_DA_GIOCO(
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
    foreign key (codCarta) references CARTE);