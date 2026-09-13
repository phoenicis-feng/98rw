---
title: "NVIDIA Nemotron 3.5 Content Safety"
model: true
date: 2026-09-12T00:00:00Z
reasoning: 80
description: "NVIDIA Nemotron 3.5 Content Safety is a compact 4B-parameter multimodal guardrail model from NVIDIA, fine-tuned from Google Gemma-3-4B. It moderates both inputs to and responses from LLMs and VLMs, ac"
specs:
  vendor: "NVIDIA"
  category: "国外"
  released: "2025"
  context: "131K tokens"
  price_input: "$0.0002/K"
  price_output: "$0.0002/K"
  modalities: "text+image->text"
  openrouter_id: "nvidia/nemotron-3.5-content-safety"

  scores:
    reasoning: 80
    coding: 85
    chinese: 70
    longtext: 85
---

## 模型概况

Nemotron 3.5 Content Safety 是由 NVIDIA 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | NVIDIA |
| OpenRouter ID | `nvidia/nemotron-3.5-content-safety` |
| 上下文窗口 | 131K tokens |
| 输入价格 | $0.0000/M |
| 输出价格 | $0.0000/M |
| 模态 | text+image->text |

## OpenRouter 平台数据

NVIDIA Nemotron 3.5 Content Safety is a compact 4B-parameter multimodal guardrail model from NVIDIA, fine-tuned from Google Gemma-3-4B. It moderates both inputs to and responses from LLMs and VLMs, accepting...

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
- 长文本对话、文档总结
- 常规文本生成与对话

## 来源

- [OpenRouter Models API](https://openrouter.ai/models)
