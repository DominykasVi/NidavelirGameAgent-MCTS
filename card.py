class Card:
    def __init__(self, color:str, value:int=None, age:int = 0, index:int = None) -> None:
        self.color = color
        # print(color)
        # print(color != 'green' and color != 'violet')

        if color != 'green' and color != 'violet':
            self.value = int(value)
        else:
            self.value = value
        self.age = age
        self.index = index

    def __str__(self) -> str:
        return f"{self.color}:{self.value} ({self.age})"
    
    def __repr__(self) -> str:
        return f"{self.color}:{self.value} ({self.age})"