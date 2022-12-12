from typing import List

from solver import Solver


class Day10(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List) -> None:
        register = 1
        action_cycles = []

        for idx, instruction in enumerate(data):
            if instruction.startswith("addx"):
                action_cycles.append(0)
                value_to_add = int(instruction.split(" ")[1])
                action_cycles.append(value_to_add)

            elif instruction == "noop":
                action_cycles.append(0)

        signal_strengths = []
        signal_cycles = list(range(20, len(action_cycles), 40))
        print("Signal cycles", signal_cycles)

        for idx, val in enumerate(action_cycles):
            actual_idx = idx + 1
            if actual_idx in signal_cycles:
                signal_strengths.append(register * actual_idx)
            register += val

        return sum(signal_strengths)

    def part2(self, data: List) -> None:
        pass


def solve_day(day: int, use_sample: bool):
    solver = Day10(day, use_sample)
    solver.solve()
