#!/usr/bin/env python3
"""
search_model_releases.py
==============================================
按品牌（data/brands.yaml 里的 15 个品牌）搜索 2025-01-01 以后发布的大模型。
数据来自模型整合站（不使用 OpenRouter，也不依赖各品牌官网可用性）：

1. Hugging Face / hf-mirror.com —— HF 官方 API 在部分网络不可达时自动切换到
   hf-mirror.com（完整镜像，路径与字段完全一致）。按官方组织名拉取模型列表，
   createdAt 时间戳精确过滤「2025 年以后」。
2. ModelScope 魔搭社区 —— 阿里官方 API，覆盖国内品牌（文心/混元/Seed 等），
   CreatedTime 时间戳过滤。两家整合站的结果合并去重。

保留品牌官网/RSS 与 Firecrawl/DuckDuckGo 网页搜索作为公告类补充。

输出：
  - .model_search/results.json     —— 全量结构化结果（去重后）
  - .model_search/report.md        —— 人读的 Markdown 报告（按品牌分组）

用法：
  python3 scripts/search_model_releases.py                  # 全部品牌
  python3 scripts/search_model_releases.py --brand qwen     # 单个品牌
  python3 scripts/search_model_releases.py --year 2025      # 只要 2025 年
  python3 scripts/search_model_releases.py --no-search      # 只用整合站，跳过官网与网页搜索
"""

import argparse
import html
import json
import os
import re
import time

