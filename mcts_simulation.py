import math
from typing import List, Any
from game import Game

from game_state import GameState

class Node:
    def __init__(self, game_state:GameState, parent=None) -> None:
        self.score = 0
        self.iterations = 0
        self.parent = parent
        self.children = []
        self.constant = 2
        self.value = self.calculate_node_value()
        self.game_state = game_state
        self.child_bets = None
        self.child_bet_player_index = None

    def calculate_node_value(self, total_runs:int) -> int:
        if self.iterations == 0:
            return -1
        return (self.score/self.iterations) + self.constant * math.sqrt(math.log(total_runs)/self.iterations)
    
    def update_parents(self, score:int) -> None:
        self.iterations += 1
        if self.parent is not None:
            self.parent.iterations += 1
            self.parent.score += score
            self.parent.update_parents()
        
    def find_max_child_node(self) -> int:
        if next(self.child_bets) is not None:
            return -1
        else:
            possible_state_scores = [node.calculate_node_value() for node in self.children]
            selected_state = possible_state_scores.index(max(possible_state_scores))
        
        return selected_state
    
    def generate_new_bet_state(self, child_node):
        for bet in self.child_bets:
            new_game_state = self.game_state.copy_state()
            new_game_state.players[self.child_bet_player_index].bets = bet
            child_node.game_state = new_game_state
            return
    
    def update_state(self, new_state, child_node):
        if new_state['type'] == 'bets':
            self.child_bets = new_state['value']
            self.child_bet_player_index = new_state['player_index']
            self.generate_new_bet_state(child_node)
            
    def generate_child_state(self):
        if next(self.child_bets) is not None:
            new_node = Node()
            new_node.parent = self
            self.children.append(new_node)
            self.generate_new_bet_state(new_node)
            return new_node

    def run_game_simulation(self, new_node, mcts_player_index):
        game = Game(new_node.game_state.copy_state(), False)
        new_node.score += game.run_game()[mcts_player_index]
        #backpropagation
        new_node.update_parents(new_node.score)

    def simulate_run(self, total_runs:int, mcts_player_index:int):
        #expansion
        if len(self.children) == 0:
            new_state = self.game_state.get_next_state()
            if new_state is None:
                new_node.update_parents(0)
            else:
                new_node = Node()
                new_node.parent = self
                self.children.append(new_node)
                #simulation
                self.update_state(new_state, new_node)
                self.run_game_simulation(new_node, mcts_player_index)
                
        else:   
            #selection
            selected_state = self.find_max_child_node()
            if selected_state == -1:
                new_node = self.generate_child_state()
                self.run_game_simulation(new_node, mcts_player_index)
            else:
                self.children[selected_state].simulate_run()

class MCTS:
    def __init__(self) -> None:
        self.total_runs = 1
        self.max_iterations = 100

    def run_simulation(self, game_state:GameState, mcts_player_index):
        root_node = Node(game_state)
        for _ in range(self.max_iterations):
            root_node.simulate_run(self.total_runs, mcts_player_index)
            self.total_runs += 1
        return_index = root_node.find_max_child_node()
        return root_node.children[return_index] 
