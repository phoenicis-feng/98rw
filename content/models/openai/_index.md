---
title: "OpenAI 模型家族"
model: false
date: 2026-09-13T00:00:00Z
description: "OpenAI 系列模型完整列表，包含 GPT-6/5/4、o1/o3/o4 推理系列、gpt-oss 开源模型、音频与图像模型的定价、上下文与发布时间。"
---

## 系列概览

OpenAI 模型按能力与定位分为以下系列：

| 系列 | 定位 | 模型数量 |
|------|------|----------|
| **GPT-6** | 最新旗舰（Astra），1M 上下文 | 2 |
| **GPT-5** | 多代演进，Sol/Luna/Terra 子系列 | 20+ |
| **GPT-4** | 上一代主流，128K-1M 上下文 | 10+ |
| **GPT-3.5** | 经典入门，高性价比 | 3 |
| **o 系列** | 推理专用（o1/o3/o4-mini） | 10+ |
| **gpt-oss** | 开源权重模型 | 3 |
| **音频/图像** | 多模态专用 | 5+ |

---

## GPT-6 系列（最新旗舰）

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID |
|------|--------|----------|----------|---------------|
| GPT-6 Astra | 1.05M | $10.00/M | $50.00/M | `openai/gpt-6-astra` |
| GPT-6 Astra Pro | 1.05M | $10.00/M | $50.00/M | `openai/gpt-6-astra-pro` |

**核心能力**：最新旗舰，1M+ 上下文窗口，高级推理、智能体任务、科学研究。

---

## GPT-5 系列（主力）

### GPT-5.6 子系列（1M 上下文）

| 型号 | 输入价格 | 输出价格 | OpenRouter ID |
|------|----------|----------|---------------|
| GPT-5.6 Sol | $2.00/M | $10.00/M | `openai/gpt-5.6-sol` |
| GPT-5.6 Sol Pro | $2.00/M | $10.00/M | `openai/gpt-5.6-sol-pro` |
| GPT-5.6 Luna | $0.20/M | $1.20/M | `openai/gpt-5.6-luna` |
| GPT-5.6 Luna Pro | $0.20/M | $1.20/M | `openai/gpt-5.6-luna-pro` |
| GPT-5.6 Terra | $2.00/M | $12.00/M | `openai/gpt-5.6-terra` |
| GPT-5.6 Terra Pro | $2.00/M | $12.00/M | `openai/gpt-5.6-terra-pro` |

### GPT-5.5 子系列（1M 上下文）

| 型号 | 输入价格 | 输出价格 | OpenRouter ID |
|------|----------|----------|---------------|
| GPT-5.5 | $5.00/M | $30.00/M | `openai/gpt-5.5` |
| GPT-5.5 Pro | $30.00/M | $180.00/M | `openai/gpt-5.5-pro` |

### GPT-5.2 子系列（1M 上下文）

| 型号 | 输入价格 | 输出价格 | OpenRouter ID |
|------|----------|----------|---------------|
| GPT-5.2 | $1.75/M | $14.00/M | `openai/gpt-5.2` |
| GPT-5.2 Chat | $1.75/M | $14.00/M | `openai/gpt-5.2-chat` |
| GPT-5.2 Pro | $15.00/M | $120.00/M | `openai/gpt-5.2-pro` |

### GPT-5.1 子系列（400K 上下文）

| 型号 | 输入价格 | 输出价格 | OpenRouter ID |
|------|----------|----------|---------------|
| GPT-5.1 | $1.25/M | $10.00/M | `openai/gpt-5.1` |
| GPT-5.1 Codex | $1.25/M | $10.00/M | `openai/gpt-5.1-codex` |
| GPT-5.1 Codex Max | $1.25/M | $10.00/M | `openai/gpt-5.1-codex-max` |
| GPT-5.1 Codex Mini | $0.25/M | $2.00/M | `openai/gpt-5.1-codex-mini` |

### GPT-5 基础版（400K 上下文）

| 型号 | 输入价格 | 输出价格 | OpenRouter ID |
|------|----------|----------|---------------|
| GPT-5 | $1.25/M | $10.00/M | `openai/gpt-5` |
| GPT-5 Pro | $15.00/M | $120.00/M | `openai/gpt-5-pro` |
| GPT-5 Mini | $0.25/M | $2.00/M | `openai/gpt-5-mini` |
| GPT-5 Nano | $0.05/M | $0.40/M | `openai/gpt-5-nano` |

