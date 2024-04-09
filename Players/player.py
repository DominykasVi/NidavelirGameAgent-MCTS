from copy import deepcopy
from card_deck import CardDeck
from card import Card
from typing import List, Dict, Tuple
from bank import Bank
from coin import Coin
import random


class Player:
    def __init__(self, index: int, crystal: int, bank_reference: Bank) -> None:
        self.index = index
        self.name = f"Player{index}"
        self.card_deck = CardDeck()
        self.crystal = crystal
        self.bank = bank_reference
        self.player_type = 'base'

        self.bets: List[Coin] = []
        self.coins: List[Coin] = [
            Coin(0, True), Coin(2), Coin(3), Coin(4), Coin(5)]
        self.left_over_coins = []

        self.distinction_cards = 0
        self.bonus_points = 0
        self.cards_taken = 0
        self.card_taken = False
        self.bet_made = False
        self.can_skip = False
        
        # self.id = self
        # self.debug = 0

    def __eq__(self, __value: object) -> bool:
        return (self.name == __value.name and self.crystal == __value.crystal)

    def __str__(self) -> str:
        return f"{self.name} ({self.crystal})"

    def __repr__(self) -> str:
        return f"{self.name} ({self.crystal})"

    # def add_card_to_deck(self, card:Card) -> None:
    #     self.card_deck.add_card(card)
    def set_crystal(self, crystal: int) -> None:
        self.crystal = crystal

    def make_bet(self, bets: List[Coin]) -> None:
        coins_copy = deepcopy(self.coins)
        for bet in bets:
            if bet not in self.coins:
                raise Exception("Trying to bet a coin that doesn't exist")
            coins_copy.remove(bet)
        self.bets = bets
        self.left_over_coins = coins_copy
        self.bet_made = True
        # TODO: can be removed later
        try:
            assert (len(self.bets)+len(self.left_over_coins) == 5)
        except:
            raise Exception(
                f"Coins don't add up to five.\n Betted coins:{self.bets}. Left over: {self.left_over_coins}")

    def has_row(self) -> bool:
        limit = self.card_deck.heroes
        for key in self.card_deck.card_count.keys():
            if key in ['black', 'coin']:
                continue
            if self.card_deck.card_count[key] <= limit:
                return False
        return True

    def choose_hero(self, hero_cards: List[Card], hero_to_take: Card) -> Tuple[List[Card], Card]:
        if hero_to_take not in hero_cards:
            raise Exception("Trying to take a card that doesn't exist")
        self.add_card(hero_to_take)
        hero_cards.remove(hero_to_take)
        self.cards_taken += 1
        self.card_taken = True
        self.card_deck.heroes += 1
        return hero_cards, hero_to_take

    def discard_cards(self, cards_to_discard: List[Card]) -> List[Card]:
        for card in cards_to_discard:
            self.card_deck.remove_card(card.index)
        return cards_to_discard

    def take_card(self, cards_to_choose: List[Card], card_to_take: Card) -> List[Card]:
        if card_to_take not in cards_to_choose:
            raise Exception("Trying to take a card that doesn't exist")
        self.add_card(card_to_take)
        cards_to_choose.remove(card_to_take)
        self.cards_taken += 1
        self.card_taken = True
        return cards_to_choose, card_to_take

    def add_card(self, card: Card, in_bets: bool = None) -> None:
        # if card.color == 'coin':
        self.card_deck.add_card(card)
            # self.increase_coin(card.value, in_bets)
        # else:
            # self.card_deck.add_card(card)
            # TODO recruit_hero?

    def make_coin_exchange(self, bet_index: int, bank: Bank) -> None:
        if self.bets[bet_index].exchangeable == True:
            # print("Made exchange. Player coins", self.coins,"\nLeft over coins:", self.left_over_coins)
            bigger_coin = max(self.left_over_coins, key=lambda x: x.value)
            lower_coin = min(self.left_over_coins, key=lambda x: x.value)

            self.coins.remove(bigger_coin)
            self.left_over_coins.remove(bigger_coin)

            new_coin_value = bank.take_coin(bigger_coin.value,
                (bigger_coin.value+lower_coin.value))
            new_coin = Coin(new_coin_value)

            # self.bets[bet_index] = new_coin
            self.coins.append(new_coin)
            self.left_over_coins.append(new_coin)
            # print(f"Changed {bigger_coin} -> {new_coin}, new left coins", self.left_over_coins, " new coins", self.coins)

    def remove_bets(self) -> None:
        self.bets.clear()
        self.bet_made = False

    def increase_coin(self, value: int, coin_to_increase: Coin, in_bets: bool) -> None:
        try:
            if coin_to_increase.exchangeable == True:
                raise Exception("Cannot increase an exchange coin")

            # print(f"{self.name} incresed coin {coin_to_increase} to", end=' ')

            new_coin_value = self.bank.take_coin(coin_to_increase.value,
                (coin_to_increase.value+value))
            new_coin = Coin(new_coin_value)

            if in_bets:
                coin_index = self.bets.index(coin_to_increase)
                self.bets[coin_index] = new_coin
            elif in_bets == False:
                self.left_over_coins.remove(coin_to_increase)
                self.left_over_coins.append(new_coin)

            self.coins.remove(coin_to_increase)
            self.coins.append(new_coin)
        except Exception as err:
            raise(err)
        # print(new_coin)

    def get_coin_points(self) -> int:
        return sum(x.value for x in self.coins)

    def remove_zero_coin(self) -> None:
        for coin in self.coins:
            if coin.value == 0:
                self.coins.remove(coin)
                break

    def add_hero_points(self):
        bonus_points = 0

        dwerg_points = {0:0, 1: 13, 2: 40, 3: 81, 4: 108, 5: 135}
        dwerg_count = 0

        for hero in self.card_deck.card_group['black']:
            if hero.name == 'ASTRID':
                bonus_points += max(self.coins, key=lambda x: x.value).value
            if hero.name == 'SKAA':
                bonus_points += 17
            if hero.name == 'GRID':
                bonus_points += 7
            if hero.name == 'IDUNN':
                bonus_points += self.card_deck.card_count['blue'] * 2
            if hero.name == 'DWERG':
                dwerg_count += 1

        if dwerg_count > 5:
            raise (Exception('Too high dwerg count'))

        bonus_points += dwerg_points[dwerg_count]
        return bonus_points

    def get_bonus_points(self) -> int:
        bonus = 0
        if self.crystal == 6:
            bonus += 3

        bonus += self.add_hero_points()
        return self.bonus_points + bonus

    def get_player_points(self) -> int:
        card_points = self.card_deck.calculate_points()
        coin_points = self.get_coin_points()
        bonus_points = self.get_bonus_points()
        return card_points + coin_points + bonus_points

    def add_red_bonus(self) -> None:
        max_coin = max(self.coins, key=lambda x: x.value)
        self.bonus_points += max_coin.value

    def print_player_points(self) -> None:
        print(self.name)
        print(f"Cards taken: {self.cards_taken}")
        print(f"Coin points: {self.get_coin_points()}")
        print(f"Card points: {self.card_deck.calculate_points()}")
        print(f"Bonus points: {self.get_bonus_points()}")
        print(f"Total points: {self.get_player_points()}")

    def get_player_points_str(self) -> str:
        values = ''
        values += self.name + '\n'
        values += f"Cards taken: {self.cards_taken}\n"
        values += f"Coin points: {self.get_coin_points()}\n"
        values += f"Card points: {self.card_deck.calculate_points()}\n"
        values += f"Bonus points: {self.get_bonus_points()}\n"
        values += f"Total points: {self.get_player_points()}"
        return values

    def get_color_count(self, color: str) -> int:
        return self.card_deck.get_color_count(color)
