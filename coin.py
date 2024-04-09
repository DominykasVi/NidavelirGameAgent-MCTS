import uuid


class Coin:
    def __init__(self, value:int, exchangeable:bool = False) -> None:
        self.value = value
        self.exchangeable = exchangeable
        self.id = uuid.uuid4()

    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return f"{self.value}({self.exchangeable})"
    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id
        # return self.value == __value.value and self.exchangeable == __value.exchangeable
    def __hash__(self):
        return hash(self.id)
        # return hash((self.value, self.exchangeable))