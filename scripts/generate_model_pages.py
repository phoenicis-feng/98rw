#!/usr/bin/env python3
"""Generate Hugo model pages from jumo_models.json (BenchLM merged data).

Creates content/models/<slug>/_index.md for every model in the merged data.
Front matter matches layouts/models/single.html specs fields.

Usage:
  python3 scripts/generate_model_pages.py --slug claude-opus-5   # one page
  python3 scripts/generate_model_pages.py --all                  # all models
  python3 scripts/generate_model_pages.py --all --force          # overwrite existing
"""

import argparse
import json
import re
import os
import shutil
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "jumo_models.json")
DATA_TS = ""


def data_ts():
    """数据构建时间戳（jumo_models.json 的 metadata.generatedAt）。

    写入 front matter 的 date 字段后，Hugo 会自动带进 sitemap <lastmod>，
    供搜索引擎与增量推送脚本判断页面新旧。
    """
    global DATA_TS
    if not DATA_TS:
        try:
            with open(DATA_FILE, encoding="utf-8") as fh:
                DATA_TS = (json.load(fh).get("metadata") or {}).get("generatedAt", "")
        except (OSError, ValueError):
            DATA_TS = ""
    return DATA_TS
MODELS_DIR = os.path.join(BASE_DIR, "content", "models")

CATEGORY_ZH = {
    "agentic": "智能体",
    "coding": "编程",
    "reasoning": "推理",
    "multimodalGrounded": "多模态",
    "knowledge": "知识",
    "multilingual": "多语言",
    "instructionFollowing": "指令遵循",
    "math": "数学",
}

