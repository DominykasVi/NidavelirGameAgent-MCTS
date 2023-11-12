from card_deck import CardDeck
from card import Card
from typing import List, Dict
from bank import Bank
from coin import Coin
import random

class Player:
    def __init__(self, name:str, crystal:int, bank_reference:Bank) -> None:
        self.name = name
        self.card_deck = CardDeck()
        self.crystal = crystal
        self.bank = bank_reference

        self.bets:List[Coin] = []
        self.coins:List[Coin] = [Coin(0, True), Coin(2), Coin(3), Coin(4), Coin(5)]
        self.left_over_coins = []

        self.distinction_cards = 0
        self.bonus_points = 0

        # self.debug = 0
    def __eq__(self, __value:object) -> bool:
        return (self.name == __value.name and self.crystal == __value.crystal)

    def __str__(self) -> str:
        return f"{self.name} ({self.crystal})"
    
    def __repr__(self) -> str:
        return f"{self.name} ({self.crystal})"

    # def add_card_to_deck(self, card:Card) -> None:
    #     self.card_deck.add_card(card)
    def set_crystal(self, crystal:int) -> None:
        self.crystal = crystal

    def make_bet(self, possible_choices:Dict[int, List[Card]]) -> None:
        coins_to_bet = self.coins.copy()
        for _ in possible_choices:
            coin_choice = random.choice(coins_to_bet)
            self.bets.append(coin_choice)
            coins_to_bet.remove(coin_choice)
        self.left_over_coins = coins_to_bet

    def make_bet_input(self, slots:Dict[int, List[Card]]) -> None:
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
    def take_card(self, cards_to_choose: List[Card]) -> List[Card]:
        taken_card = random.choice(cards_to_choose)
        self.add_card(taken_card)
        cards_to_choose.remove(taken_card)
        return cards_to_choose, taken_card


    def add_card(self, card : Card) -> None:
        if card.color == 'coin':
            self.increase_coin(card.value)
        else:
            self.card_deck.add_card(card)
            # TODO recruit_hero?


    def make_coin_exchange(self, bet_index:int) -> None:
        if self.bets[bet_index].exchangeable == True:
            # print("Made exchange. Player coins", self.coins,"\nLeft over coins:", self.left_over_coins)
            bigger_coin = max(self.left_over_coins, key=lambda x: x.value)
            lower_coin = min(self.left_over_coins, key=lambda x: x.value)

            self.coins.remove(bigger_coin)
            self.left_over_coins.remove(bigger_coin)

            new_coin_value = self.bank.take_coin((bigger_coin.value+lower_coin.value))
            new_coin = Coin(new_coin_value)

            self.bets[bet_index] = new_coin
            self.coins.append(new_coin)
            self.left_over_coins.append(new_coin)
            # print(f"Changed {bigger_coin} -> {new_coin}, new left coins", self.left_over_coins, " new coins", self.coins)
        

    def remove_bets(self) -> None:
        self.bets.clear()

    def increase_coin(self, value: int) -> None:
        iterator = True
        while iterator:
            coin_to_increase = random.choice(self.coins)
            if coin_to_increase.exchangeable == False:
                iterator = False
        print(f"{self.name} incresed coin {coin_to_increase} to", end=' ')

        new_coin_value = self.bank.take_coin((coin_to_increase.value+value))
        new_coin = Coin(new_coin_value)

        if coin_to_increase in self.bets:
            coin_index = self.bets.index(coin_to_increase)
            self.bets[coin_index] = new_coin
        else:
            self.left_over_coins.remove(coin_to_increase)
            self.left_over_coins.append(new_coin)

        self.coins.remove(coin_to_increase)
        self.coins.append(new_coin)
        print(new_coin)

    def get_coin_points(self) -> int:
        return sum(x.value for x in self.coins)
    
    def remove_zero_coin(self) -> None:
        for coin in self.coins:
            if coin.value == 0:
                self.coins.remove(coin)
                break

    def get_bonus_points(self) -> int:
        if self.crystal == 6:
            self.bonus_points += 3
        
        return self.bonus_points

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
        print(f"Coin points: {self.get_coin_points()}")
        print(f"Card points: {self.card_deck.calculate_points()}")
        print(f"Bonus points: {self.get_bonus_points()}")
        print(f"Total points: {self.get_player_points()}")

    def get_color_count(self, color:str) -> int:
        return self.card_deck.get_color_count(color)


