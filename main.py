
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
    print(f"SIMULATION {index} FINISHED")
    # done = 0
    # for i in results:
    #     if i is not None:
    #         done += 1
    # rem = len(results) - done
    # print(f"Simulations remaining {rem}")

def create_game(NUMBER_OF_PLAYERS, mode, c_value, depth):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
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
                        mode=mode)
    give_players_crystals(game_state.players)
    game_simulation = Game(game_state, True)
    return game_simulation

def create_game_lm_random(NUMBER_OF_PLAYERS, mode, max_chld_nodes):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=10, depth=200, type='MCTSLM', max_child_nodes=max_chld_nodes))
    players.append(RandomPlayer(1, None, bank))
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

def create_game_mcts_lm(NUMBER_OF_PLAYERS, mode):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=10, depth=200))
    players.append(MCTSPlayer(1, None, bank, c_value=10, depth=200, type='MCTSLM', max_child_nodes=120))
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

def create_game_wl_lm(NUMBER_OF_PLAYERS, mode):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=1.5, depth=200, type='MCTSWL'))
    players.append(MCTSPlayer(1, None, bank, c_value=10, depth=200, type='MCTSLM', max_child_nodes=120))
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

def create_game_wl_random(NUMBER_OF_PLAYERS, mode):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=1.5, depth=200, type='MCTSWL'))
    players.append(RandomPlayer(1, None, bank))
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

def create_game_wl_mcts(NUMBER_OF_PLAYERS, mode):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=1.5, depth=200, type='MCTSWL'))
    players.append(MCTSPlayer(1, None, bank, c_value=10, depth=200))
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

def create_game_vs_random(NUMBER_OF_PLAYERS, mode):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=1.5, depth=200, type='MCTSVS'))
    players.append(RandomPlayer(1, None, bank))
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

def create_game_vs_mcts(NUMBER_OF_PLAYERS, mode):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=10, depth=200))
    players.append(MCTSPlayer(1, None, bank, c_value=10, depth=200, type='MCTSVS'))
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

def create_game_vs_wl(NUMBER_OF_PLAYERS, mode):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=10, depth=200, type='MCTSVS'))
    players.append(MCTSPlayer(1, None, bank, c_value=1.5, depth=200, type='MCTSWL'))
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

def create_game_vs_lm(NUMBER_OF_PLAYERS, mode):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=10, depth=200, type='MCTSVS'))
    players.append(MCTSPlayer(1, None, bank, c_value=10, depth=200, type='MCTSLM', max_child_nodes=120))
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

def create_game_ed(NUMBER_OF_PLAYERS, mode):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=10, depth=100, type='MCTSED'))
    players.append(RandomPlayer(1, None, bank))
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

def create_game_ed_mcts(NUMBER_OF_PLAYERS, mode):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=10, depth=100, type='MCTSED'))
    players.append(MCTSPlayer(1, None, bank, c_value=10, depth=100))
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

def create_game_ed_vs(NUMBER_OF_PLAYERS, mode):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=10, depth=100, type='MCTSED'))
    players.append(MCTSPlayer(1, None, bank, c_value=10, depth=100, type='MCTSVS'))
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

def create_game_ed_lm(NUMBER_OF_PLAYERS, mode):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=10, depth=100, type='MCTSED'))
    players.append(MCTSPlayer(1, None, bank, c_value=10, depth=100, type='MCTSLM', max_child_nodes=120))
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

def create_game_ed_ws(NUMBER_OF_PLAYERS, mode):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(MCTSPlayer(0, None, bank, c_value=10, depth=100, type='MCTSED'))
    players.append(MCTSPlayer(1, None, bank, c_value=1.5, depth=100, type='MCTSWS'))
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


def get_crystals(NUMBER_OF_PLAYERS):
        if NUMBER_OF_PLAYERS == 2:
            crystals = [4, 5]
        else:
            crystals = [1, 2, 3, 4, 5]
        return crystals

