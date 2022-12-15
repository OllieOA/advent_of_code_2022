import re
from typing import List, Tuple

import numpy as np

from solver import Solver


class Day12(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _visualise(self, grid: np.array) -> None:
        LOOKUP = {0: ".", 1: "S", 2: "B", 9: "#"}

        for row in grid.T:
            row_str = ""
            for element in row:
                row_str += LOOKUP[element]
            print(row_str)

    def _get_man_dist(self, point1: Tuple, point2: Tuple) -> int:
        return sum(abs(a - b) for a, b in zip(point1, point2))

    def part1(self, data: List[str]) -> None:
        sensors_to_beacons = {}
        min_x = 10e2
        min_y = 10e2
        max_x = 0
        max_y = 0
        for line in data:
            split_line = line.split(":")
            sensor = tuple([int(x) for x in re.findall(r"=(-?\d*)", split_line[0])])
            beacon = tuple([int(x) for x in re.findall(r"=(-?\d*)", split_line[1])])

            max_x_coord = max(sensor[0], beacon[0])
            max_x = max(max_x, max_x_coord)
            max_y_coord = max(sensor[1], beacon[1])
            max_y = max(max_y, max_y_coord)

            min_x_coord = min(sensor[0], beacon[0])
            min_x = min(min_x, min_x_coord)
            min_y_coord = min(sensor[1], beacon[1])
            min_y = min(min_y, min_y_coord)

            sensors_to_beacons.update({sensor: beacon})

        grid = np.zeros((abs(min_x) + max_x + 1, abs(min_y) + max_y + 1))

        # Sensor is 1, Beacon is 2
        sensor_radii = {}
        for sensor, beacon in sensors_to_beacons.items():
            grid[sensor[0] + abs(min_x), sensor[1] + abs(min_y)] = 1
            grid[beacon[0] + abs(min_x), beacon[1] + abs(min_y)] = 2

            man_dist = self._get_man_dist(sensor, beacon)
            sensor_radii[sensor] = man_dist

        self._visualise(grid)

    def part2(self, data: List) -> None:
        pass


def solve_day(day: int, use_sample: bool):
    solver = Day12(day, use_sample)
    solver.solve()
