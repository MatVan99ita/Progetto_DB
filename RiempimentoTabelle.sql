INSERT INTO NAZIONI(nomeNazione) 
VALUES(?);

INSERT INTO CITTA(nomeCittà, IdNazione) 
VALUES(?, ?);

INSERT INTO FIERE(via, numeroCivico, nomeFiera, dataInzioFiera, dataFineFiera, IdNazione, IdCittà) 
VALUES(?, ?, ?, ?, ?, ?, ?);

INSERT INTO VENDITE(CodVendita, prodotto, quantità, dataVendita, prezzoVendita, IdStand)
VALUES(?, ?, ?, ?, ?, ?);

INSERT INTO STANDS(nome, IdFiera, CodiceBadge) 
VALUES(?, ?, ?);

INSERT INTO CONTENUTI(quantitàGiochi, codStand, codGioco)
VALUES(?, ?, ?);

INSERT INTO IMMAGAZZINATI(quantitàMateriale, codStand, codMateriale)
VALUES(?, ?, ?);

INSERT INTO GIOCHI_DA_TAVOLO(nomeGioco, descrizione, regolamento)
VALUES(?, ?, ?);

INSERT INTO FORMATI(dataInizio, dataFine, listaCarteBandite, codGioco)
VALUES(?, ?, ?, ?);

INSERT INTO SITUATI(codGioco, codTerreno)
VALUES(?, ?);

INSERT INTO TERRENI(codTerreno, descrizione)
VALUES(?, ?);

INSERT INTO TORNEI(dataTorneo, nomeTorneo, numeroSpettatori, numeroPartecipanti, codGioco, IdFiera)
VALUES(?, ?, ?, ?, ?, ?);

INSERT INTO SORVEGLIANO(turnoDiLavoro, IdFiera, CodiceBadge)
VALUES(?, ?, ?);

INSERT INTO DIPENDENTI(nome, cognome, dataDiNascita, ruolo)
VALUES(?, ?, ?, ?);

INSERT INTO PARTECIPANTI(nome, cognome, dataDiNascita, IdFiera, CodiceBadge)
VALUES(?, ?, ?, ?, ?);

INSERT INTO PADIGLIIONI(tipologia, nomePadiglione, capienzaMassima, numeroTavoli, IdFiera)
VALUES(?, ?, ?, ?, ?);

INSERT INTO PARTITE_NON_UFFICIALI(numeroPartite, codGioco, codPadiglione)
VALUES(?, ?, ?);

INSERT INTO PARTITE_UFFICIALI(dataPartita, IdGiudice, codPadiglione, IdTorneo)
VALUES(?, ?, ?, ?);

INSERT INTO VINCITORI(IdMatch, codConcorrente)
VALUES(?, ?);

INSERT INTO PERDENTI(IdMatch, codConcorrente)
VALUES(?, ?);

INSERT INTO CONCORRENTI(punteggio)
VALUES(?);

INSERT INTO POSSIEDONO(codGioco, codCarta)
VALUES(?, ?);

INSERT INTO COMPOSTI(codMazzo, codCarta)
VALUES(?, ?);

INSERT INTO SET_CARTE_BANDITE(dataInizio, dataFine, codCarta)
VALUES(?, ?, ?);

INSERT INTO CARTE(nome, tipo, descrizione, costoMana, attributo, attacco, difesa, effetto)
VALUES(?, ?, ?, ?, ?, ?, ?, ?);

INSERT INTO MAZZI(colore_clan, dimensioni)
VALUES(?, ?);

INSERT INTO DADI(numFacce, colore, materiale)
VALUES(?, ?, ?);

INSERT INTO PEDINE(colore, materiale)
VALUES(?, ?);

INSERT INTO MATERIALI_DA_GIOCO(codMateriale, codDado, codCarta, codPedina)
VALUES(?, ?, ?, ?);
