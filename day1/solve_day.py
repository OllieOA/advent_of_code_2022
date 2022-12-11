from typing import List, Tuple

from solver import Solver


class Day1(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _get_elf_calories(self, data: List) -> List:
        elves = []
        curr_total_callories = 0
        for calorie in data:
            if calorie == "":
                elves.append(curr_total_callories)
                curr_total_callories = 0
                continue
            curr_total_callories += int(calorie)
        elves.append(curr_total_callories)  # Get the last one

        return elves

    def part1(self, data: List) -> int:
        elves = self._get_elf_calories(data)
        return max(elves)

    def part2(self, data: List) -> int:
        elves = self._get_elf_calories(data)
        return sum(sorted(elves, reverse=True)[:3])


def solve_day(day: int, use_sample: bool):
    solver = Day1(day, use_sample)
    solver.solve()
