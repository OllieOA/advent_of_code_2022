# DAY 0

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

_LOG_FILE_HANDLER = logging.FileHandler(Path(__file__).parent / "result.log", "w")
_LOG_FILE_HANDLER.setFormatter(_LOG_FORMATTER)

_LOG.addHandler(_LOG_FILE_HANDLER)
_LOG.addHandler(_LOG_STREAM_HANDLER)

_LOG.setLevel(logging.DEBUG)


def _part1(data: List) -> None:
    total_sum = 0
    for pack in data:
        compartment_1 = set([*pack[:len(pack)//2]])
        compartment_2 = set([*pack[len(pack)//2:]])

        repeated_element = compartment_1.intersection(compartment_2).pop()

        if repeated_element.isupper():
            total_sum += ord(repeated_element) - 38
        else:
            total_sum += ord(repeated_element) - 96

    return total_sum


def _part2(data: List) -> None:
    total_sum = 0
    elf_groups = [data[x:x+3] for x in range(0, len(data), 3)]

    for elf_group in elf_groups:
        common_items = set()
        for rucksack in elf_group:
            if not common_items:
                common_items = set([*rucksack])
            else:
                common_items = common_items.intersection(set([*rucksack]))

        common_item = common_items.pop()
        
        if common_item.isupper():
            total_sum += ord(common_item) - 38
        else:
            total_sum += ord(common_item) - 96

    return total_sum


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