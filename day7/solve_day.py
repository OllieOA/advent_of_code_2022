import json
from typing import List, Dict

from solver import Solver


class Day7(Solver):
    def __init__(self, day: int, use_sample: bool) -> None:
        super().__init__(use_sample)
        self.my_base_path = __file__
        self.day = day

        self.META_KEYS = ["files", "size"]

    def _recursive_get(self, directory: Dict, depth: List) -> str:
        curr_object = directory[depth[0]]
        for key in depth[1:]:
            curr_object = curr_object.get(key, None)
            if not curr_object:
                return None

        return curr_object

    def _recursive_set(self, directory: Dict, depth: List, target_object: Dict) -> None:
        curr_object = directory[depth[0]]
        for key in depth[1:-1]:
            curr_object = curr_object.get(key, None)
            if not curr_object:
                raise ValueError(f"Could not find {key} in {curr_object}")

        curr_object[depth[-1]] = target_object

    def _recursive_update_file(self, directory: Dict, depth: List, object_to_append: Dict) -> None:
        curr_object = directory[depth[0]]
        for key in depth[1:]:
            curr_object = curr_object.get(key, None)
            if not curr_object:
                raise ValueError(f"Could not find {key} in {curr_object}")

        curr_object["files"].update(object_to_append)

    def _set_size(self, subdirectory: Dict):  # TODO: CHECK THIS PROPAGATION
        subdirectory["size"] += sum(subdirectory["files"].values())
        for key, subdir in subdirectory.items():
            if key not in self.META_KEYS:
                subdir_size = self._set_size(subdir)
                subdirectory["size"] += subdir_size

        return int(subdirectory["size"])

    def _get_size(self, directory: Dict, all_dirs: Dict) -> Dict:
        for key, subdir in directory.items():
            if isinstance(subdir, Dict):
                self._get_size(subdir, all_dirs)
                if "size" in subdir.keys():
                    all_dirs[key] = subdir["size"]

        return all_dirs

    def part1(self, data: List) -> int:
        directory = {"/": {"files": {}, "size": 0}}
        curr_depth = []

        for cmd_line in data:
            if cmd_line.startswith("$ cd /"):
                curr_depth = ["/"]
            elif cmd_line.startswith("$ cd"):
                target_dir = cmd_line.split(" ")[2]
                if target_dir == "..":  # Special case
                    curr_depth.pop()
                else:
                    curr_depth.append(target_dir)

                    # if not self._recursive_get(directory, curr_depth):
                    #     self._recursive_set(directory, curr_depth, {"files": {}, "size": 0})
            elif cmd_line.startswith("dir "):
                curr_depth.append(cmd_line.split(" ")[1])
                self._recursive_set(directory, curr_depth, {"files": {}, "size": 0})
                curr_depth.pop()

            elif cmd_line[0].isnumeric():
                file_read = {cmd_line.split(" ")[1]: int(cmd_line.split(" ")[0])}
                self._recursive_update_file(directory, curr_depth, file_read)

        # Then populate size values
        _ = self._set_size(directory["/"])

        all_dirs = self._get_size(directory, {})
        # self.logger.debug(json.dumps(directory, indent=4))
        # self.logger.debug(json.dumps(all_dirs, indent=4))

        total_cleared_size = 0
        dirs = []
        for dir, size in all_dirs.items():
            if size <= 100000:
                total_cleared_size += size
                dirs.append(dir)

        self.logger.debug(dirs)
        return total_cleared_size

    def part2(self, data: List) -> None:
        pass


def solve_day(day: int, use_sample: bool):
    solver = Day7(day, use_sample)
    solver.solve()
