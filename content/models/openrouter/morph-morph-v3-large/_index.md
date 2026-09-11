---
title: "Morph V3 Large"
model: true
description: "Morph's high-accuracy apply model for complex code edits. ~4,500 tokens/sec with 98% accuracy for precise code transformations. The model requires the prompt to be in the following format: <instructio"
specs:
  vendor: "Morph"
  category: "其他"
  released: "2025"
  context: "262K tokens"
  price_input: "$0.0009/K"
  price_output: "$0.0019/K"
  modalities: "text->text"
  openrouter_id: "morph/morph-v3-large"

  scores:
    reasoning: 80
    coding: 85
    chinese: 70
    longtext: 85
---

## 模型概况

Morph V3 Large 是由 Morph 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | Morph |
| OpenRouter ID | `morph/morph-v3-large` |
| 上下文窗口 | 262K tokens |
| 输入价格 | $0.0000/M |
| 输出价格 | $0.0000/M |
| 模态 | text->text |

## OpenRouter 平台数据

Morph's high-accuracy apply model for complex code edits. ~4,500 tokens/sec with 98% accuracy for precise code transformations. The model requires the prompt to be in the following format: <instruction>{instruction}</instruction> <code>{initial_code}</code>...

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
