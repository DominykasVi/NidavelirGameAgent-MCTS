from typing import Dict

class Bank:
    def __init__(self, number_of_players:int) -> None:
        # coins {value: count}
        self.coins:Dict[int, int] = self.get_coins_from_file()
        if number_of_players == 2 or number_of_players == 3:
            self.coins[7] -= 2
            self.coins[9] -= 2
            self.coins[11] -= 2
        self.coin_limits = {
            5: number_of_players+2,
            6: 2,
            7: self.coins[7],
            8: 2,
            9: self.coins[9],
            10: 2,
            11: self.coins[11],
            12: 2,
            13: 2,
            14: 2,
            15: 1,
            16: 1,
            17: 1,
            18: 1,
            19: 1,
            20: 1,
            21: 1,
            22: 1,
            23: 1,
            24: 1,
            25: 1,
        }


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

    def take_coin(self, old_coin_value, coin_value: int) -> int:
        if coin_value < 5 and coin_value > 25:
            print("DEBUG")

        if sum(self.coins.values()) == 0:
            return old_coin_value

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
                        return_value = coin_value+addition
                        break
                    elif (coin_value-addition) > 4 and self.coins[(coin_value-addition)] > 0:
                        self.coins[(coin_value-addition)] -= 1
                        self.error_check()
                        return_value = coin_value-addition
                        break
                    else:
                        addition += 1
                    if addition > 30:
                        raise(Exception('Too high coin count'))
                    
                if old_coin_value >= return_value:
                    return old_coin_value

                if old_coin_value == 5 and self.coins[5] < 2:
                    self.coins[5] += 1
                elif old_coin_value > 5 and self.coins[old_coin_value] < self.coin_limits[old_coin_value]:
                    self.coins[old_coin_value] += 1
                return return_value
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
    