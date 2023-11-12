from card_deck import CardDeck
from typing import List, Tuple, Dict
from card import Card

import random
from datetime import datetime

class PlayingBoard:
    def __init__(self, card_deck:CardDeck, seed=datetime.now().timestamp()) -> None:
        self.card_deck = card_deck
        # self.slot_1 = []
        # self.slot_2 = []
        # self.slot_3 = []
        random.seed(seed)

    def get_player_card_limit(self, age_split:int) -> int:
        if age_split == 3:
            return 5
        else:
            return 3
        
    def get_number_of_cards(self, limit, selection_deck:List[Card]) -> List[Card]:
        selected_cards = []
        for _ in range(limit):
            card = random.choice(selection_deck)
            selected_cards.append(card)
            # TODO: may be optimized
            self.card_deck.remove_card(card.index)
            selection_deck.remove(card)
        return selected_cards

    def generate_slots(self, age_split:int, turn_number:int) -> Dict[int, List[Card]]:
        # TODO: if cases for how many cards to generate by number of playees
        range_limit = self.get_player_card_limit(age_split)

        if turn_number <= age_split:
            selection_deck = self.card_deck.get_age_one_cards().copy()
        else:
            selection_deck = self.card_deck.get_age_two_cards().copy()


        return_list = {}
        for i in range(1, 4):
            selected_cards = self.get_number_of_cards(range_limit, selection_deck)
            return_list[i] = selected_cards
        return return_list

