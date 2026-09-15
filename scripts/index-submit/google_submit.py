#!/usr/bin/env python3
"""Google 收录检查工具（增量提醒版）。

⚠ Google 没有可自由使用的收录推送接口：
  - Indexing API 官方仅限含 JobPosting（职位）/BroadcastEvent（直播）结构化数据的页面，
    普通内容页使用属超范围使用，本脚本在 API 模式下会直接拒绝执行
  - sitemap ping 接口（google.com/ping）已被 Google 于 2023 年宣布弃用并下线
  - Google 不支持 IndexNow 协议

Google 的正确姿势：
  1. Search Console 提交过 sitemap 即可，Google 会定期重取并按 lastmod 自动发现新页/改页
  2. 重要页面用「网址检查 → 请求编入索引」手动推送（Search Console 顶部搜索框输入 URL，
     右侧面板点「请求编入索引」，每日约 10 次，无 API 替代）
  3. 本工具的价值：对比 sitemap lastmod 变化，生成「值得人工推送」的核心页清单，
     并验证线上 sitemap 的可达性

用法:
  python3 scripts/index-submit/google_submit.py            # 检查变化 + 验证 sitemap + 输出建议清单
  python3 scripts/index-submit/google_submit.py --full     # 不对比状态，输出全量核心页清单
  python3 scripts/index-submit/google_submit.py --limit 10 # 清单最多列多少个（默认 10）
"""
import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from xml.etree import ElementTree as ET

SITEMAP_URL = "https://www.jumohub.com/sitemap.xml"
SITE_URL = "https://www.jumohub.com"
USER_AGENT = "jumohub-google-check/2.0 (+https://www.jumohub.com)"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE_FILE = os.path.join(BASE_DIR, ".pipeline_tmp", "google_state.json")


def fetch_sitemap():
    print(f"正在读取 sitemap: {SITEMAP_URL} ...")
    req = urllib.request.Request(SITEMAP_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status}")
        root = ET.fromstring(resp.read())
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = {}
    for loc in root.findall(".//sm:loc", ns):
        mod = loc.find("sm:lastmod", ns)
        urls[(loc.text or "").strip()] = (mod.text or "").strip() if mod is not None else ""
    print(f"  ✓ sitemap 可达，共 {len(urls)} 个 URL")
    return urls


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    return None


def save_state(urls_map):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    now = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
    with open(STATE_FILE, "w", encoding="utf-8") as fh:
        json.dump({"lastRun": now, "lastmod": urls_map}, fh, ensure_ascii=False, indent=1)


def main():
    parser = argparse.ArgumentParser(description="Google 收录检查：无推送接口，输出值得人工推送的页面清单")
    parser.add_argument("--full", action="store_true", help="忽略状态，输出全量核心页清单")
    parser.add_argument("--limit", type=int, default=10, help="建议清单最多列多少个（默认 10，对应 GSC 每日人工配额）")
    args = parser.parse_args()

    sitemap = fetch_sitemap()
    state = load_state()

    if state is None:
        save_state(sitemap)
        print("\n✓ 首次运行：已建立基线。此后每次运行会列出上次以来有变化的页面。")
        return 0

    if args.full:
        changed = list(sitemap.keys())
        label = "全量"
    else:
        prev = state.get("lastmod", {})
        changed = [u for u, m in sitemap.items() if prev.get(u) != m]
        label = "增量"

    core = [u for u in changed if "/models/" not in u]
    models = [u for u in changed if "/models/" in u]

    print(f"\n=== {label}检查结果 ===")
    if not changed:
        print("✓ sitemap 无变化，Google 会按自己的节奏重取，无需任何操作。")
        return 0

    print(f"自上次检查以来有变化的页面共 {len(changed)} 个（核心页 {len(core)} / 模型页 {len(models)}）")
    todo = core[: args.limit]
    if todo:
        print(f"\n📌 建议人工去 Search Console「网址检查 → 请求编入索引」推送以下 {len(todo)} 个")
        print("   （每日约 10 次人工配额；把下面的 URL 粘贴到 GSC 顶部搜索框即可）:")
        for u in todo:
            print(f"  - {u}")
    if models:
        print(f"\nℹ {len(models)} 个模型页有变化：无需手动推送，Google 会通过 sitemap lastmod 自动发现。")

    if not args.full:
        save_state(sitemap)
        print("\n状态已更新。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
