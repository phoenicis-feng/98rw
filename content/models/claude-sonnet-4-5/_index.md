---
title: "Claude Sonnet 4.5"
model: true
toc: true
description: "Anthropic 最强 Agent 编码模型，30+ 小时持续自主编码，OSWorld 61.4%，SWE-bench 77.2%，与 Sonnet 4 同价但能力大幅提升。"
specs:
  vendor: "Anthropic"
  category: "国外"
  released: "2025-09"
  context: "200K tokens (1M beta)"
  price_input: "$3/M"
  price_output: "$15/M"
  max_output: "64K tokens"
  modalities: "Text, Vision, PDF"
  thinking: "Extended Thinking"
  sustained_agent: "30+ hours"
  vs_code: true

  scores:
      reasoning: 91
      coding: 88
      chinese: 93
      longtext: 90

hero:
  title: "Claude Sonnet 4.5"
  subtitle: "30+ 小时持续自主编码 — OSWorld 61.4%，SWE-bench 77.2%，同价 Sonnet 4 的巨大升级。"
  highlights:
    - icon: "mdi-clock-outline"
      label: "30+ Hour Sustained Agent"
    - icon: "mdi-monitor-desktop"
      label: "OSWorld 61.4% (Computer Use)"
    - icon: "mdi-code-braces"
      label: "SWE-bench 77.2%"

  
---

## 一、模型概况

Anthropic 于 2025-09-29 发布的 **Claude Sonnet 4.5** 被官方描述为"全球最适合 Agent、编码和计算机使用的模型"。它在 SWE-bench Verified 上达到 77.2%，OSWorld 计算机使用能力从 42.2% 跃升至 61.4%，并首次实现了 30+ 小时的持续自主编码。

核心设计决策：
- **持续自主 Agent**：突破性实现 30+ 小时的持续自主编码能力，是 Agent 工作流的里程碑；
- **计算机使用突破**：OSWorld 61.4% 表示在浏览器操作、桌面应用交互等任务上大幅领先；
- **同价巨大升级**：与 Sonnet 4 相同的 $3/$15 定价，但能力大幅提升；
- **Claude Code 与 VS Code 集成**：通过 Claude Code 插件和 VS Code 扩展实现无缝开发体验。

## 二、性能评估：基准测试数据

### 2.1 核心基准横向对比

| 基准测试 | Claude Sonnet 4.5 | 说明 |
|---|---|---|
| **SWE-bench Verified** | **77.2%** | 可通过并行测试时计算提升至 82.0% |
| **OSWorld (Computer Use)** | **61.4%** | 4 个月内从 42.2% 跃升 19 个百分点 |
| **LiveCodeBench** | **71.4%** | 编程能力 |
| **Terminal-Bench** | **46.5%** | 终端操作能力 |
| **τ²-Bench** | **78.1%** | 代理工具调用 |
| **GPQA Diamond** | **82.3%–83.4%** | 科学推理 |
| **AIME 2024/2025** | **77.8%–88%** | 竞赛数学 |
| **MATH Level 5** | **97.7%** | 高等数学 |
| **ARC-AGI** | **63.7%** | 抽象推理 |
| **GDPval (win/tie)** | **50.3%** | 经济价值任务 |
| **Humanity's Last Exam** | **13.7%** | 极限推理 |
| **AA Intelligence Index** | **36.0** | 中等偏上 |
| **AA Coding Index** | 36th percentile | 编码能力 |
| **AA Agentic Index** | 39th percentile | 代理能力 |

### 2.2 定价结构（每百万 Token）

| 类型 | 成本 | vs Sonnet 4 |
|---|---|---|
| 输入 | $3.00 | 相同 |
| 输出 | $15.00 | 相同 |
| Batch 处理 | **50% 节省** ✅ | |
| Prompt 缓存 | **最高 90% 节省** ✅ | |

> 💡 **定位**：Sonnet 4.5 以与 Sonnet 4 完全相同的定价，提供了巨大的能力升级——是 Anthropic 序列中"性价比最高的升级"。

### 2.3 关键能力提升对比（vs Sonnet 4）

