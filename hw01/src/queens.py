"""
N 皇后求解器
使用回溯算法（Backtracking）求解 N 皇后问题。
"""


def solve_n_queens(n: int) -> list[list[int]]:
    """
    求解 N 皇后问题，返回所有解。

    Args:
        n: 棋盘大小（N×N），同时也是皇后数量

    Returns:
        所有合法解的列表，每个解是长度为 n 的列表，
        solution[row] = col 表示第 row 行的皇后放在第 col 列。
    """
    solutions = []

    def is_valid(placement: list[int], row: int, col: int) -> bool:
        """检查在 (row, col) 放置皇后是否与已放置的皇后冲突。"""
        for r in range(row):
            c = placement[r]
            # 列冲突
            if c == col:
                return False
            # 斜线冲突：行差等于列差则在同一对角线上
            if abs(r - row) == abs(c - col):
                return False
        return True

    def backtrack(row: int, placement: list[int]) -> None:
        if row == n:
            solutions.append(placement[:])
            return
        for col in range(n):
            if is_valid(placement, row, col):
                placement.append(col)
                backtrack(row + 1, placement)
                placement.pop()

    backtrack(0, [])
    return solutions


def count_solutions(n: int) -> int:
    """
    返回 N 皇后问题的解的数量。

    Args:
        n: 棋盘大小

    Returns:
        合法解的总数
    """
    return len(solve_n_queens(n))
