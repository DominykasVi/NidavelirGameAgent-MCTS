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