---
title: "用 opencode 白嫖 deepseek v4 Flash"
date: 2026-09-13
description: "OpenCode 开源 AI 编码助手，3 步接入 DeepSeek V4-Flash 免费模型，无需 API Key。支持 MiMo、Qwen3.7 Max 等限免模型。"
tags: ["薅羊毛", "OpenCode", "DeepSeek", "Flash"]
layout: "haoyang"
draft: false
---

## 工具介绍

**OpenCode** 是一款开源的 AI 编码助手，用 Go 语言编写，MIT 协议，支持终端 TUI、VSCode 扩展与 Web 界面。GitHub has 16 万+ Star，月活开发者 750 万。

与 Claude Code 类似，OpenCode 支持通过 API 密钥使用各大语言模型，但更厉害的是——**它内置了多个免费模型，无需 API Key 即可直接使用**！

### 内置免费模型

OpenCode 目前限免名单中的免费模型：

| 模型名称 | 厂商 | 备注 |
|----------|------|------|
| `opencode/deepseek-v4-flash-free` | DeepSeek | 注意带 `-free` 后缀才是免费版 |
| MiMo V2.5 | 小米 | 3090B 参数的 MoE 模型 |
| Qwen3.7 Max | 阿里 | 阿里最新最大参数模型 |
| Gemini 3.5 Flash | Google | Google 性价比型模型 |

> [!NOTE]
> 模型 ID 带 `-free` 后缀的才是完全免费版本，额度无限但可能用于改进模型。

## 安装 {#install}

OpenCode 支持多种安装方式，任选其一即可：

{{< tabs >}}
  {{< tab name="npm（推荐）" icon="simple-icons:npm" >}}
  ```bash
  npm install -g @open-code-ai/opencode
  ```
  {{< /tab >}}
  {{< tab name="brew（macOS）" icon="simple-icons:apple" >}}
  ```bash
  brew install opencode
  ```
  {{< /tab >}}
  {{< tab name="bun" icon="simple-icons:bun" >}}
  ```bash
  bun install -g opencode
  ```
  {{< /tab >}}
  {{< tab name="npx 临时运行" icon="simple-icons:node" >}}
  ```bash
  npx @open-code-ai/opencode
  ```
  {{< /tab >}}
  {{< tab name="Docker" icon="simple-icons:docker" >}}
  ```bash
  docker run -it --rm -v $(pwd):/workspace ghcr.io/anomalyco/opencode
  ```
  {{< /tab >}}
{{< /tabs >}}

验证安装：

```bash
opencode --version
```

## 运行 {#run}

OpenCode 提供多种使用模式，以下是白嫖 DeepSeek V4-Flash 的 3 步快速接入：

{{< steps >}}
  {{< step number="1" title="启动 OpenCode" >}}
  在任意项目目录下执行 `opencode`，进入交互式终端界面。
  ```bash
  cd your-project
  opencode
  ```
  {{< /step >}}
  {{< step number="2" title="选择免费模型" >}}
  按 `Ctrl/Cmd + M` 打开模型列表，找到 `opencode/deepseek-v4-flash-free`，注意**带 `-free` 后缀**的才是免费版，回车确认。
  {{< /step >}}
  {{< step number="3" title="开始使用" >}}
  用自然语言下指令即可，OpenCode 会自动调用 DeepSeek V4-Flash：
  ```
  帮我重构这个 React 组件，使用 TypeScript 和 Tailwind CSS
  ```
  {{< /step >}}
  {{< step number="4" title="非交互模式" >}}
  在 CI/CD 或脚本中使用 `-p` 参数：
  ```bash
  opencode -p "为我的 Express 项目添加一个 /health 路由"
  ```
  {{< /step >}}
  {{< step number="5" title="IDE 扩展模式" >}}
  OpenCode 也支持 VSCode 插件模式。启动 VS Code 后按 `Cmd+Esc`（Mac）或 `Ctrl+Esc`（Win/Linux）快速打开 OpenCode 面板。
  {{< /step >}}
  {{< step number="6" title="Claude Code 迁移" >}}
  OpenCode 会自动读取 Claude Code 的 `CLAUDE.md` 和 `Skills` 文件夹，从 Claude Code 切换过来几乎无缝。
  {{< /step >}}
  {{< step number="7" title="连接自定义 API" >}}
  若要使用付费模型，前往 [OpenCode 设置文档](https://opencode.ai/docs/zh-cn/) 配置 API 密钥。
  {{< /step >}}
  {{< step number="8" title="OpenCode Zen 账号" >}}
  注册 OpenCode Zen 账号即可使用官方精选模型网关，无需第三方 Key。
  {{< /step >}}
  {{< step number="9" title="Go 套餐（进阶）" >}}
  首月 5 美元，之后每月 10 美元，支持支付宝，国内直连。Go 的 API Key 不绑定 OpenCode，使用 OpenAI 兼容格式，可接入各种工具。
  {{< /step >}}
{{< /steps >}}

> [!NOTE]
> OpenCode 支持 **Oh My OpenCode** 插件生态，让用户能自订指令、插件与规则，类似于 Oh My Zsh 的扩展机制。

## 免费模型 {#free-models}

OpenCode 预设内置多个免费模型，以下是主要选项：

| 模型 | 提供商 | 免费额度 | 说明 |
|------|--------|----------|------|
| `opencode/deepseek-v4-flash-free` | DeepSeek | 无限 | 带 `-free` 后缀才是免费版 |
| `opencode/mimo-v2.5` | 小米 | 无限 | 3090B 参数 MoE 模型 |
| `opencode/qwen3-7b-max` | 阿里 | 无限 | 阿里最新最大参数 |
| `opencode/gemini-3.5-flash` | Google | 无限 | Google 性价比模型 |
| `ollama` 本地模型 | Ollama | 100% 本地 | 下载 Llama 3、Qwen 等开源模型 |

> [OpenRouter 免费模型列表](/openrouter/?free=1) — 400+ 免费模型统一接入。

> [!WARNING]
> **隐私风险提示**：DeepSeek V4-Flash Free 免费期间收集的数据可能被用于改进模型。学习、开源、个人项目随便薅；公司代码、客户数据走官方 API 或 Go 套餐（Go 有零保留政策，数据不用于训练）。

## 参考资料

- [OpenCode 官方文档](https://opencode.ai/docs/zh-cn/)
- [OpenCode GitHub](https://github.com/sst/opencode)
