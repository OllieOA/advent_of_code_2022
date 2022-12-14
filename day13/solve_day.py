import json
from typing import List

from solver import Solver


class Day13(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _parse_pair(self, x, y) -> bool:
        print("CHECKING PAIR", x, "AGAINST", y)
        x_is_list = isinstance(x, list)
        x_is_int = isinstance(x, int)
        y_is_list = isinstance(y, list)
        y_is_int = isinstance(y, int)

        if x_is_int and y_is_int:
            if x == y:
                print("RAISING EQUAL")
                raise ValueError("Numbers equal")
            if x > y:
                return False
            return True

        if x_is_list and y_is_list:
            if len(x) == 0 and len(y) >= 0:
                return True
            if len(y) == 0 and len(x) >= 0:
                return False

            all_true = []
            print("ZIPPING:", list(zip(x[: len(y)], y)))
            for a, b in zip(x[: len(y)], y):
                print("ALL TRUE:", all_true)
                print("COMPARING INTS", a, b)
                try:
                    print("COMPARISON INT RESULT:", self._parse_pair(a, b))
                    all_true.append(self._parse_pair(a, b))
                except ValueError:
                    continue

            if len(x) > len(y):
                return False
            print("RETURNING ALL TRUE", all_true)
            return all(all_true)

        if x_is_int and y_is_list:
            print("X INT, Y LIST")
            return self._parse_pair([x], y)

        if x_is_list and y_is_int:
            print("X LIST, Y INT")
            return self._parse_pair(x, [y])

        raise Exception

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
            correct_order = self._parse_pair(*pair)
            if correct_order:
                correct_pairs.append(idx + 1)
            print(
                f"CHECKING PAIR #{idx + 1}",
                pair[0],
                "WITH",
                pair[1],
                "CORRECT ORDER:",
                correct_order,
                "\n",
            )

        return sum(correct_pairs)

    def part2(self, data: List) -> None:
        pass


def solve_day(day: int, use_sample: bool):
    solver = Day13(day, use_sample)
    solver.solve()
