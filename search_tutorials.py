#!/usr/bin/env python3
"""
Search for AI tool 'sheep-farming' (discount/freebie) tutorials and save to JSON.

Tools searched: gemini, opencode, cline, openrouter
Usage:
    python3 search_tutorials.py [--query "额外关键词"]
"""

import json
import os
import sys
import argparse
import urllib.parse
import re
from html import unescape

# Search keywords for each tool (Chinese + English terms for tutorials/deals)
SEARCH_QUERIES = {
    "gemini": ["gemini 薅羊毛教程", "gemini 使用教程 教学", "gemini ai 教程", "gemini cli 教學"],
    "opencode": ["opencode cli 教程 使用教程 教学", "opencode 配置教程", "opencode 入门教程", "opencode cli 用法"],
    "cline": ["cline ai 教程 使用教程", "cline vscode 用法", "cline 配置教程", "cline 使用教程 教学"],
    "openrouter": ["openrouter 教程 使用教程", "openrouter 免费额度 api 用法", "openrouter 薅羊毛", "openrouter 配置教程"],
}

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tutorials.json")


def duckduckgo_search(query, max_results=15):
    """Search DuckDuckGo and return list of {title, url} results.

    Uses the HTML endpoint (no API key required).
    """
    import urllib.request

    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [warn] 请求失败: {e}", file=sys.stderr)
        return []

    # Extract result blocks: each result is in a <div class="result ..."> with <a class="result__a">
    # Pattern: <a class="result__a" href="...">Title</a>
    link_pattern = re.compile(
        r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
        re.DOTALL,
    )

    results = []
    for match in link_pattern.finditer(html):
        raw_url = match.group(1)
        raw_title = match.group(2)

        # Decode DuckDuckGo redirect URL (uddg=...)
        url = decode_ddg_url(raw_url)
        title = clean_text(raw_title)

        if url and title:
            results.append({"title": title, "url": url})

        if len(results) >= max_results:
            break

    return results


def decode_ddg_url(url):
    """Extract real URL from DuckDuckGo redirect."""
    # DDG redirect URLs look like: https://duckduckgo.com/l/?uddg=<encoded_url>&...
    if "uddg=" in url:
        parsed = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        uddg = parsed.get("uddg", [None])[0]
        if uddg:
            return unescape(uddg)
    return unescape(url)


def clean_text(html_text):
    """Strip HTML tags and decode entities from text."""
    text = re.sub(r"<[^>]+>", "", html_text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def search_tool(tool_name, queries, max_results=15):
    """Search multiple query terms for a tool, dedupe by URL."""
    all_results = []
    seen_urls = set()

    for q in queries:
        q = q.strip()
        if not q:
            continue
        print(f"  ↻ 搜索: {q}")
        results = duckduckgo_search(q, max_results=max_results)
        for r in results:
            if r["url"] not in seen_urls:
                seen_urls.add(r["url"])
                all_results.append(r)
        if len(all_results) >= max_results:
            break

    return all_results[:max_results]


def main():
    parser = argparse.ArgumentParser(description="搜索AI工具薅羊毛教程")
    parser.add_argument("--query", help="额外的搜索关键词", default=None)
    parser.add_argument("--output", "-o", help="输出JSON文件路径", default=OUTPUT_FILE)
    args = parser.parse_args()

    extra_query = args.query

    print("=" * 60)
    print("AI 工具薅羊毛教程搜索")
    print("=" * 60)

    output = {}
    for tool, queries in SEARCH_QUERIES.items():
        # Optionally append extra query to each term
        final_queries = [f"{q} {extra_query}" for q in queries] if extra_query else queries
        print(f"\n[{tool}] 搜索中...")
        results = search_tool(tool, final_queries)
        output[tool] = results
        print(f"  ✓ 找到 {len(results)} 个结果")

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"已保存到: {args.output}")
    print(f"{'=' * 60}")

    # Summary
    total = sum(len(v) for v in output.values())
    print(f"\n总结 ({total} 篇):")
    for tool, results in output.items():
        print(f"  {tool}: {len(results)} 篇")


if __name__ == "__main__":
    main()
