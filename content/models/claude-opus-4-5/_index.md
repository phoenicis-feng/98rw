---
title: "Claude Opus 4.5"
model: true
toc: true
description: "Anthropic 最强推理与编码模型，Artificial Analysis 智商指数 70 排名全球第二，66% 降价，SWE-bench 76.7%，首创上下文压缩实现无限长对话。"
specs:
  vendor: "Anthropic"
  category: "国外"
  released: "2025-11"
  context: "200K tokens"
  price_input: "$5/M"
  price_output: "$25/M"
  max_output: "64K tokens"
  modalities: "Text, Vision, PDF"
  thinking: "Extended Thinking"
  context_compaction: true

  scores:
      reasoning: 97
      coding: 93
      chinese: 89
      longtext: 93

hero:
  title: "Claude Opus 4.5"
  subtitle: "Artificial Analysis 智商指数全球第二 — 66% 降价，首创上下文压缩，最强终端编码能力。"
  highlights:
    - icon: "mdi:trophy"
      label: "AA Intelligence Index #2 (70)"
    - icon: "mdi:counter"
      label: "Terminal-Bench Hard 63.1% (史上最高)"
    - icon: "mdi:auto-repair"
      label: "Context Compaction — 无限长对话"

  
---

## 一、模型概况

Anthropic 于 2025-11-24 发布的 **Claude Opus 4.5** 是其史上最强大的旗舰模型，也是 token 效率最高的前沿模型。在 Artificial Analysis 智商指数上以 70 分排名全球第二（与 GPT-5.1 并列），同时在 Terminal-Bench Hard 上创造了 63.1% 的历史最高分。

核心设计决策：
- **Token 效率革命**：在智商指数上使用 4800 万输出 token，远少于 Gemini 3 Pro（9200万）、GPT-5.1（8100万）、Grok 4（1.2亿），处于智能 vs 输出 token 的帕累托前沿；
- **上下文压缩**：首创无限长度对话能力，通过智能摘要旧上下文实现；
- **模态扩展**：新增 PDF 输入和 Vision 支持，从纯文本升级为多模态；
- **66% 降价**：相比 Opus 4，输入从 $15/M 降至 $5/M，输出从 $75/M 降至 $25/M。

## 二、性能评估：基准测试数据

### 2.1 核心基准横向对比

| 基准测试 | Claude Opus 4.5 | 说明 |
|---|---|---|
| **AA Intelligence Index (Thinking)** | **70** | 全球第二（与 GPT-5.1 并列），仅次于 Gemini 3 Pro (73) |
| **AA Intelligence Index (非推理)** | **60** | 最强非推理模型 |
| **LiveCodeBench** | **87.1%** | 编程能力大幅领先 |
| **SWE-bench Verified** | **76.7%** | 超越 Sonnet 4.5 (77.2%) 和 Opus 4 (72.5%) |
| **Terminal-Bench Hard** | **63.1%** | 史上最高分，任何模型都无法超越 |
| **GPQA Diamond** | **86.0%** | 博士级科学推理 |
| **MMLU-Pro** | **89.5%** | 与 Gemini 3 Pro 并列第一 |
| **Humanity's Last Exam** | **25.2%** | 极限推理能力大幅提升 |
| **AIME 2024/2025** | **86.1%** | 竞赛数学 |
| **ARC-AGI** | **80.0%** | 抽象推理 |
| **τ²-bench Telecom** | **98.2%** | 电信领域代理能力最强 |
| **τ²-bench Retail** | **88.9%** | 零售领域 |
| **OSWorld** | **66.3%** | 计算机使用能力 |
| **GDPval (win/tie)** | **59.6%** | 经济价值任务 |
| **FrontierMath** | **20.7%** | 前沿数学 |
| **Omniscience Index** | **10** | 全球第二 |
| **METR task horizon** | **4.9 hours** | 任务时间跨度 |

### 2.2 定价结构（每百万 Token）

| 类型 | 成本 | vs Opus 4 |
|---|---|---|
| 输入 | $5.00 | **-66%** ✅ |
| 输出 | $25.00 | **-66%** ✅ |
| Cache Read | $0.50 | |

