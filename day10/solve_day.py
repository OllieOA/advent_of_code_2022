from typing import List

from solver import Solver


class Day10(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List) -> None:
        register = 1
        action_cycles = [] * len(data)
        print(action_cycles)
        for instruction in data:
            if instruction.startswith("addx"):
                value_to_add = int(instruction.split(" "))

            elif instruction == "noop":
                pass

    def part2(self, data: List) -> None:
        pass


def solve_day(day: int, use_sample: bool):
    solver = Day10(day, use_sample)
    solver.solve()
