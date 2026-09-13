---
title: "Claude Haiku 4"
model: true
toc: true
description: "Anthropic 最快最经济的模型，$1/M 输入 / $5/M 输出，SWE-bench 73.3%，零工具调用失败，ASL-2 安全级别，200K 上下文。"
specs:
  popularity: 85
  vendor: "Anthropic"
  category: "国外"
  released: "2025-10"
  context: "200K tokens"
  price_input: "$1/M"
  price_output: "$5/M"
  max_output: "64K tokens"
  modalities: "Text, Images"
  thinking: "Manual Extended Thinking"
  effort_control: false
  safety_level: "ASL-2"

  scores:
      reasoning: 85
      coding: 80
      chinese: 90
      longtext: 82

hero:
  title: "Claude Haiku 4"
  subtitle: "Anthropic 最快最经济 — SWE-bench 73.3%，零工具调用失败，ASL-2 最安全，1/3 成本达到 Sonnet 4.5 的 90%。"
  highlights:
    - icon: "mdi-speedometer"
      label: "Fastest in Anthropic Lineup"
    - icon: "mdi-cash"
      label: "$1/M Input — Lowest Price"
    - icon: "mdi-shield-check"
      label: "ASL-2 Safest Model"

  
---

## 一、模型概况

Anthropic 于 2025-10-15 发布的 **Claude Haiku 4**（即 Claude Haiku 4.5）是其序列中最快、最经济的模型。它以 $1/M 输入和 $5/M 输出的定价，提供了接近 Sonnet 4.5 90% 的 Agent 编码性能，同时拥有 Anthropic 序列中最快的推理速度和最低的误对齐率。

核心设计决策：
- **极致成本效率**：$1/M 输入和 $5/M 输出，是最便宜的 Claude 模型；
- **最快推理速度**：Anthropic 序列中首 token 延迟最低，适合实时应用；
- **零工具调用失败**：在头对头编码测试中零工具调用失败；
- **ASL-2 安全级别**：统计上显著少于其他模型的误对齐行为；
- **多模型编排**：可与 Sonnet 4.5 配对——Sonnet 拆解复杂问题，Haiku 并行执行子任务。

## 二、性能评估：基准测试数据

### 2.1 核心基准横向对比

| 基准测试 | Claude Haiku 4 | 说明 |
|---|---|---|
| **SWE-bench Verified** | **73.3%** | 匹配 Sonnet 4 (72.7%)，超越 Sonnet 4 的成本效率 |
| **Terminal-Bench** | **41.75%** | 32K 思考预算下；40.21% 无思考 |
| **τ²-bench (Retail)** | **83.2%** | 零售领域代理能力 |
| **τ²-bench (Telecom)** | **83%** | 电信领域代理能力 |
| **τ²-bench (Airline)** | **63.6%** | 航空领域代理能力 |
| **GPQA Diamond** | **67.2%** | 科学推理 |
| **MMLU-Pro** | **76%** | 多语言 0-shot |
| **AIME 2025** | **80.7%** | 竞赛数学 |
| **OSWorld** | **50.7%** | 计算机使用能力 |
| **LMArena Elo** | **1378** | 通用对话能力 |
| **LMArena Coding Elo** | **1436** | 编码对话能力 |
| **Cybersecurity CTFs** | **46.88%** | 网络安全挑战 |

### 2.2 定价结构（每百万 Token）

| 类型 | 成本 | vs Sonnet 4 | vs Opus 4 |
|---|---|---|---|
| 输入 | **$1.00** | -67% ✅ | **-93%** ✅ |
| 输出 | **$5.00** | -67% ✅ | **-93%** ✅ |
| 5-min Cache Write | $1.25 / MTok | | |
| 1-hour Cache Write | $2.00 / MTok | | |
| Cache Read | **$0.10 / MTok** | | |
| Batch API | **50% 折扣** ✅ | | |
| Prompt 缓存节省 | **最高 90%** ✅ | | |

> 💡 **定位**：Haiku 4 是"用最少的钱获得最接近前沿的编码能力"的完美选择。约 90% 的 Sonnet 4.5 性能，1/3 的成本，2x 的速度。