| 能力维度 | Sonnet 4 | Sonnet 4.5 | 提升 |
|---|---|---|---|
| SWE-bench | 72.7% | **77.2%** | +4.5 pts |
| OSWorld | 42.2% | **61.4%** | **+19.2 pts** ✅ |
| τ²-Bench | 64.6% | **78.1%** | +13.5 pts |
| Terminal-Bench | 31.1% | **46.5%** | +15.4 pts |
| LiveCodeBench | 65.5% | **71.4%** | +5.9 pts |
| MATH Level 5 | 99.1% | **97.7%** | 略降 |

## 三、优势分析

### 3.1 30+ 小时持续自主编码：Agent 工作流里程碑

Sonnet 4.5 最突出的优势是实现了 **30+ 小时的持续自主编码**：
- 在复杂任务上可以持续工作数小时而不丢失目标或上下文；
- 通过 Agent SDK 的 checkpoints、context editing、memory tools 实现状态管理；
- 首次使"一天一个功能的自主开发"成为可能。

这一能力使 Sonnet 4.5 成为：
- **长时程软件开发**：从需求到实现的完整循环；
- **自主代码重构**：大规模代码库的分析和重构；
- **持续集成/部署**：自动化测试、修复、部署流水线的核心。

### 3.2 OSWorld 61.4%：计算机使用能力飞跃

OSWorld 基准衡量模型在真实桌面环境中的计算机使用能力。Sonnet 4.5 从 Sonnet 4 的 42.2% 跃升至 61.4%，4 个月内提升了 19 个百分点：
- **浏览器导航**：可以操作复杂的网页应用；
- **电子表格处理**：可以读写和分析数据表格；
- **桌面应用交互**：可以操作本地应用程序；
- **Claude for Chrome**：Chrome 扩展演示了浏览器导航和电子表格任务的完整能力。

### 3.3 代码解释器能力

Simon Willison 高度评价了 Sonnet 4.5 的代码解释器表现：
- **克隆 GitHub 仓库**：可以自动拉取、分析和理解代码库；
- **安装依赖**：自动安装和配置开发环境；
- **运行测试套件**：执行测试并根据结果修复代码；
- **完整开发循环**：从代码克隆到测试通过的全流程。

### 3.4 Claude Code 与 VS Code 集成

Sonnet 4.5 深度集成了开发工具链：
- **Claude Code CLI**：终端中的自主编码代理；
- **VS Code 扩展**：在 IDE 中直接与 Claude 交互；
- **Agent SDK**：提供 checkpoints、context editing、memory tools 等高级功能；
- **代码解释器**：可以在沙箱中执行代码、克隆仓库、运行测试。

### 3.5 1M 上下文窗口 Beta

Sonnet 4.5 提供了 1M 上下文窗口的 Beta 访问：
- 支持超长文档的分析和理解；
- 可以处理完整的代码库上下文；
- 为大规模 Agent 任务提供了上下文基础。

## 四、对比分析

### 4.1 vs Claude Sonnet 4

| 维度 | Claude Sonnet 4.5 | Claude Sonnet 4 |
|---|---|---|
| SWE-bench | **77.2%** ✅ | 72.7% |
| OSWorld | **61.4%** ✅ | 42.2% |
| τ²-bench | **78.1%** ✅ | 64.6% |
| Terminal-Bench | **46.5%** ✅ | 31.1% |
| 持续 Agent | **30+ 小时** ✅ | 有限 |
| 定价 | $3/$15 | $3/$15（相同） |
| 代码解释器 | **Yes** ✅ | No |
| VS Code 集成 | **Yes** ✅ | No |

**结论**：同价位下，Sonnet 4.5 是巨大升级。如果已经使用 Sonnet 4，强烈建议升级到 Sonnet 4.5。

### 4.2 vs Claude Opus 4.5

