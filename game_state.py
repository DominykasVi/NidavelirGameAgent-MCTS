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

    def __str__(self):
        strings_to_print = []
        for player in self.players:
            strings_to_print.append(f"Player {player}")
            strings_to_print.append(f"Bets: {player.bets}")
        
        return '\n'.join(strings_to_print)

    def copy_state(self):
        return GameState(playing_board=deepcopy(self.playing_board),
                         players=deepcopy(self.players),
                         card_deck=deepcopy(self.deck),
                         bank=deepcopy(self.bank),
                         turn=self.turn,
                         slot_index=self.slot_index,
                         slots=self.slots,
                         mode=self.mode)
    
    def get_next_state(self):
        if self.slot_index == 1:
            for idx, player in enumerate(self.players):
                if len(player.bets) == 0:
                    # state_copy = self.copy_state()
                    # state_copy.players[idx].bets = self.get_possible_bet(idx)
                    return {'value':self.get_possible_bet(idx), 'type':'bets', 'player_index':idx}
            raise("Went through all players and they all have bets")
        else:
           cards_taken_max = self.players[0].cards_taken
           for idx, player in enumerate(self.players):
                if cards_taken_max > player.cards_taken:
                    return self.get_possible_card_choice(player)
           if self.slot_index == 4:
                return self.get_possible_board_layout()
           else:
               return self.get_possible_card_choice(self.players[0])
        
    def get_possible_bet(self, index:int):
        bets = itertools.permutations(self.players[index].coins)
        print(bets)
        return bets