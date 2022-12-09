from typing import List, Tuple

from solver import Solver

class Day4(Solver):
    def __init__(self, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__

    def _get_group(self, group: str) -> Tuple[int]:
        group_spec = group.split(",")
        group0 = group_spec[0]
        group1 = group_spec[1]

        min_group0 = int(group0.split("-")[0])
        max_group0 = int(group0.split("-")[1])

        min_group1 = int(group1.split("-")[0])
        max_group1 = int(group1.split("-")[1])

        return (min_group0, max_group0, min_group1, max_group1)
    
    
    def part1(self, data: List) -> int:
        contained_count = 0
        for group in data:
            min_group0, max_group0, min_group1, max_group1 = self._get_group(group)

            if min_group0 <= min_group1 and max_group0 >= max_group1:
                contained_count += 1
            elif min_group1 <= min_group0 and max_group1 >= max_group0:
                contained_count += 1

        return contained_count

    def part2(self, data: List) -> int:
        any_overlap_count = 0
        for group in data:
            min_group0, max_group0, min_group1, max_group1 = self._get_group(group)

            group0_range = range(min_group0, max_group0)
            group1_range = list(range(min_group1, max_group1))

            for idx in group0_range:
                if idx in group1_range:
                    any_overlap_count += 0
                    break

        return any_overlap_count

def solve_day(use_sample: bool):
    solver = Day4(use_sample)
    solver.solve_day()