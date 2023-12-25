from copy import deepcopy
import itertools
import math
from typing import List, Any
from game import Game
from timeit import default_timer as timer
import uuid
from game_state import GameState
from Players.random_player import RandomPlayer
from tree_visualizer import Visualizer

class Node:
    def __init__(self, game_state:GameState, depth:int, name:str='', parent=None) -> None:
        self.score = 0
        self.iterations = 0
        self.parent = parent
        self.children = []
        self.constant = 2
        # self.value = self.calculate_node_value(1)
        self.game_state = game_state
        self.child_bets = None
        self.child_bet_player_index = None
        self.name = name
        self.id = str(uuid.uuid4())
        self.child_takes = None
        self.depth = depth + 1

    def has_next(self, iterator):
        try:
            next_item = next(iterator)
            return True, itertools.chain([next_item], iterator)
        except Exception:
            return False, iter([])  # Empty iterator

    def calculate_node_value(self, total_runs:int) -> int:
        if self.iterations == 0:
            return -1
        return (self.score/self.iterations) + self.constant * math.sqrt(math.log(total_runs)/self.iterations)
    
    def update_parents(self, score:int) -> None:
        self.iterations += 1
        if self.parent is not None:
            self.parent.iterations += 1
            self.parent.score += score
            self.parent.update_parents(score)
        
    def find_max_child_node(self, total_runs:int) -> int:
        has_states_unexplored = False

        if has_states_unexplored == False:
            has_states_unexplored, self.child_bets = self.has_next(self.child_bets)
        if has_states_unexplored == False:
            has_states_unexplored, self.child_takes = self.has_next(self.child_takes)

        if has_states_unexplored is True:
            return -1
        else:
            possible_state_scores = [node.calculate_node_value(total_runs) for node in self.children]
            selected_state = possible_state_scores.index(max(possible_state_scores))
        
        return selected_state
    
    def generate_new_bet_state(self, child_node):
        for bet in self.child_bets:
            new_game_state = self.game_state.copy_state()
            new_bet = [val for val in bet]
            # print(new_bet)
            new_game_state.players[self.child_bet_player_index].make_bet(None, None, new_bet)
            child_node.game_state = new_game_state
            child_node.name = f'Player{self.child_bet_player_index}\n' + 'Bet: ' + f' {new_bet}'
            return 
        # if new_game_state is None:
        #     print('debug')
        # return

    def generate_new_take_state(self, child_node, new_game_state):
        for card in self.child_takes:
            # taken_card = self.take_card(player, bet_index)
            bet_index = new_game_state.slot_index - 1
            # TODO: nned to somehow handle coin increase
            new_game_state.slots[new_game_state.slot_index], taken_card = new_game_state.players[self.child_take_player_index]\
                                                                                .take_card(new_game_state.slots[new_game_state.slot_index], card[0]) #MCTS decision
            new_game_state.players[self.child_take_player_index].make_coin_exchange(bet_index)
            child_node.game_state = new_game_state
            child_node.name = f'Player{self.child_take_player_index}\n' + 'Take: ' + f' {card[0]}'
            return 
    
    def generate_new_slots_state(self, child_node, new_game_state):
        new_game_state.slots.clear()
        new_game_state.turn += 1
        new_game_state.slot_index = 1
        # new_game_state.slots = 1

        for player in new_game_state.players:
            player.remove_bets()
            player.card_taken = False

        for slots in self.child_slots:
            # TODO: should work with more players
            slots_formated  = {1:list(slots[:3]), 2:list(slots[3:6]), 3:list(slots[6:])}
            new_game_state.slots = slots_formated
            child_node.game_state = new_game_state
            child_node.name = f'Generated slots {new_game_state.slots}'
            return
    
    def update_state(self, new_state, child_node):
        if new_state['type'] == 'bets':
            self.child_bets = new_state['value']
            self.child_bet_player_index = new_state['player_index']
            self.generate_new_bet_state(child_node)
        if new_state['type'] == 'take':
            self.child_takes = new_state['value']
            self.child_take_player_index = new_state['player_index']
            new_game_state = self.game_state.copy_state()
            self.generate_new_take_state(child_node, new_game_state)
        if new_state['type'] == 'next_slot':
            self.child_takes = new_state['value']
            self.child_take_player_index = new_state['player_index']
            new_game_state = self.game_state.copy_state()

            #Advancing slots and resetting card taken
            new_game_state.slot_index += 1
            for player in new_game_state.players:
                if player.index != self.child_take_player_index:
                    player.card_taken = False

            self.generate_new_take_state(child_node, new_game_state)
        if new_state['type'] == 'next_slots':
            self.child_slots = new_state['value']
            # self.child_bet_player_index = new_state['player_index']
            new_game_state = self.game_state.copy_state()
            self.generate_new_slots_state(child_node, new_game_state)
            

        # if new_state['type'] == 'take':
        #     self.child_takes = new_state['value']
        #     self.child_take_player_index = new_state['player_index']
        #     self.generate_new_take_state(child_node)

            
    def generate_child_state(self):
        # if next(self.child_bets) is None:
        #     print('debug')
        bets_left, self.child_bets = self.has_next(self.child_bets)
        if bets_left == True:
            new_node = Node(None, self.depth)
            new_node.parent = self
            self.children.append(new_node)
            self.generate_new_bet_state(new_node)
            # if new_node.game_state is None:
            #     print('debug')
            return new_node
        takes_left, self.child_takes = self.has_next(self.child_takes)
        if takes_left == True:
            new_node = Node(None, self.depth)
            new_node.parent = self
            self.children.append(new_node)
            new_game_state = self.game_state.copy_state()

            # TODO: should depend on player count
            if len(new_game_state.slots[new_game_state.slot_index]) < 2:
                new_game_state.slot_index += 1
                for player in new_game_state.players:
                    if player.index != self.child_take_player_index:
                        player.card_taken = False

            self.generate_new_take_state(new_node, new_game_state)
            return new_node
        slots_left, self.child_slots = self.has_next(self.child_slots)
        if slots_left == True:
            new_node = Node(None, self.depth)
            new_node.parent = self
            self.children.append(new_node)
            new_game_state = self.game_state.copy_state()
            self.generate_new_slots_state(new_node, new_game_state)
            return new_node
        raise("No new child state")

    def run_game_simulation(self, new_node, mcts_player_index):
        # if new_node.game_state is None:
        #     print('debug')
        game = Game(new_node.game_state.copy_state(), False)
        game_scores = game.run_game()
        new_node.score += game_scores[mcts_player_index]
        #backpropagation
        new_node.update_parents(new_node.score)

    def simulate_run(self, total_runs:int, mcts_player_index:int):
        #expansion
        if len(self.children) == 0:
            new_state = self.game_state.get_next_state()
            if new_state is None:
                return
                # new_node.update_parents(0)
            else:
                new_node = Node(self.game_state, self.depth)
                new_node.parent = self
                self.children.append(new_node)
                #simulation
                self.update_state(new_state, new_node)
                self.run_game_simulation(new_node, mcts_player_index)  
        else:   
            #selection
            selected_state = self.find_max_child_node(total_runs)
            if selected_state == -1:
                new_node = self.generate_child_state()
                self.run_game_simulation(new_node, mcts_player_index)
            else:
                self.children[selected_state].simulate_run(total_runs, mcts_player_index)

