import json
from copy import deepcopy
import time
from typing import List

from solver import Solver


class Day13(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _pair_in_order(self, x, y) -> bool:
        x_is_list = isinstance(x, list)
        x_is_int = isinstance(x, int)
        y_is_list = isinstance(y, list)
        y_is_int = isinstance(y, int)

        if x_is_int and y_is_list:
            return self._pair_in_order([x], y)

        if x_is_list and y_is_int:
            return self._pair_in_order(x, [y])

        if x_is_int and y_is_int:
            if x == y:
                raise ValueError("Numbers equal")
            if x > y:
                return False

            return True

        if x_is_list and y_is_list:
            while len(x) > 0 and len(y) > 0:
                a = x.pop(0)
                b = y.pop(0)

                try:
                    comparison = self._pair_in_order(a, b)
                    if comparison is None:
                        continue
                    else:
                        return comparison
                except ValueError:
                    continue

            if len(x) == 0 and len(y) > 0:
                return True
            if len(x) > 0 and len(y) == 0:
                return False

    def part1(self, data: List) -> None:
        pairs = []
        current_pair = []
        for line in data:
            if line == "":
                pairs.append(current_pair)
                current_pair = []
            else:
                current_pair.append(json.loads(line))
        pairs.append(current_pair)

        correct_pairs = []
        for idx, pair in enumerate(pairs):
            correct_order = self._pair_in_order(*pair)
            if correct_order:
                correct_pairs.append(idx + 1)
        return sum(correct_pairs)

    def sort_lines(lines: List) -> List:
        pass

    def part2(self, data: List) -> None:
        packets = [
            [[2]],
            [[6]],
        ]

        for line in data:
            if line != "":
                packets.append(json.loads(line))

        packets_sorted = False

        iters = -1
        while not packets_sorted:
            # Assume true
            packets_sorted = True
            iters += 1
            for idx in range(len(packets) - 1):
                packet_1 = deepcopy(packets[idx])  # Make copies
                packet_2 = deepcopy(packets[idx + 1])

                if not self._pair_in_order(packet_1, packet_2):
                    packets_sorted = False
                    packets[idx], packets[idx + 1] = packets[idx + 1], packets[idx]

        first_divisor = packets.index([[2]]) + 1
        second_divisor = packets.index([[6]]) + 1

        return first_divisor * second_divisor


def solve_day(day: int, use_sample: bool):
    solver = Day13(day, use_sample)
    solver.solve()
