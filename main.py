
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
    mode = 0

    start = timer()

    card_deck = CardDeck(NUMBER_OF_PLAYERS, True)
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    players:List[Player] = []
    for i in range(NUMBER_OF_PLAYERS):
        players.append(RandomPlayer(i, None, bank))
        print(f"Player {i} added")

# {"score": 227.4, "c_value": 3.4680925162101737, "c": 0.5604952853346341, "alpha": 1.4473637176345078, "e": 0.05281024338707091, "date": "2024-05-13 02:03:27"}
    idx = 2
    players[idx] = MCTSPlayer(idx, None, bank, 3.4680925162101737, 500)#, pw=True, c=0.5604952853346341, eq_param=0.05281024338707091, alpha=1.4473637176345078, oma=True)
    # players.append(RandomPlayer(1, None, bank))
    # players.append()

    game_state = GameState(playing_board=playing_board,
                        players=players,
                        card_deck=card_deck,
                        bank=bank, 
                        turn=0,
                        slot_index=0,
                        slots=[],
                        mode=mode)
    give_players_crystals(game_state.players)

    # game_state.turn = 3
    # players[0].card_deck.cards[14] = Card('blue', 5, 1, 14)
    # players[0].card_deck.card_count['blue'] = 1


    game_simulation = Game(game_state, True)
    print(str(game_simulation.game_id))
    print(game_simulation.run_game())
    # print(str(game_simulation.game_id))
    # print_game_results(game_simulation.players)
    # print(game_simulation.result)
    end = timer()
    
    

    print(f"Simulation time: {end - start}")

#     {
#   "textPayload": "[[{'type': 'random'}, {'type': 'random'}, {'type': 'MCTS-PW-OMA', 'iterations': 500, 'c_value': 2.8612678080814935, 'eq': 0.5400455966221653, 'c': 1.3423930766078094, 'alpha': 0.380030259109943}, {'type': 'random'}, {'type': 'random'}]]",
#   "insertId": "663b00ec000845126a52be99",
#   "resource": {
#     "type": "cloud_run_revision",
#     "labels": {
#       "project_id": "butu-414613",
#       "configuration_name": "test3",
#       "location": "europe-central2",
#       "service_name": "test3",
#       "revision_name": "test3-00024-gus"
#     }
#   },
#   "timestamp": "2024-05-08T04:34:52.541970Z",
#   "labels": {
#     "goog-managed-by": "cloudfunctions",
#     "instanceId": "00f46b9285462037ee110ffd5758d17a2fa5a0ae1824eac63083e9f3617fe689314d755fcae2acc0929976d83fa1cb7fe807927fbaf0b4efb629452dd5f16d2555"
#   },
#   "logName": "projects/butu-414613/logs/run.googleapis.com%2Fstdout",
#   "receiveTimestamp": "2024-05-08T04:34:52.544921010Z"
# }


