SELECT T.IdTorneo, T.nomeTorneo, T.numeroSpettatori, T.numeroPartecipanti, T.codGioco, T.IdFiera, PU.IdMatch, PU.dataPartita, P.nomePadiglione
FROM TORNEI T, PARTITE_UFFICIALI PU, PADIGLIONI P, BATTAGLIE B, CONCORRENTI C
WHERE T.IdTorneo = PU.IdTorneo AND
P.CodPadiglione = PU.CodPadiglione AND
PU.IdMatch = B.IdMatch AND
B.codConcorrente = C. codConcorrente AND
T.dataTorneo="10/12/1990";

############################################################################

SELECT nomeGioco, descrizione, regolamento, SUM(numeroPartite) AS partiteTotali
FROM PARTITE_NON_UFFICIALI PNU, GIOCHI_DA_TAVOLO G
WHERE PNU.CodGioco = G.CodGioco
GROUP BY CodGioco
ORDER BY 4
LIMIT 1

############################################################################

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

############################################################################

SELECT v.codStand, SUM(prezzoTotale) AS guadagnoTotale,
(SELECT AVG(prezzoTotale) FROM vendite v1, ven_gioco vg WHERE v1.codStand = vg.codStand AND v1.codVendita = vg.codVendita AND v1.codStand = v.codStand) AS guadagnoMedioGiochiDaTavolo, 
(SELECT AVG(prezzoTotale) FROM vendite v1, ven_mat vm WHERE v1.codStand = vm.codStand AND v1.codVendita = vm.codVendita AND v1.codStand = v.codStand) AS guadagnoMedioMaterialiDaGioco
FROM vendite v
group by v.codStand

############################################################################

SELECT *
FROM SET_CARTE_BANDITE S, FORMATI F
WHERE F.dataInizio = S.dataInizio AND
F.dataFine = S.dataFine AND
dataInizio <= NOW() AND
dataFine > NOW()

############################################################################

SELECT M.codMazzo, colore_clan, C.codCarta, nome, tipo, descrizione, costoMana, attributo, attacco, difesa, effetto
FROM MAZZI M, CARTE C, COMPOSTI CO
WHERE CO.codiceMazzo = M.codiceMazzo AND
C.codCarta = CO.codCarta AND
codiceMazzo = ?
