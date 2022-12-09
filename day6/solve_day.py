from typing import List

from solver import Solver

class Day6(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day
    
    def _get_start_of_packet(self, message: str) -> int:
        for idx in range(len(message)):
            window = message[idx:idx+4]
            if len(set(window)) == len(window):
                return idx + 4

    def _get_start_of_message(self, message: str, packet_start: int) -> int:
        for idx in range(packet_start, len(message)):
            window = message[idx:idx+14]
            if len(set(window)) == len(window):
                return idx + 14

    def part1(self, data: List) -> int:
        message = data[0]
        return self._get_start_of_packet(message)
        

    def part2(self, data: List) -> None:
        message = data[0]
        packet_start = self._get_start_of_packet(message)

        return self._get_start_of_message(message, packet_start)



def solve_day(day: int, use_sample: bool):
    solver = Day6(day, use_sample)
    solver.solve_day()