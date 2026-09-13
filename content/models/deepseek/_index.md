---
title: "DeepSeek 模型家族"
model: false
date: 2026-09-13T00:00:00Z
description: "DeepSeek 系列模型完整列表，包含 V3/R1 推理模型的定价、上下文与发布时间。"
---

## 系列概览

| 系列 | 定位 |
|------|------|
| **V3 系列** | 通用对话与编程 |
| **R1 系列** | 推理专用 |

---

## V3 系列

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID |
|------|--------|----------|----------|---------------|
| DeepSeek V3.2 | 164K | $0.27/M | $0.40/M | `deepseek/deepseek-v3.2` |
| DeepSeek V3.1 Terminus | 164K | $0.27/M | $1.00/M | `deepseek/deepseek-v3.1-terminus` |
| DeepSeek V3.1 | 164K | $0.25/M | $0.95/M | `deepseek/deepseek-chat-v3.1` |
| DeepSeek Chat V3 | 164K | $0.26/M | $1.03/M | `deepseek/deepseek-chat` |

---

## R1 系列（推理）

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID |
|------|--------|----------|----------|---------------|
| DeepSeek R1 0528 | 164K | $0.50/M | $2.15/M | `deepseek/deepseek-r1-0528` |
| DeepSeek R1 | 64K | $0.70/M | $2.50/M | `deepseek/deepseek-r1` |
| DeepSeek R1 Distill Llama 70B | 8K | $0.80/M | $0.80/M | `deepseek/deepseek-r1-distill-llama-70b` |

---

## 选型指南

| 场景 | 推荐模型 |
|------|----------|
| 通用对话 / 编程 | DeepSeek V3.2 |
| 数学 / 逻辑推理 | DeepSeek R1 0528 |
| 低成本推理 | DeepSeek R1 Distill |

---

## 来源

- [OpenRouter Models API](https://openrouter.ai/models)
- [DeepSeek 官方](https://www.deepseek.com/)
