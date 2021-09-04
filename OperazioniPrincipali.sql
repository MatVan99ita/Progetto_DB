SELECT *
FROM 	TORNEI T, PARTITE_UFFICIALI PU, DIPENDENTI D, PADIGLIONI P, VINCITORI V, PERDENTI PE, CONCORRENTI C
WHERE T.IdTorneo = PU.IdTorneo AND
D.CodiceBadge = PU.IdGiudice AND
P.CodPadiglione = PU.CodPadiglione AND
PU.IdMatch = V.IdMatch AND
PU.IdMatch = PE.IdMatch AND
PE.codConcorrente = C. codConcorrente AND
V.codConcorrente = C. codConcorrente AND
T.dataTorneo=? 