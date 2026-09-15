#!/usr/bin/env python3
"""
Generate Hugo leaderboard pages from jumo_leaderboards.json (BenchLM merged data).

Creates content/leaderboards/<key>.md for every leaderboard in the merged data.
Each page contains a markdown table with up to 200 rows.
国产模型榜（domestic）与国产性价比榜（domestic_value）额外内嵌 ECharts 横向条形图。

Usage:
  python3 scripts/generate_leaderboard_pages.py --all                  # all leaderboards
  python3 scripts/generate_leaderboard_pages.py --key overall          # single board
  python3 scripts/generate_leaderboard_pages.py --all --force          # overwrite existing
"""

import argparse
import json
import os
import sys

# 国产榜单（内嵌 ECharts 图表）的图标配置
ECHARTS_BOARDS = {
    "domestic": {
        "chart_title": "国产模型综合评分 Top 10",
        "value_key": "score",
        "value_name": "综合评分",
        "unit": "分",
        "color": "#e74c3c",
        "height": "460px",
    },
    "domestic_value": {
        "chart_title": "国产模型性价比 Top 10（价格 70% + 评分 30%）",
        "value_key": "valueScore",
        "value_name": "性价比",
        "unit": "分",
        "color": "#f39c12",
        "height": "460px",
    },
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "jumo_leaderboards.json")
DATA_TS = ""


def data_ts():
    """数据构建时间戳，写入 front matter date → Hugo sitemap <lastmod>。"""
    global DATA_TS
    if not DATA_TS:
        try:
            with open(DATA_FILE, encoding="utf-8") as fh:
                DATA_TS = (json.load(fh).get("metadata") or {}).get("generatedAt", "")
        except (OSError, ValueError):
            DATA_TS = ""
    return DATA_TS
LEADERBOARDS_DIR = os.path.join(BASE_DIR, "content", "leaderboards")


def fmt_price(v):
    """Format price field for markdown table."""
    if v is None:
        return "—"
    return f"${v}/M"


def fmt_speed(v):
    """Format speed field for markdown table."""
    if v is None:
        return "—"
    return f"{v} tokens/秒"


def fmt_ttft(v):
    """格式化首字延迟（TTFT）字段为表格单元格文本。"""
    if v is None:
        return "—"
    return f"{v:.2f}秒"


def render_table(rows, max_items=200):
    """Render markdown table rows from leaderboard rows."""
    lines = []
    for i, r in enumerate(rows[:max_items]):
        rank = r.get("rank", i + 1)
        slug = r.get("slug", "")
        name = r.get("name", "")
        creator = r.get("creatorZh", r.get("creator", ""))
        score = r.get("score")

        # Format score: show as integer if whole number, else 2 decimals
        if score is not None:
            if score == int(score):
                score_str = str(int(score))
            else:
                score_str = f"{score:.2f}"
        else:
            score_str = "—"

        input_price = fmt_price(r.get("inputPrice"))
        output_price = fmt_price(r.get("outputPrice"))
        speed = fmt_speed(r.get("speed"))
        ttft = fmt_ttft(r.get("ttft"))

        url = f"/models/{slug}/" if slug else "#"
        lines.append(
            f"| {rank} | [{name}]({url}) | {creator} | {score_str} | "
            f"{input_price} | {output_price} | {speed} | {ttft} |"
        )
    return "\n".join(lines)


