from operator import add, sub, mul, floordiv, eq
import sympy
from typing import List, Dict

from solver import Solver


class Day21(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

        self.OPERATIONS = {
            "+": add,
            "-": sub,
            "*": mul,
            "/": floordiv,
        }

    def _resolve_monkey(self, monkey: str, monkeys: Dict) -> int:
        if monkeys[monkey]["value"] is not None:
            return monkeys[monkey]["value"]

        # Otherwise we have an operation monkey
        monkeys_for_operation = [
            self._resolve_monkey(x, monkeys) for x in monkeys[monkey]["depends_on"]
        ]
        return monkeys[monkey]["operation"](*monkeys_for_operation)

    def _make_str_equation(self, monkey: str, monkeys: Dict) -> str:
        if monkeys[monkey]["value"] is not None:
            return str(monkeys[monkey]["value"])

        # Otherwise we have an operation monkey
        monkeys_for_operation = [x for x in monkeys[monkey]["depends_on"]]

        operator_str = monkeys[monkey]["operation_str"]

        operation_str = (
            f"({self._make_str_equation(monkeys_for_operation[0], monkeys)}"
            f"{operator_str}"
            f"{self._make_str_equation(monkeys_for_operation[1], monkeys)})"
        )
        return operation_str

    def _solve_equation(self, condition_monkey: str, monkeys: Dict) -> int:
        condition_monkey_depends = monkeys[condition_monkey]["depends_on"]
        lhs_monkey = self._make_str_equation(condition_monkey_depends[0], monkeys)
        rhs_monkey = self._make_str_equation(condition_monkey_depends[1], monkeys)

        lhs_parse = sympy.parsing.sympy_parser.parse_expr(lhs_monkey)
        rhs_parse = sympy.parsing.sympy_parser.parse_expr(rhs_monkey)

        x = sympy.Symbol("x")

        monkey_eq = sympy.Eq(lhs_parse, rhs_parse)
        res = sympy.solvers.solve(monkey_eq, x)

        return res[0]

    def _get_monkeys(self, data: List) -> Dict:
        monkeys = {
            x.split(": ")[0]: {
                "value": None,
                "operation": None,
                "operation_str": "",
                "depends_on": [],
            }
            for x in data
        }
        for monkey_spec in data:
            monkey_name, monkey_data = monkey_spec.split(": ")

            if monkey_data.isnumeric():
                monkeys[monkey_name]["value"] = int(monkey_data)
            else:
                monkey_data_split = monkey_data.split(" ")
                monkeys[monkey_name]["depends_on"].extend(
                    [monkey_data_split[0], monkey_data_split[2]]
                )
                monkeys[monkey_name]["operation"] = self.OPERATIONS[monkey_data_split[1]]
                monkeys[monkey_name]["operation_str"] = monkey_data_split[1]

        return monkeys

    def part1(self, data: List) -> None:
        monkeys = self._get_monkeys(data)
        return self._resolve_monkey("root", monkeys)

    def part2(self, data: List) -> None:
        monkeys = self._get_monkeys(data)
        # Update monkeys
        monkeys["root"]["operation"] = eq
        monkeys["humn"]["value"] = "x"

        return self._solve_equation("root", monkeys)


def solve_day(day: int, use_sample: bool):
    solver = Day21(day, use_sample)
    solver.solve()
