---
title: "Claude Sonnet 4"
model: true
toc: true
description: "Anthropic 平衡性能与成本的默认推荐模型，200K 上下文 + 1M(Vertex)，SWE-bench 72.7%，免费层可用，AA Agentic Index 第12名。"
specs:
  popularity: 87
  vendor: "Anthropic"
  category: "国外"
  released: "2025-05"
  context: "200K tokens (1M via Vertex)"
  price_input: "$3/M"
  price_output: "$15/M"
  max_output: "64K tokens"
  modalities: "Text, Vision"
  thinking: "Extended Thinking"
  free_tier: true

  scores:
      reasoning: 90
      coding: 85
      chinese: 92
      longtext: 88

hero:
  title: "Claude Sonnet 4"
  subtitle: "Anthropic 默认推荐 — 平衡性能与成本，免费层可用，99.1% MATH 500，AA Agentic Index 第12名。"
  highlights:
    - icon: "mdi-scale-balance"
      label: "最佳性价比平衡"
    - icon: "mdi-account-multiple"
      label: "免费层可用"
    - icon: "mdi-math"
      label: "MATH 500: 99.1%"

  
---

## 一、模型概况

Anthropic 于 2025-05-22 与 Claude Opus 4 同日发布的 **Claude Sonnet 4** 是 Anthropic 序列中的"默认推荐"模型。它在 SWE-Bench Verified 上达到 72.7%，在 MATH 500 上达到 99.1%，以 $3/$15 的亲民定价和免费层可用性，成为大多数用户的首选。

核心设计决策：
- **性能与成本平衡**：在编码和推理能力上接近 Opus 4，但价格仅为其 1/5；
- **全层级可用**：从 Free 到 Pro 到 Enterprise，所有用户均可使用；
- **1M 上下文（Vertex）**：通过 Google Vertex AI 可获得 1M 上下文窗口；
- **Vision 图像输入**：支持图像理解，扩展了多模态应用场景。

## 二、性能评估：基准测试数据

### 2.1 核心基准横向对比