> 💡 **定位**：Opus 4.5 以 66% 的降价幅度提供了比 Opus 4 更强的能力，是"最强性价比旗舰"的完美诠释。

### 2.3 Token 效率帕累托分析

Opus 4.5 在 Artificial Analysis 的智商 vs 输出 token 帕累托图上处于前沿位置：
- 智商指数 70，仅使用 4800万输出 token
- Gemini 3 Pro 智商 73，但需要 9200万输出 token
- GPT-5.1 智商 70，需要 8100万输出 token
- **结论**：Opus 4.5 用更少的 token 达到相同的智能水平

## 三、优势分析

### 3.1 Terminal-Bench Hard 63.1%：史上最高

Opus 4.5 在 Terminal-Bench Hard 上达到 63.1%，这是该基准测试的历史最高纪录，甚至超越了所有更大的模型。这一成绩证明了其在终端操作、命令执行、环境导航等真实 Agent 任务中的卓越能力。

### 3.2 上下文压缩：无限长对话

Opus 4.5 首创了**上下文压缩**功能：
- 通过智能摘要旧上下文，实现理论上的无限长度对话；
- 在 30+ 小时的自主 Agent 任务中保持上下文一致性；
- 自动识别和总结不再需要的旧信息，释放上下文空间。

### 3.3 Token 效率：帕累托最优

在 Artificial Analysis 的智商指数评估中，Opus 4.5 是 token 效率最高的前沿模型：
- **48M 输出 token** → 智商 70
- Gemini 3 Pro：92M 输出 token → 智商 73
- GPT-5.1：81M 输出 token → 智商 70
- Grok 4：120M 输出 token → 智商更低
- **结论**：Opus 4.5 在"智能 per token"维度上处于绝对领先地位

### 3.4 模态扩展：PDF + Vision

相比 Opus 4 的纯文本，Opus 4.5 增加了：
- **PDF 输入**：可直接解析和分析 PDF 文档；
- **Vision**：支持图像理解；
- **更丰富的输入格式**：为文档分析、研究辅助等场景打开了新可能。

### 3.5 τ²-bench 98.2%：代理能力标杆

在 τ²-bench Telecom 上达到 98.2%，这是所有模型中的最高分。表明 Opus 4.5 在需要精确工具调用和协议遵循的 Agent 任务中表现卓越。

## 四、对比分析

### 4.1 vs Claude Opus 4

| 维度 | Claude Opus 4.5 | Claude Opus 4 |
|---|---|---|
| Intelligence Index | **70** ✅ | ~21–26 |
| SWE-bench | **76.7%** ✅ | 72.5% |
| Terminal-Bench Hard | **63.1%** ✅ | 31.1% |
| 定价（输入） | **$5/M** ✅ | $15/M |
| 定价（输出） | **$25/M** ✅ | $75/M |
| 模态 | **Text+Vision+PDF** ✅ | Text only |
| 上下文压缩 | **Yes** ✅ | No |
| Max Output | **64K** ✅ | 32K |

**结论**：Opus 4.5 在所有维度上都优于 Opus 4，且价格仅为 1/3。如果已经使用 Opus 4，升级到 Opus 4.5 是明确的选择。

### 4.2 vs GPT-5.1

| 维度 | Claude Opus 4.5 | GPT-5.1 |
|---|---|---|
| Intelligence Index | **70** (并列) | 70 |
| 编码基准 | **更强** ✅ | 稍弱 |
| Token 效率 | **更高** ✅ | 较低 |
| 推理能力 | 相当 | 相当 |

**结论**：两者智商指数并列，但 Opus 4.5 在编码和 token 效率上更优。

### 4.3 vs Gemini 3 Pro

| 维度 | Claude Opus 4.5 | Gemini 3 Pro |
|---|---|---|
| Intelligence Index | 70 | **73** ✅ |
| Omniscience Index | **10** ✅ | 13 |
| Token 效率 | **更高** ✅ | 较低 |
| 上下文 | 200K | **1M+** ✅ |
| 模态 | Text+Vision+PDF | **多模态更强** ✅ |

