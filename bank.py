from typing import Dict

class Bank:
    def __init__(self, number_of_players:int) -> None:
        # coins {value: count}
        self.coins:Dict[int, int] = self.get_coins_from_file()
        if number_of_players == 2 or number_of_players == 3:
            self.coins[7] -= 2
            self.coins[9] -= 2
            self.coins[11] -= 2


    def get_coins_from_file(self) -> Dict[int, int]:
        with open('./Resources/coins.txt', 'r') as f:
            text = f.read()

        coins_text = text.split('\n')
        coins_dict = {}
        for coin in coins_text:
            if int(coin) in coins_dict.keys():
                coins_dict[int(coin)] += 1
            else:
                coins_dict[int(coin)] = 1

        return coins_dict

    def take_coin(self, coin_value: int) -> int:
        if coin_value < 5 and coin_value > 25:
            print("DEBUG")

        if coin_value > 25:
            coin_value = 25
        try:
            if self.coins[coin_value] > 0:
                self.coins[coin_value] -= 1
                self.error_check()
                return coin_value
            else:
                addition = 1
                while(True):
                    if (coin_value+addition) < 26 and self.coins[(coin_value+addition)] > 0:
                        self.coins[(coin_value+addition)] -= 1
                        self.error_check()
                        return (coin_value+addition)
                    elif (coin_value-addition) > 4 and self.coins[(coin_value-addition)] > 0:
                        self.coins[(coin_value-addition)] -= 1
                        self.error_check()
                        return (coin_value-addition)
                    else:
                        addition += 1
        except Exception as err:
            raise(err)
        # if self.coins[(coin_value+1)] > 0:
        #     self.coins[(coin_value+1)] -= 1
        #     self.error_check()

        #     return (coin_value+1)
        # elif self.coins[(coin_value-1)] > 0:
        #     self.coins[(coin_value-1)] -= 1
        #     self.error_check()
        #     return (coin_value-1)
        # else:
        #     return self.take_coin((coin_value-1))
                
    def error_check(self) -> None:
        for key in self.coins.keys():
            if self.coins[key] < 0:
                raise("Negative coins")
                exit()
    