import json
from typing import List

from solver import Solver


class Day13(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _parse_element(self, element: str) -> List:
        output_element = json.loads(element)
        # output_element = []
        # parsing_element = element[1:-1]  # Discard outer brackets
        # parsed = False
        # while not parsed:
        #     # Find the inner-most [] combination

        #     if "[" in parsing_element:
        #         opening_bracket_index = -1
        #         closing_bracket_index = -1
        #         for idx, object in enumerate(parsing_element):
        #             if object == "[":
        #                 opening_bracket_index = idx
        #             if object == "]" and opening_bracket_index > -1:
        #                 closing_bracket_index = idx

        #         if opening_bracket_index == -1 and closing_bracket_index == -1:
        #             opening_bracket_index = 0  # Can use the whole element

        #         sub_element = [
        #             int(x)
        #             for x in parsing_element[opening_bracket_index : closing_bracket_index + 1]
        #         ]

        #         output_element.append()

        #     parsed = len(element) == 0

        return output_element

    def part1(self, data: List) -> None:
        pairs = []
        current_pair = []
        for line in data:
            if line == "":
                pairs.append(current_pair)
                current_pair = []
            else:
                current_pair.append(line)
        pairs.append(current_pair)

        parsed_pairs = []
        for pair in pairs:
            curr_pair = []
            for element in pair:
                current_pair.append(self._parse_element(element))
            parsed_pairs.append(current_pair)

        print(parsed_pairs)

    def part2(self, data: List) -> None:
        pass


def solve_day(day: int, use_sample: bool):
    solver = Day13(day, use_sample)
    solver.solve()