**结论**：Gemini 3 Pro 在智商指数上领先 3 分，但 Opus 4.5 在 token 效率和成本上优势明显。选型取决于是否需要极致智能 vs 极致效率。

### 4.4 vs Claude Sonnet 4.5

| 维度 | Claude Opus 4.5 | Claude Sonnet 4.5 |
|---|---|---|
| Intelligence Index | **70** ✅ | 36.0 |
| LiveCodeBench | **87.1%** ✅ | 71.4% |
| SWE-bench | 76.7% | 77.2% |
| τ²-bench | **98.2%** ✅ | 78.1% |
| 定价 | $5/$25 | $3/$15 |

**结论**：Opus 4.5 在推理和 Agent 能力上大幅领先，Sonnet 4.5 在 SWE-bench 上略胜但价格更低。复杂任务选 Opus 4.5，日常 Agent 选 Sonnet 4.5。

## 五、用户评价与社区口碑

### 5.1 开发者社区反馈

**正面评价：**
- **"史上最强编码模型"**：Terminal-Bench Hard 63.1% 的成绩引发开发者社区轰动；
- **性价比极高**：66% 降价让更多用户能够负担旗舰级能力；
- **上下文压缩创新**：无限长对话能力被评价为"游戏改变者"；
- **Token 效率**：用更少的 token 达到相同的智能水平，降低了实际使用成本；
- **PDF/Image 支持**：从纯文本升级为多模态，扩展了应用场景。

**负面评价：**
- **200K 上下文仍有限**：相比 Gemini 3 Pro 的 1M+ 仍显不足（1M 上下文在 Opus 4.6 才到来）；
- **基础设施质量担忧**：2025年9月起用户报告推理和代码质量下降；
- **有效成本节省有限**：虽然定价降 66%，但实际使用中可能消耗更多 token；
- **社区质量回归**：部分用户报告 2025年9月起所有 Claude 模型质量下降。

### 5.2 行业评价

- **Artificial Analysis**：评为全球第二智能模型，Token 效率第一；
- **企业用户**：金融、法律、科研领域广泛采用，用于高风险决策场景；
- **开发者社区**：在 Terminal-Bench、SWE-bench 等硬基准上获得一致好评；
- **Anthropic 官方**：定位为"最强大且最 token 高效的前沿模型"。

### 5.3 口碑综合研判

Opus 4.5 的评价呈现**高度正面**特征：
1. **能力维度**：几乎在所有基准上处于第一梯队或领先；
2. **成本维度**：66% 降价大幅降低了使用门槛；
3. **创新维度**：上下文压缩和 Token 效率是行业首创；
4. **争议点**：2025年9月的质量回归和基础设施问题需要持续关注。

## 六、推荐用法

### 6.1 最佳实践场景

| 场景 | 推荐度 | 说明 |
|---|---|---|
| 复杂编码任务（Terminal-Bench, SWE-bench） | ⭐⭐⭐⭐⭐ | 63.1% Terminal-Bench Hard 史上最高 |
| 长时程自主 Agent（30+ 小时） | ⭐⭐⭐⭐⭐ | 上下文压缩实现无限长对话 |
| 企业级推理工作流 | ⭐⭐⭐⭐⭐ | 最强推理 + 成本效率 |
| 金融/科学分析 | ⭐⭐⭐⭐⭐ | GPQA 86%, MMLU-Pro 89.5% |
| 计算机使用/浏览器自动化 | ⭐⭐⭐⭐⭐ | OSWorld 66.3% |
| 文档分析（PDF） | ⭐⭐⭐⭐ | 新增 PDF 输入支持 |
| 日常编码 | ⭐⭐⭐ | Sonnet 4.5 性价比更高 |
| 高并发批量处理 | ⭐⭐⭐ | 降价后更可行，但仍有成本考量 |

### 6.2 实用建议

