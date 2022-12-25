from typing import List

from solver import Solver


class Day25(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day
        self.SNAFU_LOOKUP = {
            "0": 0,
            "1": 1,
            "2": 2,
            "=": -2,
            "-": -1,
        }

        self.DECIMAL_LOOKUP = [(x, 0 if x.isnumeric() else 1) for x, y in self.SNAFU_LOOKUP.items()]
        self.DECIMAL_LOOKUP.append(("0", 1))
        print(self.DECIMAL_LOOKUP)

    def _decimal_to_snafu(self, decimal: int) -> str:
        digits = []
        # print("----------------")
        # print("Converting", decimal)
        while decimal > 0:
            digits.append(decimal % 5)
            # print("Appended", digits[-1])
            decimal //= 5
            # print("Decimal now", decimal)

        # print("Digits:", digits)
        # Solution based on https://www.reddit.com/r/adventofcode/comments/zur1an/comment/j1lw5uc/?utm_source=share&utm_medium=web2x&context=3
        snafu_str, remainder = "", 0
        for digit in digits:
            # print("---")
            # print("Processing", digit)
            digit += remainder
            # print("Updated to", digit)
            s_char, remainder = self.DECIMAL_LOOKUP[digit]
            # print("Appending", s_char)
            snafu_str += s_char

        return snafu_str[::-1]

    def _snafu_to_decimal(self, snafu: str) -> int:
        places = [5**x for x in range(len(snafu) - 1, -1, -1)]
        components = [self.SNAFU_LOOKUP[x] for x in snafu]

        return sum([x * y for x, y in zip(places, components)])

    def part1(self, data: List) -> None:
        dec_number = sum([self._snafu_to_decimal(x) for x in data])
        return self._decimal_to_snafu(dec_number)

    def part2(self, data: List) -> None:
        pass


def solve_day(day: int, use_sample: bool):
    solver = Day25(day, use_sample)
    solver.solve()