### 2.3 速度优势

Haiku 4 在 Anthropic 序列中拥有最快的推理速度：
- **首 token 延迟最低**：适合实时交互应用；
- **2x 速度快于 Sonnet 4**；
- **设计目标**：实时、低延迟应用场景。

## 三、优势分析

### 3.1 SWE-bench 73.3%：接近 Sonnet 4 的编码能力

Haiku 4 在 SWE-bench Verified 上达到 73.3%，与 Sonnet 4 的 72.7% 基本持平，甚至略高。这意味着：
- **近前端编码能力**：以最低价格获得接近 Sonnet 4 的编码质量；
- **零工具调用失败**：在头对头编码测试中零失败率；
- **高性价比**：以 Sonnet 4 1/3 的成本获得相当的编码能力。

### 3.2 最快推理：实时应用首选

Haiku 4 是 Anthropic 序列中最快的模型：
- **最低首 token 延迟**：适合聊天助手、客服等实时应用；
- **高速响应**：2x 快于 Sonnet 4；
- **低延迟体验**：用户几乎感知不到等待时间。

### 3.3 零工具调用失败：Agent 可靠性

在头对头编码测试中，Haiku 4 实现了**零工具调用失败**：
- 所有工具调用都正确执行；
- 无幻觉、无错误参数；
- 对于需要高可靠性的 Agent 工作流至关重要。

### 3.4 ASL-2 安全级别：最安全的模型

Anthropic 的自动化评估表明，Haiku 4 是其序列中最安全的模型：
- **统计上显著更少**的误对齐行为；
- **ASL-2 安全级别**：比 Sonnet 4.5 和 Opus 4.1 的 ASL-3 更低限制；
- 适合对安全性要求高的应用场景。

### 3.5 多模型编排：Sonnet + Haiku 组合

Haiku 4 的最佳使用方式之一是与 Sonnet 4.5 配对：
- **Sonnet 4.5**：拆解复杂问题，制定计划；
- **Haiku 4**：并行执行子任务，高速完成；
- **优势**：兼顾规划质量和执行效率。

### 3.6 LMArena Coding Elo 1436

LMArena Coding Elo 达到 1436，表明：
- 在社区众包编码对比中表现优异；
- 与远大于自身的模型竞争时编码能力出色；
- 开发者社区对 Haiku 4 的编码能力高度认可。

## 四、对比分析

### 4.1 vs Claude Sonnet 4

| 维度 | Claude Haiku 4 | Claude Sonnet 4 |
|---|---|---|
| SWE-bench | **73.3%** ✅ | 72.7% |
| 速度 | **快 2x** ✅ | 慢 (51.7 t/s) |
| 定价 | **$1/$5** ✅ | $3/$15 |
| 复杂推理 | 基础 | **更强** ✅ |
| 工具调用 | **零失败** ✅ | 可用 |
| 通用能力 | 略弱 | **更强** ✅ |

**结论**：Haiku 4 在 SWE-bench 上略胜 Sonnet 4，速度更快，价格更低。复杂推理选 Sonnet 4，编码和速度选 Haiku 4。

### 4.2 vs Claude Sonnet 4.5

| 维度 | Claude Haiku 4 | Claude Sonnet 4.5 |
|---|---|---|
| 编码性能 | ~90% | **100%** ✅ |
| 定价 | **$1/$5** ✅ | $3/$15 |
| 速度 | **2x 快** ✅ | 中等 |
| Agent 时长 | 有限 | **30+ 小时** ✅ |
| OSWorld | 50.7% | **61.4%** ✅ |
| Effort 控制 | **无** | Yes |

**结论**：约 90% 的 Sonnet 4.5 性能，1/3 的成本，2x 的速度。预算敏感选 Haiku 4，需要最强 Agent 选 Sonnet 4.5。

### 4.3 vs GPT-4o-mini

