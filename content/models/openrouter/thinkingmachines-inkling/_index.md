---
title: "Thinking Machines Inkling"
model: true
date: 2026-09-12T00:00:00Z
reasoning: 85
description: "Inkling is an open-weight multimodal mixture-of-experts model from Thinking Machines Lab, with 41B active parameters out of 975B total. It is designed for general-purpose reasoning, coding, agentic an"
specs:
  vendor: "Thinking Machines"
  category: "其他"
  released: "2025"
  context: "1M tokens"
  price_input: "$0.0010/K"
  price_output: "$0.0040/K"
  modalities: "text+image+audio->text"
  openrouter_id: "thinkingmachines/inkling"

  scores:
    reasoning: 85
    coding: 90
    chinese: 70
    longtext: 95
---

## 模型概况

Inkling 是由 Thinking Machines 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | Thinking Machines |
| OpenRouter ID | `thinkingmachines/inkling` |
| 上下文窗口 | 1M tokens |
| 输入价格 | $0.0000/M |
| 输出价格 | $0.0000/M |
| 模态 | text+image+audio->text |

## OpenRouter 平台数据

Inkling is an open-weight multimodal mixture-of-experts model from Thinking Machines Lab, with 41B active parameters out of 975B total. It is designed for general-purpose reasoning, coding, agentic and tool-use systems,...

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

- 图像理解、视觉问答
- 长文档分析、大代码库处理
- 长文本对话、文档总结
- 常规文本生成与对话

## 来源

- [OpenRouter Models API](https://openrouter.ai/models)