class MCTS:
    def __init__(self) -> None:
        self.total_runs = 1
        self.max_iterations = 100

    def handle_special_case(self, root_node:Node, special_case, mcts_player_index):
        if special_case[0] == 'distinction_selection':
            root_node.child_takes = itertools.permutations(special_case[1], 1)
            root_node.child_take_player_index = mcts_player_index
            card_array = deepcopy(special_case[1])
            # self.generate_new_take_state(child_node, new_game_state)
            for card in root_node.child_takes:
                iteration_cards = deepcopy(card_array)
                new_node = Node(root_node.game_state, root_node.depth)
                new_node.parent = root_node
                root_node.children.append(new_node)
                new_game_state = root_node.game_state.copy_state()
                # bet_index = new_game_state.slot_index - 1
                # TODO: nned to somehow handle coin increase
                
                left_cards, _ = new_game_state.players[mcts_player_index]\
                                    .take_card(iteration_cards, taken_card=card[0])
                for left_card in left_cards:
                    new_game_state.playing_board.card_deck.add_card(left_card)
                new_game_state.players[mcts_player_index].distinction_cards += 1
                new_node.game_state = new_game_state
                new_node.name = f'Player{root_node.child_take_player_index}\n' + 'Take: ' + f' {card[0]}'
                root_node.run_game_simulation(new_node, mcts_player_index) 

    def run_simulation(self, game_state:GameState, mcts_player_index:int, special_case=None) -> GameState:
        start = timer()
 
        game_state.players[mcts_player_index] = RandomPlayer(index=mcts_player_index,
                                                              crystal=game_state.players[mcts_player_index].crystal,
                                                              bank_reference=game_state.players[mcts_player_index].bank,
                                                              coins=game_state.players[mcts_player_index].coins,
                                                              bets=game_state.players[mcts_player_index].bets,
                                                              left_over=game_state.players[mcts_player_index].left_over_coins,
                                                              card_deck=game_state.players[mcts_player_index].card_deck)
        root_node = Node(game_state, 0, 'Root')
        if special_case is not None:
            self.handle_special_case(root_node, special_case, mcts_player_index)
        for i in range(self.max_iterations):
            # print("Iteration: ", i)
            # if i == 60:
            #     print('debug 60')
            root_node.simulate_run(self.total_runs, mcts_player_index)
            # viz = Visualizer(root_node)
            # viz.visualize()
            self.total_runs += 1
        end = timer()
        print(f"Simulation of {self.total_runs} took: {end - start}")
        return_index = root_node.find_max_child_node(self.total_runs)
        # viz = Visualizer(root_node)
        # viz.visualize()
        # root_children = len(root_node.children)
        # possible_combs = [i for i in itertools.permutations(game_state.players[mcts_player_index].coins, 3)]
        # child_combs = [child.game_state.players[mcts_player_index].bets for child in root_node.children]
        # print(root_children)
        # print(possible_combs)
        # print(child_combs)
        self.total_runs = 1
        return root_node.children[return_index].game_state 
