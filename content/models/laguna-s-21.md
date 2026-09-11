---
title: "Laguna S 2.1"
model: true
toc: true
description: "Poolside 开源 MoE 代码模型，118B 总参数 / 8B 激活，1M 上下文，Agentic Coding 专用。"
specs:
  category: "开源代码"
  vendor: "Poolside"
  released: "2026-07"
  context: "1M tokens"
  price_input: "$0.10 / 1M"
  price_output: "$0.20 / 1M"
  architecture: "MoE 118B-A8B"
  license: "OpenMDW-1.1"
scores:
  terminal_bench_2_1: 70.2
  swe_multilingual: 78.5
  swe_pro: 59.4
  deepswe: 40.4
  toolathlon: 49.7
hero:
  title: "Laguna S 2.1"
  subtitle: "118B MoE 开源代码模型 — 在参数效率维度击败 1T+ 对手的长时程代理。"
  highlights:
    - icon: "mdi:code-braces"
      label: "Agentic Coding"
    - icon: "mdi:brain"
      label: "Thinking Mode +9.8~+23.9 pts"
    - icon: "mdi:open-source-initiative"
      label: "OpenMDW-1.1 / Hugging Face"
---

## 一、模型概况

Poolside 于 2026-07-21 发布的 **Laguna S 2.1** 是一款 Mixture-of-Experts 开源代码模型：**118B 总参数，8B 每 token 激活，1M 上下文窗口**。训练从 2026-05-22 开始，约 9 周完成，首次采用 FP8 精度强化学习，重量格式覆盖 BF16 / FP8 / INT4 / NVFP4，提供官方 GGUF 与 MLX 转换及 DFlash 投机解码草稿模型。

![Poolside 官方发布配图](/laguna_s21/images/og_poolside_1200x628.png)

核心设计决策：
- **极低激活比（约 6.8%）**：推理成本接近 8B 稠密模型，同时保留 118B 级知识容量，可在单台 NVIDIA DGX Spark 本地运行；
- **1M 上下文与长思考协同**：思考序列可达数十万 token（DeepSWE 平均完成 token 约 249k），长上下文是支撑长时程推理的实际基础设施；
- **工业化发布节奏**：2026 年内 M.1（225B-A23B）→ XS 2.1（33B-A3B）→ S 2.1 三连发，反映 Model Factory 管线成熟。

## 二、性能评估：以小搏大的实证数据

### 2.1 六大基准横向对比（Poolside 官方评估，thinking 模式，pass@1 取多次均值）

| 基准测试 | Laguna S 2.1 | Tencent Hy3 | Inkling | DeepSeek-V4-Pro-Max | Kimi K3 | Claude Fable 5 |
|---|---|---|---|---|---|---|
| Terminal-Bench 2.1 | **70.2** | 71.7 | 63.8 | 64.0 | 88.3 | 88.0 |
| SWE-Bench Multilingual | **78.5** | 75.8 | — | 76.2 | — | — |
| SWE-Bench Pro (Public) | **59.4** | 57.9 | 54.3 | 55.4 | — | 80.3 |
| DeepSWE v1.1（3 次） | **40.4** | — | — | 9.0 | 69.0 | 70.0 |
| SWE Atlas | **46.2** | — | — | 27.2 | — | — |
| Toolathlon Verified | **49.7** | — | 45.5 | 55.9 | — | — |

