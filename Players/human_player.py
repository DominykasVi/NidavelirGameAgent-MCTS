from typing import Dict, List
from card import Card
from game_state import GameState
from player import Player


class HumanPlayer(Player):
    # TODO: fix this to work with generic
    def make_bet_input(self, slots:Dict[int, List[Card]], game_state:GameState) -> None:
        coins_to_bet = self.coins.copy()
        for slot in slots.items():
            print("Please make a bet for this slot")
            for card in slot:
                print(card)
            coin = int(input())
            while int(coin) in self.bets:
                print("This amount has already been betted!")
                print(self.bets)
                print("Please imput bet amount again.")
                coin = int(input())
            coins_to_bet.remove(coin)
            self.bets.append(coin)
        self.left_over_coins = coins_to_bet
        # for cards in possible_choices:
        #     self.bets.append(random.choice(range(len(cards) + 1)))