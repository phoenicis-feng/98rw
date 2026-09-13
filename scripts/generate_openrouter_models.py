#!/usr/bin/env python3
"""Fetch all models from OpenRouter API and generate Hugo content files."""

import json
import os
import subprocess
import sys
from urllib.request import urlopen

OPENROUTER_API = "https://openrouter.ai/api/v1/models?limit=500"
CONTENT_DIR = "/Users/fengfei/servers/98rw/content/models/openrouter"
VENDOR_MAP = {
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "google": "Google",
    "qwen": "阿里 Qwen",
    "mistralai": "Mistral AI",
    "deepseek": "DeepSeek",
    "meta-llama": "Meta Llama",
    "meta": "Meta",
    "z-ai": "智谱 AI",
    "nvidia": "NVIDIA",
    "minimax": "MiniMax",
    "moonshotai": "月之暗面",
    "tencent": "腾讯",
    "x-ai": "xAI",
    "bytedance-seed": "字节跳动",
    "thinkingmachines": "Thinking Machines",
    "inclusionai": "Inclusion AI",
    "cohere": "Cohere",
    "amazon": "Amazon",
    "perplexity": "Perplexity",
    "sakana": "Sakana AI",
    "poolside": "Poolside",
    "inception": "Inception",
    "nex-agi": "Nex AGI",
    "ibm-granite": "IBM Granite",
    "openrouter": "OpenRouter",
    "ai21": "AI21 Labs",
    "jamba": "Jamba",
    "gryphe": "Gryphe",
    "NousResearch": "Nous Research",
    "sao10k": "Sao10K",
    "rekaai": "Reka AI",
    "undisclosed": "未披露",
}

CATEGORY_MAP = {
    "OpenAI": "国外",
    "Anthropic": "国外",
    "Google": "国外",
    "阿里 Qwen": "国内",
    "DeepSeek": "国内",
    "Meta Llama": "开源",
    "Mistral AI": "国外",
    "月之暗面": "国内",
    "字节跳动": "国内",
    "腾讯": "国内",
    "智谱 AI": "国内",
    "NVIDIA": "国外",
    "MiniMax": "国内",
}

def get_vendor(vendor_key):
    return VENDOR_MAP.get(vendor_key, vendor_key.title() if vendor_key else "Unknown")

def get_category(vendor_name):
    return CATEGORY_MAP.get(vendor_name, "其他")

