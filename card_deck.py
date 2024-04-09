from card import Card
from typing import List, Dict, Tuple


class CardDeck:
    def __init__(self, number_of_players: int = 5, initialization: bool = False) -> None:

        self.card_count: Dict[str, int] = {
            'red': 0, 'green': 0, 'orange': 0, 'violet': 0, 'blue': 0, 'coin': 0, 'black': 0}
        self.card_group: Dict[str, List[Card]] = {
            'red': [], 'green': [], 'orange': [], 'violet': [], 'blue': [], 'coin': [], 'black': []}

        self.heroes = 0
        self.hero_cards: List[Card] = []
        if initialization:
            self.cards: Dict[int, Card] = {}
            if number_of_players != 5:
                age_one_cards_list, age_two_cards_list = self.read_cards_from_file(
                    '2')
            else:
                age_one_cards_list, age_two_cards_list = self.read_cards_from_file(
                    '5')
            self.put_cards_into_dict(age_one_cards_list, age_two_cards_list)
            self.hero_cards: List[Card] = [Card(name='DWERG', index=200, color='black'),
                                           Card(name='DWERG', index=201,
                                                color='black'),
                                           Card(name='DWERG', index=202,
                                                color='black'),
                                           Card(name='DWERG', index=203,
                                                color='black'),
                                           Card(name='DWERG', index=204,
                                                color='black'),
                                           Card(name='SKAA', index=300,
                                                color='black'),
                                           Card(name='ASTRID', index=301,
                                                color='black'),
                                           Card(name='GRID', index=400,
                                                color='black'),
                                           Card(name='KRALL', index=500,
                                                color='red', value=7, rank=2),
                                           Card(name='TARAH', index=501, value=14,
                                                color='red'),
                                           Card(name='ARAL', index=600, rank=2,
                                                color='green'),
                                           Card(name='DAGDA', index=601, rank=3,
                                                color='green'),
                                           Card(name='AEGUR', index=700, rank=2,
                                                color='violet'),
                                           Card(name='BONFUR', index=701, rank=3,
                                                color='violet'),
                                           Card(name='ZORAL', index=800, value=1, rank=3,
                                                color='orange'),
                                           Card(name='LOKDUR', index=801, value=3, rank=1,
                                                color='orange'),
                                           Card(name='HOURYA', value=20, rank=1,
                                                index=900, color='blue'),
                                           Card(name='IDUNN', index=901, color='blue', value=7, rank=1)]
        else:
            self.cards: Dict[int, Card] = {}

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

        self.green_points = {
            0: 0,
            1: 1,
            2: 4,
            3: 9,
            4: 16,
            5: 25,
            6: 36,
            7: 49,
            8: 64,
            9: 81,
            10: 100,
            11: 121,
            12: 144,
            13: 169,
            14: 196,
            15: 225
        }

    def debug_return_slots_with_coin(self) -> List[Card]:
        return_list = []
        coin_found = False
        for card in self.get_age_two_cards():
            if card.color == 'coin' and coin_found == False:
                return_list.append(card)
                self.remove_card(card.index)
                coin_found = True
            elif len(return_list) < 3 and coin_found == True and card.color != 'coin':
                return_list.append(card)
                self.remove_card(card.index)
            elif len(return_list) > 3:
                break

        if len(return_list) < 3:
            for card in self.get_age_two_cards():
                if len(return_list) < 3:
                    return_list.append(card)
                    self.remove_card(card.index)
                else:
                    break

        return return_list

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

    def parse_card_text(self, input_text: str) -> List[Card]:
        text_list = input_text.split('\n')
        return [Card(value.split(' ')[0], value.split(' ')[1]) for value in text_list if value != '']

    def read_cards_from_file(self, card_file_name: str) -> (List[Card], List[Card]):
        with open(f'./Resources/cards_{card_file_name}.txt', 'r') as f:
            text = f.read()
        age_one_text, age_two_text = text.split('---')
        return self.parse_card_text(age_one_text), self.parse_card_text(age_two_text)

    def get_card_deck_string(self) -> str:
        values = []
        for key in self.cards.keys():
            values.append(f"{key} -> {self.cards[key]}")
        return '\n'.join(values)

    def get_age_one_cards(self) -> List[Card]:
        return [self.cards[key] for key in self.cards.keys() if self.cards[key].age == 1]

    def get_age_two_cards(self) -> List[Card]:
        return [self.cards[key] for key in self.cards.keys() if self.cards[key].age == 2]

    def remove_card(self, index: int) -> None:
        try:
            removed_card = self.cards.pop(index)
            self.card_count[removed_card.color] -= removed_card.rank
            self.remove_card_from_group(removed_card)
        except Exception as e:
            raise(Exception(e))

    def remove_card_from_group(self, card: Card) -> None:
        self.card_group[card.color].remove(card)

    def add_card(self, card: Card) -> None:
        if card.index < 200:
            self.cards[card.index] = card
            self.card_group[card.color].append(card)
            self.card_count[card.color] += card.rank
        else:
            self.cards[card.index] = card
            self.card_group[card.color].append(card)
            self.hero_cards.append(card)
            # self.card_count[card.color] += card.rank

    # def hero_rank_increase(self, hero_name:str) -> None:
    #     if hero_name == 'KRALL':
    #         self.hero_ranks['red'] += 2
    #     if hero_name == 'TARAH':
    #         self.hero_ranks['red'] += 1
    #     if hero_name == 'ARAL':
    #         self.hero_ranks['green'] += 2
    #     if hero_name == 'DAGDA':
    #         self.hero_ranks['green'] += 3
    #     if hero_name == 'AEGUR':
    #         self.hero_ranks['violet'] += 2
    #     if hero_name == 'BONFUR':
    #         self.hero_ranks['violet'] += 3
    #     if hero_name == 'ZORAL':
    #         self.hero_ranks['violet'] += 3

    # def get_hero_ranks_by_color(self, color:str) -> Tuple[int, int]:
    #     extra_ranks = 0
    #     extra_points = 0
    #     for card in self.hero_cards:
    #         if card.color == 'KRALL':
    #             ranks = 2
    #             points = 7
    #             color = 'red'
    #         if card.color == 'TARAH':
    #             ranks = 1
    #             points = 14
    #             color = 'red'
    #         if card.color == 'ARAL':
    #             ranks = 2
    #             points = 0
    #             color = 'green'
    #         if card.color == 'DAGDA':
    #             ranks = 3
    #             points = 0
    #             color = 'green'
    #         if card.color == 'AEGUR':
    #             ranks = 2
    #             points = 0
    #             color = 'violet'
    #         if card.color == 'BONFUR':
    #             ranks = 3
    #             points = 0
    #             color = 'violet'
    #         if card.color == 'ZORAL':
    #             ranks = 3
    #             points = 1
    #             color = 'orange'
    #         if card.color == 'LOKDUR':
    #             ranks = 1
    #             points = 3
    #             color = 'orange'
    #         if card.color == 'HOURYA':
    #             ranks = 1
    #             points = 20
    #             color = 'blue'
    #         if card.color == 'IDUNN':
    #             ranks = 1
    #             points = 7
    #             color = 'blue'

    def calculate_points(self) -> int:
        color_counts: Dict[str, int] = {
            'red': 0, 'green': 0, 'orange': 0, 'violet': 0, 'blue': 0, 'coin': 0, 'black': 0}

        blue_sum = 0
        orange_sum = 0
        red_sum = 0

        for key in self.cards.keys():
            if self.cards[key].color == 'green':
                color_counts['green'] += self.cards[key].rank
            elif self.cards[key].color == 'violet':
                color_counts['violet'] += self.cards[key].rank
            if self.cards[key].color == 'blue':
                blue_sum += self.cards[key].value
                color_counts['blue'] += self.cards[key].rank
            elif self.cards[key].color == 'red':
                red_sum += self.cards[key].value
                color_counts['red'] += self.cards[key].rank
            elif self.cards[key].color == 'orange':
                orange_sum += self.cards[key].value
                color_counts['orange'] += self.cards[key].rank
        # # --------------------
        # if color_counts['green'] != self.card_count['green']:
        #     raise (Exception('Green card count is off'))
        # if color_counts['violet'] != self.card_count['violet']:
        #     raise (Exception('Violet card count is off'))
        # if color_counts['blue'] != self.card_count['blue']:
        #     raise (Exception('Blue card count is off'))
        # if color_counts['red']  != self.card_count['orange']:
        #     raise (Exception('Orange card count is off'))
        # if color_counts['orange'] != self.card_count['red']:
        #     raise (Exception('Red card count is off'))
        # # --------------------

        if self.card_count['violet'] > 15:
            self.card_count['violet'] = 15
            color_counts['violet'] = 15
        if self.card_count['green'] > 15:
            color_counts['green'] = 15
            self.card_count['green'] = 15

        card_sum = blue_sum + red_sum + \
            (orange_sum * color_counts['orange']) + self.violet_points[color_counts['violet']
                                                                          ] + self.green_points[color_counts['green']]

        return card_sum

    def get_color_count(self, color: str) -> int:
        temp_count = self.card_count[color]
        for hero in self.hero_cards:
            if hero.color == color:
                temp_count += hero.rank
        return temp_count
# cd = CardDeck(True)
# cd.print_card_deck()
# age_one_cards = cd.get_age_two_cards()
# for card in age_one_cards:
#     print(card)
