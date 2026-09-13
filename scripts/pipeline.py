#!/usr/bin/env python3
"""
Daily Content Pipeline
==============================
1. Search  → firecrawl → raw.json
2. Translate + Structure → Cloudflare AI → structured.json
3. Dedup + Polish → Cloudflare AI → polished.json
4. Generate Hugo MD → content/posts/
5. Validate → git push
"""

import json
import os
import sys
import urllib.request
import urllib.error
import hashlib
import re
from datetime import datetime, timedelta

# === Config ===
ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
MODEL = "@cf/openai/gpt-oss-120b"
FIRECRAWL_KEY = os.environ.get("FIRECRAWL_API_KEY", "")
BASE_DIR = os.getcwd()
DATE_STR = datetime.now().strftime("%Y-%m-%d")

TMPDIR = os.path.join(BASE_DIR, ".pipeline_tmp")
os.makedirs(TMPDIR, exist_ok=True)

def api_call(url, headers, data):
    """Generic API call helper"""
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"❌ API Error {e.code}: {e.read().decode()[:500]}")
        sys.exit(1)

def cf_ai(prompt, max_tokens=3000):
    """Call Cloudflare Workers AI"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODEL}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    return api_call(url, headers, {"prompt": prompt, "max_tokens": max_tokens})

def firecrawl_search(query, limit=5):
    """Call Firecrawl search API"""
    url = "https://api.firecrawl.dev/v1/search"
    headers = {"Authorization": f"Bearer {FIRECRAWL_KEY}", "Content-Type": "application/json"}
    data = {"query": query, "limit": limit, "temporalScope": "day"}
    return api_call(url, headers, data)

# === Step 1: Search ===
def step1_search():
    print("🔍 Step 1: Searching...")
    with open(os.path.join(BASE_DIR, "targets.json")) as f:
        targets = json.load(f)

    raw_results = []
    for target in targets["targets"]:
        query = target["search_query"]
        limit = targets["settings"]["max_results_per_target"]
        print(f"   → Searching: {target['name']}")
        try:
            result = firecrawl_search(query, limit)
            items = result.get("result", {}).get("content", result.get("result", {}).get("items", []))
            for item in items:
                raw_results.append({
                    "source": target["name"],
                    "url": item.get("url", item.get("link", "")),
                    "title": item.get("title", ""),
                    "description": item.get("description", item.get("content", "")),
                    "published_at": item.get("published_at", item.get("date", "")),
                    "raw_content": item.get("raw_content", item.get("content", "")),
                    "content": item.get("content", ""),
                    "image_url": item.get("image", item.get("image_url", ""))
                })
        except Exception as e:
            print(f"   ⚠️  {target['name']}: {e}")

    raw_data = {
        "generated_at": datetime.now().isoformat(),
        "total_results": len(raw_results),
        "results": raw_results
    }

    with open(os.path.join(TMPDIR, "raw.json"), "w") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)

    print(f"   ✅ Found {len(raw_results)} articles")
    return raw_data

# === Step 2: Translate + Structure ===
def step2_structure(raw_data):
    print("✍️ Step 2: Translating & structuring...")

    results_text = "\n".join([
        f"[{i+1}] 标题: {r['title']}\nURL: {r['url']}\n摘要: {r['description']}\n来源: {r['source']}\n时间: {r['published_at']}"
        for i, r in enumerate(raw_data["results"])
    ])

    prompt = f"""你是AI新闻编辑。请将以下搜索结果转换为结构化JSON。

搜索结果：
{results_text}

输出一个JSON对象，格式如下：
{{
  "articles": [
    {{
      "id": "唯一标识",
      "title": "中文标题",
      "url": "原始链接",
      "source": "来源名称",
      "published_at": "发布时间",
      "summary": "100字以内的中文摘要",
      "category": "分类标签（如：模型发布、开源、行业动态、监管等）",
      "fact_summary": "事实性内容总结（仅陈述已确认的事实）",
      "inference": "基于事实的推测（如有）",
      "commentary": "评论/观点（如有）",
      "toc_entries": ["## 要点1", "## 要点2", "## 值得关注"],
      "has_table": true/false,
      "has_code": true/false
    }}
  ],
  "toc": ["## 分类1", "## 分类2", "## 值得关注"],
  "categories": ["模型发布", "行业动态", "开源"]
}}

