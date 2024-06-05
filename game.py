import os
from typing import List
from bank import Bank
from card import Card
from card_deck import CardDeck
from coin import Coin
from Players.player import Player
# from memory_profiler import profile
import random
from game_state import GameState
import uuid
from playing_board import PlayingBoard
from datetime import datetime


class Game:
    def calculate_age_split(self) -> int:
        if self.NUMBER_OF_PLAYERS < 4:
            return 4
        else:
            return 3

            # players.append(Player(f"Player {i+1}", crystal, bank))

    def __init__(self, game_state:GameState, initialize=False) -> None:
        # SEED = 10
        self.players = game_state.players
        self.NUMBER_OF_PLAYERS = len(self.players)
        self.game_id = str(uuid.uuid4())
        # self.game_id = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f')
        # if initialize:
        #     self.give_players_crystals(self.players)
        self.card_deck = game_state.card_deck
        self.bank = game_state.bank
        self.playing_board = game_state.playing_board
        self.turn = game_state.turn
        self.age_split = self.calculate_age_split()
        self.mode = game_state.mode
        self.slots = game_state.slots
        self.slot_index = game_state.slot_index
        self.number_of_slot_cards = GameState.get_number_of_cards(self.NUMBER_OF_PLAYERS)
        self.write_path = 'Logs/GameRuns'
        self.result = None

    def generate_slots(self):
        self.slots = self.playing_board.generate_slots(
            self.turn, self.age_split, self.number_of_slot_cards)
        self.slot_index = 1
        self.print_function(str(self.slots))

    def create_game_state(self) -> GameState:
        game_state = GameState(playing_board=self.playing_board,
                         players=self.players,
                         card_deck=self.card_deck,
                         bank=self.bank,
                         turn=self.turn,
                         slot_index=self.slot_index,
                         slots=self.slots,
                         mode=self.mode)
        game_state.game_id = self.game_id
        return game_state

    def make_player_bets(self):
        for player in self.players:
            if len(player.bets) != 3 and player.can_skip == False:
                if 'MCTS' in player.player_type:
                    game_state = self.create_game_state()
                else:
                    game_state = None
                player.make_bet(self.slots, game_state) 

    def take_card(self, player: Player, bet_index: int) -> Card:
        if 'MCTS' in player.player_type:
            game_state = self.create_game_state()
        else:
            game_state = None
        player.make_coin_exchange(bet_index, self.bank)
        self.slots[self.slot_index], taken_card = player.take_card(
            self.slots[self.slot_index], game_state=game_state)  # MCTS decision
        if taken_card.color == 'coin':
            player.increase_coin(taken_card.value)
        return taken_card

##################################################################################################################
    # @profile
    def run_game(self, main=False):
        # self.print_function(f'Game: {self.game_id}')
        # print(f'Game: {self.game_id}')
        try:
            try:
                while self.turn < self.age_split*2:
                    try:
                    # in halfway point we award bonuses to players, no decision needed
                        self.coin_test()

                        if self.slot_index == 0:

                            self.print_function(f"Turn {self.turn}")

                            if self.turn == self.age_split:
                                self.print_function("Granting players distinction bonuses")
                                GameState.award_distinction_cards(
                                    self.players, self.playing_board, self)

                        # take cards which will be shown to players
                            if len(self.slots) == 0:
                                self.generate_slots()

                        # here we can have update player function, which to MCTS player would pass the game state
                        # for player in self.players:
                        #     player.update_state(self.card_deck, self.players, self.bank, self.turn)
                        self.make_player_bets()
                    except Exception as e:
                        raise(e)
                    # else:
                    #     self.check_if_bets_need_to_be_made()
                    try:
                        # for slot_index in self.slots.keys():
                        while self.slot_index < 4:
                            bet_index = self.slot_index - 1

                            self.print_function(f"Turn {self.turn}")
                            self.print_player_bets()
                            self.print_function(
                                f"SLOT {self.slot_index} : {self.slots[self.slot_index]}")

                            player_queue = GameState.create_player_queue(
                                self.players, bet_index)
                            self.print_function(f"Player turns: {player_queue}")
                            GameState.exchange_crystals(self.players, bet_index, self.mode)
                            self.print_function(f"Crystals changed: {player_queue}")

                            
                            try:
                                for player in player_queue:
                                    self.print_function(str(player))
                                    if player.card_taken == False:
                                        taken_card = self.take_card(player, bet_index)
                                        if player.has_row() and len(self.card_deck.hero_cards) != 0:
                                            self.print_function('Row reached')
                                            self.playing_board.card_deck.hero_cards, hero = player.choose_hero(
                                                self.playing_board.card_deck.hero_cards)
                                            self.print_function(f'Taken card: {hero}')
                                            action = GameState.hero_has_action(hero)
                                            if action == 'Discard':
                                                parameters = GameState.get_discard_parameters(hero)
                                                self.print_function(f'Hero {hero.name} discards cards')
                                                # here finished add hero action parser
                                                discarded_cards = player.discard_cards(discard_card_count=parameters['discard_count']
                                                                                    ,available_colors=parameters['available_colors'])
                                                self.print_function(f'Hero discards cards {str(discarded_cards)}')
                                            elif action =='AddCoins':
                                                player.increase_coin(value=7)
                                        self.coin_test()
                                        self.print_function(f"Taken card {taken_card}")
                                        self.breakpoint()
                                    self.print_function(
                                        f"{player} coins: {player.coins}, {player.bets}, {player.left_over_coins}")
                            except Exception as e:
                                raise(e)
                            for player in player_queue:
                                player.card_taken = False
                            
                            # if self.players[0].bets[bet_index] == self.players[1].bets[bet_index]:
                            #     self.exchange_crystals_two_players(self.players)

                            # self.slots.pop(slot_index)
                            self.slot_index += 1
                            self.clear_console()
                    except Exception as e:
                        raise(e)
                    try:
                        self.slots.clear()
                        self.slot_index = 0
                        self.turn += 1
                    except Exception as e:
                        raise(e)
                    try:
                        for player in self.players:
                            player.remove_bets()
                        if self.turn == self.age_split*2:
                            try:
                                red_highest_players = GameState.get_player_with_highest_count(
                                    self.players, 'red')
                                for player in red_highest_players:
                                    player.add_red_bonus()
                            except Exception as e:
                                raise(e)
                    except Exception as e:
                        raise(e)
            except Exception as e:
                raise(e)
            try:
                self.print_game_results(main)
            except Exception as e:
                raise(e)
            try:
                return [player.get_player_points() for player in self.players]
            except Exception as e: 
                raise(e)

        except Exception as e:
            raise(e)
