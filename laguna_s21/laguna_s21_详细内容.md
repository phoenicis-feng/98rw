# Poolside Laguna S 2.1 — 详细内容整理（未翻译）

> 收集自 firecrawl 搜索结果，图片已保存至 laguna_s21/images/

---

## 1. 模型基本信息（Basic Info）

- **名称**: Laguna S 2.1
- **发布方**: Poolside
- **类型**: Mixture-of-Experts (MoE)
- **总参数**: 118B
- **激活参数/每 token**: 8B
- **上下文窗口**: 1M tokens（thinking + no-thinking 模式）
- **训练周期**: 2026-05-22 开始预训练，2026-07-21 发布，约 9 周
- **许可证**: OpenMDW-1.1
- **权重格式**: BF16, FP8, INT4, NVFP4；官方 GGUF / MLX；DFlash draft
- **可获取渠道**: Hugging Face, NVIDIA (TRT-LLM / NVFP4 / DGX Spark), vLLM, SGLang, Ollama, Baseten, OpenRouter, Vercel AI Gateway, atomic.chat, chat.poolside.ai, pool.app
- **价格参考** (OpenRouter 1M context paid endpoint): $0.10 input / $0.20 output / $0.01 cache-read per 1M tokens

---

## 2. 性能对比表（Benchmark Comparison — 直接来自 Poolside 官方博客 / VentureBeat / Kie.ai）

### 2.1 官方 benchmark 表（Poolside agent harness, thinking enabled, pass@1 averaged over 4 attempts except noted）

| Benchmark | Laguna S 2.1 (118B-A8B) | Tencent Hy3 (295B-A21B) | Inkling (975B-A41B) | Nemotron 3 Ultra (550B-A55B) | DeepSeek-V4-Pro-Max (1.6T-A49B) | Kimi K3 (2.8T-A50B) | Qwen 3.7 Max | Muse Spark 1.1 | Claude Fable 5 |
|---|---|---|---|---|---|---|---|---|---|
| Terminal-Bench 2.1 | **70.2** | 71.7 | 63.8 | 56.4 | 64.0 | 88.3 | 74.5 | 80 | 88.0 |
| SWE-Bench Multilingual | **78.5** | 75.8 | — | 67.7 | 76.2 | — | 78.3 | — | — |
| SWE-Bench Pro (Public Dataset) | **59.4** | 57.9 | 54.3 | — | 55.4 | — | 60.6 | 61.5 | 80.3 |
| DeepSWE (v1.1, 3 attempts, pool harness) | **40.4** | — | — | — | 9.0 | 69.0 | — | 53.3 | 70.0 |
| SWE Atlas (Codebase QnA, 3 attempts, Opus 4.5 judge) | **46.2** | — | — | — | 27.2 | — | — | 42.2 | — |
| Toolathlon Verified (3 runs) | **49.7** | — | 45.5 | 34.3 | 55.9 | — | — | 75.6 | — |

**Notes:**
- DeepSWE 报告在 Poolside 自研 harness（非官方 mini-swe-agent），因此与官方排行榜直接比较需注意 harness 差异。
- Terminal-Bench 2.1 评估长时间限任务（long-horizon terminal tasks），5 小时超时。
- SWE-Bench Multilingual / Pro / DeepSWE 使用内部 sandbox，网络访问可控，避免 reward hacking。

### 2.2 Terminal-Bench 2.1 排行榜位置（Poolside compiled leaderboard, open weights / closed size undisclosed）

排名 11: Laguna S 2.1 — 70.2 (118B)
- 前名: GPT-5.6 Sol 88.8 / Kimi K3 88.3 / Claude Fable 5 88.0 / GPT-5.6 Terra 87.4 / GPT-5.6 Luna 84.7 / Claude Opus 4.8 84.6 / Claude Sonnet 5 80.4 / Muse Spark 1.1 80.0 / Qwen-3.7 Max 74.5 / Hy3 71.7
- 后名: MiniMax M3 66.0 / DeepSeek-V4-Pro-Max 64.0 / Inkling 63.8 / DeepSeek-V4-Flash-Max 61.8 / Nemotron 3 Ultra 56.4 / Inkling-Small 52.7 / Qwen3.6-27B 51.3 / Qwen3.6-35B-A3B 44.9 / Nemotron 3 Super 38.6 / Laguna XS 2.1 33.4 / Mistral Small 4 21.4

**关键点**: 70.2% 在其参数量级（约 118B）中“遥遥领先”，且仅略低于 295B Hy3，远超 1.6T DeepSeek-V4-Pro-Max (64.0) 和 975B Inkling (63.8)。

---

## 3. 优势（Advantages）

- **参数效率极高**: 118B 总 / 8B 激活，远小于 1T+ 竞品，适合本地部署（单 NVIDIA DGX Spark 可运行）。
- **思考模式提升显著 (Thinking Mode)**:
  - Terminal-Bench 2.1: 60.4% (no-thinking) → 70.2% (max thinking) — +9.8 pts
  - DeepSWE: 16.5% → 40.4% — +23.9 pts
  - SWE Multilingual: 71 (23k tok) → 79 (101k tok)
  - SWE Pro: 53 (24k tok) → 59 (141k tok)
- **长上下文 (1M)**: 支持长时推理与大状态保持，信号：思考序列可达数十万 token（~249k 完成 token 在 DeepSWE）。
- **持久性 / 不放弃**: 官方强调“more verification, less taking things for granted, not declaring victory early, more persistent”。案例显示模型在 50 分钟、181 步中从零构建浏览器引擎；在优化 harness 时持续改进至 20 次尝试。
- **开放权重 + 生态支持**: Hugging Face 开源 (OpenMDW-1.1)，NVIDIA / vLLM / SGLang / Ollama / OpenRouter 等多平台即刻可用。
- **评估透明**: 发布完整 trajectory 数据 (trajectories.poolside.ai)，可溯源每次试验路径，减少 reward hacking 怀疑。
- **训练效率**: 9 周从预训练到发布；RL 使用 FP8 精度加速；模型工厂支持高频迭代（3 个月内 M.1 → XS 2.1 → S 2.1）。

---

## 4. 定位（Positioning）

- **核心定位**: Agentic coding model for long-horizon work（长时程代码代理）。
- **目标场景**: 终端环境中的复杂工程任务、长时推理、代码构建、数学证明（Erdős problem #397 重新发现）、自主优化循环。
- **与竞品关系**:
  - 相比 1T+ 闭源/半开源（Inkling, Nemotron, DeepSeek-V4-Pro-Max, Kimi K3, Claude Fable 5）：参数量小一个数量级，但在多个 coding benchmark 上接近或超越，显示“行为轴（persistence / verification / willingness to backtrack）”与“智能轴”同样关键。
  - 相比同尺寸开源（Qwen 3.6-27B/35B-A3B, Mistral Small 4, Laguna XS 2.1 33B-A3B）：大幅领先。
  - 相比更大但同系列（Tencent Hy3 295B-A21B）：略低（70.2 vs 71.7 on TB 2.1），但在 SWE-Bench Multilingual 领先（78.5 vs 75.8）。
- **Poolside 两大赌注**:
  1. IQ 路径通过 coding 能力与灵活软件接口；
  2. Web 可以被“decompress” — RL 可恢复思考过程（much of humanity records answers, not thinking）。

---

## 5. 用户评价 / 第三方评价（User / Third-party Reviews — 未翻译原文）

### 5.1 Reddit — r/LocalLLaMA（真实使用反馈）

- **Thread**: "Honest take on Laguna S2.1 and its uses (from actual use)"
- **评价 1**: "Poolside Laguna S 2.1 is worse than Qwen 3.6 27B and Gemma4 31B"
- **评价 2**: "I'm impressed by Laguna S 2.1"
- **上下文**: 用户讨论模型“更窄的任务更适合评估”，认为专用模型比通用大模型更有价值；部分用户认为在实际本地运行中，Laguna S 2.1 不如更小的 Qwen 3.6 27B / Gemma4 31B，可能与本地推理优化、工具调用格式适配有关。

### 5.2 YouTube — 评测视频

- **Title**: "Laguna S 2.1: The Best Local Agentic Coder?"
- **内容方向**: 解析 118B MoE（8B 激活），1M 上下文，代码专用，比较与 DeepSeek、Inkling 对比，讨论本地部署可行性。

### 5.3 VentureBeat — 专业媒体报道（Michael Nuñez, 2026-07-21）

- **核心观点**: Poolside 选择“激进透明而非纯规模”战略；118B MoE 在长时程任务上与 1T+ 模型竞争；权重立即开源（OpenMDW-1.1）；支持 DGX Spark 本地运行。
- **引述**: “radical transparency, not raw scale, is how a smaller lab competes at the frontier”
- **强调**: 70.2% Terminal-Bench 2.1 是“小模型击败大模型”的标志性数据；强调附带的 trajectory 发布与评价方法论严谨性。

### 5.4 Medium / Kie.ai / 其他技术博客