---

## GPT-4 系列

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID |
|------|--------|----------|----------|---------------|
| GPT-4.1 | 1M | $2.00/M | $8.00/M | `openai/gpt-4.1` |
| GPT-4.1 Mini | 1M | $0.40/M | $1.60/M | `openai/gpt-4.1-mini` |
| GPT-4.1 Nano | 1M | $0.10/M | $0.40/M | `openai/gpt-4.1-nano` |
| GPT-4o | 128K | $2.50/M | $10.00/M | `openai/gpt-4o` |
| GPT-4o Mini | 128K | $0.15/M | $0.60/M | `openai/gpt-4o-mini` |
| GPT-4 Turbo | 128K | $10.00/M | $30.00/M | `openai/gpt-4-turbo` |
| GPT-4 | 8K | $30.00/M | $60.00/M | `openai/gpt-4` |

---

## GPT-3.5 系列

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID |
|------|--------|----------|----------|---------------|
| GPT-3.5 Turbo | 16K | $0.50/M | $1.50/M | `openai/gpt-3.5-turbo` |
| GPT-3.5 Turbo 16K | 16K | $3.00/M | $4.00/M | `openai/gpt-3.5-turbo-16k` |
| GPT-3.5 Turbo Instruct | 4K | $1.50/M | $2.00/M | `openai/gpt-3.5-turbo-instruct` |

---

## o 系列（推理专用）

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID |
|------|--------|----------|----------|---------------|
| o1 | 200K | $15.00/M | $60.00/M | `openai/o1` |
| o1 Pro | 200K | $150.00/M | $600.00/M | `openai/o1-pro` |
| o3 | 200K | $2.00/M | $8.00/M | `openai/o3` |
| o3 Pro | 200K | $20.00/M | $80.00/M | `openai/o3-pro` |
| o3 Mini | 200K | $1.10/M | $4.40/M | `openai/o3-mini` |
| o3 Mini High | 200K | $1.10/M | $4.40/M | `openai/o3-mini-high` |
| o4 Mini | 200K | $1.10/M | $4.40/M | `openai/o4-mini` |
| o4 Mini High | 200K | $1.10/M | $4.40/M | `openai/o4-mini-high` |

---

## gpt-oss 系列（开源）

| 型号 | 上下文 | 输入价格 | 输出价格 | OpenRouter ID |
|------|--------|----------|----------|---------------|
| gpt-oss-120b | 131K | $0.037/M | $0.17/M | `openai/gpt-oss-120b` |
| gpt-oss-20b | 131K | $0.03/M | $0.13/M | `openai/gpt-oss-20b` |
| gpt-oss-safeguard-20b | 131K | $0.075/M | $0.30/M | `openai/gpt-oss-safeguard-20b` |

---

## 音频与图像

| 型号 | 类型 | 输入价格 | 输出价格 | OpenRouter ID |
|------|------|----------|----------|---------------|
| GPT Audio | 音频 | $2.50/M | $10.00/M | `openai/gpt-audio` |
| GPT Audio Mini | 音频 | $0.60/M | $2.40/M | `openai/gpt-audio-mini` |
| GPT-5 Image | 图像 | $10.00/M | $10.00/M | `openai/gpt-5-image` |
| GPT-5 Image Mini | 图像 | $2.50/M | $2.00/M | `openai/gpt-5-image-mini` |

---

## 选型指南

| 场景 | 推荐模型 |
|------|----------|
| 最强推理 / 科学研究 | GPT-6 Astra Pro |
| 编程 / 智能体 | GPT-5.2 Pro / GPT-5.6 Sol Pro |
| 日常对话 | GPT-5.1 / GPT-5.6 Luna |
| 高并发 / 低成本 | GPT-5 Nano / GPT-4.1 Nano |
| 数学 / 逻辑推理 | o4 Mini High / o3 |
| 开源部署 | gpt-oss-20b / gpt-oss-120b |

---

## 来源

- [OpenRouter Models API](https://openrouter.ai/models)
- [OpenAI 官方文档](https://platform.openai.com/docs/models)
