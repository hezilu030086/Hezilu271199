# 八皇后问题核心求解器：支持任意N皇后，采用回溯法实现
class NQueens:
    def __init__(self, n: int):
        self.n = n  # 棋盘大小与皇后数量
        self.solutions = []  # 存储所有合法解的列表

    def is_safe(self, board: list, row: int, col: int) -> bool:
        """
        判断(row, col)位置放置皇后是否安全
        检查列、左上到右下对角线、右上到左下对角线是否有冲突
        """
        # 检查列冲突
        for i in range(row):
            if board[i] == col:
                return False
        # 检查左上-右下对角线冲突
        for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
            if board[i] == j:
                return False
        # 检查右上-左下对角线冲突
        for i, j in zip(range(row-1, -1, -1), range(col+1, self.n)):
            if board[i] == j:
                return False
        return True

    def backtrack(self, board: list, row: int):
        """回溯递归核心：逐行放置皇后，找到所有解"""
        if row == self.n:
            self.solutions.append(board.copy())
            return
        # 遍历当前行的每一列，尝试放置
        for col in range(self.n):
            if self.is_safe(board, row, col):
                board[row] = col
                self.backtrack(board, row + 1)
                board[row] = -1  # 回溯，撤销放置

    def find_all_solutions(self) -> list:
        """入口方法：初始化棋盘并执行回溯"""
        board = [-1] * self.n  # -1表示无皇后，索引为行，值为列
        self.backtrack(board, 0)
        return self.solutions

# 运行示例：验证4皇后与8皇后解数量
if __name__ == "__main__":
    # 测试4皇后（预期2个解）
    n4 = NQueens(4)
    print(f"4皇后问题解数量: {len(n4.find_all_solutions())}")

    # 测试8皇后（预期92个解）
    n8 = NQueens(8)
    print(f"8皇后问题解数量: {len(n8.find_all_solutions())}")