| 基准测试 | Claude Sonnet 4 | 说明 |
|---|---|---|
| **SWE-Bench Verified** | **72.7%** | 与 Opus 4 (72.5%) 几乎相同 |
| **MMLU-Pro** | **84.2%** | 知识广度良好 |
| **GPQA Diamond** | **75.4%** | 科学推理能力 |
| **MATH 500** | **99.1%** | 数学推理接近满分 |
| **AIME 2025** | **74.3%** | 竞赛数学通过率 |
| **LiveCodeBench** | **65.5%** | 代码生成能力 |
| **Terminal-Bench Hard** | **31.1%** | 终端操作基础能力 |
| **τ²-Bench** | **64.6%** | 代理工具调用 |
| **IFBench** | **54.7%** | 指令遵循 |
| **HLE (Humanity's Last Exam)** | **9.6%** | 极限推理 |
| **AA Overall Intelligence** | #101 of 398 | 中等偏上 |
| **AA Coding Index** | #73 of 173 | 编码能力中上 |
| **AA Agentic Index** | #12 of 154 | **代理能力突出** |

### 2.2 定价结构（每百万 Token）

| 类型 | 成本 | vs Opus 4 |
|---|---|---|
| 输入 | $3.00 | **-80%** ✅ |
| 输出 | $15.00 | **-80%** ✅ |
| Cache Read | — | |

> 💡 **定位**：Sonnet 4 是 Anthropic 的"甜点"模型——性能接近 Opus 4，价格仅为其 1/5，且免费层可用。

### 2.3 速度表现

Sonnet 4 的速度在 Anthropic 序列中相对较慢：
- **51.7 tokens/s**（排名 #232/294）
- 首 token 延迟高于 Haiku 系列
- 适合非实时、批量处理场景

## 三、优势分析

### 3.1 SWE-Bench 72.7%：接近旗舰的编码能力

Sonnet 4 在 SWE-Bench Verified 上达到 72.7%，与 Opus 4 的 72.5% 几乎持平。这意味着对于日常编码任务，Sonnet 4 的输出质量与旗舰模型**几乎没有可感知的差异**。

这一成绩使得 Sonnet 4 成为：
- **个人开发者**：无需为 Opus 4 支付 5 倍费用；
- **团队项目**：在预算内获得旗舰级编码质量；
- **批量处理**：低成本完成大量编码任务。

### 3.2 MATH 500 99.1%：数学推理接近满分

在 MATH 500 上达到 99.1% 的惊人成绩，表明 Sonnet 4 在数学推理方面几乎达到了人类专家的水平。这对于：
- 教育场景（数学辅导、解题）
- 科学研究（公式推导、验证）
- 工程计算（算法分析、优化）

都是极具价值的能力。

### 3.3 全层级可用性

Sonnet 4 是 Anthropic 唯一一个在所有计划层级（Free、Pro、Team、Enterprise）均可使用的 Claude 4 模型：
- **Free 层**：所有新用户可免费体验 Claude 4 的能力；
- **Pro 层**：更高的使用限额和优先访问；
- **Team/Enterprise**：协作功能和管理工具。

### 3.4 Vision 图像输入

Sonnet 4 支持图像输入，可以：
- 分析上传的图片；
- 识别图表、截图中的信息；
- 进行视觉-文本交叉推理。

### 3.5 AA Agentic Index #12：代理能力突出

在 Artificial Analysis 的 Agentic Index 中排名第 12（共 154 个模型），表明 Sonnet 4 在 Agent 工作流方面表现出色：
- 工具调用准确率高；
- 多步任务执行稳定；
- 适合构建 Agent 应用。

## 四、对比分析

### 4.1 vs Claude Opus 4

| 维度 | Claude Sonnet 4 | Claude Opus 4 |
|---|---|---|
| SWE-bench | 72.7% | 72.5% |
| 定价（输入） | **$3/M** ✅ | $15/M |
| 定价（输出） | **$15/M** ✅ | $75/M |
| 速度 | **快 5x** ✅ | 慢 |
| 推理深度 | 日常足够 | **更强** ✅ |
| 免费层 | **Yes** ✅ | No |
| 复杂调试 | 基本可用 | **更强** ✅ |
| 长时程 Agent | 有限 | **7+ 小时** ✅ |

**结论**：SWE-bench 分数几乎相同，但 Sonnet 4 便宜 5 倍且速度快 5 倍。日常任务选 Sonnet 4，复杂任务选 Opus 4。

### 4.2 vs Claude Sonnet 4.5

| 维度 | Claude Sonnet 4 | Claude Sonnet 4.5 |
|---|---|---|
| SWE-bench | 72.7% | **77.2%** ✅ |
| OSWorld | 42.2% | **61.4%** ✅ |
| τ²-bench | 64.6% | **78.1%** ✅ |
| 定价 | $3/$15 | $3/$15（相同） |
| Agent 时长 | 有限 | **30+ 小时** ✅ |

**结论**：同价位下，Sonnet 4.5 是巨大升级。日常任务 Sonnet 4 足够，但 Agent 场景强烈推荐 Sonnet 4.5。

### 4.3 vs Claude Haiku 4

| 维度 | Claude Sonnet 4 | Claude Haiku 4 |
|---|---|---|
| SWE-bench | 72.7% | 73.3% ✅ |
| 速度 | 较慢 (51.7 t/s) | **快 2x** ✅ |
| 定价 | $3/$15 | **$1/$5** ✅ |
| 复杂推理 | **更强** ✅ | 基础足够 |
| 日常编码 | 优秀 | 优秀 |

**结论**：Haiku 4 在 SWE-bench 上甚至略胜 Sonnet 4，且价格更低、速度更快。Sonnet 4 的优势在于更复杂的推理和更丰富的经验。

### 4.4 vs GPT-4o

| 维度 | Claude Sonnet 4 | GPT-4o |
|---|---|---|
| 定价 | **$3/$15** ✅ | ~$5/$15 |
| 代理能力 | **#12** ✅ | 稍弱 |
| 多模态 | Vision | **更强** ✅ |
| 数学 | **99.1% MATH** ✅ | 稍弱 |

**结论**：Sonnet 4 在定价和代理能力上优势明显，GPT-4o 在多模态上更胜一筹。

## 五、用户评价与社区口碑

### 5.1 开发者社区反馈

**正面评价：**
- **"免费层的神"**：作为免费层可用的最强模型，获得了极高评价；
- **"日常任务完全够用"**：大多数开发者表示 Sonnet 4 已能满足日常编码需求；
- **MATH 99.1% 令人印象深刻**：数学推理能力接近满分；
- **价格合理**：$3/$15 的定价被广泛认可为"甜点价"。

**负面评价：**
- **速度较慢**：51.7 tokens/s 排名 #232/294，实时应用中体验不佳；
- **Agent 能力有限**：τ²-bench 64.6% 远低于 Opus 4.5 的 98.2%；
- **基础设施 bug（2025年8-9月）**：影响了输出质量；
- **长对话质量下降**：在非常长的复杂提示上，输出质量不如 Opus 层。

### 5.2 社区使用数据

- **AA Agentic Index #12**：表明社区广泛使用 Sonnet 4 构建 Agent 应用；
- **免费层最受欢迎**：大量新用户通过 Free 层首次体验 Claude 4；
- **批量处理首选**：企业用户用 Sonnet 4 进行高批量、低成本的处理任务。

### 5.3 口碑综合研判

Sonnet 4 的评价呈现**高度实用主义**特征：
1. **日常任务**：高度正面，是大多数用户的首选；
2. **复杂任务**：足够但非最优，Opus 4/4.5 更合适；
3. **Agent 场景**：可用但非最佳，Sonnet 4.5 更强大；
4. **速度**：是主要短板，不适合实时应用。

## 六、推荐用法

### 6.1 最佳实践场景

| 场景 | 推荐度 | 说明 |
|---|---|---|
| 日常编码与快速迭代 | ⭐⭐⭐⭐⭐ | 免费层可用，性价比最高 |
| 批量处理/高吞吐量 | ⭐⭐⭐⭐⭐ | $3/$15 定价适合大规模 |
| RAG 检索与合成 | ⭐⭐⭐⭐⭐ | 知识整合能力强 |
| 内容生成与迭代写作 | ⭐⭐⭐⭐⭐ | 写作质量优秀 |
| 客户聊天机器人 | ⭐⭐⭐⭐ | 成本低，适合大规模部署 |
| 数学/科学计算 | ⭐⭐⭐⭐ | MATH 99.1% 表现优异 |
| 复杂多步推理 | ⭐⭐⭐ | Opus 4/4.5 更强 |
| 长时程 Agent 任务 | ⭐⭐ | Sonnet 4.5 更适合 |
| 实时应用 | ⭐⭐ | 速度较慢 (51.7 t/s) |

### 6.2 实用建议

1. **作为默认起点**：所有新项目先尝试 Sonnet 4，不够再升级；
2. **利用免费层**：个人项目和小规模测试完全可以用 Free 层；
3. **结合 Vertex 1M 上下文**：需要长上下文时通过 Google Vertex 使用 1M 窗口；
4. **批量处理优化**：利用 Sonnet 4 的高吞吐量进行批量文本处理；
5. **Agent 场景升级**：如果需要更强的 Agent 能力，升级到 Sonnet 4.5。

### 6.3 模型选择决策树

```
需要最强推理/Agent？
  → 是 → Claude Opus 4/4.5 ✅
  → 否 → 需要免费/低成本？
    → 是 → Claude Sonnet 4 ✅ (免费层可用)
    → 否 → 需要更快速度？
      → 是 → Claude Haiku 4 ✅
      → 否 → Claude Sonnet 4 ✅ (默认推荐)
```

## 七、已知局限

1. **速度较慢**：51.7 tokens/s 排名 #232/294，实时应用中体验不佳；
2. **Agent 能力有限**：τ²-bench 64.6% 远低于 Opus 4.5 的 98.2%；
3. **Terminal-Bench Hard 31.1%**：终端操作能力一般；
4. **长对话质量下降**：在非常长的复杂提示上不如 Opus 层；
5. **基础设施 bug**：2025年8-9月影响了输出质量；
6. **复杂推理不足**：对于需要深度多步推理的任务，能力有限；
7. **无上下文压缩**：不支持无限长对话。

## 八、综合评价

**核心结论**：Claude Sonnet 4 是 Anthropic 的"甜点模型"——在 SWE-bench（72.7%）、MATH（99.1%）等核心基准上表现优异，以 $3/$15 的定价和免费层可用性，成为大多数用户的默认选择。AA Agentic Index 第 12 名证明了其在 Agent 工作流中的实用性。

**适用 / 不适用：**

| 适合 | 不适合 |
|---|---|
| 日常编码与快速迭代 | 复杂多步深度推理 |
| 批量处理/高吞吐量 | 长时程自主 Agent |
| 免费层用户 | 实时应用（速度慢） |
| RAG 与内容生成 | 终端操作密集任务 |
| 数学/科学计算 | 极端复杂推理场景 |
| 客户聊天机器人 | 需要最强推理的任务 |

**风险提示**：速度是主要短板，不适合实时应用；2025年8-9月的基础设施问题影响了部分用户信任；Agent 能力有限，复杂场景推荐 Sonnet 4.5。

## 九、来源列表

1. [Anthropic — Claude 4 Family 发布](https://www.anthropic.com/news/claude-4)
2. [Artificial Analysis — Sonnet 4 Benchmarks](https://artificialanalysis.ai/)
3. [SWE-bench Leaderboard](https://www.swebench.com/)
4. [MATH Benchmark](https://github.com/hendrycks/math)
5. [AA Agentic Index](https://artificialanalysis.ai/leaderboard)
6. [Anthropic API Pricing](https://www.anthropic.com/pricing)
7. [Google Vertex AI — 1M Context](https://cloud.google.com/vertex-ai)
8. [MasterPrompting — Sonnet 4 vs Opus 4](https://masterprompting.net/blog/claude-sonnet-4-vs-opus-4-which-to-use)
9. [InfoQ — Anthropic Infrastructure Bugs](https://www.infoq.com/news/2025/10/anthropic-infrastructure-bugs/)
10. [Anthropic — April 2025 Postmortem](https://www.anthropic.com/engineering/april-23-postmortem)
11. [DeployBase — LLM Stats](https://deploybase.com/blog/llm-stats)
12. [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
13. [Reddit r/LocalLLaMA — Sonnet 4 Discussions](https://www.reddit.com/r/LocalLLaMA/)
14. [Toolso.AI — Sonnet 4 Rating](https://toolso.ai/)
15. [Anthropic — Claude for Free Tier](https://www.anthropic.com/)