| 维度 | Claude Sonnet 4.5 | Claude Opus 4.5 |
|---|---|---|
| Intelligence Index | 36.0 | **70** ✅ |
| LiveCodeBench | 71.4% | **87.1%** ✅ |
| SWE-bench | 77.2% | 76.7% |
| τ²-bench | 78.1% | **98.2%** ✅ |
| 定价 | **$3/$15** ✅ | $5/$25 |
| Agent 时长 | **30+ 小时** ✅ | 上下文压缩 |

**结论**：Opus 4.5 在推理和编码上限上更强，但 Sonnet 4.5 在同价位下提供了最强的 Agent 编码能力。复杂任务选 Opus 4.5，日常 Agent 选 Sonnet 4.5。

### 4.3 vs GPT-4o / 其他竞品

| 维度 | Claude Sonnet 4.5 | GPT-4o |
|---|---|---|
| Agent 时长 | **30+ 小时** ✅ | 有限 |
| OSWorld | **61.4%** ✅ | 较低 |
| 定价 | **$3/$15** ✅ | ~$5/$15 |
| 多模态 | Vision+PDF | **更强** ✅ |

**结论**：Sonnet 4.5 在 Agent 能力和定价上优势明显，GPT-4o 在多模态上更胜一筹。

## 五、用户评价与社区口碑

### 5.1 开发者社区反馈

**正面评价：**
- **"游戏改变者"**：30+ 小时自主编码能力被开发者称为"革命性"；
- **OSWorld 61.4% 令人震撼**：计算机使用能力的飞跃被广泛称赞；
- **同价巨大升级**：与 Sonnet 4 相同的价格但能力大幅提升，被称为"最好的价值主张"；
- **Claude Code 集成**：VS Code 和 CLI 集成被开发者高度评价；
- **代码解释器**：Simon Willison 等知名开发者称赞其代码解释器表现。

**负面评价：**
- **质量回归（2025年9月起）**：部分用户报告推理和代码质量下降；
- **1M 上下文 Beta**：尚未完全 GA，可能存在稳定性问题；
- **Intelligence Index 36.0**：相比 Opus 4.5 的 70 仍有差距；
- **τ²-bench 78.1%**：相比 Opus 4.5 的 98.2% 仍有差距。

### 5.2 行业评价

- **Toolso.AI 评分 4.9/5**：被称为"game-changing for developers and AI agents"；
- **Simon Willison**：高度评价代码解释器能力；
- **Anthropic 官方**：定位为"全球最适合 Agent、编码和计算机使用的模型"；
- **企业用户**：广泛采用用于自动化开发流程。

### 5.3 口碑综合研判

Sonnet 4.5 的评价呈现**高度正面**特征：
1. **Agent 编码**：30+ 小时持续自主编码是核心亮点；
2. **计算机使用**：OSWorld 61.4% 是重大突破；
3. **性价比**：与 Sonnet 4 同价但能力大幅提升；
4. **争议点**：2025年9月的质量回归问题和 Intelligence Index 低于 Opus 4.5。

## 六、推荐用法

### 6.1 最佳实践场景

| 场景 | 推荐度 | 说明 |
|---|---|---|
| Agentic 编码工作流 | ⭐⭐⭐⭐⭐ | **核心推荐场景**，30+ 小时持续编码 |
| 长时程自主开发 | ⭐⭐⭐⭐⭐ | 从需求到实现的完整循环 |
| 计算机使用/浏览器自动化 | ⭐⭐⭐⭐⭐ | OSWorld 61.4% |
| 软件开发（Claude Code/VS Code） | ⭐⭐⭐⭐⭐ | 深度工具链集成 |
| 复杂多步任务 | ⭐⭐⭐⭐ | 需要持续专注的场景 |
| 团队协作开发 | ⭐⭐⭐⭐ | Agent SDK 支持多代理编排 |
| 日常快速编码 | ⭐⭐⭐ | Sonnet 4 更快更便宜 |
| 最强推理任务 | ⭐⭐⭐ | Opus 4.5 更强 |

### 6.2 实用建议

