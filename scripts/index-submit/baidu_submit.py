#!/usr/bin/env python3
"""百度链接主动推送（增量优先 + 轮转覆盖版）。

百度普通站每日主动推送配额极小（常见 10 条）。旧脚本每次都推 sitemap 前 10 条，
其余页面永远轮不到。本脚本策略：
  1. 优先推 lastmod 有变化的 URL（最多占满当日配额）
  2. 配额有剩则按轮转游标推「还没推过」的页面，逐日覆盖全站，推完自动重新轮转
  3. 严格不超过当日配额（DAILY_CAP，可用环境变量 BAIDU_DAILY_CAP 覆盖）

用法:
  python3 scripts/index-submit/baidu_submit.py            # 增量 + 轮转（每日 cron 用这个）
  python3 scripts/index-submit/baidu_submit.py --dry-run  # 只看会推哪些，不调用 API
  python3 scripts/index-submit/baidu_submit.py /models/kimi-k3/   # 手动指定（消耗当日配额）
  python3 scripts/index-submit/baidu_submit.py --reset    # 清空已推记录与游标，重新轮转

首次运行只建立基线不推送；状态文件 .pipeline_tmp/baidu_state.json（gitignore）。
纯标准库；所有请求带自定义 UA（站点 CF 防护会拦 Python-urllib 默认 UA）。
"""
import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from xml.etree import ElementTree as ET

SITEMAP_URL = "https://www.jumohub.com/sitemap.xml"
BAIDU_API_URL = "http://data.zz.baidu.com/urls?site=www.jumohub.com&token=dTxLYHaZsI2Sg4DO"
USER_AGENT = "jumohub-baidu-push/2.0 (+https://www.jumohub.com)"
DAILY_CAP = int(os.environ.get("BAIDU_DAILY_CAP", "10"))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE_FILE = os.path.join(BASE_DIR, ".pipeline_tmp", "baidu_state.json")


def fetch_sitemap():
    print(f"正在读取 sitemap: {SITEMAP_URL} ...")
    req = urllib.request.Request(SITEMAP_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status}")
        root = ET.fromstring(resp.read())
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = {}
    # 注意：<lastmod> 是 <loc> 的兄弟节点（同在 <url> 内），不能在 <loc> 里找
    for url_el in root.findall(".//sm:url", ns):
        loc = url_el.find("sm:loc", ns)
        if loc is None or not (loc.text or "").strip():
            continue
        mod = url_el.find("sm:lastmod", ns)
        urls[(loc.text or "").strip()] = (mod.text or "").strip() if mod is not None else ""
    print(f"  sitemap 共 {len(urls)} 个 URL")
    return urls


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def save_state(state, note):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    state["lastRun"] = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
    state["note"] = note
    with open(STATE_FILE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)
    print(f"状态已保存: {STATE_FILE}")


def pick_daily(urls_map, state):
    """返回 (picked, new_cursor, note)：变更优先，轮转补足，总量 <= DAILY_CAP。"""
    prev_mod = state.get("lastmod")
    if prev_mod is None:
        return [], state.get("cursor", 0), "首次运行"

    changed = [u for u, m in urls_map.items() if prev_mod.get(u) != m]
    picked = changed[:DAILY_CAP]
    note_parts = []
    if changed:
        dropped = "" if len(changed) <= DAILY_CAP else f"（另有 {len(changed) - DAILY_CAP} 个变更超出配额，靠轮转逐步覆盖）"
        note_parts.append(f"变更 {len(picked)}{dropped}")

    new_cursor = state.get("cursor", 0)
    if len(picked) < DAILY_CAP:  # 配额有剩，轮转补足
        # 核心页优先：非模型页（首页/榜单/攻略等，约 26 个）先轮完，356 个模型页殿后
        all_urls = [u for u in urls_map if "/models/" not in u] + [u for u in urls_map if "/models/" in u]
        n = len(all_urls)
        pushed_set = set(state.get("pushed", []))
        cursor = new_cursor % max(n, 1)
        rotated, step, last_idx = [], 0, cursor - 1
        for step in range(n):
            idx = (cursor + step) % n
            u = all_urls[idx]
            if u not in picked and u not in pushed_set:
                rotated.append(u)
                last_idx = idx
                if len(picked) + len(rotated) >= DAILY_CAP:
                    break
        if rotated:
            picked += rotated
            new_cursor = (last_idx + 1) % n
            note_parts.append(f"轮转 {len(rotated)}")
    return picked, new_cursor, " + ".join(note_parts) if note_parts else "无变更且无可轮转的新页面"


