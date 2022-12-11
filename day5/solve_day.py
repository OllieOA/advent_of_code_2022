from collections import OrderedDict
from typing import List, Tuple

from solver import Solver


class Day5(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _get_top_row(self, crates: OrderedDict) -> str:
        bottom_row = []
        for column in crates.values():
            bottom_row.append(column[-1])

        return "".join(bottom_row)

    def _parse_crates_and_instructions(self, data) -> Tuple[OrderedDict, List]:
        label_row = -1
        for idx, line in enumerate(data):
            if "[" not in line:  # Crate definition finished
                label_row = idx
                break

        instructions_specs = data[(label_row + 2) :]

        # Parse crates
        crate_specs = data[label_row - 1 :: -1]
        crates = OrderedDict()
        for crate_spec in crate_specs:
            for idx in range((len(crate_spec) // 4) + 1):  # 4 chars per spec
                single_crate = crate_spec[4 * idx : (4 * idx + 3)]
                if (idx + 1) not in crates:
                    crates[idx + 1] = []

                stripped_crate = single_crate.replace("[", "").replace("]", "")
                if stripped_crate.isalpha():
                    crates[idx + 1].append(stripped_crate)
        # Parse instructions
        instructions = []
        for instruction in instructions_specs:
            parsed_instruction = [int(x) for x in instruction.split(" ") if x.isnumeric()]
            instructions.append(parsed_instruction)

        return crates, instructions

    def part1(self, data: List) -> None:
        crates, instructions = self._parse_crates_and_instructions(data)

        for instruction in instructions:
            num, source, dest = instruction

            for _ in range(num):
                target_crate = crates[source].pop()
                crates[dest].append(target_crate)

        return self._get_top_row(crates)

    def part2(self, data: List) -> None:
        crates, instructions = self._parse_crates_and_instructions(data)

        for instruction in instructions:
            num, source, dest = instruction

            substack = []
            for _ in range(num):
                substack.append(crates[source].pop())

            crates[dest].extend(substack[::-1])

        return self._get_top_row(crates)


def solve_day(day: int, use_sample: bool):
    solver = Day5(day, use_sample)
    solver.solve()
