from card import Card
from typing import List, Dict

class CardDeck:
    def __init__(self, number_of_players:int=5, initialization:bool=False) -> None:

        self.card_count:Dict[str, int] = {'red':0, 'green':0, 'orange':0, 'violet':0, 'blue':0, 'coin':0}

        if initialization:
            self.cards:Dict[int, Card] = {}
            age_one_cards_list, age_two_cards_list = self.read_cards_from_file(number_of_players)
            self.put_cards_into_dict(age_one_cards_list, age_two_cards_list)
        else:
            self.cards:Dict[int, Card] = {}

        
        self.violet_points = {
            0: 0,
            1: 3,
            2: 7,
            3: 12,
            4: 18,
            5: 25,
            6: 33,
            7: 42,
            8: 52,
            9: 63,
            10: 75,
            11: 88,
            12: 102,
            13: 117,
            14: 133,
            15: 150
        }
        
    def put_cards_into_dict(self, age_one_cards_list, age_two_cards_list):
        index = 0

        for card in age_one_cards_list:
            card.age = 1
            card.index = index
            self.add_card(card)
            index += 1
        for card in age_two_cards_list:
            card.age = 2
            card.index = index
            self.add_card(card)
            index += 1

        
    def parse_card_text(self, input_text:str) -> List[Card]:
        text_list = input_text.split('\n')
        return [Card(value.split(' ')[0], value.split(' ')[1]) for value in  text_list if value != '']

    def read_cards_from_file(self, number_of_players:int) -> (List[Card],List[Card]):
        with open(f'cards_{number_of_players}.txt', 'r') as f:
                text = f.read()
        age_one_text, age_two_text = text.split('---')
        return self.parse_card_text(age_one_text), self.parse_card_text(age_two_text)

    def print_card_deck(self) -> None:
        for key in self.cards.keys():
            print(f"{key} -> {self.cards[key]}")
    
    def get_age_one_cards(self) -> List[Card]:
        return [self.cards[key] for key in self.cards.keys() if self.cards[key].age == 1]
    
    def get_age_two_cards(self) -> List[Card]:
        return [self.cards[key] for key in self.cards.keys() if self.cards[key].age == 2]
    
    def remove_card(self, index:int) -> None:
        self.card_count[self.cards[index].color] -= 1
        self.cards.pop(index)

    def add_card(self, card:Card) -> None:
        self.cards[card.index] = card
        self.card_count[card.color] += 1

    def calculate_points(self) -> int:
        green_card_count = 0
        violet_card_count = 0
        orange_card_count = 0

        blue_sum = 0
        orange_sum = 0
        red_sum = 0

        for key in self.cards.keys():
            if self.cards[key].color == 'green':
                green_card_count += 1
            elif self.cards[key].color == 'violet':
                violet_card_count += 1
            elif self.cards[key].color == 'blue':
                blue_sum += self.cards[key].value
            elif self.cards[key].color == 'red':
                red_sum += self.cards[key].value
            elif self.cards[key].color == 'orange':
                orange_sum += self.cards[key].value
                orange_card_count += 1
        
        card_sum = blue_sum + red_sum + (orange_sum * self.card_count['orange']) + self.violet_points[self.card_count['violet']] + pow(self.card_count['green'], 2)
        return card_sum

    def get_color_count(self, color:str) -> int:
        return self.card_count[color]
# cd = CardDeck(True)
# cd.print_card_deck()
# age_one_cards = cd.get_age_two_cards()
# for card in age_one_cards:
#     print(card)