**解读要点：**
- **Terminal-Bench 2.1（70.2%）为本次发布核心战绩**。在 Compiled Leaderboard 上位列第 11，但参数量仅为邻近模型的 1/5 至 1/24：压过 1.6T DeepSeek-V4-Pro-Max（64.0）、975B Inkling（63.8）与 550B Nemotron（56.4），仅以 1.5 分落后 295B Hy3（71.7）。
- **SWE-Bench Multilingual（78.5%）为同级最优**，超过 Hy3（75.8）与 DeepSeek-V4-Pro-Max（76.2）。
- **DeepSWE（40.4%）需谨慎解读**：Poolside 使用自研 harness 而非官方 mini-swe-agent，官方坦承可比性折扣；但在 1T+ 开源模型中 DeepSeek-V4-Pro-Max 仅 9.0%，Laguna 稳居第一梯队之下、腰部之上。
- **评估透明度**：全部评估轨迹公开（[trajectories.poolside.ai](https://trajectories.poolside.ai/)），并披露 reward hacking 对抗审查（训练后期曾超 50%，现已降至 <2%）。

### 2.2 思考模式边际收益

| 基准 | 非思考 | 思考 | 提升 | 完成 token（非思考 → 思考） |
|---|---|---|---|---|
| Terminal-Bench 2.1 | 60.4% | 70.2% | +9.8 pts | 80k → 129k |
| DeepSWE | 16.5% | 40.4% | +23.9 pts | 99k → 249k |
| SWE-Bench Multilingual | ~71 | ~79 | +8 pts | 23k → 101k |
| SWE-Bench Pro | ~53 | ~59 | +6 pts | 24k → 141k |

官方判定：这是其所训练模型中思考/非思考差异最大的一个。代价是 token 消耗数倍增长，用户需在成本与性能间权衡。

## 三、优势分析

### 3.1 参数效率与本地部署可行性

118B 总 / 8B 激活配合 NVFP4 / INT4 量化，使其成为可在单机运行的最强代码智能体之一。NVIDIA 完成全栈推理优化（TRT-LLM / NVFP4 / DGX Spark）；配合 DFlash 投机解码，单流解码速度在 RTX 6000 PRO 上可从约 109 tok/s 提升至 271 tok/s。

### 3.2 持久性与验证行为：被刻意训练的"工作风格"

Poolside 明确将能力提升归因于行为而非纯粹智能：**更多验证、更少想当然、不过早宣布胜利、更坚持不懈**。训练管线落点：更宽松 rollout 预算（更长超时、更多轮次）、全新沙箱基础设施（后台进程、选择性断网、缓存）、多 harness 混合 rollout（避免单一过拟合）。

### 3.3 评估透明度

发布全部最终评估轨迹、披露 LLM-as-Judge 校准流程、公开 harness 差异对可比性的影响——"激进透明"（VentureBeat 语）构成差异化信任资产。

## 四、定位研判

### 4.1 产品定位

**Agentic Coding for Long-Horizon Work**。目标场景：终端环境多步工程任务、长时推理、代码构建、数学证明（Erdős 问题 #397 重新发现）、自主优化循环。

### 4.2 竞争坐标

- **对上**：与 1T+ 前沿模型存在明显差距（TB 2.1 上 70.2 vs 88+），但在开源可部署模型中位居第一梯队。
- **对同级**：全面领先同尺寸开源（Qwen3.6-27B：51.3；Mistral Small 4：21.4），领先幅度近 20 分。
- **对自家产品线**：相对 XS 2.1（33B-A3B，33.4）实现量级跃升；预训练数据与 XS 2.1 完全一致，提升来自规模、训练代码修复与后训练配方（首次 FP8 RL）。

### 4.3 战略叙事

Poolside 押注两条路径：其一，通往智能的道路穿过编码能力与灵活软件接口；其二，互联网记录答案而非思考过程，RL 可"解压缩"出被省略的思考。S 2.1 是第一条路径的阶段性证据。

![VentureBeat 报道配图](/laguna_s21/images/venturebeat_illustration.webp)

## 五、标志性案例

### 5.1 从空目录构建浏览器引擎

50 分钟、181 步、零人工干预：parser → cascade → layout → renderer 完整管线。模型无视觉能力，遂自行启动 headless Chromium 读取 canvas 并数值比对截图——用间接手段完成自我验证闭环。

![浏览器引擎渲染对比：左为模型引擎，右为宿主浏览器](/laguna_s21/images/browser_engine.png)

### 5.2 优化自家 agent harness

20 轮自动化优化：发现流式 token 之 O(n²) 字符串拼接并改为缓冲区；通过记忆化与预分配消除冗余拷贝。成果：**墙钟时间 -5.19%，内存分配 -71.1%**。当速度优化边际收益降低后，模型自主转向内存维度继续推进，并通过 Go race detector / `go vet` 验证，排除以竞态换性能的可能。

### 5.3 独立重推 Erdős 问题 #397

1975 年提出，悬置逾 50 年，2026 年 1 月由 GPT-5.2 Pro 首次解决。S 2.1 在沙箱无 Python 条件下发现 Perl 可用，完成精确质因数分解、模式分析到构造性证明，得出与已知六指标族**结构不同**的八指标无限解族。知识截止 2025 年 11 月，可确认独立重发现而非复述。

## 六、用户评价与社区口碑

### 6.1 Reddit r/LocalLLaMA（多条主题汇总）

**正面：**
- **"I'm impressed by Laguna S 2.1"**：认可编码潜力，指出"推理循环造成主要问题"——过度思考在交互场景中成为负担。
- **"How are we feeling...?"**："几乎纯粹的编码模型，非常擅长；我不会拿它做任何其他事"——印证专用模型窄而深特征。
- 持续正反馈与快速修复公告（chat template / GGUF 兼容问题已修复）。

**负面：**
- **"Honest take on Laguna S2.1"**："不是我期望的 planner，推理风格过于深入，难以有效执行"；部分实测认为在本地运行中不如 Qwen 3.6 27B / Gemma 4 31B。
- **"Failed Basic Intelligence Litmus Test"**：基础常识测试失败，通用能力存在短板。
- **"PSA / update"**：早期部署问题已修复，提示本地工程细节对实测体验影响显著。

### 6.2 第三方媒体

- **VentureBeat（Michael Nuñez）**：定性为"开源权重编码模型击败十倍于己的对手"，强调透明度战略与轨迹公开。
- **Medium / Kie.ai**：确认 40.4% DeepSWE 在开源阵营领先，同时指出仍落后 Claude Fable 5 / Kimi K3 / GPT-5.6 系列；补充 DFlash 解码加速细节。
- **Poolside X**："as far as we can measure, the most capable agentic coding model in its weight class by a wide margin"；强调 DeepSWE 40.4% 超越多 1T+ 开源模型。

### 6.3 口碑综合研判

评价呈现**场景分化**：
1. **主战场（终端编码、agentic 工作流、充分思考预算）**：积极，与基准互证；
2. **通用推理、规划（planner）、低延迟交互**：负面集中，**过度思考**是最被诟病的一点，与官方自认"thinking duration 过长"完全吻合；
3. **负面体验可归因于部署层面**（chat template / GGUF 版本），而非模型本身，修复后已改善。

因此"worse than Qwen 3.6 27B"与"I'm impressed"并不矛盾：前者多来自通用场景或配置不当，后者来自正确配置下的编码主战场。

## 七、已知局限

1. **Harness 过拟合**：第三方 harness（如 Hermes Agent 终端工具）中可能依赖记忆接口而非严格遵循 schema；通常需 harness 拒绝后重试修正。
2. **嵌套工具调用缺陷**：JSON 数组参数（如 Pi edit 工具）可能生成错误转义或无效 JSON——XML 工具标签与 JSON 参数混合的薄弱点。
3. **过度思考**：尤其竞赛数学问题上思考序列过长；未来引入 low/medium/high 思考力度控制。
4. **通用智能短板**：非编码基础测试中表现不佳，专用化训练代价明确可见。

## 八、综合评价

**核心结论**：Laguna S 2.1 是 2026 年年中参数效率维度上最值得关注的开源编码模型，以 118B-A8B 体量在 TB 2.1 达 70.2%，位列含 1T+ 模型在内总榜第 11，SWE-Bench Multilingual 达同级最优 78.5%。其方法论贡献在于验证：**持久性、验证习惯与回溯意愿等"行为轴"可通过后训练系统性注入，与智能轴同等重要**。

**适用 / 不适用：**

| 适合 | 不适合 |
|---|---|
| 终端驱动长时程编码代理 | 通用对话与常识推理 |
| 本地/私有化自动化工程流水线 | 低延迟交互（过度思考） |
| 大规模代码库问答与修复 | 严格遵循第三方工具 schema（需重试兜底） |
| 数学/算法推导辅助 | 复杂 JSON 嵌套工具场景 |

**风险提示**：DeepSWE 等部分成绩基于自研 harness；思考模式高 token 消耗显著放大实际成本；第三方 harness 兼容性依赖 in-context 重试；选型前应以自身负载实测为准。

## 九、来源列表

1. [Poolside — Introducing Laguna S 2.1](https://poolside.ai/blog/introducing-laguna-s-2-1)
2. [Hugging Face — poolside/Laguna-S-2.1](https://huggingface.co/poolside/Laguna-S-2.1)
3. [VentureBeat — Poolside drops Laguna S 2.1](https://venturebeat.com/infrastructure/poolside-drops-laguna-s-2-1-an-open-weight-coding-model-that-beats-rivals-10x-its-size)
4. [Reddit — Honest take on Laguna S2.1](https://www.reddit.com/r/LocalLLaMA/comments/1v5g2c4/honest_take_on_laguna_s21_and_its_uses_from/)
5. [Reddit — I'm impressed by Laguna S 2.1](https://www.reddit.com/r/LocalLLaMA/comments/1v5qb9b/im_impressed_by_laguna_s_21/)
6. [Reddit — How are we feeling...?](https://www.reddit.com/r/LocalLLaMA/comments/1v3wyre/how_are_we_feeling_about_poolsides_laguna_s_21/)
7. [Reddit — Failed Basic Intelligence Litmus Test](https://www.reddit.com/r/LocalLLaMA/comments/1v3kvgz/lagunas21_failed_basic_intelligence_litmus_test/)
8. [Reddit — Updated / PSA](https://www.reddit.com/r/LocalLLaMA/comments/1v5ahaz/laguna_s21_updated_2_hours_ago_a_post_to_show/)
9. [YouTube — Laguna S 2.1: The Best Local Agentic Coder?](https://www.youtube.com/watch?v=H_Lbe69XO_8)
10. [Medium — Laguna S 2.1 beats Inkling, DeepSeek](https://medium.com/data-science-in-your-pocket/laguna-s-2-1-the-118b-open-ai-coding-model-beats-inkling-deepseek-08186481910e)
11. [Kie.ai — What Is Laguna S 2.1?](https://kie.ai/blog/what-is-laguna-s-2-1)
12. [Poolside X — 发布声明](https://x.com/poolsideai/status/2079614359446172033)
13. [NVIDIA NIM — Laguna XS 2.1 Model Card](https://build.nvidia.com/poolside/laguna-xs-2.1/modelcard)
14. [Poolside Docs — release notes](https://docs.poolside.ai/release-notes/models)
15. [trajectories.poolside.ai](https://trajectories.poolside.ai/)
