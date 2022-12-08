import argparse
import logging
from pathlib import Path
import time
from typing import List
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


def _part1(use_sample: bool) -> None:
    pass


def _part2(use_sample: bool) -> None:
    pass


def _load_data(file_path: Path) -> List:
    with open(file_path, "r") as f:
        lines = [x.strip() for x in f.readlines()]
    return lines


def _solve(solver: function, part: int, use_sample: bool) -> None:
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