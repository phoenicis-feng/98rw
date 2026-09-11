---
title: "OpenAI GPT Audio"
model: true
description: "The gpt-audio model is OpenAI's first generally available audio model. The new snapshot features an upgraded decoder for more natural sounding voices and maintains better voice consistency. Audio is p"
specs:
  vendor: "OpenAI"
  category: "国外"
  released: "2025"
  context: "128K tokens"
  price_input: "$0.0025/K"
  price_output: "$0.0100/K"
  modalities: "text+audio->text+audio"
  openrouter_id: "openai/gpt-audio"

  scores:
    reasoning: 80
    coding: 85
    chinese: 70
    longtext: 85
---

## 模型概况

GPT Audio 是由 OpenAI 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | OpenAI |
| OpenRouter ID | `openai/gpt-audio` |
| 上下文窗口 | 128K tokens |
| 输入价格 | $0.0000/M |
| 输出价格 | $0.0000/M |
| 模态 | text+audio->text+audio |

## OpenRouter 平台数据

The gpt-audio model is OpenAI's first generally available audio model. The new snapshot features an upgraded decoder for more natural sounding voices and maintains better voice consistency. Audio is priced...

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