def give_players_crystals(players):
    number_of_players = len(players)
    crystals = get_crystals(number_of_players)
    for i in range(number_of_players):
        crystal = random.choice(crystals)
        crystals.remove(crystal)
        players[i].set_crystal(crystal)

def create_game_randoms(NUMBER_OF_PLAYERS, mode, c_value, depth):
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True, '2')
    bank = Bank(NUMBER_OF_PLAYERS)
    playing_board = PlayingBoard(card_deck)
    # colors = ['red', 'green', 'orange', 'violet', 'blue']

    #here we can define random, MCTS or human players
    players:List[Player] = []
    players.append(RandomPlayer(0, None, bank))
    players.append(RandomPlayer(1, None, bank))
    players[0].crystal = 4
    players[1].crystal = 5
    game_state = GameState(playing_board=playing_board,
                        players=players,
                        card_deck=card_deck,
                        bank=bank, 
                        turn=0,
                        slot_index=0,
                        slots=[],
                        mode=mode)
    game_simulation = Game(game_state, True)
    return game_simulation

def save_scores(results, save_name):
    with open(f'{save_name}.txt', 'w') as file:
        for tup in results:
            try:
                line = ' '.join(map(str, tup)) + '\n'
                file.write(line)
            except:
                continue

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

if __name__ == "__main__":
    # turn = 0
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
    # mode = 0

    
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
    num_simulations = 1
    manager = Manager()
    

    # depths = [50, 100, 150, 200, 250, 300, 350, 400]
    # depth = 200
    # depths = [100]
    # c_values = [0, 1, 1.5, 2, 5, 10, 20, 40, 60, 80, 100]

    start = timer()
    # c_value = 10
    # depth = 100
    # while c_value <= 0:
    # max_child_nodes = [20, 60, 120, 180]
    # max_child_nodes = [10]

    # game_simulation_1 = create_game_ed(NUMBER_OF_PLAYERS, 0)
    # game_simulation_2 = create_game_ed_mcts(NUMBER_OF_PLAYERS, 0)
    # game_simulation_3 = create_game_ed_vs(NUMBER_OF_PLAYERS, 0)
    # game_simulation_4 = create_game_ed_lm(NUMBER_OF_PLAYERS, 0)
    # game_simulation_5 = create_game_ed_ws(NUMBER_OF_PLAYERS, 0)


    

    # game_simulation_2 = create_game_wl_lm(NUMBER_OF_PLAYERS, 0) 
    # sims= [game_simulation_1]
    # for game_simulation in sims:
    # for depth in depths:
        # print(max_child)
        
        
    for i in range(50):
        print(f"SIMULATION {i}")
        # game_simulation = create_game_lm_random(NUMBER_OF_PLAYERS, 0, max_child) 
        # game_simulation = create_game_wl_random(NUMBER_OF_PLAYERS, 0) 
        results = []
        results.append(None)
        game_simulation = create_game_ed(NUMBER_OF_PLAYERS, 0)
        run_game_threaded(game_simulation, results, 0)
        processes = []
        results = manager.list([None] * num_simulations)
        process = Process(target=run_game_threaded, args=(game_simulation, results, i))
        processes.append(process)
        process.start()

        # for process in processes:
        #     process.join()
        now_ts = datetime.now()
        ts = now_ts.strftime('%Y%m%d_%H%M%S')
        save_scores(results=results, save_name=f'Results\\raw\\ed\\ed_random_{ts}')
    # threads = [None] * 10
    # results = [None] * 10
    # for i in range(10):
    #     

    #     for i in range(len(threads)):
    # game_simulation = create_game(NUMBER_OF_PLAYERS, 2)
    # p0, p1 = game_simulation.run_game()
    # results[0] = (p0, p1)
    #         threads[i] = Thread(target=run_game_threaded, args=(game_simulation, results, i))
    #         threads[i].start()
    #     # p0, p1 = game_simulation.run_game()
    #     # results.append((p0, p1))
    # for i in range(len(threads)):
    #     threads[i].join()

    end = timer()
    # interpret_data(results)
    # print_game_results(players, colors)
    print(f"Simulation time: {end - start}")


