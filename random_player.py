import random
from typing import Dict, List
from card import Card
from player import Player


class RandomPlayer(Player):
    
    def make_bet(self, possible_choices:Dict[int, List[Card]]) -> None:
        coins_to_bet = self.coins.copy()
        chosen_bets = []
        for _ in possible_choices:
            coin_choice = random.choice(coins_to_bet)
            chosen_bets.append(coin_choice)
            coins_to_bet.remove(coin_choice)
        
        super().make_bet(chosen_bets)

    def take_card(self, cards_to_choose: List[Card]) -> List[Card]:
        taken_card = random.choice(cards_to_choose)
        return super().take_card(cards_to_choose, taken_card)
        
        