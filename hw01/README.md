# HW01：N 皇后问题工程化实践

## 项目简介

本项目是课程作业 HW01，以"N 皇后问题"为载体，练习 Python 工程化开发流程，包括：
- 模块化代码组织（`src/` 包结构）
- 单元测试（pytest）
- AI 辅助开发与调试（Claude Code）

## 项目结构

```
hw01/
├── src/
│   ├── __init__.py
│   └── queens.py          # N 皇后求解器（回溯算法）
├── tests/
│   ├── __init__.py
│   └── test_queens.py     # pytest 单元测试
├── prompt_log.md          # 与 AI 的交互日志
└── README.md              # 本文件
```

## 环境要求

- Python 3.13+
- pytest 8.x（`pip install pytest`）

## 运行测试

```bash
cd Desktop\hw01
python -m pytest tests/ -v
```

期望输出：所有测试 `PASSED`，共 7 个测试用例。

## 算法简介

### 回溯算法（Backtracking）

N 皇后问题要求在 N×N 的棋盘上放置 N 个皇后，使得任意两个皇后互不攻击（不在同一行、列或对角线）。

**思路：**

1. 逐行放置皇后（每行恰好一个），从第 0 行开始。
2. 在当前行尝试每一列，检查是否与已放置的皇后冲突：
   - **列冲突**：`placement[r] == col`
   - **斜线冲突**：`abs(r - row) == abs(placement[r] - col)`
3. 若合法，则递归处理下一行；若无合法位置，则回溯。
4. 当所有 N 行都放置完毕，记录该解。

**时间复杂度**：最坏 O(N!)，实际因剪枝远小于此。

### 已知解的数量

| N | 解的数量 |
|---|---------|
| 1 | 1 |
| 2 | 0 |
| 3 | 0 |
| 4 | 2 |
| 8 | 92 |

## 数据格式

`solve_n_queens(n)` 返回 `list[list[int]]`，每个内层列表表示一种解：

```
solution[row] = col  # 第 row 行的皇后位于第 col 列（0-indexed）
```

示例（N=4 的两种解）：
```python
[[1, 3, 0, 2], [2, 0, 3, 1]]
```
