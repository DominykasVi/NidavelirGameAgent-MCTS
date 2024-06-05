from copy import deepcopy
import itertools
import math
from multiprocessing import Pool
import random
from typing import Dict, List, Any
from card import Card
from coin import Coin
from game import Game
from timeit import default_timer as timer
import uuid
from game_state import GameState
from Players.random_player import RandomPlayer
from tree_visualizer import Visualizer
from game import Game

class Node:
    def __init__(self, game_state:GameState, depth:int, name:str='', parent=None, constant=None, pw=False, c=2, alpha=0.5, oma=False, eq_param=math.e) -> None:
        self.score = 0
        self.iterations = 0
        self.parent = parent
        self.children = []
        if constant is None:
            self.constant = 2
        else:
            self.constant = constant
        self.game_state = game_state
        self.depth = depth + 1

        self.name = name
        self.obj_name = name
        self.id = str(uuid.uuid4())
        self.child_states = None
        self.meta_information = {}
        self.action = None
        self.pw = pw
        self.c = c
        self.alpha = alpha
        self.oma = oma
        self.mcts = False
        # if oma:
        self.history = hash(0)
        self.eq_param = eq_param

    def find_child_index_by_value(self, max_value):
        for index, node in enumerate(self.children):
            if node.iterations != 0 and node.score / node.iterations == max_value:
                return index
        return -1  # Return -1 if no class matches the max value

    def __str__(self) -> str:
        return f"{self.obj_name}"
    
    def __repr__(self) -> str:
        return f"{self.obj_name}"

    def has_next(self, iterator):
        try:
            next_item = next(iterator)
            return True, itertools.chain([next_item], iterator)
        except StopIteration as e:
            return False, iter([])  # Empty iterator
        except Exception as e2:
            raise(e2)

    def calculate_node_value(self, total_runs:int, hashes:Dict[int, Dict[str, float]]={}) -> int:
        if self.iterations == 0:
            return -1
        if self.oma and self.mcts:
            try:
                e = math.sqrt(self.eq_param / (3*self.iterations) + self.eq_param)
                # print(hashes.keys())
                # print(self.history)
                return e*(hashes[self.history]['scores']/hashes[self.history]['iterations']) + \
                        (1-e)*(self.score/self.iterations) + self.constant * math.sqrt(math.log(total_runs)/self.iterations)
            except Exception as e:
                raise(e)
        else:
            return (self.score/self.iterations) + self.constant * math.sqrt(math.log(total_runs)/self.iterations)
    
    def update_parents(self, score:int) -> None:
        self.iterations += 1
        node = self
        while node.parent is not None:
            self.parent.iterations += 1
            self.parent.score += score
            node = node.parent
        
    def find_max_child_node(self, total_runs:int, hashes:Dict[int, Dict[str, float]]={}, ignore_leftover:bool=False) -> int:
        has_states_unexplored, self.child_states = self.has_next(self.child_states)

        if has_states_unexplored is True and ignore_leftover is False:
            return -1
        else:
            possible_state_scores = [node.calculate_node_value(total_runs, hashes) for node in self.children]
            selected_state = possible_state_scores.index(max(possible_state_scores))
        
        return selected_state
    
    def get_root_node(self, node):
        if node.parent is not None:
            return self.get_root_node(node.parent)
        return node

            
    def generate_child_state(self, mcts_player_index:int):
        states_left, self.child_states = self.has_next(self.child_states)
        if states_left:
            child_object = next(self.child_states)
            new_node = Node(game_state=child_object['state']
                            ,depth=self.depth
                            ,parent=self
                            ,constant=self.constant
                            ,pw = self.pw
                            ,alpha=self.alpha
                            ,c=self.c
                            ,oma=self.oma
                            ,eq_param=self.eq_param)
            self.children.append(new_node)
            new_node.name = child_object['name']
            new_node.obj_name = child_object['name']
            new_node.meta_information = child_object['return']
            if mcts_player_index == child_object['return']['player']:
                new_node.mcts = True
                new_node.history = hash(self.history + hash(child_object['name']))
            return new_node
        # child_object = next(self.child_states)
        raise("No new child state")

    def run_game_simulation(self, new_node, mcts_player_index:int, hashes:Dict[int, Dict[str, int]]=None):
        # if new_node.game_state is None:
        #     print('debug')
        try:
            game = Game(new_node.game_state.copy_state(), False)
        except Exception as err:
            raise(err)
        game_scores = game.run_game()
        new_node.score += game_scores[mcts_player_index]
        if hashes is not None:
            if new_node.history in hashes.keys():
                hashes[new_node.history]['scores'] += new_node.score
                hashes[new_node.history]['iterations'] += 1
            else:
                hashes[new_node.history] = {}
                hashes[new_node.history]['scores'] = new_node.score
                hashes[new_node.history]['iterations'] = 1
        #backpropagation
        new_node.update_parents(new_node.score)

    def progressive_widening(node) -> int:
        t = node.iterations + 1
        k = math.ceil(node.c * t ** node.alpha)
        return k


    def simulate_run(self, total_runs:int, mcts_player_index:int, hashes:Dict[int, Dict[str, int]]):
        #expansion

        if len(self.children) == 0:

            if self.action is not None:
                action_information = (self.action, self.meta_information['player'])
                child_states = self.game_state.get_next_state(action_information)
            else:
                child_states = self.game_state.get_next_state()
            
            if child_states is None:
                self.update_parents(0)
            else:
                self.child_states = child_states
                new_node = self.generate_child_state(mcts_player_index)
                if new_node.meta_information['player'] == mcts_player_index:
                    self.run_game_simulation(new_node, mcts_player_index, hashes) 
                else:
                    new_node.simulate_run(total_runs, mcts_player_index, hashes)
        else:   
            #selection
            selected_state = self.find_max_child_node(total_runs, hashes)
            if self.pw:
                if selected_state == -1:
                    # print(f'{len(self.children)}/{self.progressive_widening()}')
                    if len(self.children) < self.progressive_widening():
                        new_node = self.generate_child_state(mcts_player_index)
                        self.run_game_simulation(new_node, mcts_player_index, hashes)
                    else:
                        selected_state = self.find_max_child_node(total_runs, hashes, ignore_leftover=True)
                        self.children[selected_state].simulate_run(total_runs, mcts_player_index, hashes)
                else:
                    self.children[selected_state].simulate_run(total_runs, mcts_player_index, hashes)
            else:
                if selected_state == -1:
                    new_node = self.generate_child_state(mcts_player_index)
                    self.run_game_simulation(new_node, mcts_player_index, hashes)
                else:
                    self.children[selected_state].simulate_run(total_runs, mcts_player_index, hashes)

