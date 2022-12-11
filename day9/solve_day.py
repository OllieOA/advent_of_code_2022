import time
from typing import List

import numpy as np

from solver import Solver


class Day9(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day
        self.DIRECTIONS = {
            "U": [0, 1],
            "D": [0, -1],
            "L": [-1, 0],
            "R": [1, 0],
        }

    def _is_snap_rope_required(self, head_pos: List, tail_pos: List) -> bool:
        # True if rope needs to be snapped
        snap_required = abs(head_pos[0] - tail_pos[0]) > 1 or abs(head_pos[1] - tail_pos[1]) > 1
        return snap_required

    def _get_rope_direction_bias(self, parent_pos: List, child_pos: List) -> List[int]:
        pass

    def part1(self, data: List) -> None:
        pos_h = [0, 0]
        pos_t = [0, 0]

        all_pos_t = {",".join([str(x) for x in pos_t])}

        for instruction in data:
            direction = instruction.split(" ")[0]
            num = int(instruction.split(" ")[1])

            direction_vector = self.DIRECTIONS[direction]

            for _ in range(num):
                lag_pos_h = pos_h.copy()
                pos_h = [sum(i) for i in zip(pos_h, direction_vector)]
                if self._is_snap_rope_required(pos_h, pos_t):
                    pos_t = lag_pos_h
                    all_pos_t.add(",".join([str(x) for x in pos_t]))
        return len(all_pos_t)

    def part2(self, data: List) -> None:
        links = [[0, 0]] * 4

        all_pos_t = {",".join([str(x) for x in [0, 0]])}

        for instruction in data:
            direction = instruction.split(" ")[0]
            num = int(instruction.split(" ")[1])

            direction_vector = self.DIRECTIONS[direction]

            # TODO FIX THE LOGIC TO PULL THE ROPE IN RATHER THAN DRAG
            for _ in range(num):
                parent_link_prev = links[0].copy()
                links[0] = [sum(i) for i in zip(links[0], direction_vector)]
                print("Moved", links[0])

                for idx in range(1, len(links)):
                    if self._is_snap_rope_required(links[idx - 1], links[idx]):
                        prev_location = links[idx].copy()
                        links[idx] = parent_link_prev
                        parent_link_prev = prev_location.copy()
                        print(f"Update: {idx}", links)

                print("Step finished")
                all_pos_t.add(",".join([str(x) for x in links[-1]]))
            print("Instruction finished")

        return len(all_pos_t)


def solve_day(day: int, use_sample: bool):
    solver = Day9(day, use_sample)
    solver.solve()
