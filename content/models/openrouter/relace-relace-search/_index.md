---
title: "Relace Search"
model: true
date: 2026-09-12T00:00:00Z
reasoning: 80
description: "The relace-search model uses 4-12 `view_file` and `grep` tools in parallel to explore a codebase and return relevant files to the user request. In contrast to RAG, relace-search performs agentic..."
specs:
  vendor: "Relace"
  category: "其他"
  released: "2025"
  context: "256K tokens"
  price_input: "$0.0010/K"
  price_output: "$0.0030/K"
  modalities: "text->text"
  openrouter_id: "relace/relace-search"

  scores:
    reasoning: 80
    coding: 85
    chinese: 70
    longtext: 85
---

## 模型概况

Relace Search 是由 Relace 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | Relace |
| OpenRouter ID | `relace/relace-search` |
| 上下文窗口 | 256K tokens |
| 输入价格 | $0.0000/M |
| 输出价格 | $0.0000/M |
| 模态 | text->text |

## OpenRouter 平台数据

The relace-search model uses 4-12 `view_file` and `grep` tools in parallel to explore a codebase and return relevant files to the user request. In contrast to RAG, relace-search performs agentic...

### 定价信息

| 项目 | 价格 |
|------|------|
| 输入 | $0.0000/M |
| 输出 | $0.0000/M |

### 支持的参数

该模型支持以下参数：
- 温度调节
- Top-P / Top-K 采样
- 流式输出
- 工具调用（如支持）

## 适用场景

- 长文本对话、文档总结
- 常规文本生成与对话

## 来源

- [OpenRouter Models API](https://openrouter.ai/models)
