# Progetto per Esame MC con Geant
Questo repository contiene una simulazione Monte Carlo sviluppata con Geant4 per studiare il deposito di dose di fasci adronici in un fantoccio d’acqua con geometria semplificata. Sono stati simulati fasci di protoni e ioni leggeri a energie terapeutiche e sono stati prodotti profili di dose in profondità (longitudinali) e laterali che sono stati analizzati successivamente con semplici script Python.
Questo repository contiene una simulazione Monte Carlo sviluppata con Geant4 partendo dall'esempio _Radiobiology_ per studiare il deposito di dose di fasci adronici in un fantoccio d’acqua con geometria semplificata. Sono stati simulati fasci di protoni e ioni leggeri a energie terapeutiche e sono stati prodotti profili di dose in profondità (longitudinali) e laterali che sono stati analizzati successivamente con semplici script Python.
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
Solamente per una simulazione longitudinale per protoni da 200 MeV con 1M di eventi è stata usata una geometria più piccola pari a 30 cm x 6 cm x 6 cm. 
### Voxellizazione
Per tracciare il profilo longitudinale di di rilascio della dose è stata utilizzata una voxelizzazione del fantoccio ad acqua pari a 1 mm × 100 mm × 100 mm, integrando la dose sulla sezione trasversale del fantoccio.
Per ottenere la distribuzione laterale della dose rispetto all'asse del fascio è stata utilizzata una voxellizazione 1 mm × 1 mm × 100 mm. 
## Simulazione 
La simulazione è stata organizzata in due fasi.
### 1. Test a bassa statistica
Prima di lanciare le simulazioni lunghe, sono stati fatti dei test con file macro da 10.000 eventi per valutare:
- correttezza della geometria;
- corretta generazione delle particelle;
- produzione dei file di output;
- corretto funzionamento degli script Python per la visualizzazione dei risultati;
- stimare il tempo richiesto per la simulazione.
### 2. Simulazioni finali con più eventi
Dopo i test, sono state effettuate simulazioni da 100.000 eventi per tutte le particelle con la geometria 40 cm x 10 cm x 10 cm sia per profili longitudinali che trasversali e una simulazione da 1M di eventi per protoni da 200 MeV con una geometria più piccola pari a 30 cm x 6 cm x 6 cm al fine di contenere i tempi richiesti per la simulazione. 
Queste simulazioni permettono di ottenere curve meno rumorose che possono essere confrontate con le curve ottenute con le simulazioni a minore statistica di test.
Sono stati anche confrontate le distribuzioni di dose sia in profondità che laterali dei vari ioni simulati. 
## Analisi dei risultati
Gli output generati dalle macro di Geant4 vengono analizzati e graficati con semplici script Python contenuti nella cartella analysis/.
Gli script principali sono:
- plot_depth_dose.py per i profili di dose longitudinali;
- plot_lateral_profiles.py per i profili laterali;
- plot_all_particles.py per il confronto tra particelle.


# README RADIOBIOLOGY

\page Exampleradiobiology Example radiobiology

\author L Pandola, D Chiappara, GAP Cirrone, G Petringa, A Sciuto, S Fattori; - INFN LNS (Italy) \n
 
Radiobiology is an application realized for dosimetric and radiobiological applications of proton and ion beams. 
Specific tools were built to evaluate primaries and secondary energy spectra and a set of classes, dedicated to 
the computation of biological, as LET (Linear Energy Transfer), RBE (Relative Biological Effectiveness), Survival 
Fraction, and physical (as dose and fluence) quantities were implemented.

## 1- GEOMETRY DEFINITION
 
The physical and dosimetric quantities are calculated in the water tank by scoring every quantity in each of the 
slices, representing a customizable (in terms of dimensions and materials) volume that can be voxelized depending 
on the user's needs.

In the proposed example, the “default” water tank represents a phantom typically used in the clinical hadrontherapy 
practice, to reconstruct the dose profile distributions in water.
The phantom has a standard dimension of 4 x 4 x 4 cm and was sectioned into 0.2 x 40 x 40 mm slices (See Figure 1). 
The voxel dimensions can be user defined and can vary from 1um to 1 mm
The source is positioned on one of the faces of the box

