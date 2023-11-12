import math
from typing import List, Any

class Node:
    def __init__(self, parent=None) -> None:
        self.score = 0
        self.iterations = 0
        self.parent = parent
        self.children = []
        self.constant = 2

    def calculate_node_value(self, total_runs:int) -> int:
        if self.iterations == 0:
            return -1
        return (self.score/self.iterations) + self.constant * math.sqrt(math.log(total_runs)/self.iterations)
    

class MCTS:
    def __init__(self) -> None:
        self.total_runs = 1
        self.max_iterations = 100

    def run_simulation(self, possible_choices: List[Any]):
        for _ in range(self.max_iterations):
            pass