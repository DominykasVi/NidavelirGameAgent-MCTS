from datetime import datetime
import traceback
import uuid
from game import Game
from card_deck import CardDeck
from bank import Bank
import math
from multiprocessing import Pool
import os
from typing import List
from game_state import GameState
from Players.mcts_player import MCTSPlayer
from Players.player import Player
from playing_board import PlayingBoard
from Players.random_player import RandomPlayer
import random
import numpy as np


class sol:
    def __init__(self, c_value, iterations):
        self.c_value = c_value
        self.iterations = iterations
        self.results = []
        self.fitness = 0
        # self.game_state = self.create_game_state()

    def run_game_threaded(self, param):
        try:
            c, iterations = param
            NUMBER_OF_PLAYERS = 5
            mode = 0
            card_deck = CardDeck(NUMBER_OF_PLAYERS, True)
            bank = Bank(NUMBER_OF_PLAYERS)
            playing_board = PlayingBoard(card_deck)
            players:List[Player] = []
            for i in range(NUMBER_OF_PLAYERS):
                players.append(RandomPlayer(i, None, bank))
                # print(f"Player {i} added")

            position = random.randint(0, NUMBER_OF_PLAYERS-1)
            players[position] = MCTSPlayer(position, None, bank, c_value=c, depth=iterations)

            game_state = GameState(playing_board=playing_board,
                                players=players,
                                card_deck=card_deck,
                                bank=bank, 
                                turn=0,
                                slot_index=0,
                                slots=[],
                                mode=mode)
            SA.give_players_crystals(game_state.players)

            game_simulation = Game(game_state, True)
            # print(f'Starting simulation on process {os.getpid()}')
            result = game_simulation.run_game()
            mcts = []
            for player in game_simulation.players:
                if player.player_type == 'MCTS':
                    mcts.append(player.index)
            result = result + [':'] + mcts
            return result
        except Exception as e:
            print(e)
            traceback.print_exc()
            return []

    def get_fitness(self):
        c = self.c_value
        iterations = self.iterations
        mcts_scores = []


        num_processes = os.cpu_count()
        with Pool(num_processes) as pool:
            # Create a list of tuples for each task
            parameters = (c, iterations)
            tasks = [(parameters) for i in range(10)]
            
            # Use pool.map to process tasks
            results = pool.map(self.run_game_threaded, tasks)


        result_strings = []
        for ls in results:
            res_str = ''
            for val in ls:
                res_str += f' {str(val)}'
            result_strings.append(res_str)


        for result in result_strings:
            if result == '':
                continue
            scores = [int(score) for score in result.split(':')[0].split(' ') if score != '']
            mcts_indexes = [int(number) for number in  result.split(':')[1].split(' ') if number != '']
            for idx in mcts_indexes:
                mcts_scores.append(scores[idx])
        
        if len(mcts_scores) == 0:
            self.fitness = 0
            return
        
        self.results.append(results)
        self.fitness = sum(mcts_scores)/len(mcts_scores)
        with open('Logs/TestResults/sa_c_iter/optimization.txt', 'a') as f:
            f.write(f'{self.fitness}-{self.c_value}-{self.iterations}\n')
            for res in result_strings:
                f.write(f'{res}\n')
            f.write('#---#\n')

        

class SA:
    def __init__(self, temperature, internal_n, external_n):
        # Set the parameters
        self.c = temperature
        self.L = internal_n
        self.n = external_n
        self.id = str(uuid.uuid4())
        # store the initial temperature value
        self.c0 = self.c
        self.solutions = []
        self.temperatures = [self.c0]
        self.run_start = datetime.now().strftime('%Y%m%d_%H%M%S')

        with open('Logs/TestResults/sa_c_iter/optimization.txt', 'a') as f:
            f.write(f'RUN {self.id}:{self.run_start}\n')


    def get_crystals(NUMBER_OF_PLAYERS):
        if NUMBER_OF_PLAYERS == 2:
            return [4, 5]
        if NUMBER_OF_PLAYERS == 3:
            return [3, 4, 5]
        if NUMBER_OF_PLAYERS == 4:
            return [2, 3, 4, 5]
        if NUMBER_OF_PLAYERS == 5:
            return [1, 2, 3, 4, 5]
        raise Exception("Not a valid number of players")

    def give_players_crystals(players):
        number_of_players = len(players)
        crystals = SA.get_crystals(number_of_players)
        for i in range(number_of_players):
            crystal = random.choice(crystals)
            crystals.remove(crystal)
            players[i].set_crystal(crystal)


    

    def create_neighbors(self,sol:sol):
        # p = np.random.normal(0, 0.25)
        x = sol.c_value
        y = sol.iterations

        n1 = (x+0.5,y)
        n2 = (x-0.5,y)
        n3 = (x,y+25)
        n4 = (x,y-25)
        n5 = (x+0.5,y+25)
        n6 = (x-0.5,y-25)
        n7 = (x+0.5,y-25)
        n8 = (x-0.5,y+25)
    
        return [n1,n2,n3,n4,n5,n6,n7,n8]
    
    def fit(self):
        
        # iterations = random.randint(50, 150)
        # c_value = np.random.normal(0.1, 2)
        c_value = 2.3
        iterations = 200
        # create a solution with the random route
        s = sol(c_value, iterations)
        s.get_fitness()
        
        self.solutions.append(s)
        neighbor_params = []
        # external loop
        for i in range(self.n):
            # internal loop
            # neighbor_params = self.create_neighbors(s)
            for j in range(self.L):
                
                # create the neighbor
                if len(neighbor_params) == 0:
                    neighbor_params = self.create_neighbors(s)
                
                neighbor_param = neighbor_params.pop()
                    # compare its fitness to the current solution's fitness
                c, iterations_param = neighbor_param
                print(f'test{i} {j} with c={c} and iter={iterations_param}')
                neighbor = sol(c, iterations_param)
                neighbor.get_fitness()

                if neighbor.fitness < s.fitness:   
                    s = neighbor
                    self.solutions.append(s)
                # initiate probabilistic acceptance
                else:
                    #if math.exp(-math.fabs(neighbor.fitness - s.fitness) / self.c) > random.random():
                    if math.exp((s.fitness - neighbor.fitness) / self.c) > random.random():
                        s = neighbor
                        self.solutions.append(s)
                    else:
                        self.solutions.append(s)
            # cooling schedule
            self.c = self.c0 * random.uniform(0.8, 0.9)
            self.temperatures.append(self.c)
        
        print('Training Finished!')


if '__main__' == __name__:
    t = 100
    L = 10
    n = 100


    
    sa = SA(t,L,n)
    sa.fit()