要求：
- 按类别分组
- 每个条目必须有 title, url, source, summary
- 不要捏造原文没有的信息
- 明确区分 fact_summary（事实）、inference（推测）、commentary（评论）
- 保留原始URL
- 如果某条结果不适合做文章，直接跳过"""

    result = cf_ai(prompt)
    text = result.get("result", {}).get("choices", [{}])[0].get("text", "")

    # Parse JSON from AI response
    try:
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            structured = json.loads(json_match.group())
        else:
            structured = {"articles": [], "toc": [], "categories": []}
    except json.JSONDecodeError:
        structured = {"articles": [], "toc": [], "categories": []}

    with open(os.path.join(TMPDIR, "structured.json"), "w") as f:
        json.dump(structured, f, ensure_ascii=False, indent=2)

    print(f"   ✅ Structured {len(structured.get('articles', []))} articles")
    return structured

# === Step 3: Dedup + Polish ===
def step3_polish(structured):
    print("✍️ Step 3: Dedup & polishing...")

    articles_text = json.dumps(structured.get("articles", []), ensure_ascii=False, indent=2)
    existing_urls = set()

    # Check existing posts for duplicates
    posts_dir = os.path.join(BASE_DIR, "content", "posts")
    if os.path.exists(posts_dir):
        for fname in os.listdir(posts_dir):
            if fname.endswith(".md"):
                # Extract URL from frontmatter would be ideal, but for now just skip
                pass

    prompt = f"""你是资深AI新闻编辑。请对以下文章列表进行去重和润色。

文章列表（JSON）：
{articles_text}

已有文章的URL集合（去重用）：
{json.dumps(list(existing_urls))}

要求：
1. 去重：删除标题或URL高度相似的文章
2. 保留原文所有事实信息，不要捏造
3. 明确区分事实、推测、评论
4. 保留原始链接
5. 润色中文表达，使其自然流畅
6. 确认每篇文章都有：title, url, source, summary, category

输出完整的JSON数组：
[
  {{
    "title": "...",
    "url": "...",
    "source": "...",
    "category": "...",
    "summary": "...",
    "fact_summary": "...",
    "inference": "...",
    "commentary": "...",
    "toc_entries": ["..."],
    "has_table": true/false,
    "has_code": true/false,
    "reference_url": "原始链接"
  }}
]"""

    result = cf_ai(prompt)
    text = result.get("result", {}).get("choices", [{}])[0].get("text", "")

    try:
        json_match = re.search(r'\[.*\]', text, re.DOTALL)
        if json_match:
            polished = json.loads(json_match.group())
        else:
            polished = []
    except json.JSONDecodeError:
        polished = []

    with open(os.path.join(TMPDIR, "polished.json"), "w") as f:
        json.dump(polished, f, ensure_ascii=False, indent=2)

    print(f"   ✅ {len(polished)} articles after polish")
    return polished

# === Step 4: Generate Hugo MD ===
def step4_generate_md(polished):
    print("✍️ Step 4: Generating Hugo posts...")

    posts_dir = os.path.join(BASE_DIR, "content", "posts")
    os.makedirs(posts_dir, exist_ok=True)

    posts_generated = []

    for article in polished:
        # Build TOC from article's toc_entries or categories
        toc_items = article.get("toc_entries", [article.get("category", "内容")])
        toc_items_str = "\n".join([f"## {t}" for t in toc_items])
        toc_html = "\n".join([f"{'  ' * i}- [{t}](#{t.lower().replace(' ', '-')})" for i, t in enumerate(toc_items)])

        # Build reference links
        ref_links = []
        if article.get("reference_url"):
            ref_links.append(f"- [{article['title']}]({article['reference_url']})")
        # Also add source link
        if article.get("url"):
            ref_links.append(f"- [原文链接]({article['url']})")

        # Build content sections
        sections = []
        sections.append(f"## {article.get('category', '内容')}")
        sections.append(f"\n{article.get('fact_summary', article.get('summary', ''))}\n")

        if article.get("inference"):
            sections.append(f"\n### 分析与推测\n{article['inference']}\n")
        if article.get("commentary"):
            sections.append(f"\n### 评论与观点\n{article['commentary']}\n")

        sections.append(f"\n### 参考来源\n")
        sections.extend(ref_links)

        content = "\n".join(sections)

        # Generate slug from title
        slug = re.sub(r'[^\w\s-]', '', article['title']).strip().lower()
        slug = re.sub(r'[\s]+', '-', slug)[:50]
        post_filename = f"{DATE_STR}-{slug}.md"
        post_path = os.path.join(posts_dir, post_filename)

        # Check if file already exists (avoid overwrite)
        if os.path.exists(post_path):
            print(f"   ⏭️  Skipping (exists): {post_filename}")
            continue

        frontmatter = f"""---
