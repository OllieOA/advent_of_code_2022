from copy import deepcopy
from enum import Enum
from itertools import combinations_with_replacement
import re
from typing import List, Dict

from solver import Solver


class Resources(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


class Blueprint:
    def __init__(self, blueprint: str) -> None:
        blueprint_split = blueprint.split(":")
        self.id = int(blueprint_split[0].split(" ")[-1])

        self.initial_resources = {
            Resources.ORE.value: 0,
            Resources.CLAY.value: 0,
            Resources.OBSIDIAN.value: 0,
            Resources.GEODE.value: 0,
        }

        self.initial_robots = {
            Resources.ORE.value: 1,
            Resources.CLAY.value: 0,
            Resources.OBSIDIAN.value: 0,
            Resources.GEODE.value: 0,
        }

        self.robot_cost = {
            Resources.ORE.value: {},
            Resources.CLAY.value: {},
            Resources.OBSIDIAN.value: {},
            Resources.GEODE.value: {},
        }

        for idx, robot_spec in enumerate(blueprint_split[1].split(".")):
            costs = re.findall(r"(\d+\s[a-z]*)", robot_spec)

            for cost in costs:
                qty, resource_type = cost.split(" ")
                qty = int(qty)

                self.robot_cost[Resources(idx).value][Resources[resource_type.upper()].value] = qty

        robot_list = [robot.value for robot in Resources]
        self.paths = list(combinations_with_replacement(robot_list, 24))

        self.simulation_results = []

    def __str__(self) -> str:
        return f"Blueprint {self.id}: {self.robot_cost}"

    def run_simulation(self) -> None:
        run_resources = deepcopy(self.initial_resources)
        run_robots = deepcopy(self.initial_robots)
        for path in self.paths:
            for p_idx in range(24):
                # Generate resources
                for robot_type, robot_qty in run_robots.items():
                    run_resources[robot_type] += robot_qty

                # Attempt to spend resources
                desired_robot  ## TODO


class Day19(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List) -> None:
        for blueprint_spec in data:
            blueprint = Blueprint(blueprint_spec)

    def part2(self, data: List) -> None:
        pass


def solve_day(day: int, use_sample: bool):
    solver = Day19(day, use_sample)
    solver.solve()
