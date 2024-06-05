
from copy import deepcopy
import json
import math
import os
import random
from typing import List
from bank import Bank
from card import Card
from card_deck import CardDeck
from coin import Coin
from game import Game
from Players.player import Player
from game_state import GameState
from Players.mcts_player import MCTSPlayer
from playing_board import PlayingBoard
from Players.random_player import RandomPlayer
import time
from timeit import default_timer as timer
import matplotlib.pyplot as plt
from threading import Thread
from multiprocessing import Pool, Process, Manager
import time
from datetime import datetime
import psutil
from time import sleep
import signal
import sys
import time

GLOBAL_DEPTH = 500 #Tested
GLOBAL_C_VALUE = 4 #Tested
NUMBER_OF_PLAYERS = 2
C_VALUE_WL = 0.6 #Tested
GLOBAL_MAX_NODES = 120 #Tested

# def run_game_threaded(game_simulation:Game, results, index):
def run_game_threaded(index_function_parameter):
    try:
        # print(f"Starting process {os.getpid()}") 
        index, function, parameters = index_function_parameter 
        game_simulation, players = function(parameters)
        print(f"{index}: Started {game_simulation.game_id}")

        with open(f'Logs/StrategyAnalysis/{game_simulation.game_id}.txt', 'a') as f:
            f.write(json.dumps(players))
        game_simulation.write_path = 'Logs/StrategyAnalysis'
        result = game_simulation.run_game(main=True)
 
        print(f"{index}: End {game_simulation.game_id}")
        return (game_simulation.game_id, result)
    except Exception as e:
        time = datetime.now().strftime('%Y%m%d_%H%M%S')
        print(e)
        with open(f'Logs/Failures/{time}.txt', 'w') as f:
            f.write(str(e))


def debug_mcts(NUMBER_OF_PLAYERS, number_of_mcts, c_value, iterations
               , pw_param=None):
    # print(datetime.now())
    # print(datetime.now().timestamp())
    # print(os.getpid())


    card_deck = CardDeck(NUMBER_OF_PLAYERS, True)
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    for i in range(0, NUMBER_OF_PLAYERS):
        players.append(RandomPlayer(i, None, bank))

    unique_seed = int.from_bytes(os.urandom(8), 'big')

    random.seed(unique_seed)
    random_indexes = []
    for _ in range(number_of_mcts):
        random_index = -1
        while random_index == -1:
            random_index = random.randint(0, NUMBER_OF_PLAYERS-1)
            if random_index in random_indexes:
                random_index = -1
            else:
                if pw_param is not None:
                    players[random_index] = MCTSPlayer(random_index, None, bank, c_value, iterations, 'MCTS', pw=True, c=pw_param['c'], alpha=pw_param['alpha'])
                else:
                    players[random_index] = MCTSPlayer(random_index, None, bank, c_value, iterations, 'MCTS')
                random_indexes.append(random_index)
    
    
    game_state = GameState(playing_board=playing_board,
                        players=players,
                        card_deck=card_deck,
                        bank=bank, 
                        turn=0,
                        slot_index=0,
                        slots=[],
                        mode=0)
    # print(random_indexes)
    give_players_crystals(game_state.players)
    game_simulation = Game(game_state, True)
    return game_simulation

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
    crystals = get_crystals(number_of_players)
    for i in range(number_of_players):
        crystal = random.choice(crystals)
        crystals.remove(crystal)
        players[i].set_crystal(crystal)

#new
def save_scores(results, save_name, data):
    check_and_create_folder(save_name)

    player_names = []
    for player in data:
        inserted = False
        id = 0
        while not inserted:
            if f"{player['type']}{id}" in player_names:
                id += 1
            else:
                player_names.append(f"{player['type']}{id}")
                inserted = True

    res_json = []
    for result in results:
        for idx, player_name in enumerate(player_names):
            new_res = {'name':player_name, 'points':result['scores'][idx], 'game_id':result['game_id']}
            if 'MCTS' in player_name:
                new_res['c_value'] = data[idx]['c_value']
                new_res['iterations'] = data[idx]['iterations']

                if 'PW' in player_name:
                    new_res['c'] = data[idx]['c']
                    new_res['alpha'] = data[idx]['alpha']
                else:
                    new_res['c'] = None
                    new_res['alpha'] = None

                if 'OMA' in player_name:
                    new_res['eq'] = data[idx]['eq']
                else:
                    new_res['eq'] = None

            else:
                new_res['c_value'] = None
                new_res['iterations'] = None
                new_res['c'] = None
                new_res['alpha'] = None
                new_res['eq'] = None
            res_json.append(new_res)
        

    with open(save_name, 'w') as f:
        f.write(json.dumps(res_json))

    # now_ts = datetime.now()
    # print(f"Time: {now_ts.strftime('%Y-%m-%d_%H:%M:%S')}, Test {save_name}")


