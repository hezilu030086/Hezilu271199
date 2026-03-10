import pytest
from hw01.src.queen import NQueens

def test_four_queens_solution_count():
    """测试4皇后：正确解数量应为2"""
    n4 = NQueens(4)
    solutions = n4.find_all_solutions()
    assert len(solutions) == 2, "4皇后问题求解错误，正确解数量为2"

def test_eight_queens_solution_count():
    """测试8皇后：正确解数量应为92"""
    n8 = NQueens(8)
    solutions = n8.find_all_solutions()
    assert len(solutions) == 92, "8皇后问题求解错误，正确解数量为92"

def test_queen_safety_check():
    """测试安全检查方法：验证冲突判断逻辑"""
    n8 = NQueens(8)
    board = [0, 2, -1, -1, -1, -1, -1, -1]
    assert n8.is_safe(board, 2, 4) is True
    assert n8.is_safe(board, 2, 0) is False
    assert n8.is_safe(board, 2, 3) is False
