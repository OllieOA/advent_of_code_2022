from collections import deque
from copy import deepcopy
from typing import List


from solver import Solver


class Day20(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _mix_message(self, encrypted_list: deque, times: int) -> int:
        original_list = deepcopy(encrypted_list)
        for _ in range(times):
            for each_object in original_list:
                # Rotate the encrypted list to 0th position
                idx = encrypted_list.index(each_object)
                encrypted_list.rotate(-idx)

                popped_item = encrypted_list.popleft()

                # Find it and rotate it to its requested position
                encrypted_list.rotate(-popped_item[1] % len(encrypted_list))
                encrypted_list.appendleft(popped_item)

            curr_base = encrypted_list[0]

        # Find base element to do the sum from
        while curr_base[1] != 0:
            encrypted_list.rotate(-1)
            curr_base = encrypted_list[0]

        coords = []
        for i in [1000, 2000, 3000]:
            coords.append(encrypted_list[i % len(encrypted_list)][1])

        return sum(coords)

    def part1(self, data: List) -> None:
        encrypted_list = deque((x, int(y)) for x, y in enumerate(data))
        return self._mix_message(encrypted_list, 1)

    def part2(self, data: List) -> None:
        D_KEY = 811589153
        encrypted_list = deque((x, int(y) * D_KEY) for x, y in enumerate(data))
        return self._mix_message(encrypted_list, 10)


def solve_day(day: int, use_sample: bool):
    solver = Day20(day, use_sample)
    solver.solve()
