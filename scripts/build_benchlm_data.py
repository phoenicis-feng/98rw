#!/usr/bin/env python3
"""Build jumohub model data from BenchLM machine-readable exports.

Reads the downloaded BenchLM JSON files (benchlm-data/), merges model basics
with pricing and speed metrics, translates enum fields into Chinese, and
emits Hugo-ready data files:

  data/jumo_models.json       - merged model master table (with benchmark scores)
  data/jumo_leaderboards.json - overall / category / speed / latency / price /
                                value / free / open-source leaderboards
  data/jumo_benchmarks.json   - benchmark metadata with Chinese category labels

Usage:
  python3 scripts/build_benchlm_data.py [--refresh] [--benchlm-dir DIR] [--data-dir DIR]
"""

import argparse
import json
import math
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCHLM_DIR = os.path.join(BASE_DIR, "benchlm-data")
DATA_DIR = os.path.join(BASE_DIR, "data")

BENCHLM_BASE = "https://benchlm.ai/data"
BENCHLM_FILES = [
    "models.json",
    "leaderboard.json",
    "benchmarks.json",
    "pricing.json",
    "speed.json",
]

# ---------------------------------------------------------------------------
# Chinese translation dictionaries
# ---------------------------------------------------------------------------

# 国产模型榜单厂商白名单（匹配 creatorZh 中文名；数据源无国产标记，此处人工维护）
DOMESTIC_VENDORS = {
    "深度求索", "阿里通义", "智谱 AI", "月之暗面", "腾讯", "腾讯混元",
    "字节跳动", "小米", "MiniMax", "百度", "阶跃星辰", "百川智能",
    "美团", "蚂蚁集团 InclusionAI", "书生 InternScience", "清华 OpenBMB",
    "零一万物", "面壁智能", "科大讯飞", "讯飞",
}

CREATOR_ZH = {
    "OpenAI": "OpenAI",
    "Anthropic": "Anthropic",
    "Google": "谷歌",
    "DeepSeek": "深度求索",
    "Alibaba": "阿里通义",
    "Moonshot AI": "月之暗面",
    "Z.AI": "智谱 AI",
    "Zhipu AI": "智谱 AI",
    "Meta": "Meta",
    "Mistral": "Mistral AI",
    "Mistral AI": "Mistral AI",
    "MiniMax": "MiniMax",
    "ByteDance": "字节跳动",
    "Tencent": "腾讯",
    "Tencent Hunyuan": "腾讯混元",
    "Xiaomi": "小米",
    "NVIDIA": "英伟达",
    "Microsoft": "微软",
    "Amazon": "亚马逊",
    "IBM": "IBM",
    "Cohere": "Cohere",
    "xAI": "xAI",
    "StepFun": "阶跃星辰",
    "Baichuan": "百川智能",
    "Meituan": "美团",
    "InclusionAI": "蚂蚁集团 InclusionAI",
    "OpenBMB": "清华 OpenBMB",
    "LG AI Research": "LG AI 研究院",
    "SK Telecom": "SK 电讯",
    "Naver Cloud": "Naver 云",
    "Upstage": "Upstage",
    "Sarvam": "Sarvam",
    "LiquidAI": "Liquid AI",
    "Thinking Machines Lab": "Thinking Machines",
    "Cognition": "Cognition",
    "Cursor": "Cursor",
    "JetBrains": "JetBrains",
    "Databricks": "Databricks",
    "ElevenLabs": "ElevenLabs",
    "Deepgram": "Deepgram",
    "Kyutai": "Kyutai",
    "Fixie AI": "Fixie AI",
    "Poolside": "Poolside",
    "Inception": "Inception",
    "Arcee AI": "Arcee AI",
    "AI Singapore": "新加坡国家 AI 团队",
    "OpenMOSS": "复旦 OpenMOSS",
    "ICTNLP": "北大 ICTNLP",
    "Infinigence AI": "生数科技",
    "H Company": "H Company",
    "InternScience": "书生 InternScience",
    "Sakana AI": "Sakana AI",
    "Kakao": "Kakao",
    "Community": "社区",
}

