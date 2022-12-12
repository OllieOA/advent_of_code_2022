from operator import add, sub, mul, floordiv
from typing import List, Dict

from solver import Solver


class Monkey:
    def __init__(
        self,
        monkey_number: int,
        items: List[int],
        operator: str,
        modifier: int,
        divisible_by: int,
        true_target: int,
        false_target: int,
        worries: bool,
    ) -> None:
        self.monkey_number = monkey_number
        self.items = items
        self.operator = operator
        self.modifier = modifier
        self.divisible_by = divisible_by
        self.true_target = true_target
        self.false_target = false_target
        self.worries = worries

        self.OPERATIONS = {"+": add, "-": sub, "*": mul, "/": floordiv}
        self.operation = self.OPERATIONS[self.operator]

        self.inspections = 0

    def __str__(self):
        output_str = f"Monkey {self.monkey_number}: items={self.items}"
        return output_str

    def add_item(self, item: int):
        self.items.append(item)

    def _do_operation(self, input_value: int) -> int:
        modifier = input_value if self.modifier is None else self.modifier
        op_val = self.operation(input_value, modifier)
        if self.worries:
            op_val = op_val // 3
        return op_val

    def _do_test(self, input_value: int) -> bool:
        return self.true_target if input_value % self.divisible_by == 0 else self.false_target

    def inspect_items(self) -> zip:
        inspected_items = [self._do_operation(x) for x in self.items]
        item_target_map = [self._do_test(x) for x in inspected_items]

        self.inspections += len(self.items)
        self.items = []  # All thrown

        return zip(item_target_map, inspected_items)


class Day11(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

        self.OPERATORS = ["-", "+", "*", "/"]

    def _build_monkey_list(self, data: List, worries: bool) -> List[Monkey]:
        monkeys = []
        for idx, instruction in enumerate(data):
            if instruction.startswith("Monkey"):
                items = [int(x) for x in data[idx + 1].split(": ")[1].split(", ")]
                operation_formula = data[idx + 2].split(" = ")[1].split(" ")

                for component in operation_formula[1:]:
                    if component in self.OPERATORS:
                        operator = component
                    else:
                        modifier = None if component == "old" else int(component)

                divisible_by = int(data[idx + 3].split(" ")[-1])
                true_target = int(data[idx + 4].split(" ")[-1])
                false_target = int(data[idx + 5].split(" ")[-1])

                monkeys.append(
                    Monkey(
                        len(monkeys),
                        items,
                        operator,
                        modifier,
                        divisible_by,
                        true_target,
                        false_target,
                        worries,
                    )
                )
        return monkeys

    def _do_monkey_business(self, monkeys: List[Monkey], rounds: int) -> int:
        for _ in range(rounds):
            for monkey in monkeys:
                for target_monkey, item in monkey.inspect_items():
                    monkeys[target_monkey].add_item(item)
        monkey_business = sorted([x.inspections for x in monkeys], reverse=True)

        return monkey_business[0] * monkey_business[1]

    def part1(self, data: List) -> None:
        ROUNDS = 20
        monkeys = self._build_monkey_list(data, worries=True)
        return self._do_monkey_business(monkeys, ROUNDS)

    def part2(self, data: List) -> None:
        ROUNDS = 700
        monkeys = self._build_monkey_list(data, worries=False)
        return self._do_monkey_business(monkeys, ROUNDS)


def solve_day(day: int, use_sample: bool):
    solver = Day11(day, use_sample)
    solver.solve()
