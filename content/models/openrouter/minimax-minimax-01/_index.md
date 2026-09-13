---
title: "MiniMax 01"
model: true
date: 2026-09-12T00:00:00Z
reasoning: 85
description: "MiniMax-01 is a combines MiniMax-Text-01 for text generation and MiniMax-VL-01 for image understanding. It has 456 billion parameters, with 45.9 billion parameters activated per inference, and can han"
specs:
  vendor: "MiniMax"
  category: "国内"
  released: "2025"
  context: "1M tokens"
  price_input: "$0.0002/K"
  price_output: "$0.0011/K"
  modalities: "text+image->text"
  openrouter_id: "minimax/minimax-01"

  scores:
    reasoning: 85
    coding: 90
    chinese: 70
    longtext: 95
---

## 模型概况

MiniMax-01 是由 MiniMax 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | MiniMax |
| OpenRouter ID | `minimax/minimax-01` |
| 上下文窗口 | 1M tokens |
| 输入价格 | $0.0000/M |
| 输出价格 | $0.0000/M |
| 模态 | text+image->text |

## OpenRouter 平台数据

MiniMax-01 is a combines MiniMax-Text-01 for text generation and MiniMax-VL-01 for image understanding. It has 456 billion parameters, with 45.9 billion parameters activated per inference, and can handle a context...

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