1. **作为默认旗舰**：所有需要最强推理能力的任务首选 Opus 4.5；
2. **充分利用上下文压缩**：在长对话中开启此功能，避免上下文窗口溢出；
3. **结合 Sonnet 4.5 做路由**：用 Sonnet 4.5 处理日常任务，Opus 4.5 处理高价值任务；
4. **注意知识截止日期**：确保重要任务使用最新数据，或结合检索增强；
5. **监控质量回归**：关注 Anthropic 基础设施更新，确保获得最佳输出质量。

### 6.3 模型选择矩阵

```
需要最强推理能力？
  → 是 → Opus 4.5 ✅ (全球第二智能)
  → 否 → 需要长时程 Agent？
    → 是 → Opus 4.5 ✅ (上下文压缩)
    → 否 → 需要低成本？
      → 是 → Sonnet 4.5 ($3/$15) 或 Haiku 4 ($1/$5)
      → 否 → Sonnet 4.5 (性价比最优)
```

## 七、已知局限

1. **200K 上下文窗口**：相比 Gemini 3 Pro 的 1M+ 仍显不足（1M 在 Opus 4.6 才到来）；
2. **基础设施质量**：2025年9月起用户报告质量回归，影响部分用户信任；
3. **有效成本节省存疑**：虽然定价降 66%，但实际 token 消耗可能更高，有效节省不如表面；
4. **无默认 Effort 控制**：不像 Sonnet 4.5 有灵活的努力级别调节；
5. **200K 输出限制**：虽然比 Opus 4 的 32K 好很多，但仍不如某些竞品；
6. **知识截止日期**：可能不是最新的，需结合检索使用；
7. **社区质量回归担忧**：2025年9月起多用户报告推理、代码质量下降。

## 八、综合评价

**核心结论**：Claude Opus 4.5 是 2025 年末 Anthropic 的巅峰之作，以 Artificial Analysis 智商指数 70（全球第二）、Terminal-Bench Hard 63.1%（史上最高）、Token 效率帕累托最优三大成就，重新定义了"最强模型"的标准。66% 的降价使其从"奢侈品"变为"可负担的旗舰"。

**适用 / 不适用：**

| 适合 | 不适合 |
|---|---|
| 复杂编码与 Agent 任务 | 日常低成本任务 |
| 长时程自主 Agent（30+小时） | 高并发批量处理（成本仍高） |
| 企业级高风险推理 | 纯文本简单对话 |
| 金融/科学/法律分析 | 预算极有限的个人项目 |
| 计算机使用/浏览器自动化 | 需要 1M+ 上下文的场景 |

**风险提示**：2025年9月的基础设施质量回归问题需持续关注；Token 效率优势在实际使用中可能不如基准测试显著；200K 上下文窗口在 Opus 4.6 才扩展到 1M。

## 九、来源列表

1. [Anthropic — Claude Opus 4.5 发布](https://www.anthropic.com/news/claude-opus-4-5)
2. [Artificial Analysis — Opus 4.5 Intelligence Index](https://artificialanalysis.ai/)
3. [SWE-bench Leaderboard](https://www.swebench.com/)
4. [Terminal-Bench Hard](https://terminal-bench.com/)
5. [METR — Task Horizon Evaluation](https://metr.org/)
6. [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
7. [Kashif Mukhtar — Claude Review](https://kashifmukhtar.com/claude-review/)
8. [InfoQ — Anthropic Infrastructure Bugs](https://www.infoq.com/news/2025/10/anthropic-infrastructure-bugs/)
9. [Anthropic API Pricing](https://www.anthropic.com/pricing)
10. [Toolso.AI — Opus 4.5 Rating](https://toolso.ai/)
11. [Simon Willison — Claude Code Review](https://simonwillison.net/)
12. [Anthropic — Novo Nordisk Case Study](https://www.anthropic.com/)
13. [Salesforce — Agentforce Integration](https://www.anthropic.com/)
14. [DeployBase — LLM Stats](https://deploybase.com/blog/llm-stats)
15. [Anthropic Engineering — Postmortems](https://www.anthropic.com/engineering/)
