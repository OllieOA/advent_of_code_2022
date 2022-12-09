from typing import List

from solver import Solver

class Day2(Solver):
    def __init__(self, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__

        self.SHAPE_SCORES = {
            "rock": 1,
            "paper": 2,
            "scissors": 3,
        }

        self.LOOKUP = {
            "A": "rock",
            "B": "paper",
            "C": "scissors",
            "X": "rock",
            "Y": "paper",
            "Z": "scissors",
        }

        self.BEATS = {
            "rock": "scissors",
            "scissors": "paper",
            "paper": "rock"
        }

        self.LOSES_TO = {
            "rock": "paper",
            "scissors": "rock",
            "paper": "scissors",
        }

        self.RESULT_SCORES = {
            "loss": 0,
            "draw": 3,
            "win": 6,
        }

        self.LOOKUP_UPDATE = {
            "A": "rock",
            "B": "paper",
            "C": "scissors",
            "X": "loss",
            "Y": "draw",
            "Z": "win",
        }

    def _part1(self, data: List) -> int:
        match_results = []
        for match in data:
            match_score = 0

            throws = match.split(" ")
            their_throw = self.LOOKUP[throws[0]]
            my_throw = self.LOOKUP[throws[1]]

            if my_throw == their_throw:
                result_class = "draw"
            elif self.BEATS[my_throw] == their_throw:
                result_class = "win"
            else:
                result_class = "loss"

            match_score += self.SHAPE_SCORES[my_throw]
            match_score += self.RESULT_SCORES[result_class]

            match_results.append(match_score)

        return sum(match_results)

    def _part2(self, data: List) -> int:
        match_results = []
        for match in data:
            match_score = 0

            throws = match.split(" ")
            their_throw = self.LOOKUP_UPDATE[throws[0]]
            my_result = self.LOOKUP_UPDATE[throws[1]]

            if my_result == "draw":
                my_throw = their_throw
            elif my_result == "win":
                my_throw = self.LOSES_TO[their_throw]
            else:
                my_throw = self.BEATS[their_throw]

            match_score += self.SHAPE_SCORES[my_throw]
            match_score += self.RESULT_SCORES[my_result]
            match_results.append(match_score)

        return sum(match_results)


def solve_day(use_sample: bool):
    solver = Day2(use_sample)
    solver.solve_day()