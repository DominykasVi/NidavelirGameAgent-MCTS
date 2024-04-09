
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
from multiprocessing import Process, Manager
import time
from datetime import datetime


GLOBAL_DEPTH = 500 #Tested
GLOBAL_C_VALUE = 4 #Tested
NUMBER_OF_PLAYERS = 2
C_VALUE_WL = 0.6 #Tested
GLOBAL_MAX_NODES = 120 #Tested

def run_game_threaded(game_simulation:Game, results, index):
    try:
        result = game_simulation.run_game()
        mcts = []
        for player in game_simulation.players:
            if player.player_type == 'MCTS':
                mcts.append(player.index)
        result = result + [':'] + mcts
        results[index] = result
    except Exception as e:
        time = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f'Logs/Failures/{time}.txt', 'w') as f:
            f.write(str(e))


def iteration_test(depth):
    card_deck = CardDeck(2, True, '2')
    bank = Bank(2)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=10, depth=depth, type='MCTS'))
    players.append(RandomPlayer(1, None, bank))
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
    return game_simulation

def c_value_test(c_value):
    card_deck = CardDeck(2, True, '2')
    bank = Bank(2)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=c_value, depth=GLOBAL_DEPTH, type='MCTS'))
    players.append(RandomPlayer(1, None, bank))
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
    return game_simulation

def ed_vs(manager):
    card_deck = CardDeck(2, True, '2')
    bank = Bank(2)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSED', manager=manager))
    players.append(MCTSPlayer(1, None, bank, c_value=GLOBAL_C_VALUE, depth=GLOBAL_DEPTH, type='MCTSVS'))
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
    return game_simulation

def ed_wl(manager):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSED', manager=None))
    players.append(MCTSPlayer(1, None, bank, c_value=C_VALUE_WL, depth=GLOBAL_DEPTH, type='MCTSWL'))
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
    return game_simulation

def ed_time_test(manager):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSED', manager=manager))
    players.append(RandomPlayer(1, None, bank))
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
    return game_simulation

