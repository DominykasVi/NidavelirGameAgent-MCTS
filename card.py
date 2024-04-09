class Card:
    def __init__(self, color:str, value:int=None, age:int = 0, index:int = None, rank:int = 1, name:str=None) -> None:
        self.color = color

        if color != 'green' and color != 'violet' and color != 'black':
            self.value = int(value)
        else:
            self.value = value
        self.age = age
        self.index = index
        self.rank = rank
        self.name = name

    def __str__(self) -> str:
        if self.name == None:
            rep = f"{self.color}:{self.value} ({self.age})"
        else:
            rep = f"{self.name}:{self.value} ({self.rank})"
        return rep
    
    def __repr__(self) -> str:
        if self.name == None:
            rep = f"{self.color}:{self.value} ({self.age})"
        else:
            rep = f"{self.name}:{self.value} ({self.rank})"
        return rep
    
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.color == other.color and self.value == other.value and self.age == other.age and self.index == other.index
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)