title: "{article['title']}"
date: "{DATE_STR}"
layout: "post"
description: "{article.get('summary', '')[:200]}"
tags: ["{article.get('category', 'AI')}", "daily"]
author: "AI日报"
---

{toc_items_str}

{content}
"""

        with open(post_path, "w") as f:
            f.write(frontmatter)

        posts_generated.append(post_filename)
        print(f"   ✅ Generated: {post_filename}")

    return posts_generated

# === Step 5: Validate ===
def step5_validate(posts_generated):
    print("🔍 Step 5: Validating...")
    errors = []

    # Check: files exist and not empty
    posts_dir = os.path.join(BASE_DIR, "content", "posts")
    for fname in posts_generated:
        fpath = os.path.join(posts_dir, fname)
        if not os.path.exists(fpath):
            errors.append(f"Missing file: {fname}")
            continue
        with open(fpath) as f:
            content = f.read()
        if len(content) < 200:
            errors.append(f"Too short: {fname} ({len(content)} chars)")
        if "---\n" not in content[:50]:
            errors.append(f"Missing frontmatter: {fname}")

    # Check: Hugo build
    import subprocess
    result = subprocess.run(
        ["hugo", "--gc", "--minify"],
        capture_output=True, text=True, timeout=60,
        cwd=BASE_DIR
    )
    if result.returncode != 0:
        errors.append(f"Hugo build failed: {result.stderr[:500]}")
    else:
        print("   ✅ Hugo build passes")

    # Check: JSON validity
    for f in ["raw.json", "structured.json", "polished.json"]:
        fpath = os.path.join(TMPDIR, f)
        if os.path.exists(fpath):
            with open(fpath) as fp:
                json.load(fp)

    if errors:
        print(f"❌ Validation failed: {errors}")
        return False
    print("   ✅ All validations passed")
    return True

# === Main ===
def main():
    print(f"🚀 Pipeline started at {DATE_STR}\n")

    # Step 1: Search
    raw_data = step1_search()
    if not raw_data["results"]:
        print("⚠️  No results found. Exiting.")
        sys.exit(0)

    # Step 2: Structure
    structured = step2_structure(raw_data)
    if not structured.get("articles"):
        print("⚠️  No structured articles. Exiting.")
        sys.exit(0)

    # Step 3: Polish
    polished = step3_polish(structured)
    if not polished:
        print("⚠️  No polished articles. Exiting.")
        sys.exit(0)

    # Step 4: Generate MD
    posts = step4_generate_md(polished)
    if not posts:
        print("⚠️  No posts generated. Exiting.")
        sys.exit(0)

    # Step 5: Validate
    if not step5_validate(posts):
        print("❌ Validation failed. Not pushing.")
        sys.exit(1)

    print(f"\n✅ Pipeline complete! Generated {len(posts)} posts.")
    print("Run: git add -A && git commit -m 'Daily AI posts' && git push origin main")

if __name__ == "__main__":
    main()