def lim_ed(manager):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSLM', max_child_nodes=GLOBAL_MAX_NODES))
    players.append(MCTSPlayer(1, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSED', manager=manager))
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
    return game_simulation

def lim_vs(temp):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSLM', max_child_nodes=GLOBAL_MAX_NODES))
    players.append(MCTSPlayer(1, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSVS'))
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
    return game_simulation


def lim_wl(temp):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSLM', max_child_nodes=GLOBAL_MAX_NODES))
    players.append(MCTSPlayer(1, None, bank, depth=GLOBAL_DEPTH, c_value=C_VALUE_WL, type='MCTSWL'))
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
    return game_simulation

def limit_test(limit):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSLM', max_child_nodes=limit))
    players.append(RandomPlayer(1, None, bank))
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
    return game_simulation

def mcts_ed(manager):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTS'))
    players.append(MCTSPlayer(1, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSED', manager=manager))
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
    return game_simulation

def mcts_lim(temp):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTS'))
    players.append(MCTSPlayer(1, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSLM', max_child_nodes=GLOBAL_MAX_NODES))
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
    return game_simulation

def mcts_vs(temp):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTS'))
    players.append(MCTSPlayer(1, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSVS'))
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
    return game_simulation

def mcts_wl(temp):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTS'))
    players.append(MCTSPlayer(1, None, bank, depth=GLOBAL_DEPTH, c_value=C_VALUE_WL, type='MCTSWL'))
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
    return game_simulation

def mcts_time_test(depth):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=depth, c_value=GLOBAL_C_VALUE, type='MCTS'))
    players.append(RandomPlayer(1, None, bank))
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
    return game_simulation

def random_ed(manager):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSED'))
    players.append(RandomPlayer(1, None, bank))
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
    return game_simulation

def random_lim(temp):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSLM', max_child_nodes=GLOBAL_MAX_NODES))
    players.append(RandomPlayer(1, None, bank))
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
    return game_simulation

def random_mcts(temp):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTS'))
    players.append(RandomPlayer(1, None, bank))
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
    return game_simulation

def random_vs(temp):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSVS'))
    players.append(RandomPlayer(1, None, bank))
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
    return game_simulation

def random_wl(temp):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=C_VALUE_WL, type='MCTSWL'))
    players.append(RandomPlayer(1, None, bank))
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
    return game_simulation

def wl_vs(temp):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=C_VALUE_WL, type='MCTSWL'))
    players.append(MCTSPlayer(1, None, bank, depth=GLOBAL_DEPTH, c_value=GLOBAL_C_VALUE, type='MCTSVS'))
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
    return game_simulation

def c_value_wl(c_value):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=c_value, type='MCTSWL'))
    players.append(RandomPlayer(1, None, bank))
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
    return game_simulation

def debug_mcts(NUMBER_OF_PLAYERS, number_of_mcts, c_value):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True)
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    for i in range(0, NUMBER_OF_PLAYERS):
        players.append(RandomPlayer(i, None, bank))

    random_indexes = []
    for _ in range(number_of_mcts):
        random_index = -1
        while random_index == -1:
            random_index = random.choice([i for i in range(0, NUMBER_OF_PLAYERS)])
            if random_index in random_indexes:
                random_index == -1
                continue
            players[random_index] = MCTSPlayer(random_index, None, bank, c_value, 200, 'MCTS')

    # players.append(MCTSPlayer(0, None, bank, depth=GLOBAL_DEPTH, c_value=1.2, type='MCTS'))
    # players.append(RandomPlayer(1, None, bank))
    
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

def save_scores(results, save_name):
    folder_path = os.path.dirname(save_name)
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # If the folder does not exist, create it including any necessary parent directories
        os.makedirs(folder_path)

    with open(f'{save_name}.txt', 'w') as file:
        for game in results:
            print(game)
            try:
                line = ' '.join([str(value) for value in game]) + '\n'
                file.write(line)
            except:
                continue

def run_tests(results, iter_variable, function, parameter):
    processes = []
    for i in iter_variable:
        game_sim = function(*parameter)
        process = Process(target=run_game_threaded, args=(game_sim, results, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

        

if __name__ == "__main__":
    # NUMBER_OF_PLAYERS = 2
    manager = Manager()

    tests = [
        {'name': 'different_counts_of_players','function':debug_mcts, 'mode':'paralel', 'result_size':30, 
          'param': [(3, 1, 1.2), (4, 1, 1.2), (5, 1, 1.2)]},
        {'name': 'differerent_c_values','function':debug_mcts, 'mode':'paralel', 'result_size':30, 
          'param': [(5, 1, 100), (5, 1, 200), (5, 1, 10), (5, 1, 20), (5, 1, 2), (5, 1, 5)]},
        {'name': 'mcts_vs_mcts','function':debug_mcts, 'mode':'paralel', 'result_size':30, 
        'param': [(5, 2, 1.2), (5, 3, 1.2), (5, 4, 1.2), (5, 5, 1.2)]},
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


        # {'name': 'LIM_VS','function':lim_vs, 'mode':'paralel', 'result_size':100, 
        # 'param': [1]},
        # {'name': 'LIM_WL','function':lim_wl, 'mode':'paralel', 'result_size':100, 
        #  'param': [1]},
        # # {'name': 'LimitTests','function':limit_test, 'mode':'paralel', 'result_size':100, 
        # #  'param': [i for i in range(40, 201, 40)]},
        # {'name': 'MCTS_LIM','function':mcts_lim, 'mode':'paralel', 'result_size':100, 
        #  'param': [1]},
        # {'name': 'MCTS_VS','function':mcts_vs, 'mode':'paralel', 'result_size':100, 
        #  'param': [1]},
        # {'name': 'MCTS_WL','function':mcts_wl, 'mode':'paralel', 'result_size':100, 
        #  'param': [1]},
        # {'name': 'MCTSTimeTests','function':mcts_time_test, 'mode':'simple', 'result_size':20, 
        #  'param': [50, 100, 150, 200, 250, 300, 350, 400, 450, 550, 600]},
        # {'name': 'Random_VS','function':random_vs, 'mode':'paralel', 'result_size':100, 
        #  'param': [1]},
        # {'name': 'Random_LIM','function':random_lim, 'mode':'paralel', 'result_size':100, 
        #  'param': [1]},
        # # {'name': 'Random_MCTS','function':random_mcts, 'mode':'paralel', 'result_size':100, 
        # #  'param': [1]},
        # {'name': 'Random_WL','function':random_wl, 'mode':'paralel', 'result_size':100, 
        #  'param': [1]},
        # {'name': 'WL_VS','function':wl_vs, 'mode':'paralel', 'result_size':100, 
        #  'param': [1]},
        # {'name': 'Random_ED','function':random_ed, 'mode':'simple', 'result_size':15, 
        #  'param': [1]},
        # {'name': 'MCTS_ED','function':mcts_ed, 'mode':'simple', 'result_size':15, 
        #  'param': [1]},
        # {'name': 'ED_VS','function':ed_vs, 'mode':'simple', 'result_size':15, 
        #  'param': [1]},
        # {'name': 'ED_WL','function':ed_wl, 'mode':'simple', 'result_size':15, 
        # 'param': [1]},
        # {'name': 'LIM_ED','function':lim_ed, 'mode':'simple', 'result_size':15, 
        # 'param': [1]}
    ]
    for test in tests:
        for parameter in test['param']:
            start = timer()

            now_ts = datetime.now()
            test_time = now_ts.strftime('%Y%m%d_%H%M%S')
            results = manager.list([None] * test['result_size'])

            iter_variable = [i for i in range(test['result_size'])]
            if test['mode'] == 'paralel':
                run_tests(results, iter_variable, test['function'], parameter)
            else:
                for idx in iter_variable:
                    run_tests(results, [idx], test['function'], parameter)

            incomplete = True
            errors = 0
            while(incomplete):
                failed_in = []
                good_results = 0
                for index in range(test['result_size']):
                    if results[index] != None:
                        good_results += 1
                    else:
                        failed_in.append(index)
                if good_results == test['result_size']:
                    incomplete = False
                else:
                    print(f"Only {good_results} of {test['result_size']}, run again {test['name']}, value={parameter}")
                    run_tests(results, failed_in, test['function'], parameter)


                errors += 1
                if errors > 10:
                    print(f"Failed test {test['name']}")
                    incomplete = False
                    break
            if incomplete == False:
                save_scores(results=results, save_name=f'Logs/TestResults/{test["name"]}/{test_time}_{str(parameter)}')
            end = timer()
            print(f"Success {test['name']}, value={parameter}")
            duration = end - start
            print(f"Test duration: {duration}")


