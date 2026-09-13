---
title: "Claude 模型家族"
model: false
date: 2026-09-13T00:00:00Z
description: "Anthropic Claude 系列模型完整列表，包含 Opus、Sonnet、Haiku、Fable、Mythos 五条产品线的所有型号、上下文窗口、定价与发布时间。"
---

## Claude 系列概览

Claude 是 Anthropic 开发的大模型家族，按能力与定位分为五条产品线：

| 产品线 | 定位 | 模型数量 |
|--------|------|----------|
| **Opus** | 旗舰级，最强推理与编程能力 | Opus 4 / 4.1 / 4.5 / 4.6 / 4.7 / 4.8 / 5 |
| **Sonnet** | 均衡型，兼顾性能与成本 | Sonnet 4 / 4.5 / 4.6 / 5 |
| **Haiku** | 最快最便宜，高吞吐低延迟 | Haiku 3 / Haiku 4.5 |
| **Fable** | 面向叙事与创意写作 | Fable 5 / Fable 5.1 |
| **Mythos** | 面向深度研究与知识工作 | Mythos 5.1 |

---

## Opus 系列（旗舰）

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID | 发布 |
|------|--------|----------|----------|---------------|------|
| Claude Opus 5 | 1M | $5.00/M | $25.00/M | `anthropic/claude-opus-5` | 2026-07 |
| Claude Opus 4.8 | 1M | $5.00/M | $25.00/M | `anthropic/claude-opus-4.8` | 2026 |
| Claude Opus 4.7 | 1M | $5.00/M | $25.00/M | `anthropic/claude-opus-4.7` | 2026 |
| Claude Opus 4.6 | 1M | $5.00/M | $25.00/M | `anthropic/claude-opus-4.6` | 2025 |
| Claude Opus 4.5 | 200K | $5.00/M | $25.00/M | `anthropic/claude-opus-4.5` | 2025-11 |
| Claude Opus 4.1 | 200K | $15.00/M | $75.00/M | `anthropic/claude-opus-4.1` | 2025-08 |
| Claude Opus 4 | 200K | $15.00/M | $75.00/M | `anthropic/claude-opus-4` | 2025-05 |

**核心能力**：最强编程（SWE-bench 领先）、长时任务执行、代码审查、视觉分析、复杂推理。

---

## Sonnet 系列（均衡）

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID | 发布 |
|------|--------|----------|----------|---------------|------|
| Claude Sonnet 5 | 1M | $2.00/M | $10.00/M | `anthropic/claude-sonnet-5` | 2026 |
| Claude Sonnet 4.6 | 1M | $3.00/M | $15.00/M | `anthropic/claude-sonnet-4.6` | 2026 |
| Claude Sonnet 4.5 | 1M | $3.00/M | $15.00/M | `anthropic/claude-sonnet-4.5` | 2025-09 |
| Claude Sonnet 4 | 1M | $3.00/M | $15.00/M | `anthropic/claude-sonnet-4` | 2025-05 |

**核心能力**：智能体工作流、编程、大规模数据分析。Sonnet 4.5 起支持 1M 上下文。

---

## Haiku 系列（高吞吐）

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID | 发布 |
|------|--------|----------|----------|---------------|------|
| Claude Haiku 4.5 | 200K | $1.00/M | $5.00/M | `anthropic/claude-haiku-4.5` | 2025-10 |
| Claude Haiku 3 | 200K | $0.25/M | $1.25/M | `anthropic/claude-3-haiku` | 2025 |

**核心能力**：最快响应、最低成本。Haiku 4.5 性能匹配 Sonnet 4，适合高并发场景。

---

## Fable 系列（叙事创作）

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID | 发布 |
|------|--------|----------|----------|---------------|------|
| Claude Fable 5.1 | 1M | $10.00/M | $50.00/M | `anthropic/claude-fable-5.1` | 2026 |
| Claude Fable 5 | 1M | $10.00/M | $50.00/M | `anthropic/claude-fable-5` | 2025 |

**核心能力**：长篇叙事、创意写作、角色扮演、内容生成。

---

## Mythos 系列（深度研究）

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID | 发布 |
|------|--------|----------|----------|---------------|------|
| Claude Mythos 5.1 | — | — | — | 暂未上架 OpenRouter | 2026 |

**核心能力**：深度研究、知识工作、复杂分析与推理。与 Fable 5.1 同期发布。

---

## 选型指南

| 场景 | 推荐模型 |
|------|----------|
| 最强编程 / 复杂推理 | Claude Opus 5 |
| 日常编程 / 智能体 | Claude Sonnet 4.5 / 4.6 |
| 高并发 / 低成本 | Claude Haiku 4.5 |
| 长文本 / 大代码库 | Sonnet 4.5+ 或 Opus（1M 上下文） |
| 创意写作 | Claude Fable 5.1 |
| 深度研究 | Claude Mythos 5.1 |

---

## 模型发布时间线

```
2025-05    Opus 4, Sonnet 4
2025-08    Opus 4.1
2025-09    Sonnet 4.5
2025-10    Haiku 4.5
2025-11    Opus 4.5
2026       Opus 4.6/4.7/4.8, Sonnet 4.6/5, Fable 5.1, Mythos 5.1
2026-07    Opus 5
```

---

## 官方来源

- [Anthropic Claude 模型页](https://www.anthropic.com/claude)
- [Opus](https://www.anthropic.com/claude/opus) · [Sonnet](https://www.anthropic.com/claude/sonnet) · [Haiku](https://www.anthropic.com/claude/haiku) · [Fable](https://www.anthropic.com/claude/fable) · [Mythos](https://www.anthropic.com/claude/mythos)
- [Claude Opus 5 公告](https://www.anthropic.com/news/claude-opus-5)
- [Claude Fable 5.1 & Mythos 5.1 公告](https://www.anthropic.com/claude-fable-and-mythos-5-1)