# ___CHUNK2___
SOURCE_TYPE_ZH = {
    "Proprietary": "闭源专有",
    "Open Weight": "开源权重",
    "Pending": "待确认",
}

REASONING_TYPE_ZH = {
    "Reasoning": "推理模型",
    "Non-Reasoning": "非推理模型",
    "Hybrid": "混合推理",
}

EVIDENCE_STATUS_ZH = {
    "supported": "已验证",
    "estimated": "估算值",
}

MARKET_ZH = {
    "Korea": "韩国",
    "Japan": "日本",
}

CATEGORY_ZH = {
    "agentic": "智能体",
    "coding": "编程",
    "reasoning": "推理",
    "multimodalGrounded": "多模态",
    "knowledge": "知识",
    "multilingual": "多语言",
    "instructionFollowing": "指令遵循",
    "math": "数学",
    "external": "外部评测",
    "korean": "韩语评测",
}

CATEGORY_DESC_ZH = {
    "agentic": "工具调用、网页操作、多步任务执行等智能体能力基准加权得分",
    "coding": "代码生成、修复、重构与真实工程任务基准加权得分",
    "reasoning": "复杂逻辑推理、科学分析与抽象思考基准加权得分",
    "multimodalGrounded": "图像理解、视觉定位等多模态基准加权得分",
    "knowledge": "百科知识、专业领域问答基准加权得分",
    "multilingual": "跨语言理解与生成基准加权得分",
    "instructionFollowing": "指令遵循与格式约束基准加权得分",
    "math": "数学竞赛与定理证明基准加权得分",
}

# ---------------------------------------------------------------------------
# Loading / refreshing
# ---------------------------------------------------------------------------


def _fetch_url(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (jumohub-data-sync)"})
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as fh:
        fh.write(resp.read())


def refresh_raw(benchlm_dir):
    os.makedirs(benchlm_dir, exist_ok=True)
    for name in BENCHLM_FILES:
        url = f"{BENCHLM_BASE}/{name}"
        dest = os.path.join(benchlm_dir, name)
        print(f"下载 {url} -> {dest}")
        _fetch_url(url, dest)


def load_raw(benchlm_dir):
    data = {}
    for name in BENCHLM_FILES:
        path = os.path.join(benchlm_dir, name)
        with open(path, encoding="utf-8") as fh:
            data[name.removesuffix(".json")] = json.load(fh)
    return data


# ---------------------------------------------------------------------------
# pricing note 结构化提取
# ---------------------------------------------------------------------------

# 各「计费规则」类别的正则（匹配 note 英文原文，输出中文标签）
_NOTE_RULE_PATTERNS = [
    ("long_context_surcharge", r"(above|over)\s+[\d.,]+\s*[KM]?\s*(input\s+)?tokens|long[- ]context\s+(tier|rate|pricing)|charged at\s*\d+(\.\d+)?x"),
    ("fast_mode_surcharge", r"fast mode|fast tier|twice the base price|2\.5x the default speed"),
    ("batch_discount", r"\bbatch\b|\bflex\b"),
    ("promo_deadline", r"promotional|at least through \w+ \d{1,2}, \d{4}|limited[- ]time|introductory"),
]

_NOTE_RULE_LABELS = {
    "long_context_surcharge": "长上下文加价",
    "fast_mode_surcharge": "Fast 模式加价",
    "batch_discount": "Batch/Flex 折扣",
    "promo_deadline": "限时促销价",
}

# note 中的「出处页类型」表述（用于提取溯源信息）
_NOTE_PAGE_TYPE_RE = re.compile(
    r"(?:official\s+|API\s+|public\s+)?"
    r"(pricing\s+page|price\s+sheet|pricing\s+docs|model\s+page|"
    r"launch\s+announcement|announcement|launch\s+page|launch\s+post|documentation)",
    re.IGNORECASE,
)

_NOTE_PAGE_TYPE_ZH = {
    "pricing page": "官方定价页",
    "price sheet": "价目表",
    "pricing docs": "定价文档",
    "model page": "模型页面",
    "launch announcement": "发布公告",
    "announcement": "发布公告",
    "launch page": "发布页",
    "launch post": "发布页",
    "documentation": "官方文档",
}

_MONTHS = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
    "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12",
}

