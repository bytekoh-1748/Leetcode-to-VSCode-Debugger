import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from python.leetcode_debug_runtime import evaluate_module_cases, load_solution_module


class LeetCodeDebugRuntimeTests(unittest.TestCase):
    def run_solution(self, source: str, case_text: str) -> tuple[int, str]:
        with TemporaryDirectory() as temp_dir:
            solution_path = Path(temp_dir) / "solution.py"
            solution_path.write_text(source, encoding="utf-8")
            module = load_solution_module(solution_path)
            return evaluate_module_cases(module, None, case_text)

    def test_helper_method_does_not_block_entrypoint_inference(self) -> None:
        source = """
from typing import List

class Solution:
    def dfs(self, nums, idx):
        return idx

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for index, value in enumerate(nums):
            need = target - value
            if need in seen:
                return [seen[need], index]
            seen[value] = index
        return []
"""
        case_text = "Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\n"

        exit_code, output_text = self.run_solution(source, case_text)

        self.assertEqual(exit_code, 0)
        self.assertIn("Case 1: PASS", output_text)

    def test_named_inputs_fall_back_to_positional_for_renamed_params(self) -> None:
        source = """
from typing import List

class Solution:
    def helper(self, values, goal):
        seen = {}
        for index, value in enumerate(values):
            need = goal - value
            if need in seen:
                return [seen[need], index]
            seen[value] = index
        return []

    def twoSum(self, values: List[int], goal: int) -> List[int]:
        return self.helper(values, goal)
"""
        case_text = "Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\n"

        exit_code, output_text = self.run_solution(source, case_text)

        self.assertEqual(exit_code, 0)
        self.assertIn("Case 1: PASS", output_text)


if __name__ == "__main__":
    unittest.main()
