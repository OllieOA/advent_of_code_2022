from copy import deepcopy
import math
from typing import List

import numpy as np

from solver import Solver


class Day22(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

        self.INTMAPPING = {
            ".": 0,
            "#": 1,
            " ": 2,
            "o": 3,
            "x": 4,
        }

        self.STRMAPPING = {
            0: ".",
            1: "#",
            2: " ",
            3: "o",
            4: "x",
        }

    def _get_heading(self, angle: int, turn: str) -> int:
        if turn == "L":
            angle = (angle - 90) % 360
        elif turn == "R":
            angle = (angle + 90) % 360
        return angle

    def _visualise_step(self, grid: np.array, curr_pos: List) -> None:
        grid_snapshot = deepcopy(grid)
        grid_snapshot[curr_pos[0], curr_pos[1]] = 4

        grid_map = ""
        for row in grid_snapshot:
            for element in row:
                grid_map += self.STRMAPPING[element]
            grid_map += "\n"

        print(grid_map)

    def part1(self, data: List) -> None:
        max_line_len = max([len(line) for line in data])

        grid_spec = []
        for line in data[:-2]:
            row = [self.INTMAPPING[x] for x in line]
            while len(row) < max_line_len:
                row.append(2)  # Buffer the output
            grid_spec.append(row)

        grid = np.array(grid_spec)
        grid = np.pad(grid, 1, constant_values=2)
        path_spec: List[str] = [x for x in data[-1]]

        curr_angle = 90  # degrees
        top_row = np.where(grid[1, :] == 0)
        curr_pos = [1, top_row[0][0]]

        while len(path_spec) > 0:
            instruction = ""
            if path_spec[0].isalpha():
                instruction = path_spec.pop(0)
                curr_angle = self._get_heading(curr_angle, instruction)
            else:
                while path_spec[0].isnumeric():
                    instruction += path_spec.pop(0)
                    if len(path_spec) == 0:
                        break
                paces = int(instruction)
                heading = [
                    -int(math.cos(math.radians(curr_angle))),
                    int(math.sin(math.radians(curr_angle))),
                ]

                for _ in range(paces):
                    next_pos = [x + y for x, y in zip(curr_pos, heading)]
                    if grid[next_pos[0], next_pos[1]] == 1:  # Run into wall
                        break
                    elif grid[next_pos[0], next_pos[1]] == 2:  # Need to wrap
                        flyover_position = deepcopy(curr_pos)
                        while grid[flyover_position[0], flyover_position[1]] != 2:
                            # Go the opposite of heading
                            flyover_position = [x - y for x, y in zip(flyover_position, heading)]
                            if (
                                flyover_position[0] >= grid.shape[0]
                                or flyover_position[1] >= grid.shape[1]
                            ):
                                break

                        flyover_position = [x + y for x, y in zip(flyover_position, heading)]

                        if grid[flyover_position[0], flyover_position[1]] == 1:
                            break
                        else:
                            curr_pos = deepcopy(flyover_position)

                    else:
                        curr_pos = deepcopy(next_pos)

        angle_score = (curr_angle - 90) // 90

        return 1000 * curr_pos[0] + 4 * curr_pos[1] + angle_score

    def part2(self, data: List) -> None:
        pass


def solve_day(day: int, use_sample: bool):
    solver = Day22(day, use_sample)
    solver.solve()
