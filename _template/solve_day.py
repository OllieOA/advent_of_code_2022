from typing import List

from solver import Solver

class DayX(Solver):
    def __init__(self, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
    
    
    def part1(self, data: List) -> None:
        pass

    def part2(self, data: List) -> None:
        pass

def solve_day(use_sample: bool):
    solver = DayX(use_sample)
    solver.solve_day()