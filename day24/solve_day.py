from copy import deepcopy
from typing import List, Tuple

import numpy as np

from solver import Solver


class Day24(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

        self.DIR_MAPPING = {
            ">": (0, 1),
            "<": (0, -1),
            "^": (-1, 0),
            "v": (1, 0),
        }

        self.GRID_MAPPING = {
            "#": 1,
            ".": 0,
            ">": 0,
            "<": 0,
            "^": 0,
            "v": 0,
        }

        self.STR_MAPPING = {0: ".", 1: "#", 2: "x", 3: "E"}

    def _vizualise(self, grid: np.array, curr_pos=(0, 1)) -> None:
        print("----")
        grid_snapshot = deepcopy(grid)

        grid_snapshot[curr_pos[0], curr_pos[1]] = 3
        grid_map = ""
        for row in grid_snapshot:
            for element in row:
                grid_map += self.STR_MAPPING[element]
            grid_map += "\n"

        print(grid_map)

    def _move_blizzard(self, grid: np.array, blizzard: List) -> List[List]:
        next_blizzard_pos = [x + y for x, y in zip(blizzard[0], blizzard[1])]

        if grid[next_blizzard_pos[0], next_blizzard_pos[1]] == 1:  # Wall
            flyover_pos = deepcopy(blizzard[0])

            while grid[flyover_pos[0], flyover_pos[1]] != 1:
                flyover_pos = [x - y for x, y in zip(flyover_pos, blizzard[1])]

            # Arrived at the other side of the map, move fwd 1 step
            flyover_pos = [x + y for x, y in zip(flyover_pos, blizzard[1])]
            next_blizzard_pos = deepcopy(flyover_pos)

        return [next_blizzard_pos, blizzard[1]]

    def _build_blizzard_lookup(self, initial_blizzards: List, lines: List) -> None:
        # Generate the blizzard for all timestamps
        blizzard_lookup = []
        initial_blizzard_map = deepcopy(initial_blizzards)
        curr_blizzard_map = deepcopy(initial_blizzards)

        while curr_blizzard_map != initial_blizzard_map or len(blizzard_lookup) < 1:
            grid_at_step = np.array(lines)

            for blizzard in curr_blizzard_map:
                blizzard_coord = blizzard[0]
                grid_at_step[blizzard_coord[0], blizzard_coord[1]] = 2
            blizzard_lookup.append(grid_at_step)
            curr_blizzard_map = [self._move_blizzard(grid_at_step, x) for x in curr_blizzard_map]

        self.logger.info(f"Blizzard permutations is {len(blizzard_lookup)} long")
        self.blizzard_lookup = blizzard_lookup

    def _run_search(self, start_node: Tuple[List, int, List], goal_node: Tuple[int]) -> Tuple[List]:
        queue = []  # Time 0
        queue.append(start_node)
        explored = set([])

        loops = 0

        while len(queue) > 0:
            loops += 1
            node = queue.pop(0)

            # if loops % 5000 == 0:
            #     self.logger.info(
            #         f"Queue is {len(queue)} long. Checking timestep {node[1]}. Goal node is {goal_node} and I am at {node[0]}"
            #     )

            if all([x == y for x, y in zip(node[0], goal_node)]):
                return node

            explored.add(node[:-1])

            # Select the correct map at timestamp
            grid = deepcopy(self.blizzard_lookup[(node[1] + 1) % len(self.blizzard_lookup)])

            # Populate the queue
            adjacent_nodes = [(node[0][0], node[0][1])]  # Waiting is possible
            for i in [-1, 1]:
                adjacent_nodes.append((node[0][0] + i, node[0][1]))
                adjacent_nodes.append((node[0][0], node[0][1] + i))

            for adjacent_node in adjacent_nodes:
                appending_node = (adjacent_node, node[1] + 1, node[0])
                if appending_node[:-1] in explored:
                    continue
                if appending_node in queue:
                    continue
                if adjacent_node[0] >= grid.shape[0] or adjacent_node[1] >= grid.shape[1]:
                    continue
                elif adjacent_node[0] < 0 or adjacent_node[1] < 0:
                    continue
                elif grid[adjacent_node[0], adjacent_node[1]] in [1, 2]:
                    continue
                else:
                    queue.append(appending_node)

        return -1

    def part1(self, data: List) -> None:
        lines = []
        blizzards = []
        for l_idx, line in enumerate(data):
            temp_line = []
            for e_idx, element in enumerate(line):
                temp_line.append(self.GRID_MAPPING[element])
                if element in self.DIR_MAPPING:
                    blizzards.append([[l_idx, e_idx], self.DIR_MAPPING[element]])
            lines.append(temp_line)

        self.grid = np.array(lines)

        self._build_blizzard_lookup(blizzards, lines)

        start_node_spec = np.where(self.grid[0, :] == 0)
        goal_node_spec = np.where(self.grid[-1, :] == 0)
        start_node = (0, start_node_spec[0][0])
        goal_node = (self.grid.shape[0] - 1, goal_node_spec[0][0])

        self.part1_node = self._run_search((start_node, 0, None), goal_node)
        return self.part1_node[1]

    def part2(self, data: List) -> None:
        # Return to start
        self.logger.info("Returning back to start")
        start_node = self.part1_node
        goal_node_spec = np.where(self.grid[0, :] == 0)
        goal_node = (0, goal_node_spec[0][0])
        returned_node = self._run_search(start_node, goal_node)

        # Return to end again
        self.logger.info("Heading to finish again")
        goal_node_spec = np.where(self.grid[-1, :] == 0)
        goal_node = (self.grid.shape[0] - 1, goal_node_spec[0][0])
        final_node = self._run_search(returned_node, goal_node)

        return final_node[1]


def solve_day(day: int, use_sample: bool):
    solver = Day24(day, use_sample)
    solver.solve()