class MCTS:
    def __init__(self) -> None:
        self.total_runs = 1
        self.max_iterations = 100
        self.c_value = 0
        self.hashes = {}

    # def save_run_info(self, time):
    #     with open('Results\\raw\\Iterations_runs\\iterations_runs_2.txt', 'a') as f:
    #         f.write(f'{self.max_iterations}_{self.c_value}:{time}\n')
    def remove_generators(node:Node):
        for child in node.children:
            MCTS.remove_generators(child)
        node.child_states = None

    def parallel_function(obj):
        node, index, hashes, total_runs, start = obj
        end = timer()
        while (end-start) < 5:
            try:
                node.simulate_run(total_runs, index, hashes)
            except Exception as e:
                raise(e)
            total_runs += 1
            end = timer()
        MCTS.remove_generators(node)
            
        return node


    def run_parallel(initial_nodes, mcts_index):
        start = timer()
        objects = [(node, mcts_index, {}, 0, start) for node in initial_nodes]
        print(len(initial_nodes))
        with Pool(len(initial_nodes)) as p:
            res = p.map(MCTS.parallel_function, objects)
        return res


    def run_simulation(self, game_state:GameState, mcts_player_index:int
                       ,pw:bool=False, alpha=0.5, c=2
                       ,oma=False, eq_param:float = math.e
                       ,parallel=False) -> Node:
        self.total_runs = 0
        start = timer()

        return_type = game_state.players[mcts_player_index].action_to_perform
        self.max_iterations = game_state.players[mcts_player_index].depth
        self.c_value = game_state.players[mcts_player_index].c_value

        for player in game_state.players:
            if player.player_type == 'MCTS':
                bet_made = game_state.players[player.index].bet_made
                card_taken = game_state.players[player.index].card_taken
                distinction_cards = game_state.players[player.index].distinction_cards
                game_state.players[player.index] = RandomPlayer(index=player.index,
                                                              crystal=game_state.players[player.index].crystal,
                                                              bank_reference=game_state.players[player.index].bank,
                                                              coins=game_state.players[player.index].coins,
                                                              bets=game_state.players[player.index].bets,
                                                              left_over=game_state.players[player.index].left_over_coins,
                                                              card_deck=game_state.players[player.index].card_deck)
                game_state.players[player.index].bet_made = bet_made
                game_state.players[player.index].card_taken = card_taken
                game_state.players[player.index].distinction_cards = distinction_cards
        game_state.mode = -1

        root_node = Node(game_state, 0, 'Root', constant=self.c_value, pw=pw, alpha=alpha, c=c, oma=oma, eq_param=eq_param)
        root_node.action = return_type
        root_node.meta_information = {'action':'None', 'player':mcts_player_index}
        # for i in range(self.max_iterations):
        end = timer()
        if parallel:
            action_information = (root_node.action, root_node.meta_information['player'])
            child_states = root_node.game_state.get_next_state(action_information)
            root_node.child_states = child_states
            new_nodes = []
            generate_states = True
            while generate_states:
                generate_states, root_node.child_states = root_node.has_next(root_node.child_states)
                if not generate_states:
                    break
                new_node = root_node.generate_child_state(mcts_player_index)
                new_node.parent = None
                new_nodes.append(new_node)
            root_node.children = []
            results = MCTS.run_parallel(new_nodes, mcts_player_index)
            for res in results:
                root_node.children.append(res)
                res.parent = root_node
        else:
            for i in range(self.max_iterations):
                try:
                    root_node.simulate_run(self.total_runs, mcts_player_index, self.hashes)
                except Exception as e:
                    raise(e)
                self.total_runs += 1
        # print(f"Simulation of {self.total_runs} took: {end - start}")
        
        viz = Visualizer(root_node, f'{str(game_state.game_id)}/{root_node.game_state.turn}_{root_node.game_state.slot_index}_{return_type}')
        viz.visualize()

        # self.save_run_info(end - start)
        return_index = -1
        return_node = root_node
        try:
            while return_type != return_node.meta_information['action'] or mcts_player_index != return_node.meta_information['player']: 
                possible_scores = [node.score/node.iterations for node in return_node.children if node.meta_information['action'] == return_type if node.iterations != 0]
                if len(possible_scores) == 0:
                    print('Partial Fail')
                    return_node = random.choice(return_node.children)
                    break
                return_index = return_node.find_child_index_by_value(max(possible_scores))
                return_node = return_node.children[return_index]
        except Exception as e:
            raise(e)

        return return_node