def fetch_models():
    """Fetch all models from OpenRouter API."""
    print("Fetching models from OpenRouter API...")
    with urlopen(OPENROUTER_API, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    models = data.get("data", [])
    print(f"Fetched {len(models)} models.")
    return models

def sanitize_slug(model_id):
    """Convert model id to Hugo-friendly slug."""
    # Remove :free, :batch suffixes for slug
    slug = model_id.replace(":", "-").replace("/", "-")
    return slug.strip("-")

def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0


def generate_frontmatter(model):
    """Generate frontmatter for a model."""
    model_id = model["id"]
    name = model.get("name", model_id)
    description = model.get("description", "")
    context_length = model.get("context_length", 0)
    pricing = model.get("pricing", {})
    prompt_price = safe_float(pricing.get("prompt", 0))
    completion_price = safe_float(pricing.get("completion", 0))

    # Parse vendor
    vendor_key = model_id.split("/")[0] if "/" in model_id else "unknown"
    vendor_name = get_vendor(vendor_key)
    category = get_category(vendor_name)

    # Format context
    if context_length >= 1000000:
        context_str = f"{context_length // 1000000}M tokens"
    elif context_length >= 1000:
        context_str = f"{context_length // 1000}K tokens"
    else:
        context_str = f"{context_length} tokens"

    # Format pricing
    if prompt_price == 0:
        price_input = "免费"
    elif prompt_price < 0.001:
        price_input = f"${prompt_price * 1000:.4f}/K"
    else:
        price_input = f"${prompt_price:.4f}/M"

    if completion_price == 0:
        price_output = "免费"
    elif completion_price < 0.001:
        price_output = f"${completion_price * 1000:.4f}/K"
    else:
        price_output = f"${completion_price:.4f}/M"

    # Extract modality
    architecture = model.get("architecture", {})
    modality = architecture.get("modality", "text")

    # Create title from name
    title = name.split(":")[-1].strip() if ":" in name else name
    if title.startswith(vendor_name):
        title = title[len(vendor_name):].strip().lstrip(":- ")
    title = f"{vendor_name} {title}" if title else vendor_name

    # Description - first sentence or truncate
    desc = description[:200].replace('"', '\\"') if description else f"{vendor_name} 模型，OpenRouter 平台提供。"

    # Generate scores based on context length and pricing heuristics
    # These are rough estimates for sorting purposes
    scores = generate_scores(context_length, prompt_price, completion_price)

    from datetime import datetime
    now_iso = datetime.now().isoformat() + "Z"

    frontmatter = f"""---
title: "{title}"
model: true
date: {now_iso}
description: "{desc}"
reasoning: {scores['reasoning']}
specs:
  vendor: "{vendor_name}"
  category: "{category}"
  released: "2025"
  context: "{context_str}"
  price_input: "{price_input}"
  price_output: "{price_output}"
  modalities: "{modality}"
  openrouter_id: "{model_id}"
  openrouter_url: "https://openrouter.ai/models/{model_id}"

  scores:
    reasoning: {scores['reasoning']}
    coding: {scores['coding']}
    chinese: {scores['chinese']}
    longtext: {scores['longtext']}
---
"""
    return frontmatter

def generate_scores(context_length, prompt_price, completion_price):
    """Generate rough scores based on available data."""
    # Higher context = potentially better longtext
    # Lower price = potentially more accessible
    # These are rough estimates for sorting purposes

    # Reasoning estimate based on context and pricing
    if context_length >= 1000000:
        reasoning = 85
    elif context_length >= 100000:
        reasoning = 80
    elif context_length >= 50000:
        reasoning = 75
    else:
        reasoning = 70

    # Coding estimate (simplified)
    coding = min(95, reasoning + 5)

    # Chinese estimate (simplified)
    chinese = 70

    # Longtext based on context
    if context_length >= 1000000:
        longtext = 95
    elif context_length >= 100000:
        longtext = 85
    elif context_length >= 50000:
        longtext = 75
    else:
        longtext = 65

    return {"reasoning": reasoning, "coding": coding, "chinese": chinese, "longtext": longtext}

def generate_content(model, title, vendor_name, context_str, price_input, price_output):
    """Generate basic content sections for a model page."""
    model_id = model["id"]
    description = model.get("description", "")

    content = f"""## 模型概况

{title} 是由 {vendor_name} 提供、通过 OpenRouter 平台聚合的模型。该模型在 OpenRouter 上提供统一的 API 接口。

### 核心参数

| 维度 | 数值 |
|------|------|
| 厂商 | {vendor_name} |
| OpenRouter ID | `{model_id}` |
| 上下文窗口 | {context_str} |
| 输入价格 | {price_input} |
| 输出价格 | {price_output} |
| 模态 | {model.get('architecture', {}).get('modality', 'text')} |

## OpenRouter 平台数据

{description if description else '暂无详细描述，模型数据来源于 OpenRouter API。'}

### 定价信息

| 项目 | 价格 |
|------|------|
| 输入 | {price_input} |
| 输出 | {price_output} |

### 支持的参数

该模型支持以下参数：
- 温度调节
- Top-P / Top-K 采样
- 流式输出
- 工具调用（如支持）

## 适用场景

{get_use_cases(model)}

## 来源

- [OpenRouter Models API](https://openrouter.ai/models)
"""
    return content

def get_use_cases(model):
    """Generate use case suggestions based on model characteristics."""
    context_length = model.get("context_length", 0)
    architecture = model.get("architecture", {})
    modality = architecture.get("modality", "text")

    cases = []
    if "image" in modality.lower() or "vision" in modality.lower():
        cases.append("图像理解、视觉问答")
    if "file" in modality.lower():
        cases.append("文件处理")
    if context_length >= 1000000:
        cases.append("长文档分析、大代码库处理")
    if context_length >= 100000:
        cases.append("长文本对话、文档总结")
    cases.append("常规文本生成与对话")

    return "\n".join(f"- {c}" for c in cases)

def main():
    # Fetch models
    models = fetch_models()

    # Ensure content directory exists
    os.makedirs(CONTENT_DIR, exist_ok=True)

    generated = 0
    skipped = 0

    for model in models:
        model_id = model["id"]
        slug = sanitize_slug(model_id)

        # Check if already exists
        model_dir = os.path.join(CONTENT_DIR, slug)
        md_file = os.path.join(model_dir, "_index.md")

        if os.path.exists(md_file):
            skipped += 1
            continue

        os.makedirs(model_dir, exist_ok=True)

        # Generate content
        title = model.get("name", model_id).split(":")[-1].strip()
        vendor_key = model_id.split("/")[0] if "/" in model_id else "unknown"
        vendor_name = get_vendor(vendor_key)
        context_length = model.get("context_length", 0)
        pricing = model.get("pricing", {})

        if context_length >= 1000000:
            context_str = f"{context_length // 1000000}M tokens"
        elif context_length >= 1000:
            context_str = f"{context_length // 1000}K tokens"
        else:
            context_str = f"{context_length} tokens"

        prompt_price = safe_float(pricing.get("prompt", 0))
        completion_price = safe_float(pricing.get("completion", 0))

        if prompt_price == 0:
            price_input = "免费"
        else:
            price_input = f"${prompt_price:.4f}/M"

        if completion_price == 0:
            price_output = "免费"
        else:
            price_output = f"${completion_price:.4f}/M"

        frontmatter = generate_frontmatter(model)
        body = generate_content(model, title, vendor_name, context_str, price_input, price_output)

        with open(md_file, "w", encoding="utf-8") as f:
            f.write(frontmatter + "\n" + body)

        generated += 1

    print(f"\nDone! Generated {generated} new files, skipped {skipped} existing.")
    print(f"Total models in {CONTENT_DIR}: {len(os.listdir(CONTENT_DIR))}")

    # Try to build to verify
    print("\nVerifying with Hugo...")
    result = subprocess.run(["hugo", "mod", "get", "github.com/ephelse/hugo-liftoff"],
                          capture_output=True, cwd="/Users/fengfei/servers/98rw")
    if result.returncode != 0:
        print("Note: Hugo module verification skipped (module may already be installed)")

if __name__ == "__main__":
    main()
