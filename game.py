import os
from typing import List
from bank import Bank
from card import Card
from card_deck import CardDeck
from coin import Coin
from Players.player import Player

import random
from game_state import GameState

from playing_board import PlayingBoard



class Game:
    def calculate_turn_split(self) -> int:
        if self.NUMBER_OF_PLAYERS < 4:
            return 4
        else:
            return 3

                # players.append(Player(f"Player {i+1}", crystal, bank))

    def __init__(self, game_state:GameState, initialize=False) -> None:
        # SEED = 10
        self.players = game_state.players
        self.NUMBER_OF_PLAYERS = len(self.players)
        # if initialize:
        #     self.give_players_crystals(self.players)
        # random.seed(SEED)#?? ar reikalingas
        self.card_deck = game_state.deck
        self.bank = game_state.bank
        self.playing_board = game_state.playing_board
        self.turn = game_state.turn
        self.turn_split = self.calculate_turn_split()
        self.mode = game_state.mode
        self.slots = game_state.slots
        self.slot_index = game_state.slot_index

    def get_possible_game_states(self):
        if self.turn > self.turn_split*2:
            raise Exception(f"Illegal game state {self.turn} reached")
        if self.turn == self.turn_split*2:
            return []
        if self.slots == []:
            pass
            # return self.playing_board.generate_possible_slots()
        else:
            pass
            # return self.generate_possible_bet_slot_variations(self.slot_index, known_player_bets, know_player_coins)

    def generate_slots(self):
        self.slots = self.playing_board.generate_slots(self.turn_split, self.turn)
        self.slot_index = 1
        self.print_function(str(self.slots))

    def create_game_state(self) -> GameState:
        return GameState(playing_board=self.playing_board,
                         players=self.players,
                         card_deck=self.card_deck,
                         bank=self.bank,
                         turn=self.turn,
                         slot_index=self.slot_index,
                         slots=self.slots,
                         mode=self.mode)

    def make_player_bets(self):
        for player in self.players:
            # if player.player_type == 'MCTS':
            #     print('debug')
            if len(player.bets) == 0:
                game_state = self.create_game_state()
                if sorted(game_state.players[1].coins, key= lambda x: x.value) != sorted(self.players[1].coins, key= lambda x: x.value):
                    raise('Players coins are not equal')
                player.make_bet(self.slots, game_state) #MCTS decision 

    def take_card(self, player:Player, bet_index:int) -> Card:
        game_state = self.create_game_state()
        self.slots[self.slot_index], taken_card = player.take_card(self.slots[self.slot_index], game_state=game_state) #MCTS decision
        player.make_coin_exchange(bet_index)
        return taken_card

##################################################################################################################
    def run_game(self):
        while self.turn < self.turn_split*2:
            # in halfway point we award bonuses to players, no decision needed
            
            if self.slot_index == 0:

                self.print_function(f"Turn {self.turn}")

                if self.turn == self.turn_split:
                    self.print_function("Granting players distinction bonuses")
                    self.award_distinction_cards(self.players, self.playing_board)

            # take cards which will be shown to players
                self.generate_slots()

            # here we can have update player function, which to MCTS player would pass the game state
            # for player in self.players:
            #     player.update_state(self.card_deck, self.players, self.bank, self.turn)
            self.make_player_bets()
            # else:
            #     self.check_if_bets_need_to_be_made()



            # for slot_index in self.slots.keys():
            while self.slot_index < 4:
                bet_index = self.slot_index - 1
                
                self.print_function(f"Turn {self.turn}")
                self.print_player_bets()
                self.print_function(f"SLOT {self.slot_index} : {self.slots[self.slot_index]}")

                player_queue = self.create_player_queue(bet_index)

                self.print_function(f"Player turns: {player_queue}")
                    
                for player in player_queue:
                    self.print_function(str(player))
                    if player.card_taken == False:
                        taken_card = self.take_card(player, bet_index)

                        self.print_function(f"Taken card {taken_card}")
                        self.breakpoint()
                    self.print_function(f"{player} coins: {player.coins}, {player.bets}, {player.left_over_coins}")
                for player in player_queue:
                    player.card_taken = False
                # TODO: modify to depend on player count
                if self.players[0].bets[bet_index] == self.players[1].bets[bet_index]:
                    self.exchange_crystals_two_players(self.players)
                
                # self.slots.pop(slot_index)
                self.slot_index += 1
                self.clear_console()


            self.slots.clear()
            self.slot_index = 0
            self.turn += 1

            for player in self.players:
                player.remove_bets()
            if self.turn == self.turn_split*2:
                red_highest_players = self.get_player_with_highest_count(self.players, 'red')
                for player in red_highest_players:
                    player.add_red_bonus()
        return [player.get_player_points() for player in self.players]
