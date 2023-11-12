import os
from typing import List
from bank import Bank
from card import Card
from card_deck import CardDeck
from coin import Coin
from Players.player import Player

import random

from playing_board import PlayingBoard



class Game:
    def get_crystals(self, NUMBER_OF_PLAYERS):
        if NUMBER_OF_PLAYERS == 2:
            crystals = [4, 5]
        else:
            crystals = [1, 2, 3, 4, 5]
        return crystals
    
    def give_players_crystals(self, players):
            number_of_players = len(players)
            crystals = self.get_crystals(number_of_players)
            for i in range(number_of_players):
                crystal = random.choice(crystals)
                crystals.remove(crystal)
                players[i].set_crystal(crystal)

    def calculate_turn_split(self) -> int:
        if self.NUMBER_OF_PLAYERS < 4:
            return 4
        else:
            return 3

                # players.append(Player(f"Player {i+1}", crystal, bank))

    def __init__(self, bank:Bank, card_deck:CardDeck, players:List[Player], playing_board:PlayingBoard, turn:int, mode:int=0, initialize=False) -> None:
        # SEED = 10
        self.players = players
        self.NUMBER_OF_PLAYERS = len(players)
        if initialize:
            self.give_players_crystals(players)
        # random.seed(SEED)#?? ar reikalingas
        self.card_deck = card_deck
        self.bank = bank
        self.playing_board = playing_board
        self.turn = turn
        self.turn_split = self.calculate_turn_split()
        self.mode = mode

    def get_possible_game_states(self):
        if self.turn > self.turn_split*2:
            raise Exception(f"Illegal game state {self.turn} reached")
        if self.turn == self.turn_split*2:
            return []
        pass

##################################################################################################################
    def run_game(self):
        while self.turn < self.turn_split*2:
            self.turn += 1
            self.print_function(f"Turn {self.turn}")
            # in halfway point we award bonuses to players, no decision needed
            if self.turn == self.turn_split+1:
                self.print_function("Granting players distinction bonuses")
                self.award_distinction_cards(self.players, self.playing_board)

            # take cards which will be shown to players
            slots = self.playing_board.generate_slots(self.turn_split, self.turn)
            self.print_function(str(slots))

            # here we can have update player function, which to MCTS player would pass the game state
            # for player in self.players:
            #     player.update_state(self.card_deck, self.players, self.bank, self.turn)

            for player in self.players:
                player.make_bet(slots) #MCTS decision

            for slot_index in slots.keys():
                bet_index = slot_index - 1
                
                self.print_function(f"Turn {self.turn}")
                self.print_player_bets()
                self.print_function(f"SLOT {slot_index} : {slots[slot_index]}")

                player_queue = self.create_player_queue(bet_index)

                self.print_function(f"Player turns: {player_queue}")
                    
                for player in player_queue:
                    self.print_function(str(player))
                    slots[slot_index], taken_card = player.take_card(slots[slot_index]) #MCTS decision
                    self.print_function(f"Taken card {taken_card}")

                    player.make_coin_exchange(bet_index)
                    self.breakpoint()
                self.clear()

            for player in self.players:
                player.remove_bets()
            if self.turn == self.turn_split*2:
                red_highest_players = self.get_player_with_highest_count(self.players, 'red')
                for player in red_highest_players:
                    player.add_red_bonus()
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
            bet = player.bets[slot_number].value
            if bet in helper_dict.keys():
                helper_dict[bet].append(player)
            else:
                helper_dict[bet] = [player]
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
                self.exchange_crystals_two_players(players)
                return [players[0], players[1]]
            else:
                self.exchange_crystals_two_players(players)
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
                left_cards, _ = player.take_card(card_to_choose_from)
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

    def clear(self) -> None:
        if self.mode == 1:
            clear = lambda: os.system('cls')
            clear()

    def breakpoint(self) -> None:
        if self.mode == 1:
            input()

    def print_function(self, text:str) -> None:
        if self.mode > 0:
            print(text)