class QuotaExceeded(RuntimeError):
    """当日推送配额已用尽（百度以 HTTP 400 + over quota 表达）。"""


def push_baidu(urls):
    body = "\n".join(urls).encode("utf-8")
    req = urllib.request.Request(
        BAIDU_API_URL,
        data=body,
        headers={"Content-Type": "text/plain", "User-Agent": USER_AGENT},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        # 百度用 HTTP 400 + JSON body 表达业务错误（如配额用尽），必须读出 body 才知道原因
        try:
            detail = json.loads(exc.read().decode("utf-8"))
        except Exception:
            raise RuntimeError(f"HTTP {exc.code}（无响应体）")
        msg = detail.get("message", "")
        if "quota" in msg.lower() or "配额" in msg or "over quota" in msg.lower():
            raise QuotaExceeded(msg) from exc
        raise RuntimeError(f"HTTP {exc.code}: {detail.get('error')} {msg}") from exc
    if "error" in result:
        msg = result.get("message", "")
        if "quota" in msg.lower() or "配额" in msg:
            raise QuotaExceeded(msg)
        raise RuntimeError(f"百度返回错误 {result.get('error')}: {msg}")
    print(f"  ✓ 成功推送 {result.get('success', 0)} 个，剩余当日配额 {result.get('remain', '?')}")
    return result.get("success", 0)


def main():
    parser = argparse.ArgumentParser(description="百度主动推送：增量优先 + 轮转覆盖全站")
    parser.add_argument("--dry-run", action="store_true", help="只打印将推送的 URL，不调用 API")
    parser.add_argument("--reset", action="store_true", help="清空已推记录与游标，重新开始轮转")
    parser.add_argument("paths", nargs="*", help="手动指定站点路径（如 /models/kimi-k3/），优先于增量/轮转")
    args = parser.parse_args()

    sitemap = fetch_sitemap()
    state = load_state()
    if args.reset:
        state = {"history": state.get("history", [])}
        print("已重置轮转状态\n")

    if args.paths:
        picked = [f"https://www.jumohub.com/{p.strip('/')}/" if p.strip("/") else "https://www.jumohub.com/" for p in args.paths]
        label = f"手动指定 {len(picked)} 个"
        new_cursor = state.get("cursor", 0)
    else:
        picked, new_cursor, label = pick_daily(sitemap, state)

    print(f"\n本次推送（{label}）共 {len(picked)} 个（当日配额上限 {DAILY_CAP}）:")
    if not picked:
        print("✓ 首次运行只建立基线，不推送。明天开始按「变更优先+轮转」推送。")
        print("  如需今天先推指定页面: python3 scripts/index-submit/baidu_submit.py /models/kimi-k3/")
        if not args.dry_run:
            state.setdefault("history", [])
            state["cursor"] = new_cursor
            state["lastmod"] = dict(sitemap)
            state["pushed"] = state.get("pushed", [])
            save_state(state, "首次基线")
        return 0
    for u in picked:
        print(f"  - {u}")

    if args.dry_run:
        print("（dry-run，未调用 API，状态未变）")
        return 0

    try:
        ok = push_baidu(picked)
    except QuotaExceeded as exc:
        print(f"\n⚠ 今日配额已用尽（{exc}）")
        print("（状态未更新，明天运行会优先重试这批页面）")
        return 0
    except Exception as exc:
        print(f"\n✗ 推送失败: {exc}")
        print("（状态未更新，下次运行会重试同样的页面）")
        return 1

    pushed_set = set(state.get("pushed", []))
    pushed_set.update(picked[:ok])
    state["pushed"] = sorted(pushed_set)[-3 * len(sitemap):]
    state["cursor"] = new_cursor
    state["lastmod"] = dict(sitemap)
    state.setdefault("history", []).append({"t": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"), "n": ok, "note": label})
    state["history"] = state["history"][-30:]
    save_state(state, label)
    return 0


if __name__ == "__main__":
    sys.exit(main())