The default macro uses the default geometry configuration mentioned above with a simple run of 100k protons with a 
Gaussian energy distribution with a mean of 62 MeV and a standard deviation of 0.65 MeV
The visualize.mac just creates a teest geometry and opens visualization

## 2- PHYSICS LIST

In Radiobiology it is possible to activate three physics lists that are those already recommended for medical physics
applications and that cover all the physics processes needed for a correct simulation in this field.

The electromagnetic interactions are modeled using the G4EmStandardPhysics_option4 constructor, which uses a 
condensed history algorithm based on the Beth-Bloch energy loss formula. This physics constructor was created for 
applications requiring high accuracy in electron, hadron, and ion tracking. It contains the most accurate standard 
and low-energy models and is recommended for simulations focused on medical physics applications.
The hadronic interactions are simulated using models implemented in the QGSP BIC and QGSP BIC HP constructors, 
which employ Geant4 native preequilibrium and de-excitation models as low energy stages of the Binary Cascade model 
for protons, neutrons, and ions. The QGSP BIC HP constructor uses, in addition, the high precision neutron package 
(ParticleHP) to transport neutrons and light-charged particles with energies from 20 MeV down to thermal energy.

Production cuts for secondary generation are an important element in any MC simulation. It has a significant impact 
on energy deposition, particularly when small quantities are examined. The production cut in Geant4 is a distance 
(given in units of length), and secondary particles (electrons, positrons, gammas, and secondary protons) are only 
monitored if their expected range in that medium is greater than the imposed cut. Otherwise, secondary energy is 
not tracked and is deposited in the secondary production position. The cut for this example is achieved through 
the standard Geant4 implementation.
```
 /run/setCutForAGivenParticle e- 0.1 mm
 /run/setCutForAGivenParticle e+ 0.1 mm
 /run/setCutForAGivenParticle proton 0.1 mm
```

## 3- LET CALCULATION

Radiobiology simulates and calculates the averaged LET-dose and LET-track fully accounting for the contribution of 
secondary particles generated in the target fragmentation 
Dependencies as respect to the transport parameters adopted during the Monte Carlo simulations as the production cut 
of secondaries particles, voxel size and the maximum steps length are minimized in the LET calculation.
At run time, data needed to calculate LET are collected. At the end of simulation, LET mean values are calculated 
and stored into a file.

The Let.out file will be produced at the end of a run, where you can
find the dose and track average LET for each tracked particles (both primary and
secondary ones) and the total mean LET.

The file is structured as follows:
     - The first three columns contain the voxel indexes (first index "i" refers to the beam direction);
     - The fourth and fifth columns contain respectively total mean dose LET (LDT) and total mean track LET (LTT)
     - The rest of columns contain LET Dose and Track for each single ion (whose name is in the top row of the file).

## 4- RBE and Survival calculation

A method was developed to assess the biological damages produced by proton and ion beams in terms of survival 
fraction curves, i.e of the number of cells able to survive after the irradiation at different dose. The approach 
is based on the combined use of Monte Carlo Geant4 simulations (to calculate the doses deposited and the energy 
spectra of particles interacting with cells) and of the Survival analytical code (Manganaro L, Russo G, et al. 
Survival: a simulation toolkit introducing a modular approach for radiobiological evaluations in ion beam therapy. 
Phys. Med. Biol. 2018;63(8). 08–01).
The Monte Carlo simulations permit the calculation of the Edep and Ekin distributions that, coupled with the 
radiobiological response model, allow the final and calculation of a survival curve.
The kinetic energy and the LET value of any primary ion and of the secondaries generated in each slice of the 
simulated water phantom are retrieved at each simulation step. The corresponding values of αi and βi, for each 
specific ion i with a kinetic energy Ei and a released dose Di, are then calculated by direct linear interpolation 
of the Look-up-tables provided by the Survival analytical code.
(G.Petringa et al., Physica Medica 58 (2019) 72–80)

The AlphaAndBeta.out and RBE.out files are produced at the end of the run.
AlphaAndBeta.out contains the average alpha (first column) and beta (second column) parameters calculated for each 
slice (third column).

RBE.out contains the following quantities:
    - Dose (Gy): the physical dose;
    - ln(S): the natural log of the Survival Fraction;
    - Survival Fraction;
    - DoseB (Gy): the biological dose;
    - RBE: relative biological effectiveness;
    - depth (slice): n. of the slice;
