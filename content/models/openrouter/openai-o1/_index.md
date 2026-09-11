---
title: "OpenAI o1"
model: true
description: "The latest and strongest model family from OpenAI, o1 is designed to spend more time thinking before responding. The o1 model series is trained with large-scale reinforcement learning to reason..."
specs:
  vendor: "OpenAI"
  category: "国外"
  released: "2025"
  context: "200K tokens"
  price_input: "$0.0150/K"
  price_output: "$0.0600/K"
  modalities: "text+image+file->text"
  openrouter_id: "openai/o1"

  scores:
    reasoning: 80
    coding: 85
    chinese: 70
    longtext: 85
---

## 模型概况

o1 是由 OpenAI 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | OpenAI |
| OpenRouter ID | `openai/o1` |
| 上下文窗口 | 200K tokens |
| 输入价格 | $0.0000/M |
| 输出价格 | $0.0001/M |
| 模态 | text+image+file->text |

## OpenRouter 平台数据

The latest and strongest model family from OpenAI, o1 is designed to spend more time thinking before responding. The o1 model series is trained with large-scale reinforcement learning to reason...

### 定价信息

| 项目 | 价格 |
|------|------|
| 输入 | $0.0000/M |
| 输出 | $0.0001/M |

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
