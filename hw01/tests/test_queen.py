from hw01.src.queen import NQueens

def test_4_queens_solution_count():
    n4 = NQueens(4)
    assert len(n4.find_all_solutions()) == 2, "4皇后解数量应为2"

def test_8_queens_solution_count():
    n8 = NQueens(8)
    assert len(n8.find_all_solutions()) == 92, "8皇后解数量应为92"

def test_is_safe_logic():
    n4 = NQueens(4)
    board = [-1, 0, -1, -1]  # 第0行第0列放置皇后
    assert not n4.is_safe(board, 2, 2), "第2行第2列应与第0行第0列对角线冲突"
    assert n4.is_safe(board, 2, 3), "第2行第3列应安全"
