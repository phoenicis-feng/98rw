---
title: "OpenRouter Auto Router (Beta)"
model: true
description: "Auto Router (Beta) is a task-aware router from OpenRouter. It classifies each request, then routes it the [most popular model](/rankings#task-spend) for that task based on aggregate spend, filtered by"
specs:
  vendor: "OpenRouter"
  category: "其他"
  released: "2025"
  context: "2M tokens"
  price_input: "$-1000.0000/K"
  price_output: "$-1000.0000/K"
  modalities: "text+image+file+audio+video->text+image"
  openrouter_id: "openrouter/auto-beta"

  scores:
    reasoning: 85
    coding: 90
    chinese: 70
    longtext: 95
---

## 模型概况

Auto Router (Beta) 是由 OpenRouter 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | OpenRouter |
| OpenRouter ID | `openrouter/auto-beta` |
| 上下文窗口 | 2M tokens |
| 输入价格 | $-1.0000/M |
| 输出价格 | $-1.0000/M |
| 模态 | text+image+file+audio+video->text+image |

## OpenRouter 平台数据

Auto Router (Beta) is a task-aware router from OpenRouter. It classifies each request, then routes it the [most popular model](/rankings#task-spend) for that task based on aggregate spend, filtered by your...

### 定价信息

| 项目 | 价格 |
|------|------|
| 输入 | $-1.0000/M |
| 输出 | $-1.0000/M |

### 支持的参数

该模型支持以下参数：
- 温度调节
- Top-P / Top-K 采样
- 流式输出
- 工具调用（如支持）

## 适用场景

- 图像理解、视觉问答
- 文件处理
- 长文档分析、大代码库处理
- 长文本对话、文档总结
- 常规文本生成与对话

## 来源

- [OpenRouter Models API](https://openrouter.ai/models)
