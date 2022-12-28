from copy import deepcopy
import re
from tqdm import tqdm
from typing import List, Tuple, Dict

import numpy as np

from solver import Solver


class Day15(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _visualise(self, grid: np.array) -> None:
        LOOKUP = {
            0: ".",
            1: "S",
            2: "B",
            9: "#",  # Blocked out
        }

        for row in grid.T:
            row_str = ""
            for element in row:
                row_str += LOOKUP[element]
            print(row_str)

    def _get_man_dist(self, point1: Tuple, point2: Tuple) -> int:
        return sum(abs(a - b) for a, b in zip(point1, point2))

    def _build_area(
        self, intervals: Dict[int, List], starting_coords: List, index: int, direction: int
    ) -> None:
        if index not in intervals:
            intervals[index] = []

        converged = False
        curr_min = starting_coords[0]
        curr_max = starting_coords[1]
        while not converged:
            curr_min += 1
            curr_max -= 1

            converged = abs(curr_max - curr_min) == 0
            index += direction
            if index not in intervals:
                intervals[index] = []
            intervals[index].append([curr_min, curr_max])

    def _consolidate_ranges(self, intervals: Dict[int, List]) -> None:
        for row, ranges in tqdm(intervals.items()):
            consolidated_ranges = sorted([tuple(x) for x in ranges])
            all_consolidated = False

            loops = 0
            while not all_consolidated:
                loops += 1
                all_consolidated = True
                if len(consolidated_ranges) == 1:
                    break

                new_ranges = set([])
                for idx in range(len(consolidated_ranges) - 1):
                    combo = (consolidated_ranges[idx], consolidated_ranges[idx + 1])
                    all_nums = [combo[0][0], combo[0][1], combo[1][0], combo[1][1]]

                    first_range = set(range(combo[0][0], combo[0][1] + 1))
                    second_range = set(range(combo[1][0], combo[1][1] + 1))

                    if len(first_range.intersection(second_range)) > 0:
                        all_consolidated = False
                        # Intersection
                        new_ranges.add((min(all_nums), max(all_nums)))
                        break
                    elif abs(combo[0][1] - combo[1][0]) == 1:  # 1 away
                        all_consolidated = False
                        new_ranges.add((min(all_nums), max(all_nums)))
                        break
                    else:
                        new_ranges.add(combo[0])
                        if idx == len(consolidated_ranges) - 1:
                            new_ranges.add(combo[1])

                if (idx + 2) < len(consolidated_ranges):  # Early exit
                    new_ranges = new_ranges.union(set(consolidated_ranges[idx + 2 :]))
                consolidated_ranges = sorted(list(new_ranges))

            intervals[row] = consolidated_ranges

    def part1(self, data: List[str]) -> None:
        print("Building object for processing...")
        sensors_to_beacons = {}
        min_x = 10e10
        min_y = 10e10
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

        # Sensor is 1, Beacon is 2
        sensor_radii = {}
        for sensor, beacon in sensors_to_beacons.items():
            man_dist = self._get_man_dist(sensor, beacon)
            sensor_radii[sensor] = man_dist

        # Go over each of the radii and build an interval for each row, then
        # consolidate. Form is {row: [(col1, col2),  (col3, col4) ...]}
        blocked_intervals = {}  # Only build this on the x axis
        for sensor_coord, sensor_radius in tqdm(sensor_radii.items()):
            base_col_idx, base_row_idx = sensor_coord
            if base_row_idx not in blocked_intervals:
                blocked_intervals[base_row_idx] = []

            base_row = [base_col_idx - sensor_radius, base_col_idx + sensor_radius]
            self._build_area(blocked_intervals, base_row, base_row_idx, 1)
            self._build_area(blocked_intervals, base_row, base_row_idx, -1)

        print("Consolidating...")
        self._consolidate_ranges(blocked_intervals)
        print("Consolidated!")

        # Extract the number of populated elements in row
        if self.use_sample:
            target_row = 10
        else:
            target_row = 2000000

        total_num = 0

        for sub_range in blocked_intervals[target_row]:
            total_num = sub_range[1] - sub_range[0]

        return total_num

    def part2(self, data: List) -> None:
        pass


def solve_day(day: int, use_sample: bool):
    solver = Day15(day, use_sample)
    solver.solve()
