from typing import List

import numpy as np

from solver import Solver


class Day12(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List) -> None:
        grid_map_lists = []
        for row in data:

            row_extract = []
            grid_map_lists.append()

        pass

    def part2(self, data: List) -> None:
        pass


def solve_day(day: int, use_sample: bool):
    solver = Day12(day, use_sample)
    solver.solve()
