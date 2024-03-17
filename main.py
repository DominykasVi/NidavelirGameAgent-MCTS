
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


def print_game_results(players):
    print("################################################################################")
    print("Results")
    colors = ['red', 'green', 'orange', 'violet', 'blue']
    for player in players:
        print(player)
        print(player.coins)
        player.card_deck.print_card_deck()
        card_sum = 0
        for color in colors:
            color_count = player.get_color_count(color)
            print(f"Has {color_count} of {color}")
            card_sum += color_count
        print(f"Player has {card_sum} cards")
        player.print_player_points()


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





if __name__ == "__main__":
 

    NUMBER_OF_PLAYERS = 5
    mode = 1

    start = timer()

    card_deck = CardDeck(NUMBER_OF_PLAYERS, True)
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    for i in range(NUMBER_OF_PLAYERS):
        players.append(RandomPlayer(i, None, bank))
        print(f"Player {i} added")
    # players.append(RandomPlayer(1, None, bank))
    # players.append(MCTSPlayer(1, None, bank, 1.2, 200))

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
    game_simulation.run_game()
    # print_game_results(game_simulation.players)
    end = timer()

    print(f"Simulation time: {end - start}")


