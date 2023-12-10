
from typing import List
from bank import Bank
from card_deck import CardDeck
from game import Game
from Players.player import Player
from playing_board import PlayingBoard
from Players.random_player import RandomPlayer
import time
from timeit import default_timer as timer

def print_game_results(players, colors):
    print("################################################################################")
    print("Results")
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



if __name__ == "__main__":
    turn = 0
    NUMBER_OF_PLAYERS = 2
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(RandomPlayer("Player1", None, bank))
    players.append(RandomPlayer("Player2", None, bank))
    # for i in range(NUMBER_OF_PLAYERS):
    #     players.append(Player(f"Player{i+1}", None, bank))
    # mode 0 - run everything
    # mode 1 - make breaks, print turns
    # mode 2 - dont make breaks, print turns
    mode = 0

    
    game_simulation = Game(bank, card_deck, players, playing_board, 0, mode, True)
    # From turn 1
    # game_simulation = Game(bank, card_deck, players, playing_board, 1, mode, True)

    game_simulation = Game(bank, card_deck, players, playing_board, 0, mode, True)
    game_simulation.generate_slots()
    game_simulation.make_player_bets()

    # Possible combinations
    # start = timer()
    # possible_card_combinatons = playing_board.generate_possible_slots(4, 1)
    # end = timer()
    # print(f"Permutations calculated in: {end - start}")

    # print(len(possible_card_combinatons))
    # exit()

    print(players)
    start = timer()
    game_simulation.run_game()
    end = timer()

    print_game_results(players, colors)
    print(f"Simulation time: {end - start}")