| 维度 | Claude Haiku 4 | GPT-4o-mini |
|---|---|---|
| 编码能力 | **远强** ✅ | 基础 |
| Agent 能力 | **远强** ✅ | 有限 |
| 定价 | $1/$5 | **$0.15/$0.60** ✅ |
| 适用场景 | 中高复杂度 | 低复杂度 |

**结论**：GPT-4o-mini 在极低复杂度任务上更便宜，但 Haiku 4 的编码和 Agent 能力远胜。

### 4.4 vs Gemini 2.5 Flash

| 维度 | Claude Haiku 4 | Gemini 2.5 Flash |
|---|---|---|
| 定价 | $1/$5 | **$0.075–$0.30/$0.30–$2.50** ✅ |
| 速度 | 快 | **更快到首 token** ✅ |
| 工具调用 | **零失败** ✅ | 可用 |
| 编码能力 | **更强** ✅ | 较弱 |
| 上下文 | 200K | **1M** ✅ |

**结论**：Gemini Flash 更便宜更快，但 Haiku 4 编码能力更强且零工具调用失败。

## 五、用户评价与社区口碑

### 5.1 开发者社区反馈

**正面评价：**
- **"最佳性价比"**：$1/$5 的定价获得接近 Sonnet 4.5 的性能；
- **"零工具调用失败"**：在头对头测试中零失败，可靠性极高；
- **"最快模型"**：实时应用中体验极佳；
- **"最安全模型"**：ASL-2 安全级别获得高度认可；
- **"近前端编码"**：73.3% SWE-bench 让个人开发者惊叹。

**负面评价：**
- **手动思考模式**：不支持自适应努力控制；
- **200K 上下文**：相比竞品的 1M+ 较短；
- **输出任务成本高**：输出 $5/M vs 输入 $1/M，输出密集型任务成本较高；
- **知识截止日期**：2025年2月（可靠）/7月（训练数据），不是最新的。

### 5.2 社区使用场景

- **高频率实时应用**：聊天助手、客服、Pair Programming；
- **子代理执行**：多模型编排中的子任务执行器；
- **高批量操作**：分类、提取、数据处理；
- **安全敏感场景**：ASL-2 最低误对齐率；
- **预算受限项目**：个人开发者、初创公司。

### 5.3 口碑综合研判

Haiku 4 的评价呈现**高度实用主义**特征：
1. **性价比**：最核心的优势，"用最少的钱办最多的事"；
2. **速度**：实时应用的首选；
3. **可靠性**：零工具调用失败是重要卖点；
4. **安全性**：ASL-2 最低误对齐率；
5. **局限**：复杂推理和长时程 Agent 不如 Opus/Sonnet 层。

## 六、推荐用法

### 6.1 最佳实践场景

| 场景 | 推荐度 | 说明 |
|---|---|---|
| 高频率实时应用（聊天、客服） | ⭐⭐⭐⭐⭐ | 最快推理速度 |
| Pair Programming | ⭐⭐⭐⭐⭐ | 快速响应 + 零工具失败 |
| 高批量数据处理 | ⭐⭐⭐⭐⭐ | $1/M 输入成本极低 |
| 多模型编排（子代理执行） | ⭐⭐⭐⭐⭐ | 并行执行子任务 |
| 预算受限项目 | ⭐⭐⭐⭐⭐ | 最低价格 |
| 安全敏感应用 | ⭐⭐⭐⭐⭐ | ASL-2 最安全 |
| 分类/提取/数据清洗 | ⭐⭐⭐⭐⭐ | 高性价比批量处理 |
| 复杂多步推理 | ⭐⭐ | Opus 4.5 更强 |
| 长时程 Agent 任务 | ⭐⭐ | Sonnet 4.5 更适合 |
| 需要 1M+ 上下文 | ⭐⭐ | 200K 较短 |

### 6.2 实用建议

1. **作为默认快速模型**：所有需要快速响应的场景首选 Haiku 4；
2. **多模型编排**：用 Sonnet 4.5 做规划，Haiku 4 做执行；
3. **利用 Prompt 缓存**：最高 90% 的缓存节省可进一步降低成本；
4. **批量 API**：50% 折扣的 Batch API 适合高吞吐场景；
5. **成本监控**：输出密集型任务注意 $5/M 的输出成本；
6. **安全场景优先**：ASL-2 安全级别使其成为监管环境的优选。

