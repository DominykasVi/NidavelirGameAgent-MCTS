from card_deck import CardDeck
from card import Card
from typing import List, Dict
from bank import Bank
from coin import Coin
import random

class Player:
    def __init__(self, index:int, crystal:int, bank_reference:Bank) -> None:
        self.index = index
        self.name = f"Player{index}"
        self.card_deck = CardDeck()
        self.crystal = crystal
        self.bank = bank_reference

        self.bets:List[Coin] = []
        self.coins:List[Coin] = [Coin(0, True), Coin(2), Coin(3), Coin(4), Coin(5)]
        self.left_over_coins = []

        self.distinction_cards = 0
        self.bonus_points = 0
        self.cards_taken = 0

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

    def make_bet(self, bets:List[Coin]) -> None:
        coins_copy = self.coins.copy()
        for bet in bets:
            if bet not in self.coins:
                raise Exception("Trying to bet a coin that doesn't exist")
            coins_copy.remove(bet)
        self.bets = bets
        self.left_over_coins = coins_copy
        #TODO: can be removed later 
        try:  
            assert(len(self.bets)+len(self.left_over_coins) == 5)
        except:
            raise Exception(f"Coins don't add up to five.\n Betted coins:{self.bets}. Left over: {self.left_over_coins}")


    def take_card(self, cards_to_choose: List[Card], card_to_take:Card) -> List[Card]:
        if card_to_take not in cards_to_choose:
            raise Exception("Trying to take a card that doesn't exist")
        self.add_card(card_to_take)
        cards_to_choose.remove(card_to_take)
        return cards_to_choose, card_to_take

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

    def increase_coin(self, value: int, coin_to_increase:Coin) -> None:
        if coin_to_increase.exchangeable == True:
            raise Exception("Cannot increase an exchange coin")

        print(f"{self.name} incresed coin {coin_to_increase} to", end=' ')

        new_coin_value = self.bank.take_coin((coin_to_increase.value+value))
        new_coin = Coin(new_coin_value)

        if coin_to_increase in self.bets:
            coin_index = self.bets.index(coin_to_increase)
            self.bets[coin_index] = new_coin
        elif coin_to_increase in self.left_over_coins:
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
        print(f"Cards taken: {self.cards_taken}")
        print(f"Coin points: {self.get_coin_points()}")
        print(f"Card points: {self.card_deck.calculate_points()}")
        print(f"Bonus points: {self.get_bonus_points()}")
        print(f"Total points: {self.get_player_points()}")

    def get_color_count(self, color:str) -> int:
        return self.card_deck.get_color_count(color)


