
from typing import List
from bank import Bank
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

def interpret_data(results):
    # Calculate average scores
    num_players = len(results[0])
    total_scores = [0] * num_players
    num_games = len(results)

    for game in results:
        for i, score in enumerate(game):
            total_scores[i] += score

    average_scores = [total / num_games for total in total_scores]

    # Print average scores
    for i, avg in enumerate(average_scores, 1):
        print(f"Player {i} average score: {avg}")

    # Save average scores to a file
    with open('simulation_scores.txt', 'w') as file:
        for tup in results:
            line = ' '.join(map(str, tup)) + '\n'
            file.write(line)
    # Plot histogram
    all_scores = [score for game in results for score in game]
    plt.hist(all_scores, bins=range(min(all_scores), max(all_scores) + 2), edgecolor='black')
    plt.title('Histogram of Scores')
    plt.xlabel('Scores')
    plt.ylabel('Frequency')
    plt.savefig('histogram_of_scores.png')

    plt.show()
    plt.close()  # Close the plot

def run_game_threaded(game_simulation, results, index):
    p0, p1 = game_simulation.run_game()
    results[index] = (p0, p1)

if __name__ == "__main__":
    turn = 0
    NUMBER_OF_PLAYERS = 2
    # card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    # bank = Bank(NUMBER_OF_PLAYERS)
    # playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    # #here we can define random, MCTS or human players
    # players:List[Player] = []
    # players.append(MCTSPlayer(0, None, bank))
    # players.append(RandomPlayer(1, None, bank))

    # players.append(RandomPlayer(0, None, bank))
    # players.append(RandomPlayer(1, None, bank))

    # players.append(RandomPlayer(0, None, bank))
    # players.append(MCTSPlayer(1, None, bank))
    # players[0].make_bet([Coin(5, False), Coin(4, False), Coin(0, True)], ga)
    # players[1].make_bet([Coin(4, False), Coin(5, False), Coin(0, True)])
    
    # players.append(RandomPlayer("Player2", None, bank))
    # for i in range(NUMBER_OF_PLAYERS):
    #     players.append(Player(f"Player{i+1}", None, bank))
    # mode 0 - run everything
    # mode 1 - make breaks, print turns
    # mode 2 - dont make breaks, print turns
    mode = 0

    
    # game_simulation = Game( players, playing_board, mode, True)
    # From turn 1
    # game_simulation = Game(bank, card_deck, players, playing_board, 1, mode, True)


    # game_simulation = Game(game_state, True)

    #######################################################
    # game_simulation.generate_slots()
    # new_state = game_simulation.create_game_state()
    # print(new_state)


    # game_simulation.make_player_bets()


    # Possible combinations
    # start = timer()
    # possible_card_combinatons = playing_board.generate_possible_slots(4, 1)
    # end = timer()
    # print(f"Permutations calculated in: {end - start}")

    # print(len(possible_card_combinatons))
    # exit()
    ###########################################################
    # print(players)
    results = []
    start = timer()

    threads = [None] * 10
    results = [None] * 10
    for i in range(10):
        print(f"SIMULATION {i}")
        card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
        bank = Bank(NUMBER_OF_PLAYERS)
        playing_board = PlayingBoard(card_deck)
        colors = ['red', 'green', 'orange', 'violet', 'blue']

        #here we can define random, MCTS or human players
        players:List[Player] = []
        players.append(MCTSPlayer(0, None, bank))
        players.append(RandomPlayer(1, None, bank))
        game_state = GameState(playing_board=playing_board,
                            players=players,
                            card_deck=card_deck,
                            bank=bank, 
                            turn=0,
                            slot_index=0,
                            slots=[],
                            mode=mode)
        game_simulation = Game(game_state, True)
        for i in range(len(threads)):
            threads[i] = Thread(target=run_game_threaded, args=(game_simulation, results, i))
            threads[i].start()
        # p0, p1 = game_simulation.run_game()
        # results.append((p0, p1))
    for i in range(len(threads)):
        threads[i].join()

    end = timer()
    interpret_data(results)
    # print_game_results(players, colors)
    print(f"Simulation time: {end - start}")


