# HW02：论文导读与 DMXAPI Chatbot 实践

## 项目简介

本项目对应《人工智能导论》课程 HW02，包含两部分内容：

1. 论文导读：阅读并整理论文 **DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning**。
2. Chatbot 示例代码：编写一个可运行的 Python 命令行程序，演示如何通过 **DMXAPI（OpenAI 兼容第三方接口）** 调用大模型回答用户问题。该实现采用作业允许的“其它官方/第三方 API”方案，不使用火山引擎。

---

## 项目结构

```text
hw02/
├── assets/
│   ├── DeepSeek-R1.pdf
│   ├── fig1_r1_pipeline.png
│   ├── fig2_aime_accuracy.png
│   ├── fig3_response_length.png
│   └── source/                  # 论文源文件（用于提取真实图表）
├── chatbot_dmxapi.py            # DMXAPI Chatbot 示例代码
├── requirements.txt             # Python 依赖
├── README.md                    # 项目说明
└── 导读_DeepSeek_R1.md          # 论文导读文档
```

---

## 任务一：论文导读说明

- 论文标题：**DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning**
- 作者：**DeepSeek-AI**
- 来源：**Nature, 2025**（论文最初以 arXiv:2501.12948 公开，后发表于 Nature）
- 使用的大模型：**Claude Code**（用于辅助整理导读结构与文字表述）
- 配图方式：导读中的图片均来自论文原文，手动从论文源文件中提取并插入。

导读文档见：`导读_DeepSeek_R1.md`

---

## 任务二：Chatbot 示例代码说明

本项目的 Chatbot 示例代码使用 **DMXAPI** 提供的 **OpenAI 兼容接口**，属于作业要求中允许的“其它官方/第三方 API”调用方式，因此不需要配置火山引擎的 Bot ID。

### 环境要求

- Python 3.10+
- 可访问 DMXAPI 的网络环境

### 安装依赖

```bash
cd C:/Users/a1/Desktop/hw02
python -m pip install -r requirements.txt
```

### 配置 API Key

运行前先设置环境变量：

```bash
set DMXAPI_API_KEY=你的_API_Key
set DMXAPI_API_URL=https://www.dmxapi.cn/v1/chat/completions
set DMXAPI_MODEL=claude-sonnet-4-6
```

其中：

- `DMXAPI_API_KEY`：你的 DMXAPI Key
- `DMXAPI_API_URL`：DMXAPI 的 OpenAI 兼容聊天接口地址
- `DMXAPI_MODEL`：当前默认模型名，已设置为 `claude-sonnet-4-6`

如果你后续改用别的模型，只需要修改：

```bash
set DMXAPI_MODEL=你的模型名
```

### 功能对应作业要求

本示例已经覆盖作业要求的最小流程：

1. 在命令行输入一段文本问题
2. 程序将问题发送到 DMXAPI 的 `/v1/chat/completions` 接口
3. 获取模型返回结果并在终端打印回复

因此，它满足“发送一段文本问题 → 调用模型 → 获取并打印/展示模型回复”的要求。

### 运行方式

```bash
python chatbot_dmxapi.py
```

运行后在命令行输入问题即可，输入 `exit` 或 `quit` 可退出。

### 示例

```text
你：请用一句话介绍 DeepSeek-R1
模型：DeepSeek-R1 是一类通过强化学习提升推理能力的大语言模型。
```

---

## 实现说明

### 论文导读部分

本次导读重点整理了以下内容：

- 研究背景：为什么大模型推理仍然依赖人工标注轨迹
- 核心方法：DeepSeek-R1-Zero 与 DeepSeek-R1 的训练思路
- 关键机制：GRPO、规则奖励、多阶段训练流程
- 实验结果：在数学、代码、通用能力上的表现变化
- 个人总结：对强化学习提升推理能力的理解

### Chatbot 部分

`chatbot_dmxapi.py` 采用最小可运行设计：

- 从环境变量读取 `DMXAPI_API_KEY`
- 通过 DMXAPI 的 OpenAI 兼容 `chat/completions` 接口调用模型
- 默认模型为 `claude-sonnet-4-6`
- 在命令行中循环接收输入并输出回复
- 完整覆盖“输入问题 → 调用模型 → 打印回复”的基本流程
- 缺少配置时给出清晰提示

---

## 注意事项

1. 若未设置 `DMXAPI_API_KEY`，程序会提示配置错误并退出。
2. 若网络异常或 API 返回错误，程序会打印错误信息，便于排查。
3. 导读中的图片路径均为相对路径，建议保持当前目录结构不变。

---

## 论文链接

- Nature 期刊页面：https://www.nature.com/articles/s41586-025-09422-z
- arXiv 摘要页：https://arxiv.org/abs/2501.12948
- PDF：https://arxiv.org/pdf/2501.12948
