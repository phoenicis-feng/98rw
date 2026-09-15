# MEMORY — jumohub 项目要点

## 国产模型榜（2026-09 新增）
- `scripts/build_benchlm_data.py` 顶部 `DOMESTIC_VENDORS` 白名单维护国产厂商（匹配 creatorZh），新增国产厂商时先补这里
- 生成两个榜：`domestic`（国产模型榜，综合评分）、`domestic_value`（国产性价比榜）
- 国产性价比榜为平衡算法：价格分×70%（输出价格对数归一化）+ 评分分×30%（min-max 归一化），0~100 平衡分；免费模型不参与；权重在 `build_benchlm_data.py` 的 `VALUE_PRICE_WEIGHT`/`VALUE_SCORE_WEIGHT` 调整
- 这两个榜的页面自动内嵌 ECharts 横向条形图（Top 10，柱子可点击跳模型详情页），配置在 `scripts/generate_leaderboard_pages.py` 的 `ECHARTS_BOARDS`
- 首页「综合/低价/免费」面板之后追加「国产模型榜/国产性价比榜」两个面板

## 数据管线（从原始数据到站点构建）

### 第 1 步：生成主数据文件
```bash
python3 scripts/build_benchlm_data.py
```
- 输入：`benchlm-data/*.json`（benchlm.ai 导出缓存；`--refresh` 重新联网下载）
- 厂商模型数 < 5 整体剔除（`--min-vendor-models` 默认 5）
- 输出：`data/jumo_models.json`（模型主表）、`data/jumo_leaderboards.json`（榜单数据）、`data/jumo_benchmarks.json`

### 第 2 步：生成模型详情页
```bash
python3 scripts/generate_model_pages.py --all --force
```
- 输入：`data/jumo_models.json` → 输出：`content/models/<slug>/index.md`（356 个）
- specs 含：vendor、series、category、context、released、price_input/output/cached、price_notes（计费规则徽章）、pricing_source（价格溯源）、open_note（开源计划）、free_note（免费口径）、speed、ttft、scores（综合/已验证/五维度）、use_cases、best_use
- note 结构化字段由 `build_benchlm_data.py` 的 `extract_pricing_note_facts()` 从 pricing.note 英文原文正则提取（rules/source_line/open_note/free_text），溯源日期优先取 Observed 观察日
- **自动清理孤儿页面**：数据里已不存在的模型目录默认删除（`--no-prune` 可关闭），所以更新数据一律用 `--all`（可不带 --force）
- 场景规则：维度评分 ≥ 80 打标，兜底「通用对话」

### 第 3 步：生成排行榜页面
```bash
python3 scripts/generate_leaderboard_pages.py --all --force
```
- 输入：`data/jumo_leaderboards.json` → 输出：`content/leaderboards/<key>.md`（15 个，模型名链接详情页）
- 影响范围：各榜单详情页 + /leaderboards/ 索引页面板 + 首页三个榜单面板（综合/低价/免费）

### 第 4 步：构建站点
```bash
hugo
```
各页面数据依赖（第 4 步自动完成所有页面的"重新生成"，无需额外脚本）：
- /models/ 模型库、/compare/ 对比页、/recommendations/ 应用场景、首页「最新排行榜」→ 依赖第 2 步
- 首页「综合/低价/免费」面板、/leaderboards/ 全部 → 依赖第 3 步
- /models/<slug>/ 详情页 → md 本身（第 2 步）

## 注意事项
- `data/`、`*.json` 不提交 git；`scripts/` 下的管线脚本已用 `git add -f` 强制入库（.gitignore 的 `scripts/` 规则仍在，新增脚本需同样 `-f`）；页面只依赖 content/ 的 md → 改数据必须跑完 1→2→3→4，顺序不能颠倒，第 2/3 步 `--force` 不能省
- /compare/ 支持 `/compare/?model=<slug>` 预选模型 A
- 已废弃脚本：`fetch_hf_top_vendors.py`、`regroup_series.py`、`build_vendor_series.py`（不要再用）

## IndexNow 增量提交
- `python3 scripts/index-submit/indexnow_submit.py`：默认增量（sitemap lastmod 与 `.pipeline_tmp/indexnow_state.json` 基线对比，只提交有变化的 URL）
- `--full` 全量（仅新站首次/整站改版）；`--dry-run` 预览；传路径（如 `/leaderboards/domestic/`）手动指定提交
- 验证 key 统一用 `4380e811...`，key 文件在 `static/4380e811ce2749c2a1b705f74803ab60.txt`（此前 content/、static/ 各有一份重复已清理）
- **站点 CF 防护会拦默认 Python-urllib UA（403）**，脚本所有请求必须带 User-Agent 头
- 提交成功才更新基线状态文件；状态文件已 gitignore，换机器首次运行会自动重建基线

## 其他约定
- remote URL 含 GitHub token 明文，建议改用 SSH/credential manager