_DATE_RE = re.compile(r"([A-Za-z]+ \d{1,2}, \d{4})|(\d{4}-\d{2}-\d{2})")


def _note_date_iso(text):
    """从文本中找第一个日期并规范为 YYYY-MM-DD；无则 None。"""
    m = _DATE_RE.search(text)
    if not m:
        return None
    if m.group(2):
        return m.group(2)
    parts = m.group(1).replace(",", " ").split()
    if len(parts) != 3:
        return None
    mon, day, year = parts
    mm = _MONTHS.get(mon.lower()[:3])
    if not mm:
        return None
    return f"{year}-{mm}-{int(day):02d}"


def extract_pricing_note_facts(note):
    """从 pricing note 英文原文提取结构化字段。

    返回 dict：
      rules       - 命中的「计费规则」中文标签列表（长上下文加价等）
      source_line - 溯源信息（「官方定价页 · 2026-09-03」），无法识别时为 None
      free_text   - 免费/0 价口径说明的英文原句（如「免费层限速」），无则 None
      open_note   - 开源/权重状态中文说明（如「权重计划 2026-07-27 公开」），无则 None
    """
    if not note:
        return {"rules": [], "source_line": None, "free_text": None, "open_note": None}
    low = note.lower()

    rules = [
        _NOTE_RULE_LABELS[key]
        for key, pattern in _NOTE_RULE_PATTERNS
        if re.search(pattern, low)
    ]

    # 溯源：页类型 + 日期（优先取 Observed <date>（数据源实际观察日），否则取全文第一个日期）
    source_line = None
    m = _NOTE_PAGE_TYPE_RE.search(note)
    if m:
        type_zh = _NOTE_PAGE_TYPE_ZH.get(m.group(1).lower(), "官方来源")
        obs = re.search(r"[Oo]bserved\s+((?:[A-Za-z]+ \d{1,2}, \d{4})|(?:\d{4}-\d{2}-\d{2}))", note)
        date = _note_date_iso(obs.group(1)) if obs else _note_date_iso(note)
        source_line = f"{type_zh} · {date}" if date else type_zh

    # 免费口径：出现 free 且有附加说明（限速/配额等），不只是「价格为零」
    free_text = None
    if re.search(r"\bfree\b", low) and re.search(
        r"(rate[- ]limit|throttl|quot|cap\b|limited to|capped|tier)", low
    ):
        for sent in re.split(r"(?<=\.)\s+", note.strip()):
            if re.search(r"\bfree\b", sent.lower()):
                free_text = sent.strip()
                break

    # 开源/权重计划：日期 / 许可证 / 泛指，输出中文短语
    open_note = None
    m = re.search(r"(?:full\s+)?weights?\s+release[^.]{0,80}?([A-Za-z]+ \d{1,2}, \d{4})", note, re.IGNORECASE)
    if not m:
        m = re.search(r"(?:full\s+)?weights?\s+release[^.]{0,80}?(\d{4}-\d{2}-\d{2})", note, re.IGNORECASE)
    if m:
        date = _note_date_iso(m.group(0))
        open_note = f"权重计划 {date} 公开" if date else "权重将公开"
    else:
        m = re.search(r"open[- ]weights?\s+under\s+((?:modified\s+|custom\s+|the\s+)?[\w -]{0,30}?license)", note, re.IGNORECASE)
        if m:
            lic = re.sub(r"^(a|an|the)\s+", "", re.sub(r"\s+", " ", m.group(1)).strip())
            open_note = f"开源权重（{lic}）"
        elif re.search(r"\bopen[- ]weight\b", low):
            open_note = "开源权重"

    return {"rules": rules, "source_line": source_line, "free_text": free_text, "open_note": open_note}



# ---------------------------------------------------------------------------
# Merge pipeline
# ---------------------------------------------------------------------------


