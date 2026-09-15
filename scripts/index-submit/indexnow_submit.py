#!/usr/bin/env python3
"""IndexNow 增量提交工具（对比 sitemap lastmod 与本地状态文件，只提交有变化的 URL）。

用法:
  python3 scripts/index-submit/indexnow_submit.py               # 增量：只提交 lastmod 变化/新增的 URL
  python3 scripts/index-submit/indexnow_submit.py --full        # 全量提交（仅新站首次或整站改版后用）
  python3 scripts/index-submit/indexnow_submit.py --dry-run     # 只看会提交什么，不真正调用 API
  python3 scripts/index-submit/indexnow_submit.py /models/kimi-k3/ /leaderboards/domestic/
                                                                # 手动提交指定路径（相对站点根，带或不带首尾斜杠均可）

说明:
- 状态文件 .pipeline_tmp/indexnow_state.json（已 gitignore）记录每个 URL 上次提交时的 lastmod
- 首次运行自动建立基线，不提交任何 URL；此后每次运行只提交有变化的页面
- 验证 key 使用 4380e811ce2749c2a1b705f74803ab60（对应站点根目录同名 .txt 文件）
- 纯标准库实现，无第三方依赖，可直接放进 CI
"""
import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from xml.etree import ElementTree as ET

SITEMAP_URL = "https://www.jumohub.com/sitemap.xml"
SITE_HOST = "www.jumohub.com"
INDEXNOW_KEY = "4380e811ce2749c2a1b705f74803ab60"
KEY_LOCATION = f"https://{SITE_HOST}/{INDEXNOW_KEY}.txt"
USER_AGENT = "jumohub-indexnow/2.0 (+https://www.jumohub.com)"  # 站点 CF 防护会拦截默认 Python-urllib UA
INDEXNOW_API = "https://api.indexnow.org/indexnow"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE_FILE = os.path.join(BASE_DIR, ".pipeline_tmp", "indexnow_state.json")
BATCH_SIZE = 1000


def fetch_sitemap():
    """拉取 sitemap，返回 {url: lastmod}（lastmod 缺失记为空串）。"""
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
    print(f"  sitemap 共 {len(urls)} 个 URL")
    return urls


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    return None


def save_state(urls_map, note):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    now_cn = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
    with open(STATE_FILE, "w", encoding="utf-8") as fh:
        json.dump({"lastRun": now_cn, "note": note, "urls": urls_map}, fh, ensure_ascii=False, indent=1)
    print(f"状态已保存: {STATE_FILE}")


def submit(urls, dry_run=False):
    """分批提交，返回 (成功数, 失败数)。200/202 视为成功，失败自动重试一次。"""
    if dry_run:
        for u in urls[:20]:
            print(f"  [dry-run] 将提交: {u}")
        if len(urls) > 20:
            print(f"  [dry-run] ...等共 {len(urls)} 个")
        return len(urls), 0

    ok_count, fail_count = 0, 0
    total_batches = (len(urls) + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(0, len(urls), BATCH_SIZE):
        batch_num = i // BATCH_SIZE + 1
        batch = urls[i : i + BATCH_SIZE]
        payload = json.dumps(
            {"host": SITE_HOST, "key": INDEXNOW_KEY, "keyLocation": KEY_LOCATION, "urlList": batch}
        ).encode("utf-8")
        sent = False
        for attempt in (1, 2):  # 失败自动重试一次
            try:
                req = urllib.request.Request(
                    INDEXNOW_API,
                    data=payload,
                    headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": USER_AGENT},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    status = resp.status
                if status in (200, 202):
                    print(f"  第 {batch_num}/{total_batches} 批提交成功（HTTP {status}，{len(batch)} 个）")
                    ok_count += len(batch)
                    sent = True
                    break
                print(f"  第 {batch_num}/{total_batches} 批失败（HTTP {status}），第 {attempt} 次尝试")
            except Exception as exc:
                print(f"  第 {batch_num}/{total_batches} 批异常（第 {attempt} 次）: {exc}")
        if not sent:
            fail_count += len(batch)
    return ok_count, fail_count


def normalize_paths(paths):
    urls = []
    for p in paths:
        seg = p.strip("/")
        urls.append(f"https://{SITE_HOST}/" if not seg else f"https://{SITE_HOST}/{seg}/")
    return urls


def main():
    parser = argparse.ArgumentParser(description="IndexNow 增量提交（默认只提交 sitemap 中 lastmod 有变化的 URL）")
    parser.add_argument("--full", action="store_true", help="忽略状态，全量提交所有 sitemap URL")
    parser.add_argument("--dry-run", action="store_true", help="只打印将提交的 URL，不调用 API")
    parser.add_argument("paths", nargs="*", help="手动指定的站点路径（如 /models/kimi-k3/），优先于增量模式")
    args = parser.parse_args()

    sitemap = fetch_sitemap()
    state = load_state()

    # 手动指定路径模式
    if args.paths:
        urls = normalize_paths(args.paths)
        unknown = [u for u in urls if u not in sitemap]
        if unknown:
            print(f"⚠ 以下 URL 不在 sitemap 中（仍会提交）: {unknown}")
        label = f"手动指定 {len(urls)} 个"
    elif args.full:
        urls = list(sitemap.keys())
        label = f"全量 {len(urls)} 个"
    else:
        if state is None:
            save_state(sitemap, "首次运行，建立基线（未提交任何 URL）")
            print("\n✓ 首次运行：已记录基线，本次不提交。")
            print("  新站如需全量提交请执行: python3 scripts/index-submit/indexnow_submit.py --full")
            return 0
        prev = state.get("urls", {})
        urls = [u for u, m in sitemap.items() if prev.get(u) != m]
        gone = [u for u in prev if u not in sitemap]
        if gone:
            print(f"  sitemap 中已移除 {len(gone)} 个旧 URL，将从状态中清理")
        label = f"增量 {len(urls)} 个"

    print(f"\n本次提交（{label}）:")
    if not urls:
        print("✓ 无变更，无需提交。")
        if state is not None and not args.paths:
            save_state(sitemap, "无变更")
        return 0

    ok, fail = submit(urls, dry_run=args.dry_run)
    print(f"\n完成: 成功 {ok}，失败 {fail}，共 {len(urls)}")

    if not args.dry_run and fail == 0:
        merged = dict(sitemap)
        if args.paths:  # 手动模式只更新被提交的条目
            merged = dict(state.get("urls", {})) if state else dict(sitemap)
            for u in urls:
                merged[u] = sitemap.get(u, "")
        save_state(merged, label)
    elif fail > 0:
        print("⚠ 有失败批次，状态未更新，下次运行会重试这些 URL。")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
