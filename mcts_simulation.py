from copy import deepcopy
import itertools
import math
from typing import List, Any
from card import Card
from coin import Coin
from game import Game
from timeit import default_timer as timer
import uuid
from game_state import GameState
from Players.random_player import RandomPlayer
from tree_visualizer import Visualizer

class Node:
    def __init__(self, game_state:GameState, depth:int, name:str='', parent=None, constant=None) -> None:
        self.score = 0
        self.iterations = 0
        self.parent = parent
        self.children = []
        if constant is None:
            self.constant = 2
        else:
            self.constant = constant
        # self.value = self.calculate_node_value(1)
        self.game_state = game_state
        self.child_bets = None
        self.child_bet_player_index = None
        self.name = name
        self.obj_name = name
        self.id = str(uuid.uuid4())
        self.child_takes = None
        self.depth = depth + 1

        self.coin_increased = False
        self.in_bets = False
        self.coin_to_be_increased = None

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
        except Exception:
            return False, iter([])  # Empty iterator

    def calculate_node_value(self, total_runs:int) -> int:
        if self.iterations == 0:
            return -1
        return (self.score/self.iterations) + self.constant * math.sqrt(math.log(total_runs)/self.iterations)
    
    def update_parents(self, score:int) -> None:
        self.iterations += 1
        node = self
        while node.parent is not None:
        # if self.parent is not None:
            self.parent.iterations += 1
            self.parent.score += score
            node = node.parent
            # self.parent.update_parents(score)
        
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
            child_node.obj_name = f'Player{self.child_bet_player_index}_' + 'bet_' + f' {new_bet}'
            return 
        raise("No bet generated")
        # if new_game_state is None:
        #     print('debug')
        # return
    def get_root_node(self, node):
        if node.parent is not None:
            return self.get_root_node(node.parent)
        return node
    
    def simulate_coin_incease(self, player_coin:Coin, coin_card:Card, new_game_state:GameState, player_index:int, in_bets:bool, slot_index:int) -> GameState:
        new_state = new_game_state.copy_state()
        new_state.players[player_index].card_deck.add_card(coin_card)

        new_coin_value = new_state.bank.take_coin((player_coin.value+coin_card.value))
        new_coin = Coin(new_coin_value)

        if in_bets:
            coin_index = new_state.players[player_index].bets.index(player_coin)
            new_state.players[player_index].bets[coin_index] = new_coin
        elif in_bets==False:
            new_state.players[player_index].left_over_coins.remove(player_coin)
            new_state.players[player_index].left_over_coins.append(new_coin)

        new_state.players[player_index].coins.remove(player_coin)
        new_state.players[player_index].coins.append(new_coin)
        
        if slot_index != 0:
            new_state.slots[slot_index].remove(coin_card)
            new_state.players[player_index].make_coin_exchange(slot_index-1)

        new_state.players[player_index].cards_taken += 1
        new_state.players[player_index].card_taken = True
        return new_state
    
    def generate_increase_coin_state(self, new_node, bet:Coin, in_bets:bool, player_index:int, coin_card:Card, new_game_state:GameState, slot_index:int):
        new_node.coin_increased = True
        new_node.coin_to_be_increased = bet
        new_node.in_bets = in_bets
        # return cards_to_choose, card_to_take
        new_node.name = f'Player{player_index}\n' + 'Take: ' + f' {coin_card}, increase {bet}'
        new_node.obj_name = f'Player{player_index}_' + 'take_' + f' {coin_card}_increase_{bet}'
        new_state = self.simulate_coin_incease(bet, coin_card, new_game_state, player_index, in_bets, slot_index)
        new_node.game_state = new_state

        
    def generate_increase_coin_states(self, coin:Card, slot_index:int, root_node, new_game_state:GameState, player_index:int, additional_cards=None):
        child_node = root_node
        root_node = root_node.parent
        coins_taken = 0

        if additional_cards is not None:
            for bet in new_game_state.players[player_index].coins:
                if bet.exchangeable == False:
                    if coins_taken != 0:
                        new_node = Node(None, root_node.depth, constant=self.constant)
                        new_node.parent = root_node
                        root_node.children.append(new_node)
                    else:
                        new_node = child_node
                    # meta parameters
                    in_bets=None
                    self.generate_increase_coin_state(new_node, bet, in_bets, player_index, coin, new_game_state, slot_index)
                    if additional_cards is not None:
                        for additional_card in additional_cards:
                            new_node.game_state.playing_board.card_deck.add_card(additional_card)
                    if coins_taken != 0:
                        self.run_game_simulation(new_node, player_index)
                    coins_taken += 1
        # for bet in new_game_state.players[player_index].coins:
        for bet in new_game_state.players[player_index].bets:
            if bet.exchangeable == False:
                if coins_taken != 0:
                    new_node = Node(None, root_node.depth, constant=self.constant)
                    new_node.parent = root_node
                    root_node.children.append(new_node)
                else:
                    new_node = child_node
                # meta parameters
                self.generate_increase_coin_state(new_node, bet, True, player_index, coin, new_game_state, slot_index)
                if additional_cards is not None:
                    for additional_card in additional_cards:
                        new_node.game_state.playing_board.card_deck.add_card(additional_card)
                if coins_taken != 0:
                    self.run_game_simulation(new_node, player_index)
                coins_taken += 1

        for bet in new_game_state.players[player_index].left_over_coins:
            if bet.exchangeable == False:
                new_node = Node(None, root_node.depth, constant=self.constant)
                new_node.parent = root_node
                root_node.children.append(new_node)
                self.generate_increase_coin_state(new_node, bet, False, player_index, coin, new_game_state, slot_index)
                if additional_cards is not None:
                    for additional_card in additional_cards:
                        new_node.game_state.playing_board.card_deck.add_card(additional_card)
                self.run_game_simulation(new_node, player_index)
                coins_taken += 1

    def generate_new_take_state(self, child_node, new_game_state):
        for card in self.child_takes:

            if card[0].color == 'coin':
                self.generate_increase_coin_states(card[0], new_game_state.slot_index, child_node, new_game_state, self.child_take_player_index) 
            else:
                # taken_card = self.take_card(player, bet_index)
                bet_index = new_game_state.slot_index - 1
                # TODO: nned to somehow handle coin increase
                new_game_state.slots[new_game_state.slot_index], taken_card = new_game_state.players[self.child_take_player_index]\
                                                                                    .take_card(new_game_state.slots[new_game_state.slot_index], card[0]) #MCTS decision
                new_game_state.players[self.child_take_player_index].make_coin_exchange(bet_index)
                child_node.game_state = new_game_state
                child_node.name = f'Player{self.child_take_player_index}\n' + 'Take: ' + f' {card[0]}'
                child_node.obj_name = f'Player{self.child_take_player_index}_' + 'take_' + f' {card[0]}'
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
            child_node.obj_name = f'Generated slots {new_game_state.slots}'
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
            new_node = Node(None, self.depth, constant=self.constant)
            new_node.parent = self
            self.children.append(new_node)
            self.generate_new_bet_state(new_node)
            if new_node.game_state is None:
                print('debug')
            return new_node
        takes_left, self.child_takes = self.has_next(self.child_takes)
        if takes_left == True:
            new_node = Node(None, self.depth, constant=self.constant)
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
            if new_node.game_state is None:
                print('debug')
            return new_node
        slots_left, self.child_slots = self.has_next(self.child_slots)
        if slots_left == True:
            new_node = Node(None, self.depth, self.constant)
            new_node.parent = self
            self.children.append(new_node)
            new_game_state = self.game_state.copy_state()
            self.generate_new_slots_state(new_node, new_game_state)
            if new_node.game_state is None:
                print('debug')
            return new_node
        raise("No new child state")

    def run_game_simulation(self, new_node, mcts_player_index):
        # if new_node.game_state is None:
        #     print('debug')
        try:
            game = Game(new_node.game_state.copy_state(), False)
        except Exception as err:
            raise(err)
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
                new_node = Node(self.game_state, self.depth, constant=self.constant)
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
        self.c_value = 0

    def handle_special_case(self, root_node:Node, special_case, mcts_player_index):
        if special_case[0] == 'distinction_selection':
            root_node.child_takes = itertools.permutations(special_case[1], 1)
            root_node.child_take_player_index = mcts_player_index
            card_array = deepcopy(special_case[1])
            # self.generate_new_take_state(child_node, new_game_state)
            for card in root_node.child_takes:
                iteration_cards = deepcopy(card_array)
                new_node = Node(root_node.game_state, root_node.depth, constant=root_node.constant)
                new_node.parent = root_node
                root_node.children.append(new_node)
                new_game_state = root_node.game_state.copy_state()
                # bet_index = new_game_state.slot_index - 1
                # TODO: nned to somehow handle coin increase
                if card[0].color == 'coin':
                    root_node.generate_increase_coin_states(card[0], new_game_state.slot_index, new_node, new_game_state, mcts_player_index, additional_cards=iteration_cards)

                else:
                    left_cards, _ = new_game_state.players[mcts_player_index]\
                                        .take_card(iteration_cards, taken_card=card[0])
                    for left_card in left_cards:
                        new_game_state.playing_board.card_deck.add_card(left_card)
                    new_game_state.players[mcts_player_index].distinction_cards += 1
                    new_node.game_state = new_game_state
                    new_node.name = f'Player{root_node.child_take_player_index}\n' + 'Take: ' + f' {card[0]}'
                    new_node.obj_name = f'Player{root_node.child_take_player_index}_' + 'take_' + f' {card[0]}'

                root_node.run_game_simulation(new_node, mcts_player_index) 

    def save_run_info(self, time):
        with open('Results\\raw\\Iterations_runs\\iterations_runs_2.txt', 'a') as f:
            f.write(f'{self.max_iterations}_{self.c_value}:{time}\n')


    def run_simulation(self, game_state:GameState, mcts_player_index:int, special_case=None) -> GameState:
        start = timer()

        return_type = game_state.players[mcts_player_index].action_to_perform
        return_player = f'Player{mcts_player_index}'
        self.max_iterations = game_state.players[mcts_player_index].depth
        c_val = game_state.players[mcts_player_index].c_value
        self.c_value = c_val

        for player in game_state.players:
            if player.player_type == 'MCTS':
                bet_made = game_state.players[player.index].bet_made
                card_taken = game_state.players[player.index].card_taken
                game_state.players[player.index] = RandomPlayer(index=player.index,
                                                              crystal=game_state.players[player.index].crystal,
                                                              bank_reference=game_state.players[player.index].bank,
                                                              coins=game_state.players[player.index].coins,
                                                              bets=game_state.players[player.index].bets,
                                                              left_over=game_state.players[player.index].left_over_coins,
                                                              card_deck=game_state.players[player.index].card_deck)
                game_state.players[player.index].bet_made = bet_made
                game_state.players[player.index].card_taken = card_taken
                game_state.mode = 0


        root_node = Node(game_state, 0, 'Root', constant=c_val)
        
        if special_case is not None:
            self.handle_special_case(root_node, special_case, mcts_player_index)

        visualize = False
        # for key in game_state.slots.keys():
        #     for card in game_state.slots[key]:
        #         if card.color == 'coin':
        for i in range(self.max_iterations):
            root_node.simulate_run(self.total_runs, mcts_player_index)
            self.total_runs += 1
        end = timer()
        self.save_run_info(end - start)
        # print(f"Simulation of {self.total_runs} took: {end - start}")
        return_index = -1
        return_node = root_node
        try:
            while return_type not in return_node.name or return_player not in return_node.name: 
                possible_scores = [node.score/node.iterations for node in return_node.children]
                return_index = return_node.find_child_index_by_value(max(possible_scores))
                return_node = return_node.children[return_index]
        except Exception as e:
            raise(e)
        # if visualize:
        # viz = Visualizer(root_node)
        # viz.visualize()
        # root_children = len(root_node.children)
        if return_node.coin_increased == True:
            return_node.game_state.increase_meta_variable = {'in_bets': return_node.in_bets, 'coin': return_node.coin_to_be_increased}

        # possible_combs = [i for i in itertools.permutations(game_state.players[mcts_player_index].coins, 3)]
        # child_combs = [child.game_state.players[mcts_player_index].bets for child in root_node.children]
        # print(root_children)
        # print(possible_combs)
        # print(child_combs)
        self.total_runs = 1
        return return_node.game_state
        # return root_node.children[return_index].game_state 
