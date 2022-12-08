# DAY 2

import argparse
import logging
from pathlib import Path
import time
from typing import List, Callable, Tuple
import sys

_LOG_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_LOG = logging.getLogger(__name__)

_LOG_STREAM_HANDLER = logging.StreamHandler()
_LOG_STREAM_HANDLER.setFormatter(_LOG_FORMATTER)

_LOG_FILE_HANDLER = logging.FileHandler(Path(__file__).parent / "result.log")
_LOG_FILE_HANDLER.setFormatter(_LOG_FORMATTER)

_LOG.addHandler(_LOG_FILE_HANDLER)
_LOG.addHandler(_LOG_STREAM_HANDLER)

_LOG.setLevel(logging.DEBUG)

SHAPE_SCORES = {
    "rock": 1,
    "paper": 2,
    "scissors": 3,
}

LOOKUP = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}

BEATS = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock"
}

LOSES_TO = {
    "rock": "paper",
    "scissors": "rock",
    "paper": "scissors",
}

RESULT_SCORES = {
    "loss": 0,
    "draw": 3,
    "win": 6,
}

LOOKUP_UPDATE = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
    "X": "loss",
    "Y": "draw",
    "Z": "win",
}

def _part1(data: List) -> int:
    match_results = []
    for match in data:
        match_score = 0

        throws = match.split(" ")
        their_throw = LOOKUP[throws[0]]
        my_throw = LOOKUP[throws[1]]

        if my_throw == their_throw:
            result_class = "draw"
        elif BEATS[my_throw] == their_throw:
            result_class = "win"
        else:
            result_class = "loss"

        match_score += SHAPE_SCORES[my_throw]
        match_score += RESULT_SCORES[result_class]

        match_results.append(match_score)

    return sum(match_results)


def _part2(data: List) -> None:
    match_results = []
    for match in data:
        match_score = 0

        throws = match.split(" ")
        their_throw = LOOKUP_UPDATE[throws[0]]
        my_result = LOOKUP_UPDATE[throws[1]]

        if my_result == "draw":
            my_throw = their_throw
        elif my_result == "win":
            my_throw = LOSES_TO[their_throw]
        else:
            my_throw = BEATS[their_throw]

        match_score += SHAPE_SCORES[my_throw]
        match_score += RESULT_SCORES[my_result]
        match_results.append(match_score)

    return sum(match_results)


def _load_data(file_path: Path) -> List:
    with open(file_path, "r") as f:
        lines = [x.strip() for x in f.readlines()]
    return lines


def _solve(solver: Callable, part: int, use_sample: bool) -> None:
    start_time = time.time()
    _LOG.info(f"| Part {part} | File I/O |")
    if use_sample:
        data = _load_data(Path(__file__).parent / f"part{part}_sample.txt")
    else:
        data = _load_data(Path(__file__).parent / f"part{part}_input.txt")

    _LOG.info(f"| Part {part} | Solving |")
    result = solver(data)
    end_time = time.time()
    _LOG.info(f"| Solved! Answer: {result} in {(end_time-start_time) * 1000} milliseconds!")


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("-s", action="store_true", help="Run sample")

    opts = args.parse_args()
    
    _solve(_part1, 1, opts.s)
    _solve(_part2, 2, opts.s)