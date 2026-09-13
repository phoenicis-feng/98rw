---
title: "OpenAI GPT-5 Mini (batch)"
model: true
date: 2026-09-12T00:00:00Z
reasoning: 80
description: "GPT-5 Mini is a compact version of GPT-5, designed to handle lighter-weight reasoning tasks. It provides the same instruction-following and safety-tuning benefits as GPT-5, but with reduced latency an"
specs:
  vendor: "OpenAI"
  category: "国外"
  released: "2025"
  context: "400K tokens"
  price_input: "$0.0001/K"
  price_output: "$0.0010/K"
  modalities: "text+image+file->text"
  openrouter_id: "openai/gpt-5-mini:batch"

  scores:
    reasoning: 80
    coding: 85
    chinese: 70
    longtext: 85
---

## 模型概况

GPT-5 Mini (batch) 是由 OpenAI 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | OpenAI |
| OpenRouter ID | `openai/gpt-5-mini:batch` |
| 上下文窗口 | 400K tokens |
| 输入价格 | $0.0000/M |
| 输出价格 | $0.0000/M |
| 模态 | text+image+file->text |

## OpenRouter 平台数据

GPT-5 Mini is a compact version of GPT-5, designed to handle lighter-weight reasoning tasks. It provides the same instruction-following and safety-tuning benefits as GPT-5, but with reduced latency and cost....

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