# benchmark key -> (中文名, 说明)
BENCH_ZH = {
    "frontierBench": ("FrontierBench 综合任务", "前沿综合任务执行能力"),
    "browseComp": ("BrowseComp 网页浏览", "需要多步检索的网页浏览任务"),
    "hleWithTools": ("HLE 带工具", "「人类终极考试」专家级难题（允许工具）"),
    "hleWithToolsNoSearch": ("HLE 无搜索", "「人类终极考试」专家级难题（禁用搜索）"),
    "deepSearchQa": ("DeepSearchQA 深度检索", "深度检索问答"),
    "draco": ("Draco 代码修复", "真实仓库级代码修复"),
    "multiAgentBrowseCompPrerelease": ("多智能体浏览", "多智能体协作网页浏览"),
    "osWorld2": ("OSWorld 桌面操作", "真实桌面环境自动化操作"),
    "mcpAtlas": ("MCP Atlas 工具调用", "MCP 工具调用评测"),
    "mcpAtlasClaimCoverage": ("MCP Atlas 声明覆盖", "MCP 工具声明覆盖率"),
    "legalAgentBenchAllPass": ("法律智能体全过率", "法律任务全部通过率"),
    "legalAgentBenchCriterionPass": ("法律智能体逐条率", "法律任务逐条通过率"),
    "legalAgentBenchHeldoutAllPass": ("法律智能体保留全过", "保留集全部通过率"),
    "legalAgentBenchHeldoutCriterionPass": ("法律智能体保留逐条", "保留集逐条通过率"),
    "gdpvalAa": ("GDPval 经济价值", "经济价值任务评测（原始分）"),
    "gdpvalAaNormalized": ("GDPval 归一化", "经济价值任务评测（归一化分）"),
    "toolathlonVerified": ("Toolathlon 工具链", "工具链任务通过率"),
    "toolathlonVerifiedPass3": ("Toolathlon Pass@3", "工具链任务三次通过率"),
    "toolathlonVerifiedPass3All": ("Toolathlon 全量 Pass@3", "工具链全量任务三次通过率"),
    "toolathlonVerifiedAvgTurns": ("Toolathlon 平均轮次", "工具链任务平均交互轮数"),
    "automationBench": ("AutomationBench 自动化", "任务自动化能力"),
    "aaTau3Banking": ("Tau3 银行", "金融银行业务智能体评测"),
    "sweBenchVerified": ("SWE-bench Verified", "真实 GitHub issue 修复（官方验证集）"),
    "sweBenchMultilingual": ("SWE-bench 多语言", "多语言软件工程修复"),
    "terminalBenchHard": ("Terminal-Bench Hard", "高难度终端任务操作"),
    "terminalBenchCore": ("Terminal-Bench Core", "终端任务核心集"),
    "humaneval": ("HumanEval 代码生成", "函数级代码生成正确率"),
    "livecodebench": ("LiveCodeBench 竞赛", "竞赛级实时代码评测"),
    "codeforces": ("Codeforces 竞赛编程", "竞赛编程百分位"),
    "aiderPolyglot": ("Aider 多语言编辑", "Aider 多语言代码编辑"),
    "gpqaDiamond": ("GPQA Diamond 科学", "研究生级科学问答"),
    "aime": ("AIME 数学竞赛", "美国数学邀请赛"),
    "aime2025": ("AIME 2025", "2025 年美国数学邀请赛"),
    "hmmt": ("HMMT 数学竞赛", "哈佛麻省理工数学锦标赛"),
    "math500": ("MATH-500", "数学题集抽样评测"),
    "polyglotMath": ("多语言数学", "多语言数学推理"),
    "mmluPro": ("MMLU-Pro 学科知识", "大规模多任务学科理解 Pro 版"),
    "mmlu": ("MMLU 学科知识", "大规模多任务学科理解"),
    "gpqa": ("GPQA 科学问答", "研究生级科学问答"),
    "arcAgi2": ("ARC-AGI-2 抽象推理", "抽象与推理通用智能测试"),
    "arcAgi1": ("ARC-AGI-1 抽象推理", "抽象推理第一代测试"),
    "humanevalMBPP": ("MBPP 基础编程", "基础编程题集"),
    "mmmu": ("MMMU 多模态理解", "多学科多模态理解"),
    "mathvista": ("MathVista 视觉数学", "视觉数学推理"),
    "chartqa": ("ChartQA 图表问答", "图表理解问答"),
    "docvqa": ("DocVQA 文档问答", "文档图像问答"),
    "ocrbench": ("OCRBench 文字识别", "图像文字识别"),
    "videoMmmu": ("Video-MMMU 视频理解", "视频多模态理解"),
    "murphyMultimodal": ("Murphy 多模态", "多模态综合评测"),
    "mmmuPro": ("MMMU-Pro", "多学科多模态理解 Pro 版"),
    "zeroscroll": ("ZeroScroll 长文本", "长文本理解"),
    "longbench": ("LongBench 长文本", "长文本基准"),
    "frame": ("FRAMES 事实性", "事实检索与推理"),
    "simpleqa": ("SimpleQA 事实问答", "简短事实性问答"),
    "healthbench": ("HealthBench 健康", "医疗健康对话评测"),
    "healthbenchHard": ("HealthBench 困难", "医疗健康困难集"),
    "mtaustwo": ("MT-AUStwo 翻译", "机器翻译评测"),
    "globalmmluLite": ("GlobalMMLU 多语言", "多语言学科知识精简版"),
    "mgsm": ("MGSM 多语言数学", "多语言小学数学"),
    "include": ("INCLUDE 多语言", "多语言基准"),
    "lambada": ("LAMBADA 语言建模", "语言建模预测"),
    "winsogrande": ("WinoGrande 常识", "常识代词消解"),
    "hellaswag": ("HellaSwag 常识推理", "常识情景推理"),
    "drop": ("DROP 阅读理解", "离散推理阅读理解"),
    "ifeval": ("IFEval 指令遵循", "指令遵循严格评测"),
    "complexBench": ("ComplexBench 复杂指令", "复杂指令遵循"),
    "multichallenge": ("MultiChallenge 多轮", "多轮对话指令挑战"),
    "sysbench": ("SysBench 系统指令", "系统提示遵循"),
    "coldstart": ("Cold-Start 首轮", "对话首轮质量"),
    "creativeWriting": ("Creative Writing 写作", "创意写作"),
    "criteriaAstRaw": ("Criteria AST", "AST 结构化输出"),
    "mrcrV2": ("MRCR 多轮一致性", "多轮对话检索一致性"),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def fmt_ctx(m):
    cw = m.get("contextWindow")
    if cw:
        return cw
    tokens = m.get("contextWindowTokens") or 0
    if tokens >= 1_000_000:
        return f"{tokens // 1_000_000}M"
    if tokens >= 1000:
        return f"{tokens // 1000}K"
    if tokens > 0:
        return str(tokens)
    return "未公布"


def fmt_price(v):
    if v is None:
        return None
    if v == 0:
        return "免费"
    if v == int(v):
        return f"${int(v)}/M"
    return f"${v:g}/M"


def fmt_date(d):
    if not d:
        return None
    return d[:7].replace("-", "-")  # 2026-07-24 -> 2026-07


def fmt_ttft(v):
    if v is None:
        return None
    return f"{v:.2f} 秒"


def pricing_note_fields(pricing):
    """从 pricing 字典取 note 结构化字段，返回 (rules, source_line, free_text, open_note)。"""
    rules = pricing.get("rules") or []
    return (
        [str(r) for r in rules],
        pricing.get("source_line"),
        pricing.get("free_text"),
        pricing.get("open_note"),
    )


USE_CASE_ZH = {
    "coding": "编程开发",
    "agentic": "智能体自动化",
    "reasoning": "复杂推理",
    "knowledge": "知识问答",
    "multimodal": "图像理解",
    "instructionFollowing": "对话助手",
    "math": "数学解题",
    "multilingual": "多语言翻译",
}


def _cat_value(cat_scores, key):
    """categoryScores 里 multimodal 的原始 key 是 multimodalGrounded。"""
    if key == "multimodal":
        return cat_scores.get("multimodal", cat_scores.get("multimodalGrounded"))
    return cat_scores.get(key)


def derive_use_cases(cat_scores, limit=4):
    """按分类得分 >= 80 推导使用场景标签。"""
    tags = []
    for key in ("coding", "agentic", "knowledge", "reasoning", "multimodal", "instructionFollowing", "math", "multilingual"):
        v = _cat_value(cat_scores, key)
        if isinstance(v, (int, float)) and v >= 80:
            tags.append(USE_CASE_ZH[key])
        if len(tags) >= limit:
            break
    return tags or ["通用对话"]


def derive_best_use(cat_scores):
    """取得分最高的分类作为最佳用途。"""
    best, bv = None, -1
    for key in USE_CASE_ZH:
        v = _cat_value(cat_scores, key)
        if isinstance(v, (int, float)) and v > bv:
            best, bv = key, v
    return USE_CASE_ZH[best] if best else None


# ---------------------------------------------------------------------------
# Related models (近似模型 / 同厂模型)
# ---------------------------------------------------------------------------

RELATED_INDEX = {}


def build_related_index(models):
    """预计算全部模型的价格/评分/厂商索引，用于近似与同厂推荐。"""
    global RELATED_INDEX
    idx = []
    for m in models:
        slug = m.get("slug")
        if not slug:
            continue
        pricing = m.get("pricing") or {}
        s = m.get("overallScore")
        po = pricing.get("outputPrice")
        pi = pricing.get("inputPrice")
        idx.append(
            {
                "slug": slug,
                "name": m.get("name") or slug,
                "creator": m.get("creator") or "",
                "score": s,
                "in": pi,
                "out": po,
                "sum": (pi or 0) + (po or 0) if (pi is not None or po is not None) else None,
            }
        )
    RELATED_INDEX = idx


def find_similar_models(slug, limit=5):
    """价格与得分都接近的模型（价格距离 + 评分距离联合打分）。"""
    cur = next((x for x in RELATED_INDEX if x["slug"] == slug), None)
    if not cur or cur["score"] is None:
        return []
    cands = []
    for x in RELATED_INDEX:
        if x["slug"] == slug or x["score"] is None:
            continue
        ds = abs(x["score"] - cur["score"])
        if cur["sum"] is not None and x["sum"] is not None:
            base = max(cur["sum"], 0.5)
            dp = abs(x["sum"] - cur["sum"]) / base
            if dp > 1.5:  # 价格差超过 2.5 倍的直接排除
                continue
        else:
            dp = 0.5
        cands.append((ds + 2.0 * dp, ds, dp, x))
    cands.sort(key=lambda t: (t[0], t[2], t[1]))
    return [
        {"slug": c[3]["slug"], "name": c[3]["name"], "score": c[3]["score"], "out": c[3]["out"]}
        for c in cands[:limit]
    ]


def find_same_creator(slug, limit=5):
    """同厂商的其他模型，按评分降序。"""
    cur = next((x for x in RELATED_INDEX if x["slug"] == slug), None)
    if not cur or not cur["creator"]:
        return []
    cands = [x for x in RELATED_INDEX if x["creator"] == cur["creator"] and x["slug"] != slug and x["score"] is not None]
    cands.sort(key=lambda x: (-x["score"], x["name"]))
    return [
        {"slug": c["slug"], "name": c["name"], "score": c["score"], "out": c["out"]}
        for c in cands[:limit]
    ]


def pick_benchmarks(m, limit=14):
    """Pick benchmarks with Chinese labels. benchmarks = {category: {benchKey: value}}"""
    benches = m.get("benchmarks") or {}
    rows = []
    for cat, bmap in benches.items():
        if not isinstance(bmap, dict):
            continue
        cat_label = CATEGORY_ZH.get(cat, cat)
        for k, v in bmap.items():
            if not isinstance(v, (int, float)):
                continue
            meta = BENCH_LOOKUP.get(k) or {}
            name = meta.get("name") or BENCH_ZH.get(k, (k, ""))[0]
            desc = BENCH_ZH.get(k, (k, ""))[1]
            rows.append((k, cat_label, name, desc, v))
    rows.sort(key=lambda r: r[0])
    return rows[:limit]


# ---------------------------------------------------------------------------
# Page rendering
# ---------------------------------------------------------------------------


def esc(s):
    """Escape double quotes for YAML double-quoted strings."""
    if s is None:
        return ""
    return str(s).replace('"', '\\"')



# 系列（series）推导：与 build_vendor_series.py 保持一致
_SIZE_TOKEN_RE = re.compile(
    r"^(\d+(\.\d+)?[BMK]?|A\d+(\.\d+)?B|NVFP4|FP8|FP4|INT4|INT8|GGUF|AWQ|GPTQ|\d{4})$",
    re.IGNORECASE,
)
_VARIANT_TOKEN_RE = re.compile(
    r"^(Reasoning|Instruct|Chat|Base|Thinking|Preview|Distill|Mini|Nano|Lite|Turbo|Experimental|Quantized)$",
    re.IGNORECASE,
)
_PAREN_SUFFIX_RE = re.compile(r"\s*\([^)]*\)\s*$")


def derive_series(name):
    """去掉模型名尾部的参数量/量化/变体 token，剩下的作为系列名。"""
    s = _PAREN_SUFFIX_RE.sub("", name.strip())
    tokens = re.split(r"[-_\s]+", s)
    while len(tokens) > 1 and (
        _SIZE_TOKEN_RE.match(tokens[-1]) or _VARIANT_TOKEN_RE.match(tokens[-1])
    ):
        tokens.pop()
    series = " ".join(tokens).strip(" -_")
    return series or name.strip()


def render_page(m):
    slug = m["slug"]
    name = m.get("name") or slug
    creator_zh = m.get("creatorZh") or m.get("creator") or "未知厂商"
    src_zh = m.get("sourceTypeZh") or ""
    reason_zh = m.get("reasoningTypeZh") or ""
    ctx = fmt_ctx(m)
    released = fmt_date(m.get("releaseDate"))
    score = m.get("overallScore")
    verified = m.get("verifiedScore")
    rank = m.get("overallRank")
    evidence_zh = m.get("evidenceStatusZh") or ""
    confidence = (m.get("coverage") or {}).get("scoreConfidence")
    trusted_count = (m.get("coverage") or {}).get("trustedBenchmarkCount")
    pricing = m.get("pricing") or {}
    speed = m.get("speed") or {}
    note_rules, note_source, note_free, note_open = pricing_note_fields(pricing)

    price_in = fmt_price(pricing.get("inputPrice"))
    price_out = fmt_price(pricing.get("outputPrice"))
    tps = speed.get("tokensPerSecond")
    ttft = fmt_ttft(speed.get("ttft"))
    cat_scores = m.get("categoryScores") or {}
    cat_ranks = m.get("categoryRanks") or {}

    lines = []
    ap = lines.append
    ap("---")
    ap(f'title: "{esc(name)}"')
    ap("model: true")
    ts = data_ts()
    if ts:
        ap(f"date: {ts}")
    score_txt = f"{score:g}" if isinstance(score, (int, float)) else ""
    ap(
        f'description: "{esc(creator_zh)}发布的 {esc(name)} 大语言模型：'
        f"综合评分 {score_txt or '暂无'}，{esc(src_zh) or '类型未知'}，"
        f'上下文 {esc(ctx)}。含价格、速度、延迟与评分数据。"'
    )
    ap("specs:")
    ap(f'  vendor: "{esc(creator_zh)}"')
    ap(f'  series: "{esc(derive_series(name))}"')
    if src_zh:
        ap(f'  category: "{esc(src_zh)}"')
    if ctx:
        ap(f'  context: "{esc(ctx)}"')
    if released:
        ap(f'  released: "{released}"')
    if price_in:
        ap(f'  price_input: "{esc(price_in)}"')
    if price_out:
        ap(f'  price_output: "{esc(price_out)}"')
    if pricing.get("cachedInputPrice") is not None:
        price_cache = fmt_price(pricing.get("cachedInputPrice"))
        if price_cache:
            ap(f'  price_cached: "{esc(price_cache)}"')
    if note_rules:
        ap("  price_notes:")
        for r in note_rules:
            ap(f'    - "{esc(r)}"')
    if note_source:
        ap(f'  pricing_source: "{esc(note_source)}"')
    if note_open:
        ap(f'  open_note: "{esc(note_open)}"')
    if note_free:
        ap(f'  free_note: "{esc(note_free)}"')
    if tps is not None:
        ap(f'  speed: "{tps} tokens/秒"')
    if ttft:
        ap(f'  ttft: "{esc(ttft)}"')
    if score is not None or cat_scores:
        ap("  scores:")
        if score is not None:
            if rank:
                ap(f"    overall: {{score: {score:g}, rank: {rank}}}")
            else:
                ap(f"    overall: {{score: {score:g}}}")
            if verified is not None and verified != score:
                ap(f"    verified: {{score: {verified:g}}}")
        for key in ("agentic", "coding", "reasoning", "multimodalGrounded", "knowledge", "multilingual", "instructionFollowing", "math"):
            if key in cat_scores:
                r = cat_ranks.get(key)
                k = "multimodal" if key == "multimodalGrounded" else key
                if r:
                    ap(f"    {k}: {{score: {cat_scores[key]:g}, rank: {r}}}")
                else:
                    ap(f"    {k}: {{score: {cat_scores[key]:g}}}")
        uc = derive_use_cases(cat_scores)
        bu = derive_best_use(cat_scores)
        if bu:
            ap(f'  best_use: "{esc(bu)}"')
        if uc:
            ap("  use_cases:")
            for t in uc:
                ap(f'    - "{esc(t)}"')
    sim = find_similar_models(slug)
    if sim:
        ap("similar:")
        for x in sim:
            ap(f'  - slug: "{esc(x["slug"])}"')
            ap(f'    name: "{esc(x["name"])}"')
            ap(f"    score: {x['score']:g}")
            if x["out"] is not None:
                ap(f'    price: "{fmt_price(x["out"])}"')
    same = find_same_creator(slug)
    if same:
        ap("same_creator:")
        for x in same:
            ap(f'  - slug: "{esc(x["slug"])}"')
            ap(f'    name: "{esc(x["name"])}"')
            ap(f"    score: {x['score']:g}")
            if x["out"] is not None:
                ap(f'    price: "{fmt_price(x["out"])}"')
    ap("---")
    ap("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

BENCH_LOOKUP = {}


def load_bench_lookup():
    """Load benchmark key -> official name mapping from jumo_benchmarks.json."""
    global BENCH_LOOKUP
    path = os.path.join(BASE_DIR, "data", "jumo_benchmarks.json")
    try:
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
        BENCH_LOOKUP = {b["key"]: b for b in doc.get("benchmarks", []) if b.get("key")}
    except FileNotFoundError:
        BENCH_LOOKUP = {}
        print(f"警告: 未找到 {path}，基准名称将回退到内置词典", file=sys.stderr)


def write_page(m, force=False):
    slug = m["slug"]
    if not slug or "/" in slug or slug.startswith("."):
        return None
    out_dir = os.path.join(MODELS_DIR, slug)
    out_file = os.path.join(out_dir, "index.md")
    if os.path.exists(out_file) and not force:
        return None
    os.makedirs(out_dir, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as fh:
        fh.write(render_page(m))
    return out_file


def prune_orphan_pages(models):
    """删除 content/models/ 下已不在 jumo_models.json 中的模型目录。

    上游删除模型或厂商过滤剔除后，对应 md 会成为孤儿页面；
    --all 更新时默认执行本清理（--no-prune 可关闭）。
    """
    valid = {m["slug"] for m in models if m.get("slug")}
    removed = []
    for entry in sorted(os.listdir(MODELS_DIR)):
        path = os.path.join(MODELS_DIR, entry)
        if entry.startswith("_") or not os.path.isdir(path):
            continue
        if entry not in valid:
            shutil.rmtree(path)
            removed.append(entry)
    if removed:
        print(f"清理孤儿页面: 删除 {len(removed)} 个已不在数据中的模型目录")
        for e in removed:
            print(f"  - {e}")
    else:
        print("孤儿页面: 无")
    return removed


def main():
    parser = argparse.ArgumentParser(description="Generate Hugo model pages from jumo_models.json")
    parser.add_argument("--slug", help="generate a single model page by slug")
    parser.add_argument("--all", action="store_true", help="generate pages for all models")
    parser.add_argument("--force", action="store_true", help="overwrite existing pages")
    parser.add_argument("--no-prune", action="store_true", help="do not remove model dirs missing from the data")
    args = parser.parse_args()

    if not args.slug and not args.all:
        parser.error("specify --slug SLUG or --all")

    load_bench_lookup()

    with open(DATA_FILE, encoding="utf-8") as fh:
        doc = json.load(fh)
    models = doc.get("models", [])
    build_related_index(models)

    if args.slug:
        matches = [m for m in models if m["slug"] == args.slug]
        if not matches:
            print(f"错误: 未找到 slug 为 {args.slug} 的模型", file=sys.stderr)
            return 1
        path = write_page(matches[0], force=args.force)
        print(f"已生成: {path}" if path else f"已存在（跳过，用 --force 覆盖）: {matches[0]['slug']}")
        return 0

    written, skipped = 0, 0
    for m in models:
        path = write_page(m, force=args.force)
        if path:
            written += 1
        else:
            skipped += 1
    print(f"生成完成: 新建 {written} 个页面，跳过 {skipped} 个（已存在，用 --force 覆盖）")
    if not args.no_prune:
        prune_orphan_pages(models)
    return 0


if __name__ == "__main__":
    sys.exit(main())
