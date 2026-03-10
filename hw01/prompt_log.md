# Prompt Log：HW01 与 Claude Code 的交互记录

记录本次作业中与 AI（Claude Code）交互的关键节点，作为"AI 辅助开发"的过程证明。

---

## 1. 需求描述阶段

**Prompt（用户输入）：**
> 实现以下计划：[HW01 计划文档全文，包含项目结构、核心函数签名、测试用例表格]

**AI 响应要点：**
- 解析出需要创建的目录结构：`hw01/src/`、`hw01/tests/`
- 识别核心函数：`solve_n_queens(n: int) -> list[list[int]]` 和 `count_solutions(n: int) -> int`
- 确认测试用例：N=4（2解）、N=8（92解）、N=1/2/3 的边界情况

**工程决策：**
- 使用回溯算法，逐行放置皇后，`placement` 列表隐式表示行约束（无需列冲突的额外数据结构）
- 冲突检查通过 `abs(r - row) == abs(c - col)` 判断斜线

---

## 2. Bug 引入与修复阶段

### 2.1 引入的 Bug

在 `src/queens.py` 的 `is_valid` 函数中，故意将斜线冲突检查条件改错：

```python
# BUG 版本（错误）：用加法代替减法，导致无法正确检测反对角线
if abs(r + row) == abs(c + col):   # ← 错误！
    return False
```

正确版本应为：
```python
if abs(r - row) == abs(c - col):   # ← 正确
    return False
```

### 2.2 pytest 报错信息

```
FAILED tests/test_queens.py::TestCountSolutions::test_n4_has_2_solutions
FAILED tests/test_queens.py::TestCountSolutions::test_n8_has_92_solutions
FAILED tests/test_queens.py::TestSolutionValidity::test_n4_solutions_are_valid

AssertionError: assert 0 == 2
  # count_solutions(4) 返回 0，期望 2

AssertionError: assert 0 == 92
  # count_solutions(8) 返回 0，期望 92
```

### 2.3 调试过程

**分析：** `count_solutions(4)` 返回 0 意味着没有找到任何解。结合 `is_valid` 函数，问题定位在冲突检查过于严格——正常不冲突的位置被误判为冲突。

**对比错误逻辑：**
- `abs(r + row) == abs(c + col)`：对于 r=0, row=1, c=0, col=2 → `abs(1)==abs(2)` → False（不冲突，正确）
- 但对于 r=0, row=0（不可能出现，因为 `range(row)` 不含 row 本身）……

  实际上，`abs(r + row) == abs(c + col)` 在大多数情况下会误拦截合法位置，导致几乎无解。

**修复：** 将 `+` 改回 `-`，恢复正确的对角线检测逻辑。

### 2.4 修复后验证

```bash
python -m pytest tests/ -v
```

输出：
```
tests/test_queens.py::TestCountSolutions::test_n4_has_2_solutions PASSED
tests/test_queens.py::TestCountSolutions::test_n8_has_92_solutions PASSED
tests/test_queens.py::TestSolveNQueens::test_n1_single_solution    PASSED
tests/test_queens.py::TestSolveNQueens::test_n2_no_solution        PASSED
tests/test_queens.py::TestSolveNQueens::test_n3_no_solution        PASSED
tests/test_queens.py::TestSolutionValidity::test_n4_solutions_are_valid  PASSED
tests/test_queens.py::TestSolutionValidity::test_solution_values_in_range PASSED

7 passed in 0.85s
```

---

## 3. 关键 Prompt 技巧总结

### 3.1 如何描述需求

**有效做法：**
- 提供完整的函数签名和类型注解（`list[list[int]]`）让 AI 理解数据格式
- 给出具体的测试用例表格，而非模糊描述（"N=8 应有 92 个解"比"应该有很多解"有效 100 倍）
- 指定算法偏好（"使用回溯算法"），避免 AI 选择非期望的实现

### 3.2 如何引导 Bug 修复

**有效做法：**
- 将 pytest 的完整错误信息提供给 AI（包括 `AssertionError` 的具体数值）
- 指定可疑范围（"问题在 `is_valid` 函数"），缩小搜索空间
- 让 AI 解释修复逻辑，而非只给出代码（有助于理解和验证）

### 3.3 代码结构建议

**有效做法：**
- 要求 AI 将测试分组到 `class` 中（`TestCountSolutions`、`TestSolveNQueens`）提高可读性
- 要求内嵌辅助方法（`_is_valid_solution`）而非在测试外部定义，保持测试自包含

---

## 4. 反思

1. **AI 在工程化流程中的价值**：不仅是生成代码，更重要的是帮助规划结构、编写测试、分析报错。
2. **测试驱动的重要性**：Bug 在引入后立即被 pytest 捕获，说明测试覆盖了关键路径。
3. **Prompt 质量决定输出质量**：越具体的需求描述，越少的来回修改。