def build_model_master(models, pricing, speed):
    pricing_by_slug = {}
    for row in pricing.get("items", []):
        pricing_by_slug[row["slug"]] = row

    speed_by_slug = {}
    for row in speed.get("items", []):
        speed_by_slug[row["slug"]] = row

    out = []
    for it in models.get("items", []):
        slug = it["slug"]
        scores = it.get("scores") or {}
        ranking = it.get("ranking") or {}
        coverage = it.get("coverage") or {}
        pricing_row = pricing_by_slug.get(slug)
        speed_row = speed_by_slug.get(slug)

        cat_scores = scores.get("displayCategoryScores") or {}
        cat_ranks = ranking.get("categoryRanks") or {}

        rec = {
            "slug": slug,
            "name": it.get("model"),
            "creator": it.get("creator"),
            "creatorZh": zh(it.get("creator"), CREATOR_ZH),
            "sourceType": it.get("sourceType"),
            "sourceTypeZh": zh(it.get("sourceType"), SOURCE_TYPE_ZH),
            "reasoningType": it.get("reasoningType"),
            "reasoningTypeZh": zh(it.get("reasoningType"), REASONING_TYPE_ZH),
            "contextWindow": it.get("contextWindow"),
            "contextWindowTokens": it.get("contextWindowTokens"),
            "releaseDate": it.get("releaseDate"),
            "market": it.get("market"),
            "marketZh": zh(it.get("market"), MARKET_ZH),
            "overallScore": scores.get("displayScore"),
            "verifiedScore": scores.get("verifiedDisplayScore"),
            "overallRank": ranking.get("overallRank"),
            "rankingEligible": bool(ranking.get("rankingEligible")),
            "categoryScores": {k: v for k, v in cat_scores.items() if v is not None},
            "categoryRanks": {k: v for k, v in cat_ranks.items() if v is not None},
            "coverage": {
                "trustedBenchmarkCount": coverage.get("trustedBenchmarkCount"),
                "verifiedBenchmarkCount": coverage.get("verifiedBenchmarkCount"),
                "scoreConfidence": coverage.get("scoreConfidence"),
            },
            "evidenceStatus": it.get("evidenceStatus"),
            "evidenceStatusZh": zh(it.get("evidenceStatus"), EVIDENCE_STATUS_ZH),
            "sourceUrl": it.get("url"),
            "sourceMdUrl": it.get("markdownUrl"),
            "benchmarks": it.get("benchmarks") or {},
        }

        if pricing_row:
            input_price = pricing_row.get("inputPrice")
            output_price = pricing_row.get("outputPrice")
            total = None
            if input_price is not None and output_price is not None:
                total = round(input_price + output_price, 4)
            rec["pricing"] = {
                "inputPrice": input_price,
                "outputPrice": output_price,
                "cachedInputPrice": pricing_row.get("cachedInputPrice"),
                "totalPrice": total,
                "hasNumericPricing": bool(pricing_row.get("hasNumericPricing")),
                "isFree": bool(pricing_row.get("isFreePricing")),
                "scorePerOutputDollar": pricing_row.get("scorePerOutputDollar"),
                "note": pricing_row.get("note"),
                **extract_pricing_note_facts(pricing_row.get("note")),
            }
        else:
            rec["pricing"] = None

        if speed_row:
            rec["speed"] = {
                "tokensPerSecond": speed_row.get("tokensPerSecond"),
                "ttft": speed_row.get("ttft"),
                "source": speed_row.get("source"),
                "sourceUpdatedAt": speed_row.get("sourceUpdatedAt"),
            }
        else:
            rec["speed"] = None

        out.append(rec)
    return out


# ___CHUNK4___


def zh(v, table):
    """Translate a value via table, falling back to the raw value."""
    if v is None:
        return None
    return table.get(v, v)


# ___CHUNK3___


def _row_from_master(m, rank=0):
    """Build a leaderboard row from a merged master record."""
    pricing = m.get("pricing") or {}
    speed = m.get("speed") or {}
    return {
        "rank": rank,
        "slug": m["slug"],
        "name": m.get("name"),
        "creatorZh": m.get("creatorZh") or m.get("creator"),
        "sourceTypeZh": m.get("sourceTypeZh") or m.get("sourceType"),
        "contextWindow": m.get("contextWindow"),
        "score": m.get("overallScore"),
        "inputPrice": pricing.get("inputPrice"),
        "outputPrice": pricing.get("outputPrice"),
        "totalPrice": pricing.get("totalPrice"),
        "tokensPerSecond": speed.get("tokensPerSecond"),
        "ttft": speed.get("ttft"),
    }


def build_leaderboards(master, leaderboard_raw):
    """Return list of leaderboard dicts, all rows already Chinese-labelled."""
    master_by_slug = {m["slug"]: m for m in master}
    boards = []

    def add_board(key, name, desc, rows, unit="分", sort_desc=True, sort_key="score"):
        rows = [r for r in rows if r.get(sort_key) is not None]
        rows.sort(key=lambda r: r[sort_key], reverse=sort_desc)
        for i, r in enumerate(rows, 1):
            r["rank"] = i
        boards.append(
            {
                "key": key,
                "name": name,
                "description": desc,
                "unit": unit,
                "total": len(rows),
                "rows": rows,
            }
        )

    # 1. Overall score board (only ranking-eligible entries from the source)
    overall = []
    for i, e in enumerate(
        [e for e in leaderboard_raw.get("items", []) if e.get("rankingEligible")], 1
    ):
        m = master_by_slug.get(e["slug"])
        if not m:
            continue
        row = _row_from_master(m, e.get("rank") or i)
        row["rank"] = e.get("rank") or i
        overall.append(row)
    add_board(
        "overall",
        "综合评分榜",
        "基于多基准加权综合评分的总排名（数据源 benchlm.ai）",
        overall,
    )

    # 2. Eight category boards straight from the source categories dict
    for cat_key, entries in (leaderboard_raw.get("categories") or {}).items():
        cat_name = CATEGORY_ZH.get(cat_key, cat_key)
        cat_rows = []
        for e in entries:
            m = master_by_slug.get(e["slug"])
            if not m:
                continue
            row = _row_from_master(m)
            row["rank"] = e.get("rank") or 0
            row["score"] = e.get("displayScore", m.get("overallScore"))
            cat_rows.append(row)
        add_board(
            f"cat_{cat_key}",
            f"{cat_name}榜",
            CATEGORY_DESC_ZH.get(cat_key, f"{cat_name}维度基准加权得分"),
            cat_rows,
        )

    # 3. Speed board (tokens/sec, descending)
    add_board(
        "speed",
        "速度榜",
        "模型输出吞吐量（tokens/秒），来源 Artificial Analysis",
        [_row_from_master(m) for m in master if m.get("speed")],
        unit="tokens/秒",
        sort_key="tokensPerSecond",
    )

    # 4. 延迟榜（按首字延迟 TTFT 升序 = 快的在前）
    add_board(
        "latency",
        "响应延迟榜",
        "首 Token 延迟（秒，越小越快），来源 Artificial Analysis",
        [_row_from_master(m) for m in master if m.get("speed")],
        unit="秒",
        sort_desc=False,
        sort_key="ttft",
    )

    # 5. Price board (input+output per 1M tokens, ascending = cheaper first)
    add_board(
        "price",
        "低价榜",
        "输入+输出合计 API 价格（美元/百万 tokens，越小越便宜）",
        [
            _row_from_master(m)
            for m in master
            if m.get("pricing") and m["pricing"].get("hasNumericPricing")
        ],
        unit="美元/百万tokens",
        sort_desc=False,
        sort_key="totalPrice",
    )

    # 6. Value board (score per output dollar, descending)
    value_rows = []
    for m in master:
        p = m.get("pricing") or {}
        if m.get("overallScore") is not None and p.get("outputPrice"):
            row = _row_from_master(m)
            row["valueScore"] = round(m["overallScore"] / p["outputPrice"], 2)
            value_rows.append(row)
    add_board(
        "value",
        "性价比榜",
        "综合评分 ÷ 输出价格（分/美元，越高越划算）",
        value_rows,
        unit="分/美元",
        sort_key="valueScore",
    )

    # 6b. 国产模型榜（综合评分，厂商白名单过滤；评分为 0/None 视为未收录评分，剔除）
    domestic_rows = [
        _row_from_master(m)
        for m in master
        if m.get("creatorZh") in DOMESTIC_VENDORS
        and m.get("overallScore")
    ]
    add_board(
        "domestic",
        "国产模型榜",
        "国产厂商模型按综合评分排序（数据源 benchlm.ai，国内外同口径评分）",
        domestic_rows,
    )

    # 6c. 国产性价比榜（平衡算法：价格分×70% + 评分分×30%）
    #     价格分：输出价格对数刻度 min-max 归一化（价格跨数量级，线性会失真），最便宜=100，最贵=0
    #     评分分：本榜模型内 min-max 归一化，最高分=100，最低分=0
    #     平衡分 = 价格分×0.7 + 评分分×0.3（0~100）；免费模型（$0）不参与，避免"无限性价比"淹没榜单
    VALUE_PRICE_WEIGHT = 0.7
    VALUE_SCORE_WEIGHT = 0.3
    priced_rows = [r for r in domestic_rows if r.get("outputPrice")]
    if priced_rows:
        log_prices = [math.log10(r["outputPrice"]) for r in priced_rows]
        scores = [r["score"] for r in priced_rows]
        log_min, log_max = min(log_prices), max(log_prices)
        s_min, s_max = min(scores), max(scores)
        domestic_value_rows = []
        for r in priced_rows:
            if log_max > log_min:
                price_score = (
                    (log_max - math.log10(r["outputPrice"])) / (log_max - log_min) * 100
                )
            else:
                price_score = 100.0  # 全场同价，价格分不区分
            score_score = (
                (r["score"] - s_min) / (s_max - s_min) * 100 if s_max > s_min else 100.0
            )
            balance = round(
                price_score * VALUE_PRICE_WEIGHT + score_score * VALUE_SCORE_WEIGHT, 1
            )
            domestic_value_rows.append({**r, "valueScore": balance})
        add_board(
            "domestic_value",
            "国产性价比榜",
            "平衡算法：价格分×70%（对数归一化，越便宜越高）+ 评分分×30%（0-100 平衡分，越高越划算；免费模型不参与）",
            domestic_value_rows,
            unit="分",
            sort_key="valueScore",
        )

    # 7. Free models board
    add_board(
        "free",
        "免费模型榜",
        "官方 API 免费可用的模型，按综合评分排序",
        [
            _row_from_master(m)
            for m in master
            if m.get("pricing") and m["pricing"].get("isFree")
            and m.get("overallScore") is not None
        ],
    )

    # 8. Open-source board
    add_board(
        "open_source",
        "开源模型榜",
        "开源权重模型按综合评分排序",
        [
            _row_from_master(m)
            for m in master
            if m.get("sourceType") == "Open Weight"
            and m.get("overallScore") is not None
        ],
    )

    return boards


def build_benchmark_meta(benchmarks_raw):
    items = []
    for it in benchmarks_raw.get("items", []):
        items.append(
            {
                "key": it.get("benchmarkKey"),
                "name": it.get("name"),
                "fullName": it.get("fullName"),
                "category": it.get("category"),
                "categoryZh": zh(it.get("category"), CATEGORY_ZH),
                "description": it.get("description"),
                "weight": it.get("weight"),
                "year": it.get("year"),
            }
        )
    return items


def filter_small_vendors(master, min_count):
    """厂商模型数不足 min_count 的整体剔除（在源头控制厂商数量）。"""
    counts = {}
    for m in master:
        vendor = m.get("creatorZh") or m.get("creator") or "其他"
        counts[vendor] = counts.get(vendor, 0) + 1
    removed = {v for v, n in counts.items() if n < min_count}
    kept = [
        m
        for m in master
        if (m.get("creatorZh") or m.get("creator") or "其他") not in removed
    ]
    print(
        f"厂商过滤(< {min_count} 个模型): 剔除 {len(removed)} 家厂商 / "
        f"{len(master) - len(kept)} 个模型，保留 {len(kept)} 个模型"
    )
    return kept


def main():
    parser = argparse.ArgumentParser(description="Build jumohub data from BenchLM exports")
    parser.add_argument("--refresh", action="store_true", help="re-download BenchLM data first")
    parser.add_argument("--benchlm-dir", default=BENCHLM_DIR)
    parser.add_argument("--data-dir", default=DATA_DIR)
    parser.add_argument(
        "--min-vendor-models",
        type=int,
        default=5,
        help="厂商最少模型数，低于该值的厂商整体剔除（0 为不过滤）",
    )
    args = parser.parse_args()

    if args.refresh:
        refresh_raw(args.benchlm_dir)

    raw = load_raw(args.benchlm_dir)

    master = build_model_master(raw["models"], raw["pricing"], raw["speed"])
    if args.min_vendor_models > 0:
        master = filter_small_vendors(master, args.min_vendor_models)
    boards = build_leaderboards(master, raw["leaderboard"])
    bench_meta = build_benchmark_meta(raw["benchmarks"])

    now_cn = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")

    # 内容稳定时间戳：数据与上次完全一致时沿用旧 generatedAt，
    # 避免「数据未变但时间戳天天刷新」导致 sitemap lastmod 失真、增量推送误判全站有更新
    def _canon(obj):
        return json.dumps(obj, sort_keys=True, ensure_ascii=False)

    def _prev_doc(fname):
        try:
            with open(os.path.join(args.data_dir, fname), encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            return None

    def stable_ts(payload, fname, payload_key):
        old = _prev_doc(fname)
        if isinstance(old, dict):
            old_payload = old.get(payload_key)
            if old_payload is not None and _canon(old_payload) == _canon(payload):
                prev = (old.get("metadata") or {}).get("generatedAt")
                if prev:
                    return prev
        return now_cn

    ts_models = stable_ts(master, "jumo_models.json", "models")
    ts_boards = stable_ts(boards, "jumo_leaderboards.json", "leaderboards")
    ts_bench = stable_ts(bench_meta, "jumo_benchmarks.json", "benchmarks")

    master_doc = {
        "metadata": {
            "generatedAt": ts_models,
            "source": "benchlm.ai machine-readable data",
            "sourceUpdatedAt": raw["models"].get("sourceLastUpdated"),
            "totalModels": len(master),
            "scoredModels": sum(1 for m in master if m.get("overallScore") is not None),
            "pricedModels": sum(
                1 for m in master if m.get("pricing") and m["pricing"].get("hasNumericPricing")
            ),
            "speedModels": sum(1 for m in master if m.get("speed")),
        },
        "models": master,
    }

    boards_doc = {
        "metadata": {
            "generatedAt": ts_boards,
            "source": "benchlm.ai machine-readable data",
            "sourceUpdatedAt": raw["leaderboard"].get("sourceLastUpdated"),
            "boardCount": len(boards),
        },
        "leaderboards": boards,
    }

    bench_doc = {
        "metadata": {
            "generatedAt": ts_bench,
            "source": "benchlm.ai machine-readable data",
            "totalBenchmarks": len(bench_meta),
        },
        "benchmarks": bench_meta,
    }

    os.makedirs(args.data_dir, exist_ok=True)
    outputs = {
        "jumo_models.json": master_doc,
        "jumo_leaderboards.json": boards_doc,
        "jumo_benchmarks.json": bench_doc,
    }
    for fname, doc in outputs.items():
        path = os.path.join(args.data_dir, fname)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, ensure_ascii=False, indent=1)
        print(f"写入 {path} ({os.path.getsize(path) / 1024:.0f} KB)")

    print("\n===== 汇总 =====")
    md = master_doc["metadata"]
    print(
        f"模型总数: {md['totalModels']} | 有评分: {md['scoredModels']} "
        f"| 有价格: {md['pricedModels']} | 有速度: {md['speedModels']}"
    )
    for b in boards:
        print(f"榜单 {b['key']:24s} {b['name']:8s} rows={b['total']}")


if __name__ == "__main__":
    sys.exit(main())
