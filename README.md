# TODO
## Player
1. Make bet can be optimized with saving coins as dict. Or saving then in specific array slot.
2. Remove make bet assertion if I need more speed
## HumanPlayer
1. Fix make bet class
## MCTS
1. check if selection works correctly +-
2. Make simulation for take card+
3. Make simulation for increase coin+
4. Add limit when generating new nodes
5. Calculate statistics
6. Node visualizer+


## How do I test simulations?
1. check if right permutations are generated+
2. check game for a few turns+
3. check scores at the end of generation+
5. 
4. see which is chosen and why+

# Test bug that returns 2 items in player 0 and 0 inplayer 2
# Next card generations

# 2023-12-24 darbai
1. Run a lot of iterations and fix bugs (sekmadienis) DONE
2. Create simulation for next slots (Pirmadienis) DONE 
3. Simulaton for picking coins (???)
2. Algorithm to handle big search spaces (pirmadienis/treciadienis) STARTED
3. Optimizing the C value (Ketviratadienis)
4. Optimizing iteration count (Ketvirtadienis/Penktadienis)
5. Run tests with highest visited node selection (Penktadienis)
6. Statistinis testas ar taip pat performina


9 cars -> 3-9 seconds
12 cards -> 37 seconds

Weigted sampling, pvz 1000. Ir duoti kad kazkuri sample stipriau ziuretu.
Taip su kiekviena korta, ziureti bendra tasku skaiciu/wins. Kiek kinta.

Optimizuojami kintamieji:
iterations
contant for exploration
Random sampling size
Random sampling weights?

Nusistatyti max time, per kuri agentas turi atlikti ejima
Simulation of 501 took: 47.133838199981255

MCTS
Player 1 average score: 180.8
Player 2 average score: 197.0
Simulation time: 243.75574739999138

Random
Player 1 average score: 177.45
Player 2 average score: 180.9

200
Player 1 average score: 202.685
Player 2 average score: 177.435
Simulation time: 3404.554887999955
170-30

----

# Bakalauras
Todos:
1. Paleisti zaidima su 5 zmonem/4/3
2. Zaidimo teisingumo tikrinimas (log into files with Id)
2.1  - Test if coins are correct
2.2  - Test if cards are correct
2.3 - Run 500 random simulations/ when all correct, run 1000


3. Special korteliu pridejimas (isskyrus uline, ylud, thrud)

4. MCTS modification to work for more players
5. MCTS modifiction for special cards
6. MCTS tests agains random and itself, value optimizing?


 2. Tobulinama kursinio darbo metu parašyta skaitmeninė žaidimo versija, kad ja sugebėtų
 žaisti iki 5 žaidėjų (įskaitant). Planuojama atlikti iki kovo 22 d.
 Balandzio 1d. hero cards
 Balandzio 1d. MCTS pradzia
 Balandzio 2d. MCTS pabaiga
 Balandzio 4-7 MCTS rework
 Balandzio 7-9 test start
 Balandzio 10-12 test end
 Balandzio 12 susitkimas su destytoju

 3. MCTS algoritmo, sukurto kursinio darbo metu, tobulinimas, kad algoritmas sugebėtų
 veikti iki 5 žaidėjų (įskaitant) žaidime. Planuojama atlikti iki balandžio 5 d.
 4. Sukurto MCTS žaidėjo testavimas prieš atsitiktinius ir kitus MCTS žaidėjus. Tobulinamų
 sričių identifikavimas. Planuojama atlikti iki balandžio 12 d.
 5. MCTS agento optimizavimas pritaikant atrinktus metodus. Daroma prielaida, kad reikės
 modifikuoti MCTSalgoritmodalis, lygiagretinti MCTS algoritmą arba pritaikayti mašininį
 mokymąsi. Planuojama atlikti iki gegužės 3 d.
 3
6. Patobulintų MCTS agentų testavimas prieš atsitiktinius ir kitus MCTS žaidėjus. Rezultatų
 reikšmingumo įvertinimas ir rezultatų interpretacija. Planuojama atlikti iki Gegužės 17 d.
 7. Stilistinės baigiamojo darbo korekcijos. Planuojama atlikti iki gegužės 23 d.

 5. Tobulinimas ir preliminarus testai
 5. 1. Progressive widening
 5. 2. ONP ?
 5. 3. Lygiagretumas
 Backlog
 C reiksmes analize - sestadienis
1. Run su C reiksme/ieskoti kur fail
2. Progressive widening implementation
2. 5. Suzinoti kodel ta pati random reikme generuojama 
3. SA nakciai
4. Test to chekc how many child nodes are really created

 