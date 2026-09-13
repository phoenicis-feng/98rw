---
title: "cline也可以免费使用deepseek v4 Flash"
date: 2026-09-13
description: "Cline 官方免费模型详解。通过 Cline 和 ClinePass 两个提供商使用免费模型教程，包含 VSCodium 与 CLI 操作说明，以及用尽额度后的付费选项。"
tags: ["薅羊毛", "Cline", "VSCode", "DeepSeek"]
layout: "haoyang"
draft: false
---

## 工具介绍

**Cline** 是一款强大的 VSCode AI 编码插件（也支持 Cursor）。它提供 **Plan mode**（规划）与 **Act mode**（执行）双模式，允许 AI 直接读写本地文件、执行命令与调用工具。

Cline 还提供**免费模型**功能 —— 任何拥有 Cline 账号的用户都可以使用一定额度的免费模型，无需 API Key，无需付费。

> [!TIP]
> **DeepSeek V4-Flash** 就是 Cline 目前提供的免费模型之一，带 `-free` 后缀才是免费版本。

## 免费模型如何使用 {#how-it-works}

Cline 提供**免费模型活动**，让用户能在额度限制内免费试用精选模型。任何拥有 Cline 账号的用户都可以使用，额度用完后可切换到付费方案继续使用。

可用的免费模型可能因时而异，通常包含：

| 模型 | 类别 | 备注 |
|------|------|------|
| DeepSeek V4-Flash (-free) | 对话代码 | 带 `-free` 后缀才是免费版 |
| Claude 系列 | 对话代码 | 官方限时免费 |
| Gemini Flash | 多模态 | Google 性价比模型 |
| MiMo / Qwen | 国产模型 | 开源开放模型 |

### 用尽额度后怎么办

| 选项 | 适合 | 说明 |
|------|------|------|
| **ClinePass** ($9.99/月) | 频繁使用者 | 平价订阅，2-5x 速率限制 |
| **Cline (付费计费)** | 灵活使用者 | 按量计费，100+ 模型可用 |
| **自带 API Key** | 已有 Key 用户 | 配置 Anthropic/OpenAI 等 Key |

## 安装 {#install}

Cline 作为 VSCode 擴展安裝，简单快速：

{{< tabs >}}
  {{< tab name="VS Code" icon="mdi:vscode" >}}
  打开 VS Code，按 `Ctrl+Shift+X` 打开擴展面板，搜寻 `Cline`，點擊 **Install**。
  {{< /tab >}}
  {{< tab name="Cursor" icon="mdi:cursor" >}}
  在 Cursor 中搜尋 **Cline** 擴展並安裝。
  {{< /tab >}}
  {{< tab name="CLI" icon="mdi:terminal" >}}
  ```bash
  npm install -g @cline/cli
  cline
  ```
  {{< /tab >}}
{{< /tabs >}}

> [!NOTE]
> 安裝完成后，左側活動欄會出現 Cline 的圖示（🤖）。點擊即可打开。

## 运行 {#run}

OpenCode 有多种使用模式：

{{< steps >}}
  {{< step number="1" title="登录 Cline 账号" >}}
  首次使用 Cline 時，需要注册並登录 Cline 账号。前往 [Cline.dev](https://cline.dev) 注册。
  {{< /step >}}
  {{< step number="2" title="选择 API 提供商" >}}
  在 Cline 設定中，選擇 **API Provider**：
  - **Cline (usage-billing)**：選擇標示 **FREE** 的模型
  - **ClinePass**：在促销期间可使用免费模型
  {{< /step >}}
  {{< step number="3" title="IDE 擴張模式" >}}
  在 VSCode 擴展中：
  - 前往 **Settings** → **API Provider** → 選擇 **Cline** 或 **ClinePass**
  - 在模型選擇器中找到標示 **FREE** 的模型
  {{< /step >}}
  {{< step number="4" title="CLI 模式" >}}
  在 Cline CLI 中：
  - 輸入 `/settings`
  - 選擇 **Cline** 或 **ClinePass** 作為提供商
  - 瀏覽可用免費模型
  {{< /step >}}
  {{< step number="5" title="Plan Mode — 規劃階段" >}}
  輸入需求後，Cline 會分析並提出詳細的執行計劃，不會直接修改檔案。
  ```
  請幫我建立一個 React 專案，包含登入頁面與 API 串接
  ```
  {{< /step >}}
  {{< step number="6" title="Act Mode — 執行階段" >}}
  確認計劃後切換到 Act Mode，Cline 會自動執行建置、安裝、編寫與測試。
  {{< /step >}}
  {{< step number="7" title="檔案與命令整合" >}}
  Cline 可以直接在 VS Code 中創建、修改檔案，並執行終端命令，所有操作都在編輯器內完成。
  {{< /step >}}
  {{< step number="8" title="MCP 伺服器整合" >}}
  Cline 支援 MCP（Model Context Protocol）伺服器，讓你可以接入 GitHub、資料庫、雲端服務等工具。
  {{< /step >}}
  {{< step number="9" title="Bring Your Own Key" >}}
  若要使用付费模型或自己的 API Key，前往設定配置 Anthropic / OpenAI / OpenRouter 等 Key。
  {{< /step >}}
{{< /steps >}}

> [!NOTE]
> Cline 支援 **Oh My OpenCode** 插件生態，讓使用者能自訂指令、插件與規則。

## 免費模型 {#free-models}

Cline 的免費模型可以在**兩個提供商**中找到：

### Cline (usage-billing)

在 Cline (付费计费)提供商中，尋找在模型選擇器中標示 **FREE** 的模型。

- **VSCode 擴展**：前往設定 → **API Provider** → 選擇 **Cline**，找到標示 FREE 的模型。
- **CLI**：輸入 `/settings` → 選擇 **Cline**，瀏覽可用免費模型。

### ClinePass

在促銷期間，免費模型也可以通過 ClinePass 提供商使用。

- **VSCode 擴展**：前往設定 → **API Provider** → 選擇 **ClinePass**，登入即可。
- **CLI**：輸入 `/settings` → 選擇 **ClinePass**。

> [!WARNING]
> **重要注意事項**：
> 1. 免費模型用量**不支援透過 Cline API** 使用，僅限 VSCode 擴展與 CLI。
> 2. 免費模型用量**可能用於改進模型效能**，請避免用於敏感或公司代碼。

| 模型 | 提供商 | 免費額度 | 說明 |
|------|--------|----------|------|
| `deepseek-v4-flash-free` | Cline | 限時免費 | 帶 `-free` 後綴為免費版 |
| Claude 3.5/3.7 | ClinePass | 限額 | 促銷期間可用 |
| Gemini Flash | Cline | 限時 | Google 性價比模型 |
| MiMo V2.5 | Cline | 限時 | 小米開源模型 |
| Qwen3 Max | Cline | 限時 | 阿里最新模型 |

## 参考资料

- [Cline 官方文档 - 免費模型](https://docs.cline.bot/getting-started/free-models)
- [Cline 官方網站](https://cline.dev)
- [ClinePass 說明](https://docs.cline.bot/getting-started/clinepass)