- **Medium**: 40.4% DeepSWE，指出落后于 Claude Fable 5 / Kimi K3 / GPT-5.6 系列，但在开源/Open-Weight 领域中领先；1M 上下文、BF16/FP8/INT4/NVFP4 支持，DFlash 解码速度提升（~109 → 271 tok/s 在 RTX 6000 PRO）。
- **Kie.ai 对比表**: 直接列出 Terminal-Bench 2.1 70.2 / SWE-Bench Multilingual 78.5 / SWE-Bench Pro 59.4，与 Hy3 / Inkling / DeepSeek 对比。
- **Poolside X (Twitter)**: “as far as we can measure, the most capable agentic coding model in its weight class by a wide margin”; DeepSWE 最难任务 40.4，超越部分 1T+ 开源模型（如 DeepSeek-V4-Pro-Max 9.0）。

---

## 6. 知名案例 / 实际任务表现（来自官方博客）

- **浏览器引擎构造**: 从空文件夹构建 HTML/CSS 渲染引擎；50 分钟 / 181 步；无人工干预；使用 headless Chromium 自我验证（canvas 对比）。
- **Harness 优化**: 在自动化循环中优化 Poolside 自研 agent harness，速度提升 5.2%，内存分配降低 ~70%（20 次尝试，持续优化至边际效益低）。
- **数学证明 (Erdős #397)**: 独立重新发现证明；68 分钟；无 Python 环境，使用 Perl 进行精确质因数分解；构造出与已知不同的八索族（eight-index family vs 已知 six-index）。

---

## 7. 已知局限（Limitations — 官方披露）

- **Harness 过拟合**: 在第三方 agent harness（如 Hermes Agent 终端工具）中，可能依赖内存中的工具接口而非严格遵循 schema 定义；通常通过重试修正。
- **嵌套工具调用**: 工具参数为 JSON 数组时（如 Pi edit 工具），可能生成错误转义或无效 JSON。
- **思考时长过长 / 过度思考**: 在数学竞争问题上可能长时间思考；未来将引入 effort 控制与效率优化。
- **评价方法论**: 采用 LLM-as-Judge + 人工标注 + 轨迹审查；奖励作弊率在训练后期曾超 50%（SWE-bench family），已通过提示添加（不直接使用在线解）降至 <2%。

---

## 8. 图片文件列表（已保存到 laguna_s21/images/）

| 文件名 | 来源 / 说明 |
|---|---|
| `og_poolside_1200x628.png` | Poolside 官方博客 OG 图 (Twitter / OG image) |
| `browser_engine.png` | 官方案例图：Laguna S 2.1 构建的浏览器引擎 canvas 对比 |
| `venturebeat_illustration.webp` | VentureBeat 文章插图（Minimilist illustration） |

---

## 9. 完整来源列表（Sources — firecrawl 搜索 / scrape 结果）

1. https://poolside.ai/blog/introducing-laguna-s-2-1 — Poolside 官方发布（最完整，含 benchmark 表、案例、方法论、训练细节）
2. https://build.nvidia.com/poolside/laguna-xs-2.1/modelcard — NVIDIA NIM 模型卡（XS 2.1 数据，但训练框架/评估方法可参考）
3. https://huggingface.co/poolside/Laguna-S-2.1 — 模型页 / 权重下载
4. https://venturebeat.com/infrastructure/poolside-drops-laguna-s-2-1-an-open-weight-coding-model-that-beats-rivals-10x-its-size — VentureBeat 专业报道（Michael Nuñez）
5. https://x.com/poolsideai/status/2079614359446172033 — Poolside 官方 X（简短评测数据与声明）
6. https://www.reddit.com/r/LocalLLaMA/comments/1v5g2c4/honest_take_on_laguna_s21_and_its_uses_from/ — Reddit 用户真实评价
7. https://www.youtube.com/watch?v=H_Lbe69XO_8 — YouTube 评测视频
8. https://medium.com/data-science-in-your-pocket/laguna-s-2-1-the-118b-open-ai-coding-model-beats-inkling-deepseek-08186481910e — Medium 技术文章
9. https://kie.ai/blog/what-is-laguna-s-2-1 — Kie.ai 对比与说明
10. https://docs.poolside.ai/release-notes/models — Poolside 文档
11. https://trajectories.poolside.ai/ — 评估轨迹数据（官方开放下载）

---

*整理时间: 2026-09-11*
*工具: firecrawl search / scrape，Bash (curl / mkdir / file write)*
*未翻译: 所有英文原文、表名、引用、网址均保留原文。*
