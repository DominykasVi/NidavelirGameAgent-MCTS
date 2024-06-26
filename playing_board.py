import itertools
from card_deck import CardDeck
from typing import List, Tuple, Dict
from card import Card

import random
from datetime import datetime

class PlayingBoard:
    def __init__(self, card_deck:CardDeck, seed=datetime.now().timestamp()) -> None:
        self.card_deck = card_deck
        random.seed(seed)

        
    def get_number_of_cards(self, limit, selection_deck:List[Card]) -> List[Card]:
        selected_cards = []
        for _ in range(limit):
            try:
                card = random.choice(selection_deck)
                selected_cards.append(card)
                # TODO: may be optimized
                self.card_deck.remove_card(card.index)
                selection_deck.remove(card)
            except Exception as e:
                raise(e)
        return selected_cards

    def generate_slots(self, turn, age_split, number_of_cards) -> Dict[int, List[Card]]:
        if turn < age_split:
            selection_deck = self.card_deck.get_age_one_cards().copy()
        else:
            selection_deck = self.card_deck.get_age_two_cards().copy()


        return_dict = {}
        for i in range(1, 4):
            selected_cards = self.get_number_of_cards(number_of_cards, selection_deck)
            return_dict[i] = selected_cards
        return return_dict
    
    def generate_possible_slots(self, age_split:int, turn_number:int) -> List[Dict[int, List[Card]]]:
        range_limit = self.get_player_card_limit(age_split)

        if turn_number <= age_split:
            selection_deck = self.card_deck.get_age_one_cards().copy()
        else:
            selection_deck = self.card_deck.get_age_two_cards().copy()

        return list(itertools.permutations(selection_deck, range_limit*3))
        



