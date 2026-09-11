---
title: "Meituan LongCat 2.0"
model: true
description: "LongCat 2.0 is a sparse mixture-of-experts language model from Meituan, with 48B active parameters out of 1.6T total. It is suited for coding, repository-level changes, long-horizon problem solving, a"
specs:
  vendor: "Meituan"
  category: "其他"
  released: "2025"
  context: "1M tokens"
  price_input: "$0.0003/K"
  price_output: "$0.0012/K"
  modalities: "text->text"
  openrouter_id: "meituan/longcat-2.0"

  scores:
    reasoning: 85
    coding: 90
    chinese: 70
    longtext: 95
---

## 模型概况

LongCat 2.0 是由 Meituan 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | Meituan |
| OpenRouter ID | `meituan/longcat-2.0` |
| 上下文窗口 | 1M tokens |
| 输入价格 | $0.0000/M |
| 输出价格 | $0.0000/M |
| 模态 | text->text |

## OpenRouter 平台数据

LongCat 2.0 is a sparse mixture-of-experts language model from Meituan, with 48B active parameters out of 1.6T total. It is suited for coding, repository-level changes, long-horizon problem solving, and agentic...

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

- 长文档分析、大代码库处理
- 长文本对话、文档总结
- 常规文本生成与对话

## 来源

- [OpenRouter Models API](https://openrouter.ai/models)
