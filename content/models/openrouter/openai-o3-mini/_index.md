---
title: "OpenAI o3 Mini"
model: true
description: "OpenAI o3-mini is a cost-efficient language model optimized for STEM reasoning tasks, particularly excelling in science, mathematics, and coding. This model supports the `reasoning_effort` parameter, "
specs:
  vendor: "OpenAI"
  category: "国外"
  released: "2025"
  context: "200K tokens"
  price_input: "$0.0011/K"
  price_output: "$0.0044/K"
  modalities: "text+file->text"
  openrouter_id: "openai/o3-mini"

  scores:
    reasoning: 80
    coding: 85
    chinese: 70
    longtext: 85
---

## 模型概况

o3 Mini 是由 OpenAI 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | OpenAI |
| OpenRouter ID | `openai/o3-mini` |
| 上下文窗口 | 200K tokens |
| 输入价格 | $0.0000/M |
| 输出价格 | $0.0000/M |
| 模态 | text+file->text |

## OpenRouter 平台数据

OpenAI o3-mini is a cost-efficient language model optimized for STEM reasoning tasks, particularly excelling in science, mathematics, and coding. This model supports the `reasoning_effort` parameter, which can be set to...

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

- 文件处理
- 长文本对话、文档总结
- 常规文本生成与对话

## 来源

- [OpenRouter Models API](https://openrouter.ai/models)
