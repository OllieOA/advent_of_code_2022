import time
from typing import List
from tqdm import tqdm

import numpy as np

from solver import Solver

SHAPES = [
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 0), (0, 1), (1, 0), (1, 1)),
]

SHAPE_HEIGHTS = [1, 3, 3, 4, 2]


class Day17(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _visualise(self, grid: np.array) -> None:
        LOOKUP = {
            0: ".",
            1: "@",
            2: "#",
        }

        for row in np.flip(grid.T, axis=0):
            row_str = ""
            for element in row:
                row_str += LOOKUP[element]
            print(row_str)

    def part1(self, data: List) -> None:
        instructions = data[0]

        grid = np.ones((7, 1)) * 2

        highest_rock_level = 1
        instruction_count = 0

        rock_rested = True
        for ridx in tqdm(range(2023)):
            # if no rock, spawn rock
            if rock_rested:
                # print("SPAWNING ROCK")
                rock_rested = False
                rock_idx_to_spawn = ridx % 5

                # Pad if needed
                if (grid.shape[1] - highest_rock_level) < SHAPE_HEIGHTS[rock_idx_to_spawn] + 3:
                    new_padding = np.zeros((7, SHAPE_HEIGHTS[rock_idx_to_spawn] + 3))
                    grid = np.concatenate([grid, new_padding], axis=1)
                rock_shape = SHAPES[rock_idx_to_spawn]

                current_rock = (2, highest_rock_level + 3)
                for coord in rock_shape:
                    grid[coord[0] + current_rock[0], coord[1] + current_rock[1]] = 1

            while not rock_rested:
                # self._visualise(grid)
                # Get instruction
                instruction = instructions[instruction_count % len(instructions)]
                instruction_count += 1

                # print("INSTRUCTION TO DO", instruction)

                modifier = 1
                if instruction == "<":
                    modifier = -1

                # Check if all elements can move sideways
                moveable_sideways = []
                for coord in rock_shape:
                    curr_coord = (current_rock[0] + coord[0], current_rock[1] + coord[1])
                    if curr_coord[0] + modifier < 0 or curr_coord[0] + modifier == 7:
                        moveable_sideways.append(False)
                    elif grid[curr_coord[0] + modifier, curr_coord[1]] != 2:
                        moveable_sideways.append(True)
                    else:
                        moveable_sideways.append(False)

                if all(moveable_sideways):
                    new_base_coord = (current_rock[0] + modifier, current_rock[1])
                    for coord in rock_shape:
                        curr_coord = (current_rock[0] + coord[0], current_rock[1] + coord[1])
                        grid[curr_coord[0], curr_coord[1]] = 0

                    current_rock = new_base_coord

                    for coord in rock_shape:
                        curr_coord = (current_rock[0] + coord[0], current_rock[1] + coord[1])
                        grid[curr_coord[0], curr_coord[1]] = 1

                # Check if can move down
                moveable_down = []
                for coord in rock_shape:
                    curr_coord = (current_rock[0] + coord[0], current_rock[1] + coord[1])
                    if grid[curr_coord[0], curr_coord[1] - 1] != 2:
                        moveable_down.append(True)
                    else:
                        moveable_down.append(False)
                        break

                # print("MOVABLE SIDEWAYS?", moveable_sideways)
                # print("MOVABLE DOWN?", moveable_down)

                if all(moveable_down):
                    new_base_coord = (current_rock[0], current_rock[1] - 1)
                    for coord in rock_shape:
                        curr_coord = (current_rock[0] + coord[0], current_rock[1] + coord[1])
                        grid[curr_coord[0], curr_coord[1]] = 0

                    current_rock = new_base_coord

                    for coord in rock_shape:
                        curr_coord = (current_rock[0] + coord[0], current_rock[1] + coord[1])
                        grid[curr_coord[0], curr_coord[1]] = 1

                else:
                    for coord in rock_shape:
                        curr_coord = (current_rock[0] + coord[0], current_rock[1] + coord[1])
                        grid[curr_coord[0], curr_coord[1]] = 2  # Now stationary

                    rock_rested = True
                    # print("ROCK RESTED")

                    heights = []
                    for coord in rock_shape:
                        heights.append(current_rock[1] + coord[1])

                    highest_rock_level = max(heights) + 1
                    # print("SETTING NEW HEIGHT TO", highest_rock_level)

                # time.sleep(0.5)

        return highest_rock_level

    def part2(self, data: List) -> None:
        pass


def solve_day(day: int, use_sample: bool):
    solver = Day17(day, use_sample)
    solver.solve()
