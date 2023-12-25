from copy import deepcopy
import itertools
from typing import List
from bank import Bank
from card_deck import CardDeck
from Players.player import Player
from playing_board import PlayingBoard


class GameState():
    def __init__(self, playing_board:PlayingBoard, players:List[Player], card_deck:CardDeck, bank:Bank, turn:int, slot_index:int, slots, mode:int=0) -> None:
        self.deck = card_deck
        self.turn = turn
        self.mode = mode
        self.bank = bank
        self.players = players
        self.playing_board = playing_board
        self.slot_index = slot_index
        self.slots = slots
        if len(self.players) < 4:
            self.turn_split = 4
        else:
            self.turn_split = 3


    def __str__(self):
        strings_to_print = []
        for player in self.players:
            strings_to_print.append(f"Player {player}")
            strings_to_print.append(f"Bets: {player.bets}")
        
        return '\n'.join(strings_to_print)

    def copy_state(self):
        new_players = [deepcopy(player) for player in self.players]
        return GameState(playing_board=deepcopy(self.playing_board),
                         players=new_players,
                         card_deck=deepcopy(self.deck),
                         bank=deepcopy(self.bank),
                         turn=deepcopy(self.turn),
                         slot_index=deepcopy(self.slot_index),
                         slots=deepcopy(self.slots),
                         mode=self.mode)
    
    def get_possible_card_choice(self, slot_index:int):
        choice = itertools.permutations(self.slots[slot_index], 1)
        return choice
    
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
    
    def get_possible_slot_choice(self):

        # range_limit = self.playing_board.get_player_card_limit(self.turn_split)
        if self.turn < self.turn_split:
            selection_deck = self.playing_board.card_deck.get_age_one_cards().copy()
        else:
            selection_deck = self.playing_board.card_deck.get_age_two_cards().copy()
            
        slots = itertools.permutations(selection_deck, 9)
        # slots = self.playing_board.generate_slots(self.turn_split, self.turn+1)
        # print(bets)
        return slots

    def get_next_state(self, custom_slot_index:int=None):
        # if self.slot_index < 4:
        for idx, player in enumerate(self.players):
            if len(player.bets) == 0:
                # state_copy = self.copy_state()
                # state_copy.players[idx].bets = self.get_possible_bet(idx)
                return {'value':self.get_possible_bet(idx), 'type':'bets', 'player_index':idx}
        # generate new state and increase slot index in the new state
        #TODO: should depend on player count  
        if len(self.slots[self.slot_index]) > 1:
            player_queue = self.create_player_queue(self.slot_index-1)
            for player in player_queue:
                if player.card_taken == False:
                    return {'value':self.get_possible_card_choice(self.slot_index), 'type':'take', 'player_index':player.index}
        else:
            if self.slot_index > 4:
                raise(f'Unexpected slot index {self.slot_index}')
            #No more cards to take and at the last slot
            if self.slot_index == 3:
                #TODO: move to next turn
                return {'value':self.get_possible_slot_choice(), 'type':'next_slots', 'player_index':player.index}
            else:
                #TODO: move slot and take card
                player_queue = self.create_player_queue(self.slot_index)
                for player in player_queue:
                    return {'value':self.get_possible_card_choice(self.slot_index+1), 'type':'next_slot', 'player_index':player.index}
        return None
        raise("Went through all players and they all have bets")
        # elif self.slot_index == 4:
        #     #TODO: logic at end
        #     return None
        # #possible slot indexes 0, 2, 3
        # else:
              
        #     if self.slots[self.slot_index] > 1:
        #         cards_taken_max = self.players[0].cards_taken
        #         for idx, player in enumerate(self.players):
        #                 if cards_taken_max > player.cards_taken:
        #                     return {'value':self.get_possible_card_choice(self.slot_index), 'type':'take', 'player_index':idx}
        #     else:
        #         #TODO: should generate moving to next slot
        #         return None
        #    if self.slot_index == 4:
        #         return self.get_possible_board_layout()
        #    else:
        #        return self.get_possible_card_choice(self.players[0])
        
    def get_possible_bet(self, index:int):
        bets = itertools.permutations(self.players[index].coins, 3)
        # print(bets)
        return bets