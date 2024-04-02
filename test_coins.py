
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


def run_game_threaded(game_simulation, index):
    game_simulation.run_game()
    print(f"Simulation {index} ended")


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

def create_game_simulation():
    NUMBER_OF_PLAYERS = 5
    mode = 4
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True)
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    for i in range(NUMBER_OF_PLAYERS):
        players.append(RandomPlayer(i, None, bank))
    game_state = GameState(playing_board=playing_board,
                        players=players,
                        card_deck=card_deck,
                        bank=bank, 
                        turn=0,
                        slot_index=0,
                        slots=[],
                        mode=mode)
    give_players_crystals(game_state.players)


    game_simulation = Game(game_state, True)
    return game_simulation

if __name__ == '__main__':
    manager = Manager()

    processes = []
    iter_variable = range(0, 100)

    for i in iter_variable:
        game_simulation = create_game_simulation()
        process = Process(target=run_game_threaded, args=(game_simulation, i))
        processes.append(process)
        process.start()
        print(f"Simulation {i} started")

    for process in processes:
        process.join()