# def save_scores(results, save_name):
#     folder_path = os.path.dirname(save_name)
#     # Check if the folder exists
#     if not os.path.exists(folder_path):
#         # If the folder does not exist, create it including any necessary parent directories
#         os.makedirs(folder_path)


#     save_name = save_name.replace(':', '=')

#     with open(f'{save_name}.txt', 'w') as file:
#         for game in results:
#             print(game)
#             try:
#                 line = ' '.join([str(value) for value in game]) + '\n'
#                 file.write(line)
#             except Exception as e:
#                 raise(e)
#                 continue

def check_and_create_folder(file_path: str) -> None:
    if '/' in file_path:
        folder_path = '/'.join(file_path.split('/')[:-1])
    else:
        folder_path = file_path
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def run_tests(function, parameters, result_size):
    num_processes = os.cpu_count()
    with Pool(num_processes) as pool:
        # Create a list of tuples for each task
        tasks = [(i, function, parameters) for i in range(result_size)]
        
        # Use pool.map to process tasks
        results = pool.map(run_game_threaded, tasks)
    
    return results
    # processes = []
    # for i in iter_variable:
    #     game_sim = function(*parameter)
    #     process = Process(target=run_game_threaded, args=(game_sim, results, i))
    #     processes.append(process)
        
    #     process.start()


    # for process in processes:
    #     process.join()
        # print(f"Process {process.pid} joined")  # Confirm process joins

def create_mcts(player_templates:List):
    templates = deepcopy(player_templates)
    random.shuffle(templates)
    # print(templates)
    card_deck = CardDeck(len(templates), True)
    bank = Bank(len(templates))
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    for idx, player in enumerate(templates):
        if player['type'] == 'random':
            players.append(RandomPlayer(idx, None, bank))
        elif player['type'] == 'MCTS':
            players.append(MCTSPlayer(idx, None, bank, player['c_value'], player['iterations'], 'MCTS'))
        elif player['type'] == 'MCTS-PW':
            players.append(MCTSPlayer(idx, None, bank, player['c_value'], player['iterations'], 'MCTS', pw=True
                                      , c=player['c'], alpha=player['alpha']))
        elif player['type'] == 'MCTS-OMA':
            players.append(MCTSPlayer(idx, None, bank, player['c_value'], player['iterations'], 'MCTS', oma=True, eq_param=player['eq']))
        elif player['type'] == 'MCTS-PW-OMA':
            players.append(MCTSPlayer(idx, None, bank, player['c_value'], player['iterations'], 'MCTS', pw=True
                                     , c=player['c'], alpha=player['alpha']
                                     , oma=True, eq_param=player['eq']))

    game_state = GameState(playing_board=playing_board,
                        players=players,
                        card_deck=card_deck,
                        bank=bank, 
                        turn=0,
                        slot_index=0,
                        slots=[],
                        mode=0)
    give_players_crystals(game_state.players)
    game_simulation = Game(game_state, True)
    return game_simulation, templates
        
def check_and_create_folder(file_path: str) -> None:
    if '/' in file_path:
        folder_path = '/'.join(file_path.split('/')[:-1])
    else:
        folder_path = file_path
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


