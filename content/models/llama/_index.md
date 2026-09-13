---
title: "Meta Llama 模型家族"
model: false
date: 2026-09-13T00:00:00Z
description: "Meta Llama 系列开源模型完整列表，包含 Llama 4/3.3/3.2/3.1 各型号的定价与上下文。"
---

## 系列概览

| 系列 | 定位 |
|------|------|
| **Llama 4** | 最新旗舰，1M 上下文 |
| **Llama 3.3** | 70B 上一代 |
| **Llama 3.2** | 多尺寸开源（1B/3B） |
| **Llama 3.1** | 经典开源（8B/70B） |

---

## Llama 4 系列

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID |
|------|--------|----------|----------|---------------|
| Llama 4 Maverick | 1M | $0.20/M | $0.70/M | `meta-llama/llama-4-maverick` |
| Llama 4 Scout | 1.3M | $0.10/M | $0.30/M | `meta-llama/llama-4-scout` |

---

## Llama 3.3 系列

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID |
|------|--------|----------|----------|---------------|
| Llama 3.3 70B | 131K | $0.10/M | $0.32/M | `meta-llama/llama-3.3-70b-instruct` |

---

## Llama 3.2 系列

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID |
|------|--------|----------|----------|---------------|
| Llama 3.2 3B | 131K | $0.05/M | $0.33/M | `meta-llama/llama-3.2-3b-instruct` |
| Llama 3.2 1B | 60K | $0.03/M | $0.20/M | `meta-llama/llama-3.2-1b-instruct` |

---

## Llama 3.1 系列

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID |
|------|--------|----------|----------|---------------|
| Llama 3.1 70B | 131K | $0.40/M | $0.40/M | `meta-llama/llama-3.1-70b-instruct` |
| Llama 3.1 8B | 131K | $0.05/M | $0.08/M | `meta-llama/llama-3.1-8b-instruct` |

---

## Llama Guard（内容安全）

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID |
|------|--------|----------|----------|---------------|
| Llama Guard 4 12B | 164K | $0.18/M | $0.18/M | `meta-llama/llama-guard-4-12b` |

---

## 选型指南

| 场景 | 推荐模型 |
|------|----------|
| 最强开源 | Llama 4 Maverick |
| 长上下文（1M+） | Llama 4 Scout |
| 低成本部署 | Llama 3.1 8B / 3.2 1B |
| 内容安全过滤 | Llama Guard 4 12B |

---

## 来源

- [OpenRouter Models API](https://openrouter.ai/models)
- [Meta Llama](https://llama.meta.com/)
