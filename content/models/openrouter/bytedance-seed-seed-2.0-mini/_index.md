---
title: "字节跳动 Seed-2.0-Mini"
model: true
description: "Seed-2.0-mini targets latency-sensitive, high-concurrency, and cost-sensitive scenarios, emphasizing fast response and flexible inference deployment. It delivers performance comparable to ByteDance-Se"
specs:
  vendor: "字节跳动"
  category: "国内"
  released: "2025"
  context: "262K tokens"
  price_input: "$0.0001/K"
  price_output: "$0.0004/K"
  modalities: "text+image+video->text"
  openrouter_id: "bytedance-seed/seed-2.0-mini"

  scores:
    reasoning: 80
    coding: 85
    chinese: 70
    longtext: 85
---

## 模型概况

Seed-2.0-Mini 是由 字节跳动 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | 字节跳动 |
| OpenRouter ID | `bytedance-seed/seed-2.0-mini` |
| 上下文窗口 | 262K tokens |
| 输入价格 | $0.0000/M |
| 输出价格 | $0.0000/M |
| 模态 | text+image+video->text |

## OpenRouter 平台数据

Seed-2.0-mini targets latency-sensitive, high-concurrency, and cost-sensitive scenarios, emphasizing fast response and flexible inference deployment. It delivers performance comparable to ByteDance-Seed-1.6, supports 256k context, four reasoning effort modes (minimal/low/medium/high), multimodal understanding,...

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
