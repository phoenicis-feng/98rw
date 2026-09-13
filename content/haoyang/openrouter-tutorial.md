---
title: "用 OpenRouter 接入多种免费模型"
date: "2026-09-13"
description: "OpenRouter 统一 LLM API 平台教程。整合注册流程、API Key 获取、免费模型列表（ Nemotron 3 / Gemma 4 / gpt-oss ）、速率限制说明，以及与 Python/curl 的对接示例。"
tags: ["薅羊毛", "OpenRouter", "API", "LLM", "免费模型"]
layout: "haoyang"
draft: false
---

**OpenRouter** 是一个统一的 LLM API 平台，支持 400+ 个来自 OpenAI、Anthropic、Google、Meta、DeepSeek 等厂商的模型。注册即可获得 API Key，许多模型有免费试用额度。

NVIDIA Nemotron 3 Ultra（5500 亿参数）、Google Gemma 4、OpenAI gpt-oss 等真正有能力的开放模型，都通过 OpenRouter 提供完全免费的 API 接入。

## 核心优势

- **统一 API**：一个 API Key 访问 400+ 模型
- **即时切换**：可在不同模型间无缝切换
- **免费模型**：许多模型完全免费（:free 后缀）
- **标准接口**：兼容 OpenAI API 格式

## 注册与设置

OpenRouter 无需安装，直接在网页上操作：

1. 前往 [openrouter.ai](https://openrouter.ai)，使用 Google / GitHub / Email 任一方式注册。
2. 点击头像 → API Keys → Create Key，命名后即可获取金钥。
3. 前往 [Free Models 页面](https://openrouter.ai/models?fmt=table&cost=free)，查看所有免费模型。
4. 点击左侧 Activity 菜单，可查看当前用量与余额。

## 快速测试

**curl：**

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/llama-3.1-70b-instruct:free",
    "messages": [
      {"role": "user", "content": "你好，请简单介绍一下 OpenRouter。"}
    ]
  }'
```

**Python：**

```python
import requests

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json",
    },
    json={
        "model": "microsoft/phi-3-mini-4k-instruct:free",
        "messages": [
            {"role": "user", "content": "甚么是 AI 编码助手？"}
        ],
    },
)

print(response.json()["choices"][0]["message"]["content"])
```

**与 Cline / OpenCode 整合：**

在 Cline 或 OpenCode 的设定中填入 OpenRouter 的 API Key，即可使用所有支援的模型。

```jsonc
// Cline / OpenCode 设定
{
  "provider": "openrouter",
  "apiKey": "sk-or-vv你的OpenRouter金鉴",
  "baseURL": "https://openrouter.ai/api/v1"
}
```

## 免费模型的速率限制

| 账号情况 | 免费额度 |
| --- | --- |
| 从未购买积分（不足 10 美元） | 每天约 50 次请求 |
| 曾购买至少 10 美元积分 | 每天约 1,000 次请求 |
| 所有人 | 免费模型每分钟约 20 次请求 |

> 一次性充值 10 美元（不是订阅，这笔钱会留在余额中，也可用于付费模型）大约可将每日免费额度提高二十倍。每天 1,000 次请求已经远超绝大多数人的聊天需求，这是 AI 领域最划算的交易之一。

限额每日重置且可能变化，请以实时页面为准。

## 值得花时间的免费模型

名单会轮换，依赖某个端点前请始终核对实时的 [Free Models 合集](/openrouter/?free=1)。2026 年 8 月的亮点：

| 模型 | 厂商 | 特点 | 适合场景 |
| --- | --- | --- | --- |
| **Nemotron 3 Ultra** | NVIDIA | 5500 亿参数推理模型，100 万 token 上下文 | 分析、数学、多步骤问题 |
| **Nemotron 3 Nano 30B** | NVIDIA | 推理深度换速度，日常默认 | 日常对话、快速问答 |
| **Gemma 4**（26B/31B） | Google | 全能选手，262K 上下文，多语言强 | 总结、写作、翻译、日常聊天 |
| **gpt-oss 20B** | OpenAI | 体积小速度快，代码能力出色 | 编程问题、技术回答 |
| `meta-llama/llama-3.1-70b-instruct:free` | Meta | 70B 开源模型，品质不错 | 通用任务 |
| `microsoft/phi-3-mini-4k-instruct:free` | Microsoft | 小型高效，速度快 | 轻量任务 |
| `openrouter/free` | 系统随机 | 随机分配一个免费模型 | 尝鲜 |

新模型刚推出时，实验室往往免费上线，免费档有时能让你体验到当月最有意思的模型。反过来，它们也可能不声不响地离开。建议每月复查列表。

## 免费与付费：诚实的比较

| 维度 | 免费模型 | 付费模型（Claude、GPT、Gemini） |
| --- | --- | --- |
| 日常质量 | 对多数任务都很优秀 | 优秀 |
| 最难任务 | 不错，偶有失手 | 仍是标杆 |
| 速度 | 有波动，高峰期较慢 | 快而稳定 |
| 上下文长度 | 免费端点通常较短 | 模型原有的完整上下文窗口 |
| 隐私 | 部分端点可能记录数据或用于训练 | 可选不训练方案 |
| 成本 | $0 | 每次对话几美分 |

最佳策略不是全免费或全付费，而是默认免费，按需付费。摘要、草稿和快速问题用免费模型；合同分析、重要文稿、棘手调试则花几美分用 Claude 或 GPT。这样即使高强度使用一个月，也可能不到 5 美元。

## 在浏览器中使用免费模型

OpenRouter 自带的聊天界面适合试用，但真正方便的是在你本来就在工作的地方使用，浏览器中的任意网页。

1. 在 openrouter.ai → Keys → Create Key 创建 API 密钥。
2. 安装 [SurfMind](https://surfmind.ai/)，为每个网页添加 AI 侧栏，用你的专属密钥连接。
3. 在设置中粘贴密钥，密钥私密保存于浏览器本地。
4. 在下拉菜单选择免费模型（搜索 "free" 即可查看全部）。

现在你可以在任何网页上使用免费 AI：选中文本提问、总结长文或起草回复。任务值得使用高级模型时，也只需在同一菜单中切换。

## 用好免费档位的技巧

- **在不同模型系列之间分配工作**：一个端点缓慢或过载时，另一个模型系列可能马上答复。
- **让提示词保持聚焦**：免费端点上下文较短，直接询问当前页面或按章节处理，而非粘贴整篇文档。
- **不要粘贴秘密**：检查数据政策，机密内容应使用不训练数据的付费端点或本地模型。
- **尽早充值 10 美元**：每日额度提高二十倍，同时能支付偶尔的高级请求。
- **每月复查列表**：新模型经常免费出现，花两分钟浏览筛选条件就可能找到当月宝藏。

## 参考资料

- [OpenRouter 官方文档](https://openrouter.ai/docs/quickstart)
- [OpenRouter 免费模型合集](https://openrouter.ai/collections/free-models)
- [SurfMind 浏览器 AI 侧栏](https://surfmind.ai/)
- [2026 年最佳免费 OpenRouter 模型](https://surfmind.ai/zh/blog/best-free-openrouter-models)