### 6.3 模型选择决策树

```
需要最快速度/最低成本？
  → 是 → Claude Haiku 4 ✅ ($1/$5, 最快)
  → 否 → 需要最强编码/Agent？
    → 是 → Claude Sonnet 4.5 ✅ (30+小时Agent)
    → 否 → 需要最强推理？
      → 是 → Claude Opus 4/4.5 ✅
      → 否 → Claude Sonnet 4 ✅ (默认推荐)
```

## 七、已知局限

1. **手动思考模式**：不支持自适应努力控制，需手动开关思考；
2. **200K 上下文窗口**：相比竞品的 1M+ 较短，限制了长文档处理；
3. **无默认 Effort 控制**：无法像 Sonnet 4.5 那样灵活调节思考深度；
4. **输出成本高**：$5/M 输出 vs $1/M 输入，输出密集型任务成本较高；
5. **知识截止日期**：2025年2月（可靠）/7月（训练数据），不是最新的；
6. **复杂推理有限**：对于需要深度多步推理的任务，能力不足；
7. **ASL-2 安全级别**：较低限制，可能不适合高度监管环境；
8. **无上下文压缩**：不支持无限长对话。

## 八、综合评价

**核心结论**：Claude Haiku 4 是 Anthropic 序列中"极致性价比"的典范——以 $1/$5 的定价提供 SWE-bench 73.3% 的编码能力、最快的推理速度、零工具调用失败率和 ASL-2 最安全级别。约 90% 的 Sonnet 4.5 性能、1/3 的成本、2x 的速度，使其成为预算敏感和实时应用的首选。

**适用 / 不适用：**

| 适合 | 不适合 |
|---|---|
| 高频率实时应用 | 复杂多步深度推理 |
| Pair Programming | 长时程自主 Agent |
| 高批量数据处理 | 需要 1M+ 上下文的场景 |
| 多模型编排子代理 | 极端复杂推理任务 |
| 预算受限项目 | 需要最强推理的场景 |
| 安全敏感应用 | 输出密集型高成本任务 |
| 分类/提取/数据清洗 | 需要自适应思考控制 |

**风险提示**：200K 上下文较短，不适合长文档处理；手动思考模式不如自适应思考灵活；知识截止日期较早；输出成本相对较高。

## 九、来源列表

1. [Anthropic — Claude Haiku 4.5 发布](https://www.anthropic.com/news/claude-haiku-4-5)
2. [Anthropic — Our Safest Model Yet](https://www.anthropic.com/)
3. [Artificial Analysis — Haiku 4.5 Benchmarks](https://artificialanalysis.ai/)
4. [SWE-bench Leaderboard](https://www.swebench.com/)
5. [LMArena — Claude Haiku 4 Ratings](https://lmarena.ai/)
6. [Anthropic API Pricing](https://www.anthropic.com/pricing)
7. [VerticalAPI — Claude Haiku vs GPT-mini vs Gemini Flash](https://verticalapi.com/)
8. [Skywork — Claude Haiku 4.5 Comparison](https://skywork.ai/blog/claude-haiku-4-5-vs-gpt4o-mini-vs-gemini-flash-vs-mistral-small-vs-llama-comparison/)
9. [MasterPrompting — Claude Models Comparison](https://masterprompting.net/blog/claude-sonnet-4-vs-opus-4-which-to-use)
10. [DeployBase — LLM Stats](https://deploybase.com/blog/llm-stats)
11. [Anthropic — Claude Code](https://www.anthropic.com/product/claude-code)
12. [Reddit r/LocalLLaMA — Haiku 4.5 Discussions](https://www.reddit.com/r/LocalLLaMA/)
13. [Toolso.AI — Haiku 4.5 Rating](https://toolso.ai/)
14. [Anthropic — Safety Evaluations](https://www.anthropic.com/)
15. [Anthropic — April 2025 Postmortem](https://www.anthropic.com/engineering/april-23-postmortem)
