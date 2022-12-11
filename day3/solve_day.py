from typing import List

from solver import Solver


class Day3(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _part1(self, data: List) -> int:
        total_sum = 0
        for pack in data:
            compartment_1 = set([*pack[: len(pack) // 2]])
            compartment_2 = set([*pack[len(pack) // 2 :]])

            repeated_element = compartment_1.intersection(compartment_2).pop()

            if repeated_element.isupper():
                total_sum += ord(repeated_element) - 38
            else:
                total_sum += ord(repeated_element) - 96

        return total_sum

    def _part2(self, data: List) -> int:
        total_sum = 0
        elf_groups = [data[x : x + 3] for x in range(0, len(data), 3)]

        for elf_group in elf_groups:
            common_items = set()
            for rucksack in elf_group:
                if not common_items:
                    common_items = set([*rucksack])
                else:
                    common_items = common_items.intersection(set([*rucksack]))

            common_item = common_items.pop()

            if common_item.isupper():
                total_sum += ord(common_item) - 38
            else:
                total_sum += ord(common_item) - 96

        return total_sum


def solve_day(day: int, use_sample: bool):
    solver = Day3(day, use_sample)
    solver.solve()
