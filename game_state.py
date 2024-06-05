from copy import deepcopy
import itertools
import random
from typing import Dict, List, Tuple
from bank import Bank
from card import Card
from card_deck import CardDeck
from Players.player import Player
from coin import Coin
from playing_board import PlayingBoard


class GameState():
    def __init__(self, playing_board: PlayingBoard, players: List[Player], card_deck: CardDeck, bank: Bank, turn: int,
                 slot_index: int, slots, mode: int = 0, distinction_applied:bool=False) -> None:
        self.card_deck = card_deck
        self.turn = turn
        self.mode = mode
        self.bank = bank
        self.players = players
        self.playing_board = playing_board
        self.slot_index = slot_index
        self.slots = slots
        self.number_of_cards = GameState.get_number_of_cards(len(players))
        if len(self.players) < 4:
            self.turn_split = 4
        else:
            self.turn_split = 3

        # self.increase_meta_variable = None
        self.distinction_applied = distinction_applied
        self.distinction_take_cards= None
        self.game_id = None

    def get_number_of_cards(number_of_players: int) -> int:
        if number_of_players == 2:
            return 3
        else:
            return number_of_players

    def create_player_queue(players: List[Player], slot_number: int) -> List[Player]:
        player_queue = []

        helper_dict = {}
        for player in players:
            try:
                bet = player.bets[slot_number].value
                if bet in helper_dict.keys():
                    helper_dict[bet].append(player)
                else:
                    helper_dict[bet] = [player]
            except:
                raise ("DEBUG ERROR")
        sorted_helper_dict = dict(sorted(helper_dict.items(), reverse=True))
        # print(sorted_helper_dict)

        for key in sorted_helper_dict.keys():
            if len(sorted_helper_dict[key]) > 1:
                sorted_players = GameState.sort_players_by_crystal(
                    sorted_helper_dict[key])
                player_queue.extend(sorted_players)
            else:
                player_queue.extend(sorted_helper_dict[key])

        return player_queue

    def sort_players_by_crystal(players: List[Player]) -> List[Player]:
        crystals = [(player.index, player.crystal) for player in players]
        crystals.sort(key=lambda x: x[1], reverse=True)
        queue = []
        for crystal in crystals:
            for player in players:
                if player.index == crystal[0]:
                    queue.append(player)
        return queue

    def __str__(self):
        strings_to_print = []
        for player in self.players:
            strings_to_print.append(f"Player {player}")
            strings_to_print.append(f"Bets: {player.bets}")

        return '\n'.join(strings_to_print)

    def copy_state(self):
        new_card_deck = deepcopy(self.card_deck)
        new_playing_board = PlayingBoard(new_card_deck)
        new_players = [deepcopy(player) for player in self.players]
        new_bank = deepcopy(self.bank)
        for player in new_players:
            player.bank = new_bank
        return GameState(playing_board=new_playing_board,
                         players=new_players,
                         card_deck=new_card_deck,
                         bank=new_bank,
                         turn=deepcopy(self.turn),
                         slot_index=deepcopy(self.slot_index),
                         slots=deepcopy(self.slots),
                         mode=self.mode,
                         distinction_applied=self.distinction_applied)

    def shuffle_object(self, some_list):
        random.shuffle(some_list)
        return some_list

    # def get_possible_card_choice(self, slot_index: int):
    #     random_cards = self.shuffle_object(self.slots[slot_index].copy())
    #     choice = itertools.permutations(random_cards, 1)
    #     return choice

    def exchange_crystals(players: List[Player], bet_index: int, mode: int) -> List[Player]:
        if mode < 0:
            return
        bet_dict = {}
        for player in players:
            try:
                bet = player.bets[bet_index].value
                if player.crystal == 6:
                    continue
                if bet in bet_dict.keys():
                    bet_dict[bet].append(player)
                else:
                    bet_dict[bet] = [player]
            except:
                raise ("DEBUG ERROR")

        sorted_dict = {key: sorted(
            value, key=lambda x: x.crystal, reverse=True) for key, value in bet_dict.items()}
        for bet, group in sorted_dict.items():
            n = len(group)
            for i in range(n // 2):
                group[i].crystal, group[n-i-1].crystal = group[n -
                                                               i-1].crystal, group[i].crystal

    # def get_possible_slot_choice(self):

    #     # range_limit = self.playing_board.get_player_card_limit(self.turn_split)
    #     if self.turn < self.turn_split:
    #         selection_deck = self.playing_board.card_deck.get_age_one_cards().copy()
    #     else:
    #         selection_deck = self.playing_board.card_deck.get_age_two_cards().copy()

    #     random_cards = self.shuffle_object(selection_deck.copy())
    #     slots = itertools.permutations(random_cards, 9)
    #     # slots = self.playing_board.generate_slots(self.turn_split, self.turn+1)
    #     # print(bets)
    #     return slots

    def get_discard_parameters(hero: Card):
        if hero.name == "DAGDA":
            return {'discard_count': 2, 'available_colors': ['violet', 'blue', 'orange', 'red']}
        elif hero.name == "BONFUR":
            return {'discard_count': 1, 'available_colors': ['green', 'blue', 'orange', 'red']}
        else:
            raise (Exception(f'Bad hero card for discarding {hero}'))

    def hero_has_action(hero: Card):
        if hero is None:
            return 'None'
        if hero.name in ['DAGDA', 'BONFUR']:
            return 'Discard'
        if hero.name == ['GRID']:
            return 'AddCoins'
        return None

    def get_next_state(self, action:Tuple[str, int]=None):
        # if self.slot_index < 4:
        if action is not None:   
            action_name, mcts_index = action         
            if action_name == 'Bet':
                if self.players[mcts_index].bet_made == True:
                    raise(Exception('Root should not have a bet made'))
                return self.child_bets_generator(mcts_index)
            elif action_name == 'Take' and len(self.slots) > 0:
                return self.child_card_generator(self.slot_index, mcts_index, coin_exchange=False)
            elif action_name == 'TakeCoin':
                return self.child_distinction_generator()
            elif action_name == 'Take' and len(self.slots) == 0:
                return self.child_distinction_generator(self.distinction_take_cards)
            else:
                raise(Exception('Root node has unknown action'))
        else:    
            if self.slot_index == 0 and self.turn == self.turn_split and self.distinction_applied == False:
                return self.child_distinction_generator()
            elif self.slot_index == 0 and self.turn == self.turn_split:
                return self.new_slot_generator()
            if self.slot_index == 0:
                raise(Exception("Unexpected slot index"))

            for idx, player in enumerate(self.players):
                if player.bet_made == False:
                    # state_copy = self.copy_state()
                    # state_copy.players[idx].bets = self.get_possible_bet(idx)
                    return self.child_bets_generator(idx)
                elif player.bet_made == True and len(player.bets) < 3:
                    return self.partial_child_bets_generator(idx)
            # not in the first slot and can take
            if ((len(self.slots[self.slot_index]) > 1 and len(self.players) == 2) or
                    (len(self.slots[self.slot_index]) > 0 and len(self.players) > 2)):
                bet_index = self.slot_index-1
                player_queue = GameState.create_player_queue(
                    self.players, bet_index)
                for player in player_queue:
                    if player.card_taken == False:
                        return self.child_card_generator(self.slot_index, player.index)
            elif (self.turn >= (self.turn_split*2)-1 and \
                    (len(self.slots[1]) == 0 and len(self.slots[2]) == 0 and len(self.slots[3]) == 0)) \
                or (self.turn >= (self.turn_split*2)-1 and len(self.players) == 2 and \
                    (len(self.slots[1]) == 1 and len(self.slots[2]) == 1 and len(self.slots[3]) == 1)): 
                return None
            else:
                if self.slot_index > 3:
                    raise (f'Unexpected slot index {self.slot_index}')
                # New slots
                if self.slot_index == 3:
                    # TODO: move to next turn
                    return self.next_turn_generator()
                # Move to next slot
                else:
                    # TODO: move slot and take card
                    bet_index = self.slot_index
                    player_queue = GameState.create_player_queue(self.players, bet_index)
                    for player in player_queue:
                        return self.child_card_generator(bet_index+1, player.index, move_slot=True)
            # else:
            #     raise (Exception("Game not ended, no new states"))
        
    def child_distinction_generator(self, predefined_cards:List[Card]=None):
        new_state = self.copy_state()
        colors = ['red', 'green', 'orange', 'violet', 'blue']
        for color in colors:
            distinguished_players = GameState.get_player_with_highest_count(
                new_state.players, color)
            if len(distinguished_players) == 1:
                # if simple distinction move on
                if color not in ['red', 'blue']:
                    GameState.add_bonus_to_distinguished(
                        distinguished_players[0], color, new_state.playing_board)
                # if red we need to model possible coin increases and later on complete distinction
                elif color == 'red' and distinguished_players[0].distinction_cards == 0:
                    for coin in distinguished_players[0].coins:
                        if coin.exchangeable == False:
                            new_red_state = new_state.copy_state()
                            player = new_red_state.players[distinguished_players[0].index]
                            player.distinction_cards += 1
                            player.increase_coin(value=5, coin_to_increase=coin)
                            yield {'state': new_red_state, 'name': f"Next_turn.Distinction_{player}_red.Increase_coin_{coin}",
                                   'return':{'action':'TakeCoin'
                                            ,'player':player.index
                                            ,'coin_increased':coin}}
                elif color == 'blue' and distinguished_players[0].distinction_cards == 0:
                    if predefined_cards is None:
                        possible_cards = new_state.playing_board.card_deck.get_age_two_cards()
                        random_cards = new_state.shuffle_object(possible_cards.copy())
                        possible_choices = itertools.permutations(random_cards, 3)
                    else:
                        possible_choices = [predefined_cards]
                    for possible_choice in possible_choices:
                        for card in possible_choice:
                            new__blue_state = new_state.copy_state()
                            player = new__blue_state.players[distinguished_players[0].index]
                            left_cards, taken_card = player.take_card(
                                cards_to_choose=[card for card in possible_choice], taken_card=card)
                            new__blue_state.card_deck.remove_card(taken_card.index)
                            player.distinction_cards += 1
                            player.card_taken == False
                            new__blue_state.distinction_applied = True
                            yield from new__blue_state.take_card_generator(taken_card, player.index
                                                                ,f"Next_turn.Distinction_{distinguished_players[0]}_blue.Card_taken_{taken_card}.")
        new_state.distinction_applied = True
        yield {'state': new_state, 'name': f"Next_turn.Distinction_no_decisions",
               'return':{'action':'Distinction'
                                ,'player':-10}}
        
    def new_slot_generator(self):
        # new_state = self.copy_state()
        
        if self.turn < self.turn_split:
            selection_deck = self.playing_board.card_deck.get_age_one_cards().copy()
        else:
            selection_deck = self.playing_board.card_deck.get_age_two_cards().copy()

        random_cards = self.shuffle_object(deepcopy(selection_deck))
        possible_slots = itertools.permutations(random_cards, GameState.get_number_of_cards(len(self.players)) * 3)
        for slot_cards_tuple in possible_slots:
            new_state = self.copy_state()
            new_state.slot_index = 1

            slot_cards = [card for card in slot_cards_tuple]
            slots = {}
            slot_card_number = GameState.get_number_of_cards(len(new_state.players))
            for i in range(1, 4):
                selected_cards = []
                str = slot_card_number*(i-1)
                end = slot_card_number+((i-1)*slot_card_number)
                for card in slot_cards[slot_card_number*(i-1): slot_card_number+((i-1)*slot_card_number)] :
                    selected_cards.append(card)
                    new_state.card_deck.remove_card(card.index)
                slots[i] = selected_cards
            new_state.slots = slots
            yield {'state': new_state, 'name': f"Next_turn.New_slots_{slots}"
                    ,'return':{'action':'New_slots'
                                ,'player':-10}}
        

    def next_turn_generator(self):
        # shulffled_cards = self.shuffle_object([self.card_deck.cards[key] for key in self.card_deck.cards.keys()])
        new_state = self.copy_state()
        for player in new_state.players:
                player.card_taken = False
                player.remove_bets()
        new_state.turn += 1
        new_state.slot_index = 0
        new_state.slots.clear()

        if new_state.turn == self.turn_split:
            return new_state.child_distinction_generator()
        else:
            return new_state.new_slot_generator()


        # return_dict = {}
        # for i in range(1, 4):
        #     selected_cards = 
        #     return_dict[i] = selected_cards
        # return return_dict

    def child_bets_generator(self, index: int):
        random_coins = self.shuffle_object(self.players[index].coins.copy())
        for bets in itertools.permutations(random_coins, 3):
            new_state = self.copy_state()
            new_bet = [bet for bet in bets]
            new_state.players[index].make_bet(predefined_bet=new_bet)
            yield {'state': new_state, 'name': f"Player{index}_bet_{new_bet}"
                   , 'return':{'action':'Bet'
                               ,'player':index
                               ,'bet':new_bet}}

    def partial_child_bets_generator(self, index: int):
        remaining_coins = [
            coin for coin in self.players[index].coins if coin not in self.players[index].bets]
        random_remaining_coins = self.shuffle_object(remaining_coins.copy())
        for permutation in itertools.permutations(random_remaining_coins, 3 - len(self.players[index].bets)):
            new_bet = self.players[index].bets + list(permutation)
            new_state = self.copy_state()
            new_state.players[index].make_bet(predefined_bet=new_bet)
            yield {'state': new_state, 'name': f"Player{index}_bet_{new_bet}"
                   , 'return':{'action':'Bet'
                               ,'player':index
                               ,'bet':new_bet}}

    def take_card_generator(self, taken_card, player_index, name):
        new_state = self
        if taken_card.color == 'coin':
            for coin in new_state.players[player_index].coins:
                if coin.exchangeable == False:
                    new_coin_state = new_state.copy_state()
                    new_coin_state.players[player_index].increase_coin(
                        taken_card.value, coin_to_increase=coin)
                    yield {'state': new_coin_state, 'name': name+f'Increase_{coin}_by_{taken_card.value}'
                           ,'return':{'action':'Take'
                                        ,'player':player_index
                                        ,'card':taken_card
                                        ,'coin_increased':coin}}
        else:
            if new_state.players[player_index].has_row() and len(new_state.card_deck.hero_cards) != 0:
                for hero in new_state.playing_board.card_deck.hero_cards:
                    if hero.name == 'HOURYA' and new_state.players[player_index].card_deck.card_count['blue'] < 5:
                        continue
                    new__hero_state = new_state.copy_state()
                    # new_state.players[player_index].
                    new__hero_state.playing_board.card_deck.hero_cards, hero_taken = new__hero_state.players[player_index].choose_hero(
                        new__hero_state.playing_board.card_deck.hero_cards, hero_to_take=hero)
                    action = GameState.hero_has_action(hero)
                    if action is None:
                        yield {'state': new__hero_state, 'name': name+f'Row_complete_take_hero_{hero}'
                               , 'return':{'action':'Take'
                                        ,'player':player_index
                                        ,'card':taken_card
                                        ,'hero_taken':hero}}
                    elif action == 'Discard':
                        parameters = GameState.get_discard_parameters(hero)

                        if len(new__hero_state.players[player_index].card_deck.cards) < parameters['discard_count']+1:
                            continue

                        available_colors = [color for color in parameters['available_colors'] 
                                            if len(new__hero_state.players[player_index].card_deck.card_group[color]) > 0]
                        
                        if len(available_colors) < parameters['discard_count']:
                            continue

                        all_combinations = itertools.combinations(
                            available_colors, parameters['discard_count'])
                        for color_combination in all_combinations:
                            new_hero_discard_state = new__hero_state.copy_state()
                            discard_cards = [
                                new_hero_discard_state.players[player_index].card_deck.card_group[color][-1] for color in color_combination]
                            # self.print_function(f'Hero {hero.name} discards cards')
                            discarded_cards = new_hero_discard_state.players[player_index].discard_cards(
                                            discard_card_count=parameters['discard_count']
                                            ,available_colors=parameters['available_colors']
                                            ,cards_to_discard=discard_cards)
                            # self.print_function(f'Hero discards cards {str(discarded_cards)}')
                            yield {'state': new_hero_discard_state
                                    ,'name': name+f'Row_complete_take_hero_{hero}.Discarded_cards_{discarded_cards}'
                                    ,'return':{'action':'Take'
                                        ,'player':player_index
                                        ,'hero_taken':hero
                                        ,'card':taken_card
                                        ,'cards_dicarded':discarded_cards}}
                    elif action == 'AddCoins':
                        for coin in new__hero_state.players[player_index].coins:
                            if coin.exchangeable == False:
                                new_hero_coin_state = new__hero_state.copy_state()
                                new_hero_coin_state.players[player_index].increase_coin(
                                    value=7, coin_to_increase=coin)
                                yield {'state': new_hero_coin_state
                                        ,'name': name+f'Row_complete_take_hero_{hero}.Hero_increases_coin_{coin}',
                                        'return':{'action':'Take'
                                                ,'player':player_index
                                                ,'hero_taken':hero
                                                ,'card':taken_card
                                                ,'coin_increased':coin}}
            else:
                yield {'state': new_state, 'name': name
                       ,'return':{'action':'Take'
                            ,'player':player_index
                            ,'card':taken_card}}

    def child_card_generator(self, slot_index: int, player_index: int, move_slot:bool=False, coin_exchange=True):
        temp_state = self.copy_state()
        # If moving onto the next slot
        if move_slot:
            for player in temp_state.players:
                player.card_taken = False
            temp_state.slot_index = slot_index
        random_cards = self.shuffle_object(deepcopy(self.slots[slot_index]))
        for iter_card in itertools.permutations(random_cards, 1):
            taken_card = iter_card[0]
            new_state = temp_state.copy_state()
            GameState.exchange_crystals(new_state.players, slot_index-1, 1)
            if coin_exchange:
                new_state.players[player_index].make_coin_exchange(slot_index-1, new_state.bank)
            new_state.slots[slot_index], taken_card = new_state.players[player_index].take_card(
                new_state.slots[slot_index], taken_card=taken_card)
            yield from new_state.take_card_generator(taken_card, player_index, f'Player{player_index}_take_{taken_card}.')
            
# ----
    def award_distinction_cards(players: List[Player], playing_board: PlayingBoard, game=None) -> None:
        colors = ['red', 'green', 'orange', 'violet', 'blue']
        for color in colors:
            distinguished_players = GameState.get_player_with_highest_count(
                players, color)
            game.print_players_color_count(players, color)
            if len(distinguished_players) == 1:
                GameState.add_bonus_to_distinguished(
                    distinguished_players[0], color, playing_board, game)
                
    def get_player_with_highest_count(players: List[Player], color: str) -> List[Player]:
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
    
    def add_bonus_to_distinguished(player: Player, color: str, playing_board: PlayingBoard, game=None) -> None:
        if game is not None:
            game.print_function(
                f"Distinction card count: {player.distinction_cards}")
        if player.distinction_cards == 0:
            if game is not None:
                game.print_function(f"Giving bonus to player: {player}")
            if color == 'red':
                player.increase_coin(value=5, game_state=game.create_game_state())
                player.distinction_cards = 1
            elif color == 'green':
                player.remove_zero_coin()
                player.coins.append(Coin(3, True))
                player.distinction_cards = 1
            elif color == 'orange':
                player.crystal = 6
                player.distinction_cards = 1
            elif color == 'violet':
                player.add_card(Card('violet', 'None', 0, 101))
                player.add_card(Card('violet', 'None', 0, 102))
                player.distinction_cards = 1
            elif color == 'blue':
                card_to_choose_from = playing_board.get_number_of_cards(
                    3, playing_board.card_deck.get_age_two_cards())
                if game is not None:
                    game_state = game.create_game_state()
                    game.print_function(f'Cards to take {card_to_choose_from}')
                left_cards, taken_card = player.take_card(
                    card_to_choose_from, game_state=game_state)
                if game is not None:
                    game.print_function(f'Card taken {taken_card}')
                for card in left_cards:
                    playing_board.card_deck.add_card(card)
                player.distinction_cards = 1
                player.card_taken == False