##################################################################################################################


    def award_distinction_cards(self, players:List[Player], playing_board:PlayingBoard) -> None:
        colors = ['red', 'green', 'orange', 'violet', 'blue']
        for color in colors:
            distinguished_players = self.get_player_with_highest_count(players,color)
            self.print_players_color_count(players, color)
            if len(distinguished_players) == 1:
                self.add_bonus_to_distinguished(distinguished_players[0], color, playing_board)

    def create_player_queue(self, slot_number:int) -> List[Player]:
        player_queue = []

        helper_dict = {}
        for player in self.players:
            try:
                bet = player.bets[slot_number].value
                if bet in helper_dict.keys():
                    helper_dict[bet].append(player)
                else:
                    helper_dict[bet] = [player]
            except:
                raise("DEBUG ERROR")
        sorted_helper_dict = dict(sorted(helper_dict.items(), reverse=True))
        # print(sorted_helper_dict)

        for key in sorted_helper_dict.keys():
            if len(sorted_helper_dict[key]) > 1:
                sorted_players = self.sort_players_by_crystal(sorted_helper_dict[key])
                player_queue.extend(sorted_players)
            else:
                player_queue.extend(sorted_helper_dict[key])

        return player_queue
    
    def sort_players_by_crystal(self, players:List[Player]) -> List[Player]:
        if len(players) == 2:
            if players[0].crystal > players[1].crystal:
                # self.exchange_crystals_two_players(players)
                return [players[0], players[1]]
            else:
                # self.exchange_crystals_two_players(players)
                return [players[1], players[0]]
            
    def exchange_crystals_two_players(self, players:List[Player]) -> None:
        if players[0].crystal != 6 and players[1].crystal != 6:
            temp = players[0].crystal
            players[0].crystal = players[1].crystal
            players[1].crystal = temp

    def get_player_with_highest_count(self, players:List[Player], color:str) -> Player:
        max_count = players[0].get_color_count(color)
        max_player = players[0]
        max_players = [players[0]]

        for player in players:
            new_count = player.get_color_count(color)
            if new_count > max_count:
                max_count = new_count
                max_player = player
                max_players = [player]
            elif new_count == max_count and player != max_player:
                max_players.append(player)

            
        return max_players

    def add_bonus_to_distinguished(self, player:Player, color:str, playing_board:PlayingBoard) -> None:
        self.print_function(f"Distinction card count: {player.distinction_cards}")
        if player.distinction_cards == 0:
            self.print_function(f"Giving bonus to player: {player}")
            if color == 'red':
                player.distinction_cards += 1
            elif color =='green':
                player.remove_zero_coin()
                player.coins.append(Coin(3, True))
                player.distinction_cards += 1
            elif color == 'orange':
                player.crystal = 6
                player.distinction_cards += 1
            elif color == 'violet':
                player.add_card(Card('violet', 'None', 0, 101))
                player.add_card(Card('violet', 'None', 0, 102))
                player.distinction_cards += 1
            elif color == 'blue':
                card_to_choose_from = playing_board.get_number_of_cards(3, playing_board.card_deck.get_age_two_cards())
                game_state = self.create_game_state()
                left_cards, _ = player.take_card(card_to_choose_from, game_state=game_state, special_case='distinction')
                for card in left_cards:
                    playing_board.card_deck.add_card(card)
                player.distinction_cards += 1
    
        
 #Helper output functions       
    def print_players_color_count(self, players:List[Player], color):
        if self.mode > 0:
            print(f"Players have number of {color}")
            for player in players:
                print(player, ": ", player.get_color_count(color))

    def print_player_bets(self):
        if self.mode > 0:
            for player in self.players:
                print(f"{player}, bets: ", player.bets, "lefover: ", player.left_over_coins)

    
    def print_score(self):
        if self.mode > 0:
            for player in self.players:
                player.print_player_points()

    def clear_console(self) -> None:
        if self.mode == 1:
            clear = lambda: os.system('cls')
            clear()

    def breakpoint(self) -> None:
        if self.mode == 1:
            input()

    def print_function(self, text:str) -> None:
        if self.mode > 0:
            print(text)

