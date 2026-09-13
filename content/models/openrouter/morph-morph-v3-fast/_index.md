---
title: "Morph V3 Fast"
model: true
date: 2026-09-12T00:00:00Z
reasoning: 75
description: "Morph's fastest apply model for code edits. ~10,500 tokens/sec with 96% accuracy for rapid code transformations. The model requires the prompt to be in the following format: <instruction>{instruction}"
specs:
  vendor: "Morph"
  category: "其他"
  released: "2025"
  context: "81K tokens"
  price_input: "$0.0008/K"
  price_output: "$0.0012/K"
  modalities: "text->text"
  openrouter_id: "morph/morph-v3-fast"

  scores:
    reasoning: 75
    coding: 80
    chinese: 70
    longtext: 75
---

## 模型概况

Morph V3 Fast 是由 Morph 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | Morph |
| OpenRouter ID | `morph/morph-v3-fast` |
| 上下文窗口 | 81K tokens |
| 输入价格 | $0.0000/M |
| 输出价格 | $0.0000/M |
| 模态 | text->text |

## OpenRouter 平台数据

Morph's fastest apply model for code edits. ~10,500 tokens/sec with 96% accuracy for rapid code transformations. The model requires the prompt to be in the following format: <instruction>{instruction}</instruction> <code>{initial_code}</code> <update>{edit_snippet}</update>...

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

- 常规文本生成与对话

## 来源

- [OpenRouter Models API](https://openrouter.ai/models)