1. **作为 Agent 编码的首选**：所有需要长时间自主编码的场景首选 Sonnet 4.5；
2. **充分利用 1M 上下文 Beta**：在处理大型代码库时开启；
3. **结合 Claude Code 使用**：通过 VS Code 扩展和 CLI 实现无缝开发体验；
4. **使用 Agent SDK 的高级功能**：checkpoints、memory tools、context editing 等；
5. **多代理编排**：用 Sonnet 4.5 作为子代理执行器，Sonnet 4.5 或 Opus 4.5 作为编排器；
6. **注意质量回归**：关注 Anthropic 的基础设施更新。

### 6.3 模型选择矩阵

```
需要 Agent 编码？
  → 是 → 需要多长？
    → 30+ 小时 → Claude Sonnet 4.5 ✅
    → 短时间 → 需要更强推理？
      → 是 → Claude Opus 4/4.5 ✅
      → 否 → Claude Sonnet 4 ✅
  → 否 → 需要最强推理？
    → 是 → Claude Opus 4.5 ✅
    → 否 → Claude Sonnet 4 ✅
```

## 七、已知局限

1. **Intelligence Index 36.0**：相比 Opus 4.5 的 70 仍有显著差距；
2. **τ²-bench 78.1%**：相比 Opus 4.5 的 98.2% 仍有差距；
3. **1M 上下文 Beta**：尚未完全 GA，可能存在稳定性问题；
4. **质量回归（2025年9月起）**：部分用户报告推理和代码质量下降；
5. **仍可能犯错**：可以产生事实错误和对敏感话题过度谨慎；
6. **ASL-3 安全级别**：可能对某些应用场景有限制；
7. **知识截止日期**：2025年1月，可能不是最新的。

## 八、综合评价

**核心结论**：Claude Sonnet 4.5 是 2025 年 Agent 编码领域的里程碑之作，以 30+ 小时持续自主编码、OSWorld 61.4% 计算机使用能力和与 Sonnet 4 相同的定价，重新定义了"Agent 编码模型"的标准。Simon Willison 等开发者的赞誉和 Toolso.AI 4.9/5 的评分证明了其革命性地位。

**适用 / 不适用：**

| 适合 | 不适合 |
|---|---|
| Agentic 编码工作流 | 最强推理任务（选 Opus 4.5） |
| 长时程自主开发 | 需要 Intelligence Index 最高的场景 |
| 计算机使用/浏览器自动化 | 需要最低延迟的实时应用 |
| Claude Code/VS Code 开发 | 纯文本简单对话 |
| 团队协作和多代理编排 | 预算极低的项目 |
| 复杂多步任务 | 基础设施稳定性要求极高的场景 |

**风险提示**：2025年9月的质量回归问题需持续关注；1M 上下文尚在 Beta；Intelligence Index 低于 Opus 4.5。

## 九、来源列表

1. [Anthropic — Claude Sonnet 4.5 发布](https://www.anthropic.com/news/claude-sonnet-4-5)
2. [Artificial Analysis — Sonnet 4.5 Benchmarks](https://artificialanalysis.ai/)
3. [SWE-bench Leaderboard](https://www.swebench.com/)
4. [OSWorld Benchmark](https://osworld-bench.com/)
5. [Anthropic — Claude Code](https://www.anthropic.com/product/claude-code)
6. [Simon Willison — Code Interpreter Review](https://simonwillison.net/)
7. [Toolso.AI — Sonnet 4.5 Rating](https://toolso.ai/)
8. [Anthropic Agent SDK Documentation](https://docs.anthropic.com/)
9. [Kashif Mukhtar — Claude Review](https://kashifmukhtar.com/claude-review/)
10. [InfoQ — Anthropic Infrastructure Bugs](https://www.infoq.com/news/2025/10/anthropic-infrastructure-bugs/)
11. [Anthropic — April 2025 Postmortem](https://www.anthropic.com/engineering/april-23-postmortem)
12. [DeployBase — LLM Stats](https://deploybase.com/blog/llm-stats)
13. [Anthropic API Pricing](https://www.anthropic.com/pricing)
14. [Reddit r/LocalLLaMA — Sonnet 4.5 Discussions](https://www.reddit.com/r/LocalLLaMA/)
15. [VS Code Extension — Claude Dev](https://marketplace.visualstudio.com/)
