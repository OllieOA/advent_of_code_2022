from typing import List

import numpy as np
import sys

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
            "": [0, 0],
        }

    def _move_link_direction(self, parent_link: List, child_link: List) -> List[int]:
        horiz_delta = parent_link[0] - child_link[0]
        vert_delta = parent_link[1] - child_link[1]

        if abs(horiz_delta) <= 1 and abs(vert_delta) <= 1:
            return
        else:
            horiz_move = 0 if horiz_delta == 0 else int(horiz_delta / abs(horiz_delta))
            vert_move = 0 if vert_delta == 0 else int(vert_delta / abs(vert_delta))
            return [horiz_move, vert_move]

    def _visualise(self, links: List, grid_size: int) -> None:
        np.set_printoptions(threshold=sys.maxsize, linewidth=10 * grid_size)
        grid = -1 * np.ones((grid_size, grid_size))

        for idx, link in enumerate(links):
            grid[link[0] + grid_size // 2, link[1] + grid_size // 2] = idx

        print(np.array_str(np.rot90(grid)).replace("-1", ".."))

    def part1(self, data: List) -> None:
        pos_h = [0, 0]
        pos_t = [0, 0]

        all_pos_t = {",".join([str(x) for x in pos_t])}

        for instruction in data:
            direction = instruction.split(" ")[0]
            num = int(instruction.split(" ")[1])

            direction_vector = self.DIRECTIONS[direction]

            for _ in range(num):
                pos_h = [sum(i) for i in zip(pos_h, direction_vector)]
                new_t_dir = self._move_link_direction(pos_h, pos_t)
                if new_t_dir is not None:
                    pos_t = [sum(i) for i in zip(pos_t, new_t_dir)]
                    all_pos_t.add(",".join([str(x) for x in pos_t]))

        return len(all_pos_t)

    def part2(self, data: List) -> None:
        ROPE_LENGTH = 10
        GRID_SIZE = 32
        links = [[0, 0]] * ROPE_LENGTH

        all_pos_t = {",".join([str(x) for x in [0, 0]])}
        all_pos_order = []
        for instruction in data:
            direction = instruction.split(" ")[0]
            num = int(instruction.split(" ")[1])

            direction_vector = self.DIRECTIONS[direction]

            for _ in range(num):
                links[0] = [sum(i) for i in zip(links[0], direction_vector)]

                for idx in range(1, len(links)):
                    link_change_required = self._move_link_direction(links[idx - 1], links[idx])
                    if link_change_required is not None:
                        links[idx] = [sum(i) for i in zip(links[idx], link_change_required)]
                all_pos_t.add(",".join([str(x) for x in links[-1]]))
                all_pos_order.append(links[-1])

        return len(all_pos_t)


def solve_day(day: int, use_sample: bool):
    solver = Day9(day, use_sample)
    solver.solve()
