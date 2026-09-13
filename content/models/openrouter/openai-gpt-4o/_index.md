---
title: "OpenAI GPT-4o"
model: true
date: 2026-09-12T00:00:00Z
reasoning: 80
description: "GPT-4o (\"o\" for \"omni\") is OpenAI's latest AI model, supporting both text and image inputs with text outputs. It maintains the intelligence level of [GPT-4 Turbo](/models/openai/gpt-4-turbo) while bei"
specs:
  vendor: "OpenAI"
  category: "国外"
  released: "2025"
  context: "128K tokens"
  price_input: "$0.0025/K"
  price_output: "$0.0100/K"
  modalities: "text+image+file->text"
  openrouter_id: "openai/gpt-4o"

  scores:
    reasoning: 80
    coding: 85
    chinese: 70
    longtext: 85
---

## 模型概况

GPT-4o 是由 OpenAI 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | OpenAI |
| OpenRouter ID | `openai/gpt-4o` |
| 上下文窗口 | 128K tokens |
| 输入价格 | $0.0000/M |
| 输出价格 | $0.0000/M |
| 模态 | text+image+file->text |

## OpenRouter 平台数据

GPT-4o ("o" for "omni") is OpenAI's latest AI model, supporting both text and image inputs with text outputs. It maintains the intelligence level of [GPT-4 Turbo](/models/openai/gpt-4-turbo) while being twice as...

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
- 文件处理
- 长文本对话、文档总结
- 常规文本生成与对话

## 来源

- [OpenRouter Models API](https://openrouter.ai/models)