# 每个品牌：模型整合站官方组织 + 官网/搜索渠道
#   huggingface : HF/HF镜像 官方组织名（author= 参数）
#   modelscope  : 魔搭社区 搜索关键词（Name= 参数，官方组织名或模型系列名）
#   official    : [(url, source_label), ...]  RSS 会被自动解析，HTML 会抽 <a> 链接
#   queries     : 兜底搜索词（Firecrawl / DuckDuckGo）
CHANNELS = {
    "chatgpt": {
        "name": "ChatGPT / OpenAI",
        "huggingface": ["openai", "openai-community"],
        "modelscope": [],
        "official": [
            ("https://openai.com/news/rss.xml", "openai.com/news (RSS)"),
            ("https://openai.com/news/", "openai.com/news"),
        ],
        "queries": [
            "OpenAI new model release 2025 site:openai.com",
            "OpenAI GPT-5 model release date 2025",
        ],
        # ChatGPT 官网 RSS 全是企业合作/功能公告，需要严格过滤真正的模型发布
        # 只保留：模型代号是标题主语（GPT-x/o-x/Sora/Codex/ChatGPT 产品线）
        # GPT- 后必须是数字（排除 GPT-Rosalind、GPT-Live 等研究代号）
        "title_allow": re.compile(
            r'^(Introducing |Retiring |Updated )?(GPT-\d[\w.]*|o[1-5]\b|Sora|Codex|'
            r'ChatGPT (Go|Pro|Plus|Enterprise|Team|Education|Work)|gpt-oss)',
            re.I,
        ),
    },
    "claude": {
        "name": "Claude / Anthropic",
        "huggingface": [],
        "modelscope": [],
        "official": [("https://www.anthropic.com/news", "anthropic.com/news")],
        "queries": [
            "Anthropic Claude new model release 2025 site:anthropic.com",
            "Anthropic Claude new model announcement 2025",
        ],
    },
    "gemini": {
        "name": "Gemini / Google",
        "huggingface": ["google", "google-deepmind"],
        "modelscope": [],
        "official": [
            ("https://blog.google/innovation-and-ai/technology/ai/rss/", "blog.google AI (RSS)"),
            ("https://deepmind.google/discover/blog/", "deepmind.google/blog"),
        ],
        "queries": [
            "Google Gemini new model release 2025 site:blog.google",
            "Google DeepMind Gemini new model announcement 2025",
        ],
    },
    "deepseek": {
        "name": "DeepSeek",
        "huggingface": ["deepseek-ai"],
        "modelscope": ["deepseek"],
        "official": [
            ("https://api-docs.deepseek.com/news", "api-docs.deepseek.com/news"),
            ("https://api-docs.deepseek.com/zh-cn/news", "api-docs.deepseek.com/zh-cn/news"),
        ],
        "queries": [
            "DeepSeek new model release 2025 site:api-docs.deepseek.com",
            "DeepSeek V3 R1 new model release 2025",
        ],
    },
    "qwen": {
        "name": "通义千问 / Qwen",
        "huggingface": ["Qwen"],
        "modelscope": ["Qwen"],
        "official": [
            ("https://qwen.ai/research", "qwen.ai/research"),
        ],
        "queries": [
            "Qwen new model release 2025 site:qwenlm.github.io",
            "通义千问 新模型 发布 2025",
        ],
    },
    "grok": {
        "name": "Grok / xAI",
        "huggingface": ["xai-org"],
        "modelscope": ["grok"],
        "official": [("https://docs.x.ai/docs", "docs.x.ai (Grok 文档)")],
        "queries": ["xAI Grok new model release 2025 site:x.ai", "xAI Grok 4 model announcement 2025"],
    },
    "kimi": {
        "name": "Kimi / 月之暗面",
        "huggingface": ["moonshotai"],
        "modelscope": ["Kimi"],
        "official": [
            ("https://www.moonshot.cn/", "moonshot.cn"),
            ("https://moonshotai.github.io/Kimi-K2/", "Kimi K2 官方页"),
        ],
        "queries": [
            "月之暗面 Kimi 新模型 发布 2025",
            "Moonshot AI Kimi K2 new model 2025",
        ],
    },
    "glm": {
        "name": "智谱 GLM",
        "huggingface": ["zai-org", "THUDM"],
        "modelscope": ["GLM"],
        "name_allow": [r"^glm", r"^chatglm", r"^cogv?l", r"^glm-"],
        "official": [
            ("https://docs.z.ai/", "docs.z.ai (GLM 文档)"),
            ("https://chatglm.cn/blog", "chatglm.cn/blog"),
        ],
        "queries": [
            "智谱 GLM 新模型 发布 2025",
            "Zhipu GLM-4.5 GLM-4.6 new model release 2025",
        ],
    },
    "doubao": {
        "name": "豆包 / 字节 Seed",
        "huggingface": ["ByteDance-Seed", "bytedance-community"],
        "modelscope": ["Seed-OSS"],
        "name_allow": [r"^seed-oss", r"^doubao", r"^seed(?!vr)"],
        "official": [("https://www.volcengine.com/product/doubao", "volcengine.com/product/doubao")],
        "queries": [
            "豆包 豆包大模型 新版本 发布 2025",
            "Doubao Seed new model release 2025",
        ],
    },
    "minimax": {
        "name": "MiniMax",
        "huggingface": ["MiniMaxAI", "MiniMax-Validation"],
        "modelscope": ["MiniMax"],
        "name_allow": [r"^minimax"],
        "official": [
            ("https://www.minimax.io/news", "minimax.io/news"),
            ("https://www.minimax.io/news/zh", "minimax.io/news/zh"),
        ],
        "queries": ["MiniMax 新模型 发布 2025", "MiniMax M1 M2 new model release 2025"],
    },
    "ernie": {
        "name": "文心 ERNIE / 百度",
        "huggingface": ["PaddlePaddle"],
        "modelscope": ["ERNIE"],
        "name_allow": [r"^ernie"],
        "official": [("https://cloud.baidu.com/article", "cloud.baidu.com/article")],
        "queries": [
            "百度 文心大模型 新版本 发布 2025",
            "Baidu ERNIE new model release 2025",
        ],
    },
    "cohere": {
        "name": "Cohere",
        "huggingface": ["CohereLabs", "CohereForAI"],
        "modelscope": [],
        "official": [("https://cohere.com/blog", "cohere.com/blog")],
        "queries": ["Cohere new model release 2025 site:cohere.com", "Cohere Command A new model 2025"],
    },
    "stepfun": {
        "name": "阶跃星辰 StepFun",
        "huggingface": ["stepfun-ai"],
        "modelscope": ["Step"],
        "name_allow": [r"^step-?\d", r"^step3", r"^step-audio"],
        "official": [("https://www.stepfun.com", "stepfun.com")],
        "queries": ["阶跃星辰 StepFun 新模型 发布 2025", "StepFun Step-3 new model release 2025"],
    },
    "tencent": {
        "name": "腾讯混元 Hunyuan",
        "huggingface": ["Tencent-Hunyuan", "tencent"],
        "modelscope": ["Hunyuan"],
        "name_allow": [r"^hunyuan", r"^hunyuanvideo", r"^hunyuan-"],
        "official": [
            ("https://cloud.tencent.com/developer/column/100005", "腾讯云混元专栏"),
            ("https://www.tencent.com/zh-cn/", "tencent.com 新闻公告"),
        ],
        "queries": ["腾讯混元 新模型 发布 2025", "Tencent Hunyuan new model release 2025"],
    },
    "llama": {
        "name": "Meta Llama",
        "huggingface": ["meta-llama", "facebook"],
        "modelscope": ["Meta-Llama"],
        "name_allow": [r"^llama", r"^meta-llama"],
        "official": [],  # ai.meta.com 本网络不可达；Llama 主要靠整合站 + 网页搜索
        "queries": [
            "Meta Llama new model release 2025 site:ai.meta.com",
            "Meta Llama 4 Behemoth announcement 2025",
        ],
    },
}

