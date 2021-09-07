
3) Lista partite effettuate in un torneo svolto in una data specificata           (User)
SELECT T.IdTorneo, T.nomeTorneo, T.numeroSpettatori, T.numeroPartecipanti, T.codGioco, T.IdFiera, PU.IdMatch, PU.dataPartita, P.nomePadiglione
FROM TORNEI T, PARTITE_UFFICIALI PU, PADIGLIONI P, BATTAGLIE B, CONCORRENTI C
WHERE T.IdTorneo = PU.IdTorneo AND
P.CodPadiglione = PU.CodPadiglione AND
PU.IdMatch = B.IdMatch AND
B.codConcorrente = C. codConcorrente AND
T.dataTorneo="10/12/1990";










3) Gioco da tavolo con più partite non ufficiali    		      		           (Admin)
SELECT TOP 1 WITH TIES nomeGioco, descrizione, regolamento, SUM(numeroPartite) AS partiteTotali
FROM PARTITE NON UFFICIALI PNU, GIOCHI DA TAVOLO G
WHERE PNU.CodGioco = G.CodGioco
GROUP BY CodGioco
ORDER BY 4

4) Dato un concorrente ritornare il punteggio totale, numero vittorie e numero sconfitte per ogni torneo in cui ha partecipato 					    (User)
SELECT t.IdTorneo, nome, SUM(punteggio),
(SELECT COUNT(esito) FROM battaglie b, partite_ufficiali pu1 WHERE pu1.IdMatch = b.IdMatch AND esito = "vittoria" AND Idcon=? AND pu1.IdTorneo = t.IdTorneo) AS numVittorie,
(SELECT COUNT(esito) FROM battaglie b ,partite_ufficiali pu1 WHERE pu1.IdMatch = b.IdMatch AND esito = "sconfitta" AND Idcon=? AND pu1.IdTorneo = t.IdTorneo) AS numSconfitte
FROM giochi_da_tavolo g, tornei t, concorrenti c, partite_ufficiali pu,battaglie b
WHERE t.CodGioco = g.CodGioco AND
pu.IdTorneo = t.IdTorneo AND
pu.IdMatch = b.IdMatch AND 
b.Idcon = c.Idcon AND 
c.Idcon=?
GROUP BY t.IdTorneo;

5)Per ogni stand trovare il guadagno totale e il guadagno medio per i giochi da tavolo e i materiali di gioco                                                                  			                (Admin)
SELECT v.codStand, SUM(prezzoTotale) AS guadagnoTotale,
(SELECT AVG(prezzoTotale) FROM vendite v1, ven_gioco vg WHERE v1.codStand = vg.codStand AND v1.codVendita = vg.codVendita AND v1.codStand = v.codStand) AS guadagnoMedioGiochiDaTavolo, 
(SELECT AVG(prezzoTotale) FROM vendite v1, ven_mat vm WHERE v1.codStand = vm.codStand AND v1.codVendita = vm.codVendita AND v1.codStand = v.codStand) AS guadagnoMedioMaterialiDaGioco
FROM vendite v
group by v.codStand


7) Registrazione vendita per uno stand 				       		 (Admin)
INSERT INTO VENDITE (CodVendita, dataVendita, CodStand, prezzoTotale) VALUES (?, ?, ?, ?, ?)
A seconda del tipo di prodotto bisogna:
INSERT INTO VEN_GIOCHI (CodVendita, CodGioco, CodStand, quantitàGiochiSelezionati) VALUES (?, ?, ?, ?)
UPDATE CONTENUTI SET quantitàGiochi = quantitàGiochi - quantitàGiochiSelezionati WHERE 
CodGioco = ? AND CodStand = ?
Oppure:
INSERT INTO VEN_MATERIALI (CodVendita, CodMateriale, CodStand, quantitàMaterialiSelezionati) VALUES (?, ?, ?, ?)
UPDATE IMMAGAZZINATI SET quantitàMateriali = quantitàMateriali - quantitàMaterialiSelezionati  WHERE CodGioco = ? AND CodStand = ?

8) Lista delle carte bandite dell’attuale formato 	                      			    (User)
SELECT *
FROM SET_CARTE_BANDITE S, FORMATI F
WHERE F.dataInizio = S.dataInizio AND
F.dataFine = S.dataFine AND
dataInizio <= NOW() AND
dataFine > NOW()

9) Inserimento di un nuovo formato 			                        			  (Admin)
INSERT INTO FORMATI(dataInizio, dataFine, CodGioco) VALUES (?, ?, ?)
INSERT INTO SET_CARTE_BANDITE(codCarta, dataInizio, dataFine) VALUES (?, ?, ?)


10) Dato un mazzo ritornare le carte di cui è composto              		 (User)
SELECT M.codMazzo, colore_clan, C.codCarta, nome, tipo, descrizione, costoMana, attributo, attacco, difesa, effetto
FROM MAZZI M, CARTE C, COMPOSTI CO
WHERE CO.codiceMazzo = M.codiceMazzo AND
C.codCarta = CO.codCarta AND
codiceMazzo = ?