if __name__ == "__main__":
    # NUMBER_OF_PLAYERS = 2
    manager = Manager()
    tests = [
        # {'name': 'different_counts_of_players','function':debug_mcts, 'mode':'paralel', 'result_size':30, 
        #   'param': [(3, 1, 1.2), (4, 1, 1.2), (5, 1, 1.2)]},
        # {'name': 'iterations_5_1','function':debug_mcts, 'mode':'paralel', 'result_size':100, 
        #   'param': [(5, 1, 48, 100), (5, 1, 48, 150), (5, 1, 48, 200), (5, 1, 48, 250), (5, 1, 48, 300)
        #             , (5, 1, 48, 350), (5, 1, 48, 400), (5, 1, 48, 450), (5, 1, 48, 500), (5, 1, 48, 550)
        #             , (5, 1, 48, 600)]}
        # {'name': 'optimize_pw','function':debug_mcts, 'mode':'paralel', 'result_size':100, 
        #   'param': [
        #       (5, 1, 1.2, 500, {'c':2, 'alpha':0.5}),
        #       (5, 1, 1.2, 500, {'c':1, 'alpha':0.5}),
        #       (5, 1, 1.2, 500, {'c':1, 'alpha':1}),
        #       (5, 1, 1.2, 500, {'c':2, 'alpha':2}),

        #             ]}

        # {'data':[
        #         {'type':'random'},
        #         {'type':'MCTS', 'iterations':100, 'c_value':2.935643834971814},
        #         {'type':'random'},
        #         {'type':'random'},
        #         {'type':'random'}
        #         ],
        #         'size':3, 'name':'test_agents'}
                
        {'data':[
                {'type':'random'}
                ,{'type':'MCTS', 'iterations':500, 'c_value':2.935643834971814}
                ,{'type':'MCTS-OMA', 'iterations':500, 'c_value':2.935643834971814, 'eq':0.03600459242730309}
                ,{'type':'MCTS-PW', 'iterations':500, 'c_value':2.935643834971814, 'c':1.550032374665823, 'alpha':1.716192864927639}
                ,{'type':'MCTS-PW-OMA', 'c_value': 2.935643834971814, 'eq': 0.03600459242730309, 'c': 1.550032374665823, 'alpha': 1.716192864927639, 'iterations':500}
                ],
                'size':3, 'name':'analysis_1_1'}


        #   , (5, 1, 100), (5, 1, 150), (5, 1, 200), (5, 1, 250), (5, 1, 300),
        #             (5, 1, 350), (5, 1, 400), (5, 1, 450), (5, 1, 500)]}
        # {'name': 'mcts_vs_mcts','function':debug_mcts, 'mode':'paralel', 'result_size':30, 
        # 'param': [(5, 5, 1.2), (5, 4, 1.2), (5, 3, 1.2), (5, 2, 1.2), (5, 1, 1.2)]},
         
        # 'param': [(5, 2, 1.2), (5, 3, 1.2), (5, 4, 1.2), (5, 5, 1.2)]},
        # {'name': 'debug_mcts','function':debug_mcts, 'mode':'paralel', 'result_size':30, 
        # 'param': [5]},
        # {'name': 'IterationTests','function':iteration_test, 'mode':'paralel', 'result_size':100, 
        #  'param': [50, 100, 150, 200, 250, 300, 350, 400, 45s0, 500, 550, 600]}
        # {'name': 'CValueTests','function':c_value_test, 'mode':'paralel', 'result_size':100, 
        #  'param': [i for i in range(20, 101, 10)]}
        # {'name': 'CValueTestWL','function':c_value_wl, 'mode':'paralel', 'result_size':100, 
        #  'param': [i/10 for i in range(1, 21, 1)]},
        # {'name': 'EDTimeTests','function':ed_time_test, 'mode':'simple', 'result_size':50, 
        # 'param': [1]},

    ]
    for test in tests:
        # for parameter in test['param']:
        start = timer()

        now_ts = datetime.now()
        test_time = now_ts.strftime('%Y%m%d_%H%M%S')
        results = run_tests(create_mcts, test['data'], test['size'])

        return_list = []
        for res in results:
            new_obj = {}
            game_id, scores = res
            if game_id != 'failed':
                new_obj['game_id'] = game_id
                new_obj['scores'] = scores
                return_list.append(new_obj)
            else:
                print('Failed Simulation')

        end = timer()
        print(f"Success {test['name']}")
        duration = end - start
        print(f"Time: {now_ts.strftime('%Y%m%d_%H%M%S')}, Test duration: {duration}")


