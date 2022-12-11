from typing import List

import numpy as np

from solver import Solver


class Day8(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

    def _get_tree_array(self, data: List) -> np.array:
        treelines = []
        for treeline in data:
            single_treeline = [int(x) for x in treeline]
            treelines.append(single_treeline)

        return np.array(treelines)

    def part1(self, data: List) -> int:
        tree_array = self._get_tree_array(data)
        visible_trees = 0

        for (idx, idy), val in np.ndenumerate(tree_array):

            treeline_1 = tree_array[idx, idy + 1 :]
            treeline_2 = np.flip(tree_array[idx, :idy])
            treeline_3 = tree_array[idx + 1 :, idy]
            treeline_4 = np.flip(tree_array[:idx, idy])

            visible = not (
                any(treeline_1 >= val)
                and any(treeline_2 >= val)
                and any(treeline_3 >= val)
                and any(treeline_4 >= val)
            )

            if visible:
                visible_trees += 1

        return visible_trees

    def part2(self, data: List) -> int:
        tree_array = self._get_tree_array(data)

        scenic_scores = np.zeros(tree_array.shape)

        for (idx, idy), val in np.ndenumerate(tree_array):
            treeline_1 = tree_array[idx, idy + 1 :]
            treeline_2 = np.flip(tree_array[idx, :idy])
            treeline_3 = tree_array[idx + 1 :, idy]
            treeline_4 = np.flip(tree_array[:idx, idy])

            treelines = [treeline_1, treeline_2, treeline_3, treeline_4]

            single_tree_score = 1

            for treeline in treelines:
                single_treeline_score = 0
                for tree in treeline:
                    single_treeline_score += 1
                    if tree >= val:
                        break
                single_tree_score *= single_treeline_score
            scenic_scores[idx, idy] = single_tree_score

        return int(np.max(scenic_scores))


def solve_day(day: int, use_sample: bool):
    solver = Day8(day, use_sample)
    solver.solve()