import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / ".model_search"
FIRECRAWL_KEY = os.environ.get("FIRECRAWL_API_KEY", "")
SINCE = datetime(2025, 1, 1, tzinfo=timezone.utc)
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


# ============================================================
# 工具函数
# ============================================================
def http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        if e.code in (429, 403, 404):
            print(f"   ⚠️  {url[:60]}: HTTP {e.code}")
            return ""  # treat as empty/no-content (404/403/429)
        raise  # other HTTP errors still propagate
    except urllib.error.URLError:
        raise  # connection/timeout errors still propagate for caller to handle


def post_json(url, payload, headers, timeout=40):
    body = json.dumps(payload).encode()
    hdrs = {"User-Agent": UA, **(headers or {})}  # 默认浏览器 UA，避免被 WAF 拦截
    req = urllib.request.Request(url, data=body, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code in (429, 403, 404, 502, 503):
            print(f"   ⚠️  API {url[:40]}: HTTP {e.code}")
            return {}
        raise
    except Exception as e:  # noqa: BLE001 — 网络超时等均视为无数据
        print(f"   ⚠️  API {url[:40]}: {type(e).__name__}")
        return {}


def strip_html(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


def clean_title(s):
    s = strip_html(s)
    return s[:160] + ("…" if len(s) > 160 else "")


def parse_date(s):
    if not s:
        return None
    s = str(s).strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
    # 标题里的前缀日期，如 "2026-07-16 Kimi K3"
    m = re.search(r"\b(20\d{2})-(\d{2})-(\d{2})\b", s)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
    # 美式："Aug 31, 2026" / "August 31 2026"
    m = re.search(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2}),?\s+(20\d{2})\b", s, re.I)
    if m:
        mon = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"].index(m.group(1).lower()[:3]) + 1
        return datetime(int(m.group(3)), mon, int(m.group(2)), tzinfo=timezone.utc)
    m = re.search(r"(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})", s, re.I)
    if m:
        mon = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"].index(m.group(2).lower()) + 1
        return datetime(int(m.group(3)), mon, int(m.group(1)), tzinfo=timezone.utc)
    return None


# 每个品牌的官网/网页搜索用关键词（小写），用于匹配发布公告标题。
BRAND_KEYWORDS = {
    "chatgpt":   ["gpt", "openai", "chatgpt"],
    "claude":    ["claude", "opus", "sonnet", "haiku", "anthropic"],
    "gemini":    ["gemini", "google", "deepmind"],
    "deepseek":  ["deepseek"],
    "qwen":      ["qwen", "千问"],
    "grok":      ["grok", "xai"],
    "kimi":      ["kimi", "moonshot"],
    "glm":       ["glm", "智谱", "chatglm", "zhipu"],
    "doubao":    ["doubao", "seed", "字节"],
    "minimax":   ["minimax", "abab"],
    "ernie":     ["ernie", "文心", "baidu", "百度"],
    "cohere":    ["cohere", "command"],
    "stepfun":   ["step", "阶跃星辰"],
    "tencent":   ["hunyuan", "混元", "腾讯"],
    "llama":     ["llama", "meta"],
}

def keyword_for(cfg, brand_id=""):
    """返回品牌的检索关键词列表（小写）。官网标题过滤 & 网页搜索均用此。"""
    kws = BRAND_KEYWORDS.get(brand_id)
    if kws:
        return kws
    # 兜底：从品牌名抽取"/" 前的词
    return [cfg["name"].split("/")[0].strip().lower()]


# ============================================================
# 渠道 1：模型整合站（Hugging Face / hf-mirror + ModelScope 魔搭）
# ============================================================
HF_BASES = ["https://huggingface.co", "https://hf-mirror.com"]  # 依次尝试，可达者胜出
MODELSCOPE_API = "https://www.modelscope.cn/api/v1/dolphin/models"


def _looks_like_model_list(raw):
    return raw.lstrip().startswith("[") and '"id"' in raw


def fetch_org_models(base, org):
    """从 HF 或其镜像拉取单个官方组织的模型清单（createdAt 降序分页，
    拉到 2025-01-01 之前的仓库即停，保证完整覆盖 2025 以后又不浪费请求）。"""
    out, cursor, base_url = [], 0, f"{base}/api/models"
    for _page in range(10):  # 每页 1000，单组织 2025 以后模型远小于 1 万
        try:
            raw = http_get(f"{base_url}?author={org}&sort=createdAt&direction=-1"
                           f"&limit=1000&offset={cursor}", timeout=30)
        except Exception as e:  # noqa: BLE001 — 网络失败时该站整体放弃
            print(f"   ⚠️  {base} (org={org}): {type(e).__name__}: {e}")
            return out
        if not _looks_like_model_list(raw):
            print(f"   ⚠️  {base} (org={org}): 响应不是模型列表（可能被网关拦截）")
            return out
        batch = json.loads(raw)
        if not batch:
            break
        out.extend(batch)
        oldest = parse_date(batch[-1].get("createdAt", ""))
        if len(batch) < 1000 or (oldest and oldest < SINCE):
            break
        cursor += len(batch)
        time.sleep(0.2)
    return out


_ORG_CACHE = {"models": {}, "base": None}


def _get_org_models(org):
    """按组织缓存模型清单；HF 官方站失败自动降级 hf-mirror.com。"""
    key = org.lower()
    if key in _ORG_CACHE["models"]:
        return _ORG_CACHE["models"][key]
    models = []
    bases = ([_ORG_CACHE["base"]] if _ORG_CACHE["base"] else []) + \
            [b for b in HF_BASES if b != _ORG_CACHE["base"]]
    for base in bases:
        models = fetch_org_models(base, org)
        if models:
            _ORG_CACHE["base"] = base
            break
    _ORG_CACHE["models"][key] = models
    return models


def hub_matches(models, brand_id, cfg, year=None):
    """按 HF 官方组织名过滤，返回 created >= 2025-01-01（可选 --year）的模型。
    models 为 None 时逐组织按需拉取（含 HF→hf-mirror 降级与缓存）。"""
    orgs = [o.lower() for o in cfg.get("huggingface", [])]
    if not orgs:
        return []
    if models is None:
        models = []
        for org in cfg.get("huggingface", []):
            got = _get_org_models(org)
            print(f"   · [HF {org}]: {len(got)} 个仓库（2025 前后）")
            models.extend(got)
    out = []
    for m in models:
        mid = m.get("id", "")
        org = mid.split("/")[0].lower() if "/" in mid else ""
        if org not in orgs:
            continue
        name = mid.split("/", 1)[1] if "/" in mid else mid
        dt = parse_date(m.get("createdAt", ""))
        if not dt:
            continue
        if dt < SINCE or (year and dt.year != int(year)):
            continue
        # 排除量化/转发变体与非 LLM 条目，只保留官方主仓库
        if _is_quant_variant(name):
            continue
        if not _name_allowed(name, cfg):
            continue
        if not _looks_like_llm(name, m):
            continue
        out.append({
            "brand": brand_id,
            "brand_name": cfg["name"],
            "source": "huggingface",
            "source_url": f"https://huggingface.co/{mid.split('/')[0]}",
            "model_id": mid,
            "title": name,
            "url": f"https://huggingface.co/{mid}",
            "published": dt.strftime("%Y-%m"),
            "year": dt.year,
            "context": None,
            "price_input_per_m": None,
            "price_output_per_m": None,
            "description": f"tags: {', '.join((m.get('tags') or [])[:8])}",
        })
    return out


def _is_quant_variant(name):
    """识别 GGUF/GPTQ/AWQ 等量化转发仓库，避免污染「新模型」列表。"""
    n = name.lower()
    return bool(re.search(
        r"(-gguf|\bawq\b|\bgptq\b|exl2|hqq|int[48]|4.?bit|8.?bit|-i?q\d_|mlx"
        r"|w[48]a[488]|a[48]w[48]|w4a16|unsloth|bartowski|lmstudio|comfy|tflite"
        r"|onnx|openvino|-nvfp4|-bf16|-fp[48]|pruned)", n))


# 全局名称黑名单：视觉/语音/检索等非对话 LLM 仓库
_NAME_DENY_RE = re.compile(
    r"(?i)(video|t2v|i2v|v2a|audio|music|speech|tts|asr|ocr|whisper|dino"
    r"|sam\d|segment|embedding|rerank|retriev|guard|proxy|voice|image|seedvr)")


def _name_allowed(name, cfg):
    """名称白/黑名单：先过全局黑名单，再要求命中品牌自己的 allow 模式。"""
    if _NAME_DENY_RE.search(name):
        return False
    allow = cfg.get("name_allow") or []
    if not allow:
        return True
    return any(re.search(rf"(?i){p}", name) for p in allow)


def _looks_like_llm(name, m):
    """过滤明显不是 LLM 的条目（embedding/ASR/分类头/图像小仓库等）。"""
    tags = [t.lower() for t in (m.get("tags") or [])]
    bad = ("text-classification", "token-classification", "sentence-similarity",
           "feature-extraction", "reinforcement-learning", "fill-mask",
           "automatic-speech-recognition", "text-to-audio", "audio-classification",
           "text-to-speech", "image-classification", "object-detection",
           "text-to-image", "image-text-to-image", "text-to-video")
    if any(t in tags for t in bad):
        return False
    if (m.get("pipeline_tag") or "") in bad:
        return False
    # 官方 LLM 仓库名几乎都带数字版本号（GPT-5 / Llama 4 / Step-3 …）
    return bool(re.search(r"\d", name))


# ------------------------------------------------------------
# ModelScope 魔搭社区（www.modelscope.cn）—— 覆盖国内品牌官方仓库
# ------------------------------------------------------------
_MS_BAD_TASKS = ("text-classification", "token-classification", "sentence-similarity",
                 "feature-extraction", "fill-mask", "automatic-speech-recognition",
                 "text-to-audio", "audio-classification", "text-to-speech",
                 "image-classification", "object-detection", "text-to-image",
                 "image-text-to-image", "text-to-video", "image-to-video",
                 "video-generation", "text-to-3d", "anytoany")


def _looks_like_llm_ms(name, m):
    """ModelScope 版本：Tags/Tasks 判定 + 名称启发式。"""
    tags = [str(t).lower() for t in (m.get("Tags") or [])]
    tasks = [str(t).lower() for t in (m.get("Tasks") or [])]
    if any(t in tags or t in tasks for t in _MS_BAD_TASKS):
        return False
    return bool(re.search(r"\d", name))


def _kw_relevant(keyword, path, name):
    """魔搭关键词命中的非官方组织结果，要求属主或名称真的与该系列相关。"""
    kw = re.sub(r"[^a-z0-9]", "", keyword.lower())
    blob = re.sub(r"[^a-z0-9]", "", (path + name).lower())
    if not kw:
        return False
    return kw in blob or kw.rstrip("s") in blob


def modelscope_matches(keyword, brand_id, cfg, year=None):
    """魔搭按关键词搜索，返回 CreatedTime >= 2025-01-01 的官方/强相关模型。"""
    items, page = [], 1
    while page <= 6:  # 最多 600 条
        body = {"Name": keyword, "PageSize": 100, "PageNumber": page}
        try:
            data = post_json(MODELSCOPE_API, body,
                             {"Content-Type": "application/json"}, timeout=20)
        except Exception as e:  # noqa: BLE001 — 网络错误时用已收集的页继续
            print(f"   ⚠️  modelscope[{keyword}] p{page}: {type(e).__name__}: {e}")
            break
        batch = (data.get("Data") or {}).get("Model", {}).get("Models", []) or []
        if not batch:
            break
        items.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        time.sleep(0.2)

    official = {o.lower() for o in cfg.get("huggingface", [])}
    out = []
    for m in items:
        path = (m.get("Path") or "").lower()
        name = m.get("Name") or ""
        ct = m.get("CreatedTime") or 0
        dt = datetime.fromtimestamp(ct, tz=timezone.utc) if ct else None
        if not dt or dt < SINCE or (year and dt.year != int(year)):
            continue
        if _is_quant_variant(name):
            continue
        if not _name_allowed(name, cfg):
            continue
        is_official = path in official
        if not is_official and not _kw_relevant(keyword, path, name):
            continue
        if not _looks_like_llm_ms(name, m):
            continue
        url = f"https://www.modelscope.cn/models/{path}/{name}" if path else ""
        out.append({
            "brand": brand_id,
            "brand_name": cfg["name"],
            "source": "modelscope",
            "source_url": f"魔搭社区/{path}" if path else "魔搭社区",
            "model_id": f"{path}/{name}" if path else name,
            "title": name,
            "url": url,
            "published": dt.strftime("%Y-%m"),
            "year": dt.year,
            "context": None,
            "price_input_per_m": None,
            "price_output_per_m": None,
            "description": ("官方组织" if is_official else "") + f"owner: {path or '?'}".strip(" "),
        })
    return out


def hub_and_modelscope(cfg, brand_id, year=None):
    """整合站总入口：HF 官方组织 + 魔搭关键词，返回该品牌 2025 年以后的模型。"""
    out = hub_matches(None, brand_id, cfg, year=year)
    for kw in cfg.get("modelscope", []):
        hits = modelscope_matches(kw, brand_id, cfg, year=year)
        if hits:
            print(f"      · [魔搭 {kw}]: {len(hits)} 个")
        out.extend(hits)
    return out

# ============================================================
# 渠道 2：品牌官网 / RSS
# ============================================================
def parse_rss(xml_text):
    """极简 RSS/Atom 解析，不依赖第三方库。"""
    items = []
    for m in re.finditer(r"<(item|entry)[^>]*>(.*?)</\1>", xml_text, re.S | re.I):
        block = m.group(2)

        def g(tag, block=block):
            mm = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", block, re.S | re.I)
            if not mm:
                return ""
            v = mm.group(1)
            cdata = re.match(r"<!\[CDATA\[(.*?)\]\]>", v, re.S)
            return cdata.group(1) if cdata else v

        title = strip_html(g("title"))
        lm = re.search(r"<link[^>]*href=[\"']([^\"']+)[\"']", block, re.I)
        if lm:
            link = lm.group(1)
        else:
            lm2 = re.search(r"<link[^>]*>([^<]+)</link>", block, re.I)
            link = lm2.group(1).strip() if lm2 else ""
        pub = g("pubDate") or g("published") or g("updated") or g("date")
        items.append({"title": title, "url": link, "published": pub.strip()})
    return items


def scrape_official(url, label, brand_id, brand_name, keyword, year=None, title_allow=None):
    """抓品牌官网页面/RSS，提取含模型关键词 + 2025 以后年份的条目。"""
    results = []
    try:
        text = http_get(url, timeout=20)
    except Exception as e:  # noqa: BLE001 — 任何网络错误都只警告跳过
        print(f"   ⚠️  {label}: {type(e).__name__}: {e}")
        return results

    is_feed = "<rss" in text[:300] or "<feed" in text[:300]
    items = parse_rss(text) if is_feed else []
    if not items:  # HTML：抽 <a> 链接及其文本
        seen = set()
        for m in re.finditer(r"<a[^>]+href=[\"']([^\"'#]+)[\"'][^>]*>(.*?)</a>", text, re.S | re.I):
            href, t = m.group(1), clean_title(m.group(2))
            if not t or len(t) < 8 or t in seen:
                continue
            if href.startswith("/"):\
                href = urllib.parse.urljoin(url, href)
            elif not href.startswith("http"):
                href = urllib.parse.urljoin(url, href)
            if not href.startswith("http"):
                continue
            seen.add(t)
            items.append({"title": t, "url": href, "published": ""})

       # keyword_for() may return a list of keywords
    kws = keyword if isinstance(keyword, list) else [keyword]
    for it in items:
        t = it["title"]
        if not t:
            continue
        if not any(kw in t.lower() for kw in kws):
            continue
        # 品牌专属白名单（如 ChatGPT 只保留模型发布类标题）
        if title_allow and not title_allow.search(t):
            continue
        dt = parse_date(it.get("published", "")) or parse_date(t)
        if dt:
            if dt < SINCE or (year and dt.year != int(year)):
                continue
            ymd, y = dt.strftime("%Y-%m-%d"), dt.year
        else:
            yrs = re.findall(r"\b(20\d{2})\b", t)
            if year:
                yrs = [yy for yy in yrs if yy == str(year)]
            if not yrs or int(yrs[0]) < 2025:
                continue
            y, ymd = int(yrs[0]), f"{yrs[0]}（标题标注）"
        results.append({
            "brand": brand_id, "brand_name": brand_name, "source": "official",
            "source_url": label, "title": t, "url": it["url"],
            "published": ymd, "year": y, "context": None,
            "price_input_per_m": None, "price_output_per_m": None,
            "description": "",
        })
    print(f"   ✓ {label}: {len(results)} 条命中（扫描 {len(items)} 条链接）")
    return results



# ============================================================
# 渠道 3/4：Firecrawl / DuckDuckGo 搜索兜底
# ============================================================
def firecrawl_search(query, limit=5):
    if not FIRECRAWL_KEY:
        return []
    data = post_json(
        "https://api.firecrawl.dev/v1/search",
        {"query": query, "limit": limit},
        {"Authorization": f"Bearer {FIRECRAWL_KEY}", "Content-Type": "application/json"},
    )
    items = data.get("data", []) or data.get("results", [])
    # 避免 Firecrawl API 限流：请求之间适当间隔（2.5s 平衡速度与限流）
    time.sleep(2.5)
    return [{
        "title": clean_title(it.get("title", "")),
        "url": it.get("url", it.get("link", "")),
        "published": it.get("published_at", it.get("date", "")) or "",
    } for it in items]


def duckduckgo_search(query, limit=5):
    try:
        raw = http_get("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query), timeout=15)
    except Exception:  # noqa: BLE001 — 网络被墙时直接放弃该渠道
        return []
    out = []
    for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', raw, re.S):
        href = html.unescape(m.group(1))
        uddg = re.search(r"uddg=([^&]+)", href)
        if uddg:
            href = urllib.parse.unquote(uddg.group(1))
        out.append({"title": clean_title(m.group(2)), "url": href, "published": ""})
        if len(out) >= limit:
            break
    return out


def web_search(brand_id, cfg, year=None):
    results = []
    ytag = str(year) if year else "2025"
    keywords = keyword_for(cfg, brand_id)
    for q in cfg["queries"]:
        got = firecrawl_search(q) if FIRECRAWL_KEY else []
        engine = "Firecrawl"
        if not got:
            got, engine = duckduckgo_search(q), "DuckDuckGo"
        for it in got:
            t, u = it.get("title", ""), it.get("url", "")
            if not u or not t:
                continue
            tl = t.lower()
            if not any(kw in tl for kw in keywords):
                continue
            if "site:" in q:
                site = q.split("site:")[1].strip()
                host = urllib.parse.urlparse(u).netloc.lower()
                if host != site and not host.endswith("." + site):
                    continue
            dt = parse_date(it.get("published", "")) or parse_date(t)
            if dt:
                if dt < SINCE or (year and dt.year != int(year)):
                    continue
                ymd, y = dt.strftime("%Y-%m"), dt.year
            else:
                # 标题无日期：从标题或 query 中提取年份，否则跳过
                yrs = re.findall(r"\b(20\d{2})\b", t)
                if not yrs:
                    yrs = re.findall(r"\b(20\d{2})\b", q)  # fallback: 从 query 取年份
                if year:
                    yrs = [x for x in yrs if x == str(year)]
                if not yrs or int(yrs[0]) < 2025:
                    continue
                y, ymd = int(yrs[0]), f"{yrs[0]}（标题标注）"
            results.append({
                "brand": brand_id, "brand_name": cfg["name"], "source": "web",
                "source_url": engine, "title": t, "url": u,
                "published": ymd, "year": y, "context": None,
                "price_input_per_m": None, "price_output_per_m": None,
                "description": "",
            })
        time.sleep(0.3)
    return results

# ============================================================
# 去重 & 输出
# ============================================================
def dedup(results):
    seen, out = set(), []
    for r in results:
        key = r["url"].rstrip("/").lower() or r["title"].lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def write_report(results, brands_run, year=None):
    lines = [
        "# 大模型发布追踪（2025-01-01 以后）",
        "",
        f"_生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        f"_品牌：{', '.join(brands_run)}_" + (f" ｜ _年份：{year}_" if year else ""),
        "",
    ]
    for bid in brands_run:
        rows = [r for r in results if r["brand"] == bid]
        if not rows:
            lines.append(f"## {CHANNELS[bid]['name']}\n\n_无命中（整合站无该品牌仓库，官网未公开或网络不可达）_\n")
            continue
        lines.append(f"## {CHANNELS[bid]['name']}（{len(rows)} 条）\n")
        hrows = [r for r in rows if r["source"] == "huggingface"]
        if hrows:
            lines += ["### Hugging Face（官方组织仓库，HF 官方站或 hf-mirror.com 镜像）", "",
                      "| 模型 | 创建时间 | 组织 |",
                      "|------|----------|------|"]
            for r in hrows:
                lines.append(f"| [{r['title']}]({r['url']}) | {r['published']} | "
                             f"{r['model_id'].split('/')[0]} |")
            lines.append("")
        mrows = [r for r in rows if r["source"] == "modelscope"]
        if mrows:
            lines += ["### ModelScope 魔搭（国内整合站）", "",
                      "| 模型 | 创建时间 | 所属组织 |",
                      "|------|----------|----------|"]
            for r in mrows:
                lines.append(f"| [{r['title']}]({r['url']}) | {r['published']} | "
                             f"{r['model_id'].split('/')[0] if '/' in r['model_id'] else '—'} |")
            lines.append("")
        brows = [r for r in rows if r["source"] not in ("huggingface", "modelscope")]
        if brows:
            lines += ["### 官网 / 网页搜索", ""]
            for r in brows:
                pub = f"（{r['published']}）" if r["published"] else ""
                lines.append(f"- [{r['title']}]({r['url']}){pub} — _来源：{r['source_url']}_")
            lines.append("")
    out = OUT_DIR / "report.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n📝 报告已写入 {out}")


def main():
    ap = argparse.ArgumentParser(description="搜索品牌下 2025 年以后发布的大模型")
    ap.add_argument("--brand", help="只搜一个或多个品牌（id 见 CHANNELS，同 data/brands.yaml；多个用英文逗号分隔，如 --brand chatgpt,claude）")
    ap.add_argument("--year", type=int, help="限定年份，如 --year 2025（默认 2025-01-01 以后全部）")
    ap.add_argument("--no-search", action="store_true", help="只用模型整合站（HF/魔搭），跳过官网与网页搜索")
    args = ap.parse_args()

    OUT_DIR.mkdir(exist_ok=True)
    if args.brand:
        bids = [b.strip() for b in args.brand.split(",") if b.strip()]
        unknown = [b for b in bids if b not in CHANNELS]
        if unknown:
            ap.error(f"未知品牌 id: {', '.join(unknown)}（可用: {', '.join(CHANNELS)}）")
        brands = {b: CHANNELS[b] for b in bids}
    else:
        brands = CHANNELS
    brands_run = list(brands.keys())
    all_results = []

    # --- 渠道 1：模型整合站（HF/镜像 + 魔搭） ---
    for bid, cfg in brands.items():
        got = hub_and_modelscope(cfg, bid, year=args.year)
        print(f"   ✓ {cfg['name']}: {len(got)} 个模型")
        all_results.extend(got)

     # --- 渠道 2 + 3/4 ---
    if not args.no_search:
        print("\n🌐 [官网/RSS] 抓取各品牌官方发布页…")
        for bid, cfg in brands.items():
            print(f"   → {cfg['name']}")
            for url, label in cfg["official"]:
                all_results.extend(scrape_official(url, label, bid, cfg["name"],
                                                   keyword_for(cfg, bid), year=args.year,
                                                   title_allow=cfg.get("title_allow")))

        print("\n🔍 [网页搜索] 补齐 / 丰富各品牌资料…")
        for bid, cfg in brands.items():
            got = web_search(bid, cfg, year=args.year)
            print(f"   ✓ {cfg['name']}: {len(got)} 条")
            all_results.extend(got)

    results = dedup(all_results)
    results.sort(key=lambda r: (r["brand"], -(r["year"] or 0), r["published"]))

    data_file = OUT_DIR / "results.json"
    data_file.write_text(json.dumps({
        "generated_at": datetime.now().isoformat(),
        "since": SINCE.strftime("%Y-%m-%d"),
        "year_filter": args.year,
        "total": len(results),
        "results": results,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n💾 结果已写入 {data_file}（共 {len(results)} 条）")

    write_report(results, brands_run, year=args.year)

    print("\n📊 各品牌命中统计：")
    by_brand = {}
    for r in results:
        by_brand[r["brand"]] = by_brand.get(r["brand"], 0) + 1
    for bid in brands_run:
        print(f"   {CHANNELS[bid]['name']:<22} {by_brand.get(bid, 0)}")
    print("\n✅ 完成。详情见 .model_search/report.md")


if __name__ == "__main__":
    main()

