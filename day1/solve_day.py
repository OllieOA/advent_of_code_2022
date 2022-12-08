# DAY 1

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


def _part1(data: List) -> Tuple[List, int]:
    elves = []
    curr_total_callories = 0
    for calorie in data:
        if calorie == "":
            elves.append(curr_total_callories)
            curr_total_callories = 0
            continue
        
        curr_total_callories += int(calorie)
    elves.append(curr_total_callories)  # Get the last one

    return max(elves), elves


def _part2(data: List) -> None:
    _, elves = _part1(data)
    return sum(sorted(elves, reverse=True)[:3]), []


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
    _LOG.info(f"| Solved! Answer: {result[0]} in {(end_time-start_time) * 1000} milliseconds!")


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("-s", action="store_true", help="Run sample")

    opts = args.parse_args()
    
    _solve(_part1, 1, opts.s)
    _solve(_part2, 2, opts.s)