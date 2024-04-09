
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
from itertools import combinations

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



def test_queue():
    # Player0 (5), bets: [5(False), 3(False), 0(True)], lefover: [2(False), 4(False)]
    # Player1 (4), bets: [0(True), 3(False), 4(False)], lefover: [2(False), 5(False)]
    # Player2 (1), bets: [5(False), 4(False), 2(False)], lefover: [0(True), 3(False)]
    # Player3 (2), bets: [4(False), 3(False), 2(False)], lefover: [0(True), 5(False)]
    # Player4 (3), bets: [0(True), 3(False), 5(False)], lefover: [2(False), 4(False)]

    NUMBER_OF_PLAYERS = 5
    mode = 1

    card_deck = CardDeck(NUMBER_OF_PLAYERS, True)
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    for i in range(NUMBER_OF_PLAYERS):
        players.append(RandomPlayer(i, None, bank))
        print(f"Player {i} added")
    coin_5 = Coin(5)
    coin_4 = Coin(4)
    coin_3 = Coin(3)
    coin_2 = Coin(2)
    coin_0 = Coin(0)
    game_state = GameState(playing_board=playing_board,
                    players=players,
                    card_deck=card_deck,
                    bank=bank, 
                    turn=0,
                    slot_index=0,
                    slots=[],
                    mode=mode)
    
    game_simulation = Game(game_state, True)
    players[0].crystal = 5
    players[1].crystal = 4
    players[2].crystal = 1
    players[3].crystal = 2
    players[4].crystal = 3
    players[0].bets = [coin_5, coin_4, coin_3, coin_2, coin_0]
    players[1].bets = [coin_0, coin_4, coin_3, coin_2, coin_5]
    players[2].bets = [coin_5, coin_4, coin_3, coin_0, coin_4]
    players[3].bets = [coin_4, coin_4, coin_2, coin_5, coin_3]
    players[4].bets = [coin_0, coin_3, coin_0, coin_4, coin_2]
    print(players)
    print(game_simulation.create_player_queue(players, 0))


def reset_players(NUMBER_OF_PLAYERS, bank) -> List[Player]:
    players = []
    for i in range(NUMBER_OF_PLAYERS):
        players.append(RandomPlayer(i, None, bank))
    return players

def test_coin_excahnge():
    NUMBER_OF_PLAYERS = 5
    mode = 1

    card_deck = CardDeck(NUMBER_OF_PLAYERS, True)
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    for i in range(NUMBER_OF_PLAYERS):
        players.append(RandomPlayer(i, None, bank))
        print(f"Player {i} added")
        
    coin_5 = Coin(5)
    coin_4 = Coin(4)
    coin_3 = Coin(3)
    coin_2 = Coin(2)
    coin_0 = Coin(0)




    game_state = GameState(playing_board=playing_board,
                    players=players,
                    card_deck=card_deck,
                    bank=bank, 
                    turn=0,
                    slot_index=0,
                    slots=[],
                    mode=mode)
    print(players)
    game_simulation = Game(game_state, True)

    for i in range(5):
        print(f'=============={i}=================')
        players[0].crystal = 5
        players[1].crystal = 4
        players[2].crystal = 3
        players[3].crystal = 2
        players[4].crystal = 1

        players[0].bets = [coin_5, coin_4, coin_3, coin_2, coin_0]
        players[1].bets = [coin_5, coin_4, coin_3, coin_2, coin_5]
        players[2].bets = [coin_5, coin_4, coin_3, coin_0, coin_4]
        players[3].bets = [coin_5, coin_4, coin_2, coin_5, coin_3]
        players[4].bets = [coin_5, coin_3, coin_0, coin_4, coin_2]

    
    # game_simulation.exchange_crystals(players, 0)
        print(players)
        Game.exchange_crystals(players, i, 1)
        print(players)


        
    i = 0
    print(f'=============={i}=================')
    players = reset_players(NUMBER_OF_PLAYERS, bank)
    players[0].crystal = 2
    players[1].crystal = 4
    players[2].crystal = 3
    players[3].crystal = 5
    players[4].crystal = 1
    players[0].bets = [coin_5]
    players[1].bets = [coin_5]
    players[2].bets = [coin_3]
    players[3].bets = [coin_5]
    players[4].bets = [coin_5]
    print(players)
    players = GameState.create_player_queue(players, 0)
    print(players)
    Game.exchange_crystals(players, i, 1)
    print(players)
        # Player0 (5), bets: [5(False), 3(False), 4(False)], lefover: [0(True), 2(False)]
    # Player1 (1), bets: [3(False), 4(False), 0(True)], lefover: [2(False), 5(False)]
    # Player2 (3), bets: [4(False), 2(False), 0(True)], lefover: [3(False), 5(False)]
    # Player3 (4), bets: [3(False), 0(True), 2(False)], lefover: [4(False), 5(False)]
    # Player4 (2), bets: [3(False), 0(True), 5(False)], lefover: [2(False), 4(False)]
    # SLOT 1 : [red:4 (1), blue:7 (1), violet:None (1), blue:6 (1), violet:None (1)]
    # Player turns: [Player0 (5), Player2 (3), Player3 (4), Player4 (2), Player1 (1)]
    # Crystals changed: [Player0 (5), Player2 (3), Player3 (4), Player4 (1), Player1 (2)]
    i = 0
    players = reset_players(NUMBER_OF_PLAYERS, bank)
    print(f'=============={i}=================')
    players[0].crystal = 5
    players[1].crystal = 1
    players[2].crystal = 3
    players[3].crystal = 4
    players[4].crystal = 2
    players[0].bets = [coin_5]
    players[1].bets = [coin_3]
    players[2].bets = [coin_4]
    players[3].bets = [coin_3]
    players[4].bets = [coin_3]
    print(players)
    players = GameState.create_player_queue(players, 0)
    print(players)
    Game.exchange_crystals(players, i, 1)
    print(players)
        # print(f'=============={i}=================')
    # print(game_simulation.exchange_crystals(players, 1))
    # print(game_simulation.exchange_crystals(players, 2))
    # print(game_simulation.exchange_crystals(players, 3))
    # print(game_simulation.exchange_crystals(players, 4))

def test_comb():
    cards_to_take = 2
    colors = ["red", "blue", "yellow"]
    cards = {"red": ["a", "b"], "blue": ["c", "d"], "yellow": ["e", "f"]}
    all_combinations = combinations(colors, cards_to_take)
    results = []
    for color_combination in all_combinations:
        taken_cards = [(color, cards[color][-1]) for color in color_combination]
        print(taken_cards)



if __name__ == "__main__":
    # test_comb()
    # print([':'] + [1, 2])
    # print([1, 2, 3, 4, 5] + [':'] + [1, 2])
    lst = [i for i in range(0, 5)]
    random_index = random.choice(lst)
    print(lst)
    print(str((1, 20, 3)))
    # game_simulation = Game(game_state, True)
    # game_simulation.run_game()
    # # print_game_results(game_simulation.players)
    # end = timer()

    # print(f"Simulation time: {end - start}")