##################################################################################################################

    def coin_test(self):
        fives = self.NUMBER_OF_PLAYERS + 2
        if self.NUMBER_OF_PLAYERS > 3:
            sevens = 1
            nines = 1
            elevens = 1
        else:
            sevens = 3
            nines = 3
            elevens = 3

        coin_limits = {
            5: fives,
            6: 2,
            7: sevens,
            8: 2,
            9: nines,
            10: 2,
            11: elevens,
            12: 2,
            13: 2,
            14: 2,
            15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1
        }

        all_coins = {}
        for player in self.players:
            for coin in player.coins:
                if coin.value >= 5:
                    if coin.value in all_coins.keys():
                        all_coins[coin.value] += 1
                    else:
                        all_coins[coin.value] = 1

        for bank_coin in self.bank.coins.keys():
            if bank_coin in all_coins.keys():
                all_coins[bank_coin] += self.bank.coins[bank_coin]
            else:
                all_coins[bank_coin] = self.bank.coins[bank_coin]

        for coin_value in all_coins.keys():
            if all_coins[coin_value] > coin_limits[coin_value]:
                raise(Exception(f'Illegal value {coin_value}, should be {coin_limits[coin_value]}, is {all_coins[coin_value]}'))





    
            # if len(bet_dict[bet]) % 2 == 0:
            #     for i in range(0, len(group), 2):
            #         group[i].crystal, group[i+1].crystal = group[i+1].crystal, group[i].crystal
            # else:
            #     if len(group) > 1:
            #         group[0].crystal, group[-1].crystal = group[-1].crystal, group[0].crystal

        # players = []

        # for bet in bet_dict.keys():
        #     for player in bet_dict[bet]:
        #         players.append(player)

        # return players

    def exchange_crystals_two_players(self, players: List[Player]) -> None:
        if players[0].crystal != 6 and players[1].crystal != 6:
            temp = players[0].crystal
            players[0].crystal = players[1].crystal
            players[1].crystal = temp




 # Helper output functions

    def print_players_color_count(self, players: List[Player], color):
        if self.mode == 0:
            return
        if self.mode == 4:
            with open(f'{self.write_path}/{self.game_id}.txt', 'a') as f:
                f.write(f"Players have number of {color}\n")
                for player in players:
                    f.write(f"{player}: {player.get_color_count(color)}" + '\n')
            return
        if self.mode > 0:
            print(f"Players have number of {color}")
            for player in players:
                print(player, ": ", player.get_color_count(color))

    def print_player_bets(self):
        if self.mode == 0:
            return
        if self.mode == 4:
            with open(f'{self.write_path}/{self.game_id}.txt', 'a') as f:
                for player in self.players:
                    f.write(
                        f"{player}, bets: {player.bets}, lefover: {player.left_over_coins}" + '\n')
            return
        if self.mode > 0:
            for player in self.players:
                print(f"{player}, bets: ", player.bets,
                      "lefover: ", player.left_over_coins)

    def print_score(self):
        if self.mode == 0:
            return
        if self.mode == 4:
            with open(f'{self.write_path}/{self.game_id}.txt', 'a') as f:
                for player in self.players:
                    f.write(player.print_player_points() + '\n')
            return
        if self.mode > 0:
            for player in self.players:
                player.print_player_points()

    def clear_console(self) -> None:
        if self.mode == 1:
            def clear(): return os.system('cls')
            clear()

    def breakpoint(self) -> None:
        if self.mode == 1:
            input()

    def print_game_results(self, main=False):
        try:
            if main == True:
                ret_text = ['"################################################################################"']
                self.print_function("Results")
                colors = self.card_deck.card_group.keys()
                for player in self.players:
                    ret_text.append(str(player))
                    ret_text.append(str(player.coins))
                    ret_text.append(player.card_deck.get_card_deck_string())
                    card_sum = 0
                    for color in colors:
                        color_count = player.get_color_count(color)
                        ret_text.append(f"Has {player.card_deck.card_count[color]} of {color}")
                        ret_text.append(f"Has {color_count} ranks of {color}")

                        card_sum += color_count
                    ret_text.append(f"Has {str(player.card_deck.heroes)} heroes")
                    ret_text.append(f"Has {str(len(player.card_deck.hero_cards))} hero cards")

                    ret_text.append(f"Player has {card_sum} cards")
                    ret_text.append(player.get_player_points_str())

                self.result = '\n'.join(ret_text)
            else:
                if self.mode == 0:
                    return
                self.print_function(
                    "################################################################################")
                self.print_function("Results")
                colors = self.card_deck.card_group.keys()
                for player in self.players:
                    self.print_function(str(player))
                    self.print_function(str(player.coins))
                    self.print_function(player.card_deck.get_card_deck_string())
                    card_sum = 0
                    for color in colors:
                        color_count = player.get_color_count(color)
                        self.print_function(f"Has {player.card_deck.card_count[color]} of {color}")
                        self.print_function(f"Has {color_count} ranks of {color}")

                        card_sum += color_count
                    self.print_function(f"Has {str(player.card_deck.heroes)} heroes")
                    self.print_function(f"Has {str(len(player.card_deck.hero_cards))} hero cards")

                    self.print_function(f"Player has {card_sum} cards")
                    self.print_function(player.get_player_points_str())

        except Exception as e:
            self.mode = 1
            self.print_function(
                "################################################################################")
            self.print_function("Results")
            colors = self.card_deck.card_group.keys()
            for player in self.players:
                self.print_function(str(player))
                self.print_function(str(player.coins))
                self.print_function(player.card_deck.get_card_deck_string())
                card_sum = 0
                for color in colors:
                    color_count = player.get_color_count(color)
                    self.print_function(f"Has {player.card_deck.card_count[color]} of {color}")
                    self.print_function(f"Has {color_count} ranks of {color}")

                    card_sum += color_count
                self.print_function(f"Has {str(player.card_deck.heroes)} heroes")
                self.print_function(f"Has {str(len(player.card_deck.hero_cards))} hero cards")

                self.print_function(f"Player has {card_sum} cards")
                self.print_function(player.get_player_points_str())

    def print_function(self, text: str) -> None:
        if self.mode == 0:
            return
        if self.mode == 4:
            with open(f'{self.write_path}/{self.game_id}.txt', 'a') as f:
                f.write(text + '\n')
            return
        if self.mode > 0:
            print(text)

    def coin_test(self):
        fives = self.NUMBER_OF_PLAYERS + 2
        if self.NUMBER_OF_PLAYERS < 4:
            sevens = 1
            nines = 1
            elevens = 1
        else:
            sevens = 3
            nines = 3
            elevens = 3

        coin_limits = {
            5: fives,
            6: 2,
            7: sevens,
            8: 2,
            9: nines,
            10: 2,
            11: elevens,
            12: 2,
            13: 2,
            14: 2,
            15: 1,
            16: 1,
            17: 1,
            18: 1,
            19: 1,
            20: 1,
            21: 1,
            22: 1,
            23: 1,
            24: 1,
            25: 1,
        }

        all_coins = {}
        for player in self.players:
            for coin in player.coins:
                if coin.value >= 5:
                    if coin.value in all_coins.keys():
                        all_coins[coin.value] += 1
                    else:
                        all_coins[coin.value] = 1

        for bank_coin in self.bank.coins.keys():
            if bank_coin in all_coins.keys():
                all_coins[bank_coin] += self.bank.coins[bank_coin]
            else:
                all_coins[bank_coin] = self.bank.coins[bank_coin]

        for coin_value in all_coins.keys():
            if all_coins[coin_value] > coin_limits[coin_value]:
                raise Exception("More coins than possible")