def render_chart(board):
    """Render an ECharts shortcode block (horizontal bars, Top 10) for domestic boards."""
    cfg = ECHARTS_BOARDS[board["key"]]
    top = board.get("rows", [])[:10]
    names = [r.get("name", "") for r in top]
    values = [r.get(cfg["value_key"]) for r in top]
    names_js = json.dumps(names, ensure_ascii=False)
    values_js = json.dumps(values)
    lines = [
        '<div class="domestic-chart">',
        f'{{{{< echarts id="chart-{board["key"]}" height="{cfg["height"]}" enableClick="true" >}}}}',
        "title: {",
        f"  text: '{cfg['chart_title']}',",
        "  left: 'center',",
        "  textStyle: { fontSize: 15 }",
        "},",
        "tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },",
        "grid: { left: '3%', right: '8%', top: '12%', bottom: '3%', containLabel: true },",
        "xAxis: { type: 'value' },",
        "yAxis: {",
        "  type: 'category',",
        "  inverse: true,",
        f"  data: {names_js},",
        "  axisLabel: {",
        "    formatter: function(value, index) {",
        f"      var v = {values_js}[index];",
        "      return (index + 1) + '. ' + value + ' (' + v + ')';",
        "    }",
        "  }",
        "},",
        "series: [{",
        f"  name: '{cfg['value_name']}',",
        "  type: 'bar',",
        f"  data: {values_js},",
        "  barMaxWidth: 22,",
        "  itemStyle: {",
        "    borderRadius: [0, 4, 4, 0],",
        "    color: function(params) {",
        f"      var c = '{cfg['color']}';",
        "      return params.dataIndex < 3",
        "        ? echarts.color.lift(c, 0.12 * (3 - params.dataIndex))",
        "        : c;",
        "    }",
        "  },",
        "  label: { show: true, position: 'right' }",
        "}]",
        "{{< /echarts >}}",
        "</div>",
        "",
    ]
    return "\n".join(lines)


def render_page(board, max_items=200):
    """Render a single leaderboard page as markdown."""
    key = board.get("key", "unknown")
    name = board.get("name", key)
    description = board.get("description", "")
    total = board.get("total", len(board.get("rows", [])))

    rows = board.get("rows", [])
    table = render_table(rows, max_items)

    chart = render_chart(board) if key in ECHARTS_BOARDS else ""
    ts = data_ts()

    frontmatter = f"""---
title: "{name}"
model: false
count: {total}
description: "{description}"
date: "{ts}"
---

<!-- 榜单: {name} ({total}个模型) -->
{chart}
| 排名 | 模型 | 厂商 | 评分 | 输入价格 | 输出价格 | 速度 | 首字延迟 |
|------|------|------|------|----------|----------|------|------ |
{table}
"""
    return frontmatter


def write_page(board, force=False):
    """Write a leaderboard page to content/leaderboards/<key>.md."""
    key = board.get("key", "")
    if not key or "/" in key or key.startswith("."):
        return None

    out_file = os.path.join(LEADERBOARDS_DIR, f"{key}.md")
    if os.path.exists(out_file) and not force:
        return None

    os.makedirs(LEADERBOARDS_DIR, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as fh:
        fh.write(render_page(board))
    return out_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate Hugo leaderboard pages from jumo_leaderboards.json"
    )
    parser.add_argument(
        "--key", help="generate a single leaderboard page by key"
    )
    parser.add_argument(
        "--all", action="store_true", help="generate pages for all leaderboards"
    )
    parser.add_argument(
        "--force", action="store_true", help="overwrite existing pages"
    )
    parser.add_argument(
        "--max-items", type=int, default=200, help="max rows per leaderboard page"
    )
    args = parser.parse_args()

    if not args.key and not args.all:
        parser.error("specify --key KEY or --all")

    if not os.path.exists(DATA_FILE):
        print(f"错误: 未找到 {DATA_FILE}", file=sys.stderr)
        print("请先运行: python3 scripts/build_benchlm_data.py", file=sys.stderr)
        return 1

    with open(DATA_FILE, encoding="utf-8") as fh:
        doc = json.load(fh)

    boards = doc.get("leaderboards", [])
    if not boards:
        print("错误: 榜单数据为空", file=sys.stderr)
        return 1

    print(f"找到 {len(boards)} 个榜单")

    if args.key:
        matches = [b for b in boards if b.get("key") == args.key]
        if not matches:
            print(f"错误: 未找到 key 为 {args.key} 的榜单", file=sys.stderr)
            # Show available keys
            print("可用 key:", [b.get("key") for b in boards], file=sys.stderr)
            return 1
        path = write_page(matches[0], force=args.force)
        if path:
            print(f"已生成: {path}")
        else:
            print(f"已存在（跳过，用 --force 覆盖）: {args.key}")
        return 0

    # Generate all
    written, skipped = 0, 0
    for b in boards:
        path = write_page(b, force=args.force)
        if path:
            written += 1
            print(f"  ✅ {b.get('key')}: {path}")
        else:
            skipped += 1
            print(f"  ⏭️  {b.get('key')}: 已存在，跳过")

    print(f"\n生成完成: 新建 {written} 个页面，跳过 {skipped} 个（已存在，用 --force 覆盖）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
