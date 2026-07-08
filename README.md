# Progetto per Esame MC con Geant
Questo repository contiene una simulazione Monte Carlo sviluppata con Geant4 per studiare il deposito di dose di fasci adronici in un fantoccio d’acqua con geometria semplificata. Sono stati simulati fasci di protoni e ioni leggeri a energie terapeutiche e sono stati prodotti profili di dose in profondità (longitudinali) e laterali che sono stati analizzati successivamente con semplici script Python.
## Obiettivi
L'obiettivo del progetto è quello di simulare fasci di protoni e ioni in acqua e calcolandone la distribuzione di dose, ottenere profili di dise in profondità e profili laterali e confrontare particelle diverse.
Sono state considerate le seguenti particelle:
- Protoni 200 MeV;
- Elio	He	200 MeV/u
- Carbonio	C	200 MeV/u
- Ossigeno	O	200 MeV/u
- Neon	Ne	200 MeV/u
## Geometria di Simulazione
La simulazione utilizza geometria molto semplice che consiste in un fantoccio d’acqua di dimensioni:
40 cm × 10 cm × 10 cm
I vari fasci simulati si propagano lungo la direzione longitudinale del fantoccio (x) e la sorgente è posizionata in corrispondenza della faccia di ingresso del fantoccio a x = -20 cm rispetto al centro della geometria che si trova a x=0.
Questa configurazione permette di contenere il range delle particelle simulate e osservare il deposito di dose lungo la profondità.
## Voxellizazione
Per tracciare il profilo longitudinale di di rilascio della dose è stata utilizzata una voxelizzazione del fantoccio ad acqua pari a 1 mm × 100 mm × 100 mm, integrando la dose sulla sezione trasversale del fantoccio.
Per ottenere la distribuzione laterale della dose rispetto all'asse del fascio è stata utilizzata una voxellizazione 1 mm × 1 mm × 100 mm. 
 
