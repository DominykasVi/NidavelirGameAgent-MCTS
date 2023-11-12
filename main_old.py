from card_deck import CardDeck
from playing_board import PlayingBoard
from player import Player
from bank import Bank
from card import Card
from coin import Coin
from typing import List
import random
import os

SEED = 10
NUMBER_OF_PLAYERS = 2
random.seed(SEED)

def exchange_crystals_two_players(players:List[Player]) -> None:
    if players[0].crystal != 6 and players[1].crystal != 6:
        temp = players[0].crystal
        players[0].crystal = players[1].crystal
        players[1].crystal = temp

def sort_players_by_crystal(players:List[Player]) -> List[Player]:
    if len(players) == 2:
        if players[0].crystal > players[1].crystal:
            exchange_crystals_two_players(players)
            return [players[0], players[1]]
        else:
            exchange_crystals_two_players(players)
            return [players[1], players[0]]

def get_player_with_highest_count(players:List[Player], color:str) -> Player:
    max_count = players[0].get_color_count(color)
    max_player = players[0]
    break_condition = True

    for player in players:
        new_count = player.get_color_count(color)
        if new_count > max_count:
            max_count = new_count
            max_player = player
            break_condition = True
        elif new_count == max_count and player != max_player:
            break_condition = False
        
    if break_condition:
        return max_player
    else:
        return None

def add_bonus_to_distinguished(player:Player, color:str, playing_board:PlayingBoard) -> None:
    print("Distinction card count: ", player.distinction_cards)
    if player.distinction_cards == 0:
        print("Giving bonus to player: ", player)
        if color == 'red':
            player.distinction_cards += 1
        elif color =='green':
            player.remove_zero_coin()
            player.coins.append(Coin(3, True))
            player.distinction_cards += 1
        elif color == 'orange':
            player.crystal = 6
            player.distinction_cards += 1
        elif color == 'violet':
            player.add_card(Card('violet', 'None', 0, 101))
            player.add_card(Card('violet', 'None', 0, 102))
            player.distinction_cards += 1
        elif color == 'blue':
            card_to_choose_from = playing_board.get_number_of_cards(3, playing_board.card_deck.get_age_two_cards())
            card_to_choose_from = player.take_card(card_to_choose_from)
            for card in card_to_choose_from:
                playing_board.card_deck.add_card(card)
            player.distinction_cards += 1

def print_players_color_count(players:List[Player], color):
    print(f"Players have number of {color}")
    for player in players:
        print(player, ": ", player.get_color_count(color))

def award_distinction_cards(players:List[Player], playing_board:PlayingBoard) -> None:
    colors = ['red', 'green', 'orange', 'violet', 'blue']
    for color in colors:
        distinguished_player = get_player_with_highest_count(players,color)
        print_players_color_count(players, color)
        if distinguished_player is not None:
            add_bonus_to_distinguished(player, color, playing_board)

def create_player_queue(players:List[Player], slot_number:int) -> List[Player]:
    player_queue = []

    helper_dict = {}
    for player in players:
        bet = player.bets[slot_number].value
        if bet in helper_dict.keys():
            helper_dict[bet].append(player)
        else:
            helper_dict[bet] = [player]
    sorted_helper_dict = dict(sorted(helper_dict.items(), reverse=True))
    # print(sorted_helper_dict)

    for key in sorted_helper_dict.keys():
        if len(sorted_helper_dict[key]) > 1:
            sorted_players = sort_players_by_crystal(sorted_helper_dict[key])
            player_queue.extend(sorted_players)
        else:
            player_queue.extend(sorted_helper_dict[key])

    return player_queue

def print_player_bets(players):
    for player in players:
        print(f"{player}, bets: ", player.bets, "lefover: ", player.left_over_coins)


if __name__ == "__main__":
    turn = 0
    card_deck = CardDeck(NUMBER_OF_PLAYERS, True)
    bank = Bank(NUMBER_OF_PLAYERS)
    # card_deck.print_card_deck()
    playing_board = PlayingBoard(card_deck)

    # mode 0 - run everything
    # mode 1 - make breaks
    mode = 1

    if NUMBER_OF_PLAYERS == 2:
        crystals = [4, 5]
    else:
        crystals = [1, 2, 3, 4, 5]

    if NUMBER_OF_PLAYERS < 4:
        turn_split = 4
    else:
        turn_split = 3

    players: List[Player] = []
    for i in range(NUMBER_OF_PLAYERS):
        crystal = random.choice(crystals)
        crystals.remove(crystal)
        players.append(Player(f"Player {i+1}", crystal, bank))

    # for player in players:
    #     print(player)

     
    while turn < turn_split*2:
        
        turn += 1
        if turn == turn_split+1:
            print("Granting players distinction bonuses")
            award_distinction_cards(players, playing_board)
            if mode == 1:
                input()
                clear = lambda: os.system('cls')
                clear()

        slots = playing_board.generate_slots(turn_split, turn)
        print("Turn: ", turn)
        print(slots)

        # DEBUG random    
        for player in players:
            player.make_bet(slots)

        # DEBUG bot vs human
        # players[0].make_bet(slots)
        # players[1].make_bet_input(slots)

        # # DEBUG
        # players[0].bets = [5, 4, 3]
        # players[1].bets = [5, 4, 3]

        for slot_index in slots.keys():
            bet_index = slot_index - 1
            
            if mode == 1:
                print("Turn: ", turn)
                print_player_bets(players)
                print("SLOT", slot_index, ": ", slots[slot_index])
            player_queue = create_player_queue(players, bet_index)

            if mode == 1:
                print("Player turns: ", player_queue)
                
            for player in player_queue:
                print(player)
                slots[slot_index] = player.take_card(slots[slot_index])
                player.make_coin_exchange(bet_index)
                # print(player)
                if mode == 1:
                    input()
                    
            if mode == 1:
                clear = lambda: os.system('cls')
                clear()

        for player in players:
            player.remove_bets()
    
    if mode == 1:
        input()
        clear = lambda: os.system('cls')
        clear()
    for player in players:
        print(player)
        player.card_deck.print_card_deck()
        player.print_player_points()