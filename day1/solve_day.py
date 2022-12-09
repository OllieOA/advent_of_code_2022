from typing import List, Tuple

from solver import Solver

class Day1(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _part1(self, data: List) -> Tuple[List, int]:
        elves = []
        curr_total_callories = 0
        for calorie in data:
            if calorie == "":
                elves.append(curr_total_callories)
                curr_total_callories = 0
                continue
            
            curr_total_callories += int(calorie)
        elves.append(curr_total_callories)  # Get the last one

        return max(elves), elves

    def _part2(self, data: List) -> Tuple[int, List]:
        _, elves = self._part1(data)
        return sum(sorted(elves, reverse=True)[:3]), []


def solve_day(day: int, use_sample: bool):
    solver = Day1(day, use_sample)
    solver.solve_day()