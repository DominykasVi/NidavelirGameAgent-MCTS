import random
from typing import Dict, List
from bank import Bank
from card import Card
from Players.player import Player
from card_deck import CardDeck
from coin import Coin
from game_state import GameState


class RandomPlayer(Player):
    def __init__(self, index: int, crystal: int, bank_reference: Bank, coins: List[Coin] = None,
                 bets=None, left_over=None, card_deck: CardDeck = None) -> None:
        super().__init__(index, crystal, bank_reference)
        if coins is not None:
            self.coins = coins
        if bets is not None:
            self.bets = bets
        if left_over is not None:
            self.left_over_coins = left_over
        if card_deck is not None:
            self.card_deck = card_deck
            self.cards_taken = len(card_deck.cards)

    def make_bet(self, possible_choices: Dict[int, List[Card]]=None, game_state: GameState=None, predefined_bet=None) -> None:
        if predefined_bet is not None:
            super().make_bet(predefined_bet)
        else:
            coins_to_bet = [coin for coin in self.coins if coin not in self.bets]
            chosen_bets = self.bets
            for _ in range(len(chosen_bets), len(possible_choices)):
                coin_choice = random.choice(coins_to_bet)
                chosen_bets.append(coin_choice)
                coins_to_bet.remove(coin_choice)

            super().make_bet(chosen_bets)

    def choose_hero(self, hero_cards: List[Card], hero_to_take: Card = None) -> Card:
        if hero_to_take is None:
            hero_to_take = random.choice(hero_cards)
            if hero_to_take.name == 'HOURYA' and self.card_deck.card_count['blue'] < 5 and len(hero_cards) == 1:
                return hero_cards, None
            while (hero_to_take.name == 'HOURYA' and self.card_deck.card_count['blue'] < 5) \
                or (hero_to_take.name == 'DAGDA' and sum([self.card_deck.card_count[key] for key in self.card_deck.card_count.keys()
                                                          if key in ['violet', 'blue', 'orange', 'red']]) < 2) \
                or (hero_to_take.name == 'BONFUR' and sum([self.card_deck.card_count[key] for key in self.card_deck.card_count.keys()
                                                          if key in ['green', 'blue', 'orange', 'red']]) < 1):
                hero_to_take = random.choice(hero_cards)
        return super().choose_hero(hero_cards, hero_to_take)

    def discard_cards(self, discard_card_count:int, available_colors:List[str], cards_to_discard:List[Card]=None) -> None:
        if cards_to_discard == None:
            selected_color = []
            i = 0
            cards_to_discard = []
            while i < discard_card_count:
                color = random.choice(available_colors)
                if color not in selected_color:
                    cards_to_discard.append(self.card_deck.card_group[color][-1])
                    selected_color.append(cards_to_discard[i-1].color)
                    i += 1
        return super().discard_cards(cards_to_discard)

    def take_card(self, cards_to_choose: List[Card], taken_card=None, game_state=None, special_case=None) -> List[Card]:
        if taken_card is None:
            taken_card = random.choice(cards_to_choose)
        # if taken_card.color == 'coin':
        #     print('debug')
        return super().take_card(cards_to_choose, taken_card)

    def increase_coin(self, value: int, coin_to_increase: Coin = None, game_state=None):
        iterator = True
        if coin_to_increase is None:
            while iterator:
                coin_to_increase = random.choice(self.coins)
                if coin_to_increase.exchangeable == False:
                    iterator = False
        if coin_to_increase in self.left_over_coins:
            in_bets = False
        elif coin_to_increase in self.bets:
            in_bets = True
        else:
            in_bets = None
        super().increase_coin(value, coin_to_increase, in_bets)
