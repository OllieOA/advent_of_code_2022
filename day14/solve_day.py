from typing import List, Tuple

import numpy as np

from solver import Solver


class Day14(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _get_line(self, start_coord: List, end_coord: List) -> List[Tuple]:
        horiz_step = 1
        if start_coord[0] > end_coord[0]:
            horiz_step = -1

        vert_step = 1
        if start_coord[1] > end_coord[1]:
            vert_step = -1

        horiz_points = list(range(start_coord[0], end_coord[0] + horiz_step, horiz_step))
        vert_points = list(range(start_coord[1], end_coord[1] + vert_step, vert_step))

        if len(horiz_points) == 1:
            horiz_points = horiz_points * len(vert_points)
        elif len(vert_points) == 1:
            vert_points = vert_points * len(horiz_points)

        line_points = list(zip(horiz_points, vert_points))
        return line_points

    def _get_rock_coords(self, data: List) -> List[Tuple]:
        rock_coords = set([])

        for path in data:
            coord_points = path.split(" -> ")
            for idx, coord_point in enumerate(coord_points[:-1]):
                start_coord = [int(x) for x in coord_point.split(",")]
                end_coord = [int(x) for x in coord_points[idx + 1].split(",")]

                coord_line = set(self._get_line(start_coord, end_coord))
                rock_coords = rock_coords.union(coord_line)

        return rock_coords

    def _get_max_min(self, rock_coords: List[Tuple]) -> None:
        min_x = 500
        max_x = 500
        max_y = 0
        for coord in rock_coords:
            min_x = min(min_x, coord[0])
            max_x = max(max_x, coord[0])
            max_y = max(max_y, coord[1])

        self.ylim = max_y + 1
        self.xmin = min_x
        self.xmax = max_x

    def _move_sand(self, grid: np.array, sand_location: List, voidable=True) -> Tuple[List, bool]:
        if sand_location[0] + 1 == self.ylim and voidable:  # Into the void
            return [sand_location[0] + 1, sand_location[1]], False

        if grid[sand_location[0] + 1, sand_location[1]] == 0:
            return [sand_location[0] + 1, sand_location[1]], False

        # Either rested sand or rock
        if grid[sand_location[0] + 1, sand_location[1] - 1] == 0:
            return [sand_location[0] + 1, sand_location[1] - 1], False
        if grid[sand_location[0] + 1, sand_location[1] + 1] == 0:
            return [sand_location[0] + 1, sand_location[1] + 1], False

        return sand_location, True

    def _visualise(self, grid: np.array, spawn_location=[0, 0]) -> None:
        for idx, row in enumerate(grid):
            row_print = ""
            if idx == 0:
                row[spawn_location[1]] = -1
            for element in row:
                if element == 0:
                    row_print += "."
                elif element == 1:
                    row_print += "#"
                elif element == 2:
                    row_print += "o"
                elif element == -1:
                    row_print += "+"
            print(row_print)
        print("====")

    def part1(self, data: List) -> None:
        # Build rock coordinates
        rock_coords = self._get_rock_coords(data)
        self._get_max_min(rock_coords)

        grid = np.zeros((self.ylim, self.xmax - self.xmin + 3))  # + 3 for padding

        for coord in rock_coords:
            grid[coord[1], coord[0] - self.xmax - 2] = 1

        sand_spawn_location = [0, 500 - self.xmax - 2]
        sand_location = sand_spawn_location.copy()

        rested_sand = []
        # Air is 0, Rock is 1, Resting sand is a 2
        while sand_location[0] < self.ylim:
            sand_location, rested = self._move_sand(grid, sand_location)
            if rested:
                grid[sand_location[0], sand_location[1]] = 2
                rested_sand.append(tuple(sand_location))
                sand_location = sand_spawn_location.copy()
                # self._visualise(grid)

        return len(rested_sand)

    def part2(self, data: List) -> None:
        rock_coords = self._get_rock_coords(data)
        self._get_max_min(rock_coords)

        y_span_size = 3 * self.ylim

        grid = np.zeros((self.ylim + 2, y_span_size))
        grid[-1, :] = 1

        for coord in rock_coords:
            grid[coord[1], coord[0] - 500 + y_span_size // 2] = 1

        sand_spawn_location = [0, y_span_size // 2]
        sand_location = sand_spawn_location.copy()

        rested_sand = []
        while grid[sand_spawn_location[0], sand_spawn_location[1]] != 2:
            sand_location, rested = self._move_sand(grid, sand_location, voidable=False)
            if rested:
                grid[sand_location[0], sand_location[1]] = 2
                rested_sand.append(tuple(sand_location))
                sand_location = sand_spawn_location.copy()
                # self._visualise(grid)

        return len(rested_sand)


def solve_day(day: int, use_sample: bool):
    solver = Day14(day, use_sample)
    solver.solve()
