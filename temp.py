import functions_framework
import math
import os
import random
from typing import List
from bank import Bank
from card import Card
from card_deck import CardDeck
from coin import Coin
from game import Game
from player import Player
from game_state import GameState
from mcts_player import MCTSPlayer
from playing_board import PlayingBoard
from random_player import RandomPlayer
import time
from timeit import default_timer as timer
from threading import Thread
from multiprocessing import Pool, Process, Manager
import time
from datetime import datetime
import json
import traceback

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

def create_mcts(player_templates):
    card_deck = CardDeck(len(player_templates), True)
    bank = Bank(len(player_templates))
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    for idx, player in enumerate(player_templates):
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
    return game_simulation

def run_game_threaded(index_function_parameter):
    try:
        # print(f"Starting process {os.getpid()}") 
        index, function, parameters = index_function_parameter 
        game_simulation = function(*parameters)
        
        result = game_simulation.run_game()
        mcts = []
        for player in game_simulation.players:
            if player.player_type == 'MCTS':
                mcts.append(player.index)
        # print(mcts)
        # print(f"Ended {os.getpid()}")
        # results[index] = result
        return (game_simulation.game_id, result)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return ('failed', [0,0,0,0,0])

def run_tests(function, parameters, result_size):
    num_processes = result_size
    with Pool(num_processes) as pool:
        # Create a list of tuples for each task
        tasks = [(i, function, parameters) for i in range(result_size)]
        
        # Use pool.map to process tasks
        results = pool.map(run_game_threaded, tasks)
    
    return results

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    try:
        print(request.data)
        parameters = json.loads(request.data.decode())['player_templates']
        print(parameters)
    except:
        return 'Bad parameters'

    start = timer()
    game_simulation = create_mcts(parameters)
    
    result = game_simulation.run_game()
    mcts = []
    for player in game_simulation.players:
        if player.player_type == 'MCTS':
            mcts.append(player.index)

    new_obj = {}
    new_obj['game_id'] = game_simulation.game_id
    new_obj['scores'] = result
    end = timer()
    print(f'Simulation time: {end-start}')
    return json.dumps(new_obj)