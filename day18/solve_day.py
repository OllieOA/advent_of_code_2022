from copy import deepcopy
from typing import List, Tuple

import numpy as np

from solver import Solver


class Day18(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _build_sphere(self, data: List) -> Tuple[np.array, List[List]]:
        coord_list = []
        min_x = 1e2
        min_y = 1e2
        min_z = 1e2

        max_x = 0
        max_y = 0
        max_z = 0
        for line in data:

            new_coord = [int(i) for i in line.split(",")]
            coord_list.append(new_coord)

            max_x = max(max_x, new_coord[0])
            max_y = max(max_y, new_coord[1])
            max_z = max(max_z, new_coord[2])

            min_x = min(min_x, new_coord[0])
            min_y = min(min_y, new_coord[1])
            min_z = min(min_z, new_coord[2])

        grid = np.ones((max_x + 3, max_y + 3, max_z + 3))
        # + 2 for pad around the outside + 1 for offset of input

        for coord in coord_list:
            grid[coord[0] + 1, coord[1] + 1, coord[2] + 1] = 0

        return grid, coord_list

    def _in_bound(self, grid: np.array, node: List) -> bool:
        for idx, coord in enumerate(node):
            if coord < 0:
                return False
            if coord >= grid.shape[idx]:
                return False

        return True

    def _flood_find(self, grid: np.array, starting_point: Tuple) -> int:
        exposed_faces = 0
        explored = set([])
        queue = [starting_point]

        while len(queue) > 0:
            curr_node = queue.pop(0)
            explored.add(curr_node)

            adjacent_nodes = []
            for i in [-1, 1]:
                adjacent_nodes.append((curr_node[0] + i, curr_node[1], curr_node[2]))
                adjacent_nodes.append((curr_node[0], curr_node[1] + i, curr_node[2]))
                adjacent_nodes.append((curr_node[0], curr_node[1], curr_node[2] + i))

            for adjacent_node in adjacent_nodes:
                if not self._in_bound(grid, adjacent_node):
                    continue

                # Check if adjacent_node is a 0. Do not add it if it is
                if grid[adjacent_node[0], adjacent_node[1], adjacent_node[2]] == 0:
                    # print("EXPOSED FACE AT ", adjacent_node)
                    exposed_faces += 1
                    continue

                if not adjacent_node in explored:
                    if not adjacent_node in queue:
                        queue.append(adjacent_node)

        return exposed_faces

    def part1(self, data: List) -> None:
        grid, coord_list = self._build_sphere(data)

        exposed_faces = 0
        for coord in coord_list:
            for i in [-1, 1]:
                exposed_faces += grid[coord[0] + 1 + i, coord[1] + 1, coord[2] + 1]
                exposed_faces += grid[coord[0] + 1, coord[1] + 1 + i, coord[2] + 1]
                exposed_faces += grid[coord[0] + 1, coord[1] + 1, coord[2] + 1 + i]

        return int(exposed_faces)

    def part2(self, data: List) -> None:
        grid, _ = self._build_sphere(data)

        # Flood fill
        start_node = (0, 0, 0)

        return self._flood_find(grid, start_node)


def solve_day(day: int, use_sample: bool):
    solver = Day18(day, use_sample)
    solver.solve()
