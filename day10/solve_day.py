from typing import List

from solver import Solver


class Day10(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _build_action_register(self, data: List) -> List:
        action_cycles = []

        for idx, instruction in enumerate(data):
            if instruction.startswith("addx"):
                action_cycles.append(0)
                value_to_add = int(instruction.split(" ")[1])
                action_cycles.append(value_to_add)

            elif instruction == "noop":
                action_cycles.append(0)

        return action_cycles

    def part1(self, data: List) -> int:
        action_cycles = self._build_action_register(data)

        register = 1
        signal_strengths = []
        signal_cycles = list(range(20, len(action_cycles), 40))

        for idx, val in enumerate(action_cycles):
            actual_idx = idx + 1
            if actual_idx in signal_cycles:
                signal_strengths.append(register * actual_idx)
            register += val

        return sum(signal_strengths)

    def part2(self, data: List) -> str:
        action_cycles = self._build_action_register(data)

        # Initialise all of the parameters we will use
        crt_rows = []
        curr_row = ""
        curr_col = 0
        row_num = 0
        ROW_WIDTH = 40
        sprite_pos = 1

        for idx, val in enumerate(action_cycles):
            curr_col = idx - (ROW_WIDTH * row_num)
            if abs(curr_col - sprite_pos) <= 1:
                curr_row += "\u2588"
            else:
                curr_row += " "

            if (idx + 1) % ROW_WIDTH == 0 and idx > 1:
                crt_rows.append(curr_row)
                row_num += 1
                curr_row = ""
            sprite_pos += val

        for row in crt_rows:
            print(row)

        return "ABOVE"


def solve_day(day: int, use_sample: bool):
    solver = Day10(day, use_sample)
    solver.solve()
