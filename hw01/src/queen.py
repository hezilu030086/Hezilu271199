class NQueens:
    def __init__(self, n: int):
        self.n = n
        self.solutions = []

    def is_safe(self, board: list, row: int, col: int) -> bool:
        """检查(row, col)放置皇后是否安全"""
        # 检查列冲突
        for i in range(row):
            if board[i] == col:
                return False
        # 检查左上-右下对角线
        for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
            if board[i] == j:
                return False
        # 检查右上-左下对角线
        for i, j in zip(range(row-1, -1, -1), range(col+1, self.n)):
            if board[i] == j:
                return False
        return True

    def backtrack(self, board: list, row: int):
        """回溯核心：逐行放置皇后"""
        if row == self.n:
            self.solutions.append(board.copy())
            return
        for col in range(self.n):
            if self.is_safe(board, row, col):
                board[row] = col
                self.backtrack(board, row + 1)
                board[row] = -1

    def find_all_solutions(self) -> list:
        """获取所有解"""
        board = [-1] * self.n
        self.backtrack(board, 0)
        return self.solutions

if __name__ == "__main__":
    # 验证4皇后(2解)和8皇后(92解)
    n4 = NQueens(4)
    print(f"4皇后解数量: {len(n4.find_all_solutions())}")
    
    n8 = NQueens(8)
    print(f"8皇后解数量: {len(n8.find_all_solutions())}")
