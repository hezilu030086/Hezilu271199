"""
pytest 单元测试：N 皇后求解器
"""
import pytest
from src.queens import solve_n_queens, count_solutions


class TestCountSolutions:
    def test_n4_has_2_solutions(self):
        assert count_solutions(4) == 2

    def test_n8_has_92_solutions(self):
        assert count_solutions(8) == 92


class TestSolveNQueens:
    def test_n1_single_solution(self):
        assert solve_n_queens(1) == [[0]]

    def test_n2_no_solution(self):
        assert solve_n_queens(2) == []

    def test_n3_no_solution(self):
        assert solve_n_queens(3) == []


class TestSolutionValidity:
    """验证 N=4 的所有解没有行/列/斜线冲突。"""

    def _is_valid_solution(self, solution: list[int]) -> bool:
        n = len(solution)
        for row in range(n):
            for other_row in range(row + 1, n):
                col = solution[row]
                other_col = solution[other_row]
                # 列冲突
                if col == other_col:
                    return False
                # 斜线冲突
                if abs(row - other_row) == abs(col - other_col):
                    return False
        return True

    def test_n4_solutions_are_valid(self):
        solutions = solve_n_queens(4)
        assert len(solutions) == 2
        for sol in solutions:
            assert len(sol) == 4, f"解的长度应为 4，实际为 {len(sol)}"
            assert self._is_valid_solution(sol), f"解 {sol} 存在冲突"

    def test_solution_values_in_range(self):
        """每个解中列值必须在 [0, n-1] 范围内。"""
        solutions = solve_n_queens(4)
        for sol in solutions:
            for col in sol:
                assert 0 <= col < 4, f"列值 {col} 超出范围"
