import math
from queue import PriorityQueue
from typing import List, Tuple

import numpy as np

from solver import Solver


class Day12(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _get_pythag_dist(self, point1: Tuple, point2: Tuple) -> int:
        return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** 0.5

    def part1(self, data: List) -> None:
        grid_map_lists = []
        for row in data:
            row_extract = [ord(x) - 96 for x in row]
            grid_map_lists.append(row_extract)

        grid = np.array(grid_map_lists)

        start_node_components = np.where(grid == (ord("S") - 96))
        start_node = (start_node_components[0][0], start_node_components[1][0])

        goal_node_components = np.where(grid == (ord("E") - 96))
        goal_node = (goal_node_components[0][0], goal_node_components[1][0])

        explored = set([])
        queue = PriorityQueue()

        # Node format is (heuristic, (node, successor))
        queue.put(0, (start_node, None))

        # TODO Refactor this into a dictionary for convenient overwriting

        while len(queue) > 0:
            curr_node_packet = queue.get(0)
            curr_node = curr_node_packet[1][0]
            if curr_node == goal_node:
                pass  # TODO: Get back back

            # Else,
            explored.add(curr_node)
            curr_height = grid[curr_node[0], curr_node[1]]

            # Get and test adjacent nodes for suitability
            adjacent_nodes = []
            for i in [-1, 1]:
                adjacent_nodes.append((curr_node[0] + i, curr_node[1]))
                adjacent_nodes.append((curr_node[0], curr_node[1] + i))

            for adjacent_node in adjacent_nodes:
                if adjacent_node in explored:
                    continue
                elif adjacent_node[0] > grid.shape[0] or adjacent_node[1] > grid.shape[1]:
                    continue
                elif adjacent_node[0] < 0 or adjacent_node[1] < 0:
                    continue

                elif abs(curr_height - grid[adjacent_node[0], adjacent_node[1]]) > 1:
                    continue
                else:
                    queue.put(
                        (
                            self._get_pythag_dist(adjacent_node, goal_node),
                            (adjacent_node, curr_node),
                        )
                    )

    def part2(self, data: List) -> None:
        pass


def solve_day(day: int, use_sample: bool):
    solver = Day12(day, use_sample)
    solver.solve()
