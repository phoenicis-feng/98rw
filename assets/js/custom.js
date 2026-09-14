// 模型对比组件交互：读取 shortcode 内嵌的 JSON，渲染选择器与对比表
(() => {
  "use strict";

  // 对比字段配置：key 支持 "a.b" 嵌套；numeric 字段会判定胜负并高亮
  const FIELDS = [
    { group: "规格", label: "厂商", key: "vendor" },
    { group: "规格", label: "发布时间", key: "released" },
    { group: "规格", label: "上下文窗口", key: "context" },
    { group: "规格", label: "输入价格", key: "price_input" },
    { group: "规格", label: "输出价格", key: "price_output" },
    { group: "跑分", label: "推理", key: "scores.reasoning", numeric: true },
    { group: "跑分", label: "代码", key: "scores.coding", numeric: true },
    { group: "跑分", label: "中文理解", key: "scores.chinese", numeric: true },
    { group: "跑分", label: "长文本", key: "scores.longtext", numeric: true },
  ];

  const get = (obj, path) =>
    path.split(".").reduce((o, k) => (o == null ? undefined : o[k]), obj);

  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  function renderTable(root, a, b) {
    let lastGroup = "";
    const rows = FIELDS.map((f) => {
      const va = get(a.specs, f.key);
      const vb = get(b.specs, f.key);
      const groupHead =
        f.group !== lastGroup
          ? `<tr class="model-compare__group"><th colspan="3">${esc(f.group)}</th></tr>`
          : "";
      lastGroup = f.group;

      let ca = "", cb = "";
      if (f.numeric && typeof va === "number" && typeof vb === "number") {
        if (va > vb) ca = " model-compare__win";
        else if (vb > va) cb = " model-compare__win";
        const diff = Math.abs(va - vb);
        const diffText = diff ? ` <small>(+${diff})</small>` : "";
        return `${groupHead}<tr><th>${esc(f.label)}</th>` +
          `<td class="${ca.trim()}">${va}${ca ? diffText : ""}</td>` +
          `<td class="${cb.trim()}">${vb}${cb ? diffText : ""}</td></tr>`;
      }
      return `${groupHead}<tr><th>${esc(f.label)}</th>` +
        `<td>${va == null ? "—" : esc(va)}</td>` +
        `<td>${vb == null ? "—" : esc(vb)}</td></tr>`;
    }).join("");

    root.innerHTML =
      `<table class="model-compare__table">` +
      `<thead><tr><th></th>` +
      `<th><a href="${esc(a.url)}">${esc(a.name)}</a></th>` +
      `<th><a href="${esc(b.url)}">${esc(b.name)}</a></th>` +
      `</tr></thead><tbody>${rows}</tbody></table>`;
  }

  // /compare/?models=a,b：/models/ 索引页勾选后跳转带来的预选模型
  let preset = [];
  try {
    preset = (new URLSearchParams(location.search).get("models") || "")
      .split(",").map(decodeURIComponent).filter(Boolean);
  } catch { /* 参数格式非法时忽略 */ }
  let presetUsed = false;

  document.querySelectorAll(".model-compare").forEach((wrap) => {
    let models;
    try { models = JSON.parse(wrap.dataset.models); } catch { return; }
    if (!Array.isArray(models)) return;

    // 按分类过滤：specs.category 为字符串或数组，任一命中即保留
    const scope = wrap.dataset.category;
    if (scope) {
      models = models.filter((m) => {
        const c = m.specs && m.specs.category;
        return Array.isArray(c) ? c.includes(scope) : c === scope;
      });
    }

    if (models.length < 2) {
      wrap.querySelector(".model-compare__result").innerHTML =
        `<p>${scope ? `“${scope}”分类下只有 ${models.length} 个模型，` : ""}至少需要两个带 specs 数据的模型才能对比。</p>`;
      return;
    }

    // 带 ?models= 参数时：第一个不限分类的组件按参数预选两个模型（多余的忽略）
    let presetTwo = null;
    if (!presetUsed && !scope && preset.length >= 2) {
      presetUsed = true;
      const byUrl = new Map(models.map((m) => [m.url, m]));
      const picked = preset.map((u) => byUrl.get(u)).filter(Boolean).slice(0, 2);
      if (picked.length === 2) presetTwo = picked;
    }

    const picks = {};
    wrap.querySelectorAll("select[data-pick]").forEach((sel, i) => {
      sel.innerHTML = models
        .map((m, j) => `<option value="${j}">${esc(m.name)}</option>`)
        .join("");
      sel.value = String(i % Math.min(2, models.length));
      picks[sel.dataset.pick] = sel;
    });
    if (presetTwo) {
      picks.a.value = String(models.indexOf(presetTwo[0]));
      picks.b.value = String(models.indexOf(presetTwo[1]));
    }

    const result = wrap.querySelector(".model-compare__result");
    const update = () => {
      let ia = Number(picks.a.value);
      let ib = Number(picks.b.value);
      if (ia === ib) ib = (ib + 1) % models.length; // 避免自己比自己
      renderTable(result, models[ia], models[ib]);
    };

    picks.a.addEventListener("change", update);
    picks.b.addEventListener("change", update);
    update();
  });

  // /models/ 总索引页的勾选对比已移除（改为纯展示卡片）
})();

/* ===== OpenRouter 模型列表：搜索 + 筛选 + 排序 + 分页 ===== */
(() => {
  "use strict";
  const section = document.querySelector(".openrouter-section");
  if (!section) return;

  const searchInput = document.getElementById("openrouter-search");
  const freeToggle = document.getElementById("openrouter-free-toggle");
  const pagePrev = document.getElementById("openrouter-page-prev");
  const pageNext = document.getElementById("openrouter-page-next");
  const pageInfo = document.getElementById("openrouter-page-info");
  const emptyState = document.getElementById("openrouter-empty");
  const tableBody = document.getElementById("openrouter-global-tbody");
  const table = document.getElementById("openrouter-global-table");
  const sortHeaders = table?.querySelectorAll("th[data-sort]");

  const PAGE_SIZE = 20;
  let currentPage = 1;
  let sortColumn = null;
  let sortAsc = true;

  // 从 URL 恢复搜索条件
  function getUrlParams() {
    try {
      const params = new URLSearchParams(location.search);
      return { q: params.get("q") || "", free: params.get("free") === "1" };
    } catch { return { q: "", free: false }; }
  }

  // 更新 URL 参数
  function updateUrl() {
    const params = new URLSearchParams();
    if (searchInput?.value) params.set("q", searchInput.value);
    if (freeToggle?.checked) params.set("free", "1");
    const qs = params.toString();
    const newUrl = qs ? `${location.pathname}?${qs}` : location.pathname;
    history.replaceState(null, "", newUrl);
  }

  // 从 URL 恢复搜索条件到 UI
  function restoreFromUrl() {
    const { q, free } = getUrlParams();
    if (searchInput) searchInput.value = q;
    if (freeToggle) freeToggle.checked = free;
  }

  // 获取所有表格行
  function getAllRows() {
    return tableBody?.querySelectorAll("tr.openrouter-row") || [];
  }

  // 获取行数据
  function getRowData(row) {
    return {
      name: (row.dataset.name || "").toLowerCase(),
      vendor: (row.dataset.vendor || "").toLowerCase(),
      context: row.dataset.context || "",
      priceInput: row.dataset.priceInput || "",
      priceOutput: row.dataset.priceOutput || "",
      reasoning: parseInt(row.dataset.reasoning || "0"),
      coding: parseInt(row.dataset.coding || "0"),
      chinese: parseInt(row.dataset.chinese || "0"),
      longtext: parseInt(row.dataset.longtext || "0"),
      modalities: (row.dataset.modalities || "").toLowerCase(),
      isFree: row.dataset.free !== undefined,
    };
  }

  function parsePrice(str) {
    if (!str || str.includes("免费")) return 0;
    const match = str.match(/[\d.]+/);
    return match ? parseFloat(match[0]) : 0;
  }

  // 排序
  function sortRows(rows) {
    if (!sortColumn) return rows;
    return Array.from(rows).sort((a, b) => {
      const da = getRowData(a);
      const db = getRowData(b);
      let valA, valB;
      switch (sortColumn) {
        case "name":
          valA = da.name; valB = db.name; break;
        case "context":
          valA = da.context; valB = db.context; break;
        case "price_input":
          valA = parsePrice(da.priceInput); valB = parsePrice(db.priceInput); break;
        case "price_output":
          valA = parsePrice(da.priceOutput); valB = parsePrice(db.priceOutput); break;
        case "reasoning":
          valA = da.reasoning; valB = db.reasoning; break;
        case "coding":
          valA = da.coding; valB = db.coding; break;
        case "chinese":
          valA = da.chinese; valB = db.chinese; break;
        case "longtext":
          valA = da.longtext; valB = db.longtext; break;
        case "modalities":
          valA = da.modalities; valB = db.modalities; break;
        default:
          valA = da.name; valB = db.name;
      }
      if (typeof valA === "string") {
        return sortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
      }
      return sortAsc ? valA - valB : valB - valA;
    });
  }

  // 过滤并分页
  function filterRows() {
    const allRows = getAllRows();
    const q = (searchInput?.value || "").toLowerCase().trim();
    const freeOnly = freeToggle?.type === "checkbox" && freeToggle.checked;

    let filtered = [];
    allRows.forEach((row) => {
      const data = getRowData(row);
      const matchesSearch = !q || data.name.includes(q) || data.vendor.includes(q) || data.modalities.includes(q);
      const matchesFree = !freeOnly || data.isFree;
      if (matchesSearch && matchesFree) {
        filtered.push(row);
      }
    });

    const sorted = sortRows(filtered);
    const totalPages = Math.max(1, Math.ceil(sorted.length / PAGE_SIZE));
    if (currentPage > totalPages) currentPage = totalPages;

    // 隐藏所有行
    allRows.forEach((row) => row.style.display = "none");

    // 显示当前页的行
    const start = (currentPage - 1) * PAGE_SIZE;
    const end = start + PAGE_SIZE;
    sorted.forEach((row, idx) => {
      row.style.display = (idx >= start && idx < end) ? "" : "none";
    });

    // 更新分页控件
    if (pagePrev) pagePrev.disabled = currentPage <= 1;
    if (pageNext) pageNext.disabled = currentPage >= totalPages;
    if (pageInfo) pageInfo.textContent = `第 ${currentPage} 页 / 共 ${totalPages} 页`;
    if (emptyState) emptyState.style.display = filtered.length === 0 ? "block" : "none";

    // 更新 URL
    updateUrl();
  }

  // 表头排序
  sortHeaders?.forEach((th) => {
    th.style.cursor = "pointer";
    th.addEventListener("click", () => {
      const col = th.dataset.sort;
      if (sortColumn === col) {
        sortAsc = !sortAsc;
      } else {
        sortColumn = col;
        sortAsc = true;
      }
      sortHeaders.forEach((h) => {
        h.classList.remove("sort-asc", "sort-desc");
      });
      th.classList.add(sortAsc ? "sort-asc" : "sort-desc");
      currentPage = 1;
      filterRows();
    });
  });

  // 事件绑定
  searchInput?.addEventListener("input", () => { currentPage = 1; filterRows(); });
  freeToggle?.addEventListener("change", () => { currentPage = 1; filterRows(); });
  pagePrev?.addEventListener("click", () => { if (currentPage > 1) { currentPage--; filterRows(); } });
  pageNext?.addEventListener("click", () => { if (pageNext?.disabled) return; const allRows = getAllRows(); const q = (searchInput?.value || "").toLowerCase().trim(); const freeOnly = freeToggle?.type === "checkbox" && freeToggle.checked; const visible = Array.from(allRows).filter((r) => { const data = getRowData(r); const matchesSearch = !q || data.name.includes(q) || data.vendor.includes(q) || data.modalities.includes(q); return matchesSearch && (!freeOnly || data.isFree); }); const totalPages = Math.max(1, Math.ceil(visible.length / PAGE_SIZE)); if (currentPage < totalPages) { currentPage++; filterRows(); } });

  // 初始化：恢复 URL 参数并渲染
  restoreFromUrl();
  filterRows();
})();

/* ===== 推荐页面：场景/类型筛选 + 表头排序 ===== */
(() => {
  "use strict";
  const recSection = document.querySelector(".rec-section");
  if (!recSection) return;

  // 当前排序状态：{ key, dir }，dir 为 'asc' 或 'desc'
  let sortState = { key: "overall", dir: "desc" };
  let currentScene = "all";

  function parsePrice(str) {
    if (!str) return 0;
    const match = str.match(/[\d.]+/);
    return match ? parseFloat(match[0]) : 0;
  }

  function parseContext(str) {
    // 上下文："200K tokens" / "1M tokens" 等，提取数值并按 K/M 换算
    if (!str) return 0;
    const m = String(str).match(/([\d.]+)\s*([KkMm]?)/);
    if (!m) return 0;
    let v = parseFloat(m[1]);
    if (m[2] && m[2].toLowerCase() === "k") v *= 1000;
    if (m[2] && m[2].toLowerCase() === "m") v *= 1000000;
    return v;
  }

  function matchesFilter(row) {
    if (currentScene !== "all") {
      const scenario = row.dataset.scenario || "其他";
      if (!scenario.split("/").map((v) => v.trim()).includes(currentScene)) return false;
    }
    return true;
  }

  function getRowValue(row, key) {
    switch (key) {
      case "name":
        const nameEl = row.querySelector(".rec-row__name");
        return nameEl ? nameEl.textContent.trim().toLowerCase() : "";
      case "price":
      case "price_input":
        return parsePrice(row.dataset.priceInput || "0");
      case "price_output":
        return parsePrice(row.dataset.priceOutput || "0");
      case "context":
        return parseContext(row.dataset.context);
      case "speed":
        return parsePrice(row.dataset[key] || "0");
      case "overall":
      case "agentic":
      case "reasoning":
      case "coding":
      case "multimodal":
      case "knowledge":
        return parseFloat(row.dataset[key] || "0");
      default:
        return row.dataset[key] || "";
    }
  }

  function sortTable(table) {
    const tbody = table.querySelector("tbody");
    if (!tbody) return;
    const allRows = Array.from(tbody.querySelectorAll(".rec-row"));
    const visibleRows = allRows.filter(matchesFilter);
    const { key, dir } = sortState;
    const multiplier = dir === "desc" ? 1 : -1;

    visibleRows.sort((a, b) => {
      let va = getRowValue(a, key);
      let vb = getRowValue(b, key);
      if (typeof va === "number" && typeof vb === "number") {
        return (vb - va) * multiplier;
      }
      return String(va).localeCompare(String(vb)) * multiplier;
    });

    // 清空 tbody 并重新添加排序后的行（保留所有行，隐藏不符合筛选的）
    while (tbody.firstChild) tbody.removeChild(tbody.firstChild);
    // 先加符合条件的，再加不符合的（隐藏）
    visibleRows.forEach((row) => {
      row.style.display = "";
      tbody.appendChild(row);
    });

    // 处理不符合筛选的行：重新挂回但隐藏
    allRows.forEach((row) => {
      if (!matchesFilter(row)) {
        row.style.display = "none";
        tbody.appendChild(row);
      }
    });
  }

  // 更新表头高亮
  function updateHeaderHighlight() {
    recSection.querySelectorAll(".rec-th-sortable").forEach((th) => {
      th.classList.remove("rec-th-sort-asc", "rec-th-sort-desc");
      if (th.dataset.sortKey === sortState.key) {
        th.classList.add(sortState.dir === "asc" ? "rec-th-sort-asc" : "rec-th-sort-desc");
      }
    });
  }

  function apply() {
    recSection.querySelectorAll(".rec-table").forEach((table) => sortTable(table));
    updateHeaderHighlight();
  }

  // 事件委托：表头排序 / 场景筛选
  recSection.addEventListener("click", (e) => {
    // 表头排序
    const th = e.target.closest(".rec-th-sortable");
    if (th) {
      const key = th.dataset.sortKey;
      if (sortState.key === key) {
        // 同列再次点击切换方向
        sortState.dir = sortState.dir === "asc" ? "desc" : "asc";
      } else {
        sortState.key = key;
        sortState.dir = "desc";
      }
      apply();
      return;
    }
    // 场景筛选
    const sceneBtn = e.target.closest("[data-scene]");
    if (sceneBtn) {
      currentScene = sceneBtn.dataset.scene;
      recSection.querySelectorAll("[data-scene]").forEach((b) => b.classList.remove("rec-filter-btn--active"));
      sceneBtn.classList.add("rec-filter-btn--active");
      apply();
      return;
    }
  });

  // 初始化
  apply();
})();

/* ============================================
/* ============================================
   HF 模型库：厂商 → 系列级联筛选 + 分页
   样式复用 recommendations 的 rec-filter 药丸按钮
   ============================================ */
(function () {
  "use strict";

  const section = document.getElementById("hf-models");
  if (!section) return;

  const vendorFilterEl = document.getElementById("hf-vendor-filter");
  const seriesRowEl = document.getElementById("hf-series-row");
  const seriesFilterEl = document.getElementById("hf-series-filter");
  const tbody = document.getElementById("hf-model-tbody");
  const countEl = document.getElementById("hf-count");
  const paginationEl = document.getElementById("hf-pagination");

  // 相对时间：把 "YYYY-MM-DD HH:mm:ss" 渲染为「x天/月前」，超过一年显示日期
  function relTime(s) {
    if (!s) return "";
    const t = new Date(String(s).replace(" ", "T") + "Z").getTime();
    if (isNaN(t)) return s;
    const days = Math.floor((Date.now() - t) / 86400000);
    if (days < 1) return "今天";
    if (days < 30) return days + " 天前";
    if (days < 365) return Math.floor(days / 30) + " 个月前";
    return s.slice(0, 10);
  }

  // 从 DOM 收集全部模型行，解析为数据数组
  const allRows = Array.from(tbody.querySelectorAll("tr[data-hf-model]"));
  const models = allRows.map((r) => ({
    el: r,
    vendor: r.dataset.hfVendor,
    series: r.dataset.hfSeries
  }));

  // 更新时间列：绝对时间 → 相对时间
  allRows.forEach((r) => {
    const timeTd = r.querySelector(".hf-table__time");
    if (timeTd) {
      const label = relTime(timeTd.textContent.trim());
      if (label) timeTd.textContent = label;
    }
  });

  const state = { vendor: "all", series: "all", page: 1, pageSize: 20 };

  function fmt(n) { return n.toLocaleString("en-US"); }

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function scrollToTop() {
    section.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  /* ---------- 系列筛选按钮：随厂商级联刷新，选中厂商前整行隐藏 ---------- */
  function renderSeriesFilter() {
    seriesRowEl.hidden = state.vendor === "all";
    const counts = new Map(); // 系列名 -> 模型数（受当前厂商范围约束）
    models.forEach((m) => {
      if (state.vendor === "all" || m.vendor === state.vendor) {
        counts.set(m.series, (counts.get(m.series) || 0) + 1);
      }
    });
    const sorted = Array.from(counts.keys()).sort((a, b) => {
      if (a === "Other") return 1;
      if (b === "Other") return -1;
      return (counts.get(b) - counts.get(a)) || a.localeCompare(b);
    });
    let html = '<button type="button" class="rec-filter-btn' + (state.series === "all" ? " rec-filter-btn--active" : "") + '" data-hf-series="all">全部</button>';
    sorted.forEach((s) => {
      html += '<button type="button" class="rec-filter-btn' + (state.series === s ? " rec-filter-btn--active" : "") + '" data-hf-series="' + esc(s) + '">' + esc(s) +
        ' <span class="hf-filter-count">' + fmt(counts.get(s)) + '</span></button>';
    });
    seriesFilterEl.innerHTML = html;
  }

  /* ---------- 当前范围内的模型列表 ---------- */
  function currentModels() {
    let list = models;
    if (state.vendor !== "all") list = list.filter((m) => m.vendor === state.vendor);
    if (state.series !== "all") list = list.filter((m) => m.series === state.series);
    return list;
  }

  /* ---------- 渲染：模型表（分页） ---------- */
  function renderTable() {
    const list = currentModels();
    const total = list.length;
    const totalPages = Math.max(1, Math.ceil(total / state.pageSize));
    if (state.page > totalPages) state.page = totalPages;
    const start = (state.page - 1) * state.pageSize;
    const pageItems = list.slice(start, start + state.pageSize);

    allRows.forEach((r) => { r.style.display = "none"; });
    pageItems.forEach((m, i) => {
      m.el.style.display = "";
      m.el.querySelector(".hf-table__rank").textContent = String(start + i + 1);
    });

    const oldEmpty = document.getElementById("hf-empty");
    if (oldEmpty) oldEmpty.remove();
    if (total === 0) {
      const div = document.createElement("p");
      div.id = "hf-empty";
      div.className = "hf-index__meta";
      div.textContent = "没有匹配的模型，换个厂商或系列试试。";
      tableAnchor().insertBefore(div, tableAnchor().firstChild);
    }

    countEl.textContent = "共 " + fmt(total) + " 个模型";

    renderPagination(totalPages);
  }

  function tableAnchor() {
    return tbody.closest(".hf-table-wrap").parentNode;
  }

  /* ---------- 渲染：分页控件（结构与主题 pagination.html 保持一致） ----------
     页数多时固定布局：首尾各 4 页 + 当前页，其余用 …，条数恒定不增长。 */
  function renderPagination(totalPages) {
    if (totalPages <= 1) {
      paginationEl.innerHTML = "";
      return;
    }
    const step = (label, target, disabled) => disabled
      ? '<span class="pagination__step" aria-disabled="true">' + label + '</span>'
      : '<button type="button" class="pagination__step" data-page="' + target + '">' + label + '</button>';
    const pageItem = (p) => '<li>' + (p === state.page
      ? '<span class="pagination__page" aria-current="page">' + p + '</span>'
      : '<button type="button" class="pagination__page" data-page="' + p + '">' + p + '</button>') + '</li>';

    let html = '<nav class="pagination" aria-label="分页">';
    html += step("上一页", "prev", state.page === 1);
    html += '<ol class="pagination__pages">';
    if (totalPages <= 10) {
      for (let p = 1; p <= totalPages; p++) html += pageItem(p);
    } else {
      const headEnd = 4;
      const tailStart = totalPages - 3;
      for (let p = 1; p <= headEnd; p++) html += pageItem(p);
      if (state.page > headEnd && state.page < tailStart) {
        html += '<li><span class="pagination__ellipsis">…</span></li>';
        html += pageItem(state.page);
      }
      html += '<li><span class="pagination__ellipsis">…</span></li>';
      for (let p = tailStart; p <= totalPages; p++) html += pageItem(p);
    }
    html += '</ol>';
    html += step("下一页", "next", state.page === totalPages);
    html += '</nav>';
    paginationEl.innerHTML = html;
  }

  /* ---------- 厂商筛选按钮：按模型数降序生成（含计数） ---------- */
  function renderVendorFilter() {
    const counts = new Map();
    models.forEach((m) => counts.set(m.vendor, (counts.get(m.vendor) || 0) + 1));
    const sorted = Array.from(counts.entries()).sort((x, y) => y[1] - x[1]);
    let html = '<button type="button" class="rec-filter-btn' + (state.vendor === "all" ? " rec-filter-btn--active" : "") + '" data-hf-vendor="all">全部</button>';
    sorted.forEach(([v, c]) => {
      html += '<button type="button" class="rec-filter-btn' + (state.vendor === v ? " rec-filter-btn--active" : "") + '" data-hf-vendor="' + esc(v) + '">' + esc(v) +
        ' <span class="hf-filter-count">' + fmt(c) + '</span></button>';
    });
    vendorFilterEl.innerHTML = html;
  }

  function render() {
    renderVendorFilter();
    renderSeriesFilter();
    renderTable();
  }

  /* ---------- 模态：点击行查看模型详情 ---------- */
  const modal = document.createElement("div");
  modal.className = "hf-modal";
  modal.hidden = true;
  modal.innerHTML =
    '<div class="hf-modal__overlay" data-hf-close></div>' +
    '<div class="hf-modal__card" role="dialog" aria-modal="true" aria-label="模型详情">' +
    '<button type="button" class="hf-modal__close" data-hf-close aria-label="关闭">&times;</button>' +
    '<h3 class="hf-modal__title"></h3>' +
    '<p class="hf-modal__meta"></p>' +
    '<dl class="hf-modal__grid">' +
    '<dt>评分</dt><dd data-field="score"></dd>' +
    '<dt>场景</dt><dd data-field="scenario"></dd>' +
    '<dt>输入价格</dt><dd data-field="input"></dd>' +
    '<dt>输出价格</dt><dd data-field="output"></dd>' +
    '<dt>速度</dt><dd data-field="speed"></dd>' +
    '<dt>更新时间</dt><dd data-field="time"></dd>' +
    '</dl>' +
    '<a class="hf-modal__link" href="#" hidden>查看详情页 →</a>' +
    '</div>';
  document.body.appendChild(modal);

  function openModal(row) {
    const vendorPill = vendorFilterEl.querySelector('button[data-hf-vendor="' + row.dataset.hfVendor + '"]');
    modal.querySelector(".hf-modal__title").textContent = row.querySelector(".hf-table__name code")?.textContent || "";
    modal.querySelector(".hf-modal__meta").textContent =
      (vendorPill ? vendorPill.textContent.trim() : "") + " · " + row.dataset.hfSeries;
    ["score", "scenario", "input", "output", "speed", "time"].forEach((f) => {
      const cell = row.querySelector('[data-field="' + f + '"]');
      const target = modal.querySelector('[data-field="' + f + '"]');
      if (!target) return;
      if (f === "scenario" && cell) {
        // 场景列是多个标签，拼成顿号分隔的文本
        const tags = Array.from(cell.querySelectorAll(".rec-scenario-tag")).map((t) => t.textContent.trim());
        target.textContent = tags.length ? tags.join("、") : cell.textContent.trim();
      } else {
        target.textContent = cell ? cell.textContent.trim() : "—";
      }
    });
    const link = modal.querySelector(".hf-modal__link");
    const detailLink = row.querySelector(".hf-table__name a");
    if (detailLink) {
      link.href = detailLink.href;
      link.hidden = false;
    } else {
      link.hidden = true;
    }
    modal.hidden = false;
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    modal.hidden = true;
    document.body.style.overflow = "";
  }

  modal.addEventListener("click", (e) => {
    if (e.target.closest("[data-hf-close]")) closeModal();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !modal.hidden) closeModal();
  });

  /* ---------- 事件：厂商 / 系列级联 / 行模态 ---------- */
  section.addEventListener("click", (e) => {
    // 点击行打开详情模态（模型名链接保持原有跳转）。
    // 注意行自身也带 data-hf-vendor/series 属性，必须先于筛选项判断。
    const row = e.target.closest("tr[data-hf-model]");
    if (row && !e.target.closest("a")) {
      openModal(row);
      return;
    }
    const vendorBtn = e.target.closest("button[data-hf-vendor]");
    if (vendorBtn) {
      state.vendor = vendorBtn.dataset.hfVendor;
      state.series = "all";
      state.page = 1;
      vendorFilterEl.querySelectorAll("[data-hf-vendor]").forEach((b) => b.classList.remove("rec-filter-btn--active"));
      vendorBtn.classList.add("rec-filter-btn--active");
      render();
      return;
    }
    const seriesBtn = e.target.closest("button[data-hf-series]");
    if (seriesBtn) {
      state.series = seriesBtn.dataset.hfSeries;
      state.page = 1;
      seriesFilterEl.querySelectorAll("[data-hf-series]").forEach((b) => b.classList.remove("rec-filter-btn--active"));
      seriesBtn.classList.add("rec-filter-btn--active");
      renderTable();
      return;
    }
    const pageBtn = e.target.closest("[data-page]");
    if (pageBtn && !pageBtn.disabled) {
      const list = currentModels();
      const totalPages = Math.max(1, Math.ceil(list.length / state.pageSize));
      const p = pageBtn.dataset.page;
      if (p === "prev") state.page = Math.max(1, state.page - 1);
      else if (p === "next") state.page = Math.min(totalPages, state.page + 1);
      else state.page = parseInt(p, 10) || 1;
      renderTable();
      scrollToTop();
    }
  });

  // 默认视图按综合评分降序（评分缺失的排后面），并重排 DOM 行
  const scoreOf = (m) => {
    const cell = m.el.querySelector('[data-field="score"]');
    const n = cell ? parseFloat(cell.textContent) : NaN;
    return isNaN(n) ? -1 : n;
  };
  models.sort((x, y) => scoreOf(y) - scoreOf(x));
  models.forEach((m) => tbody.appendChild(m.el));

  // 初始渲染
  render();
})();

/* ============================================
   模型对比页：厂商 → 系列 → 模型 三级级联 + 多维度对比
   数据来自模型详情页 front matter（构建时内嵌为 JSON）
   ============================================ */
(function () {
  "use strict";

  const root = document.getElementById("model-compare");
  const resultEl = root && root.querySelector(".model-compare__result");
  if (!root || !resultEl) return;

  // 由扁平模型列表重建 厂商 → 系列 → 模型 树
  let vendors;
  try {
    const flat = JSON.parse(resultEl.dataset.models);
    const vMap = new Map();
    flat.forEach(function (m) {
      if (!vMap.has(m.vendor)) vMap.set(m.vendor, { name: m.vendor, series: new Map() });
      const v = vMap.get(m.vendor);
      if (!v.series.has(m.series)) v.series.set(m.series, []);
      v.series.get(m.series).push(m);
    });
    vendors = Array.from(vMap.values()).map(function (v) {
      return {
        name: v.name,
        series: Array.from(v.series.entries()).map(function (e) {
          return { name: e[0], models: e[1] };
        })
      };
    });
  } catch (e) { return; }
  if (!vendors || !vendors.length) return;

  function el(s) { return root.querySelector(s); }
  const sel = {
    aVendor: el('[data-pick="a-vendor"]'),
    aSeries: el('[data-pick="a-series"]'),
    aModel: el('[data-pick="a-model"]'),
    bVendor: el('[data-pick="b-vendor"]'),
    bSeries: el('[data-pick="b-series"]'),
    bModel: el('[data-pick="b-model"]')
  };

  // 详情页 front matter 里价格/速度等是展示字符串，数值需解析后才能比较
  function numOf(v) {
    if (v === null || v === undefined) return null;
    const m = String(v).match(/-?\d+(\.\d+)?/);
    return m ? parseFloat(m[0]) : null;
  }
  function priceNum(v) { return typeof v === "string" && v.indexOf("免费") !== -1 ? 0 : numOf(v); }
  function ctxNum(v) {
    if (!v) return null;
    const m = String(v).match(/([\d.]+)\s*([KM])?/i);
    if (!m) return null;
    let n = parseFloat(m[1]);
    if (m[2] && m[2].toUpperCase() === "M") n *= 1e6;
    else if (m[2] && m[2].toUpperCase() === "K") n *= 1e3;
    return n;
  }
  function valueOf(m) {
    const s = m.scores && m.scores.overall !== undefined ? numOf(m.scores.overall) : null;
    const out = priceNum(m.output);
    if (s === null || !out) return null;
    return Math.round((s / out) * 10) / 10;
  }
  const disp = (v) => (v === null || v === undefined || v === "" ? "—" : v);
  function fmtScen(v) { return v && v.length ? v.join("、") : "—"; }

  function setOptions(select, options, value) {
    select.innerHTML = options.map((o) => '<option value="' + o.v + '">' + o.label + "</option>").join("");
    if (value !== undefined) select.value = value;
  }
  function fillVendor(w) { setOptions(sel[w + "Vendor"], vendors.map((v, i) => ({ v: i, label: v.name }))); }
  function fillSeries(w) {
    const v = vendors[+sel[w + "Vendor"].value];
    setOptions(sel[w + "Series"], v.series.map((s, i) => ({ v: i, label: s.name })));
  }
  function fillModel(w) {
    const v = vendors[+sel[w + "Vendor"].value];
    const s = v.series[+sel[w + "Series"].value];
    setOptions(sel[w + "Model"], s.models.map((m, i) => ({ v: i, label: m.id })));
  }
  function currentModel(w) {
    const v = vendors[+sel[w + "Vendor"].value];
    const s = v.series[+sel[w + "Series"].value];
    return s.models[+sel[w + "Model"].value];
  }
  function setModel(w, vi, si, mi) {
    sel[w + "Vendor"].value = vi;
    fillSeries(w);
    sel[w + "Series"].value = si;
    fillModel(w);
    sel[w + "Model"].value = mi;
  }

  // 对比行：num 数值用于判定胜负，disp 展示文案；better=high/low 表示谁优
  function rows(a, b) {
    const cat = (k) => [numOf(a.scores[k]), numOf(b.scores[k])];
    const mk = (label, num, d, better, bar) => ({ label, num, disp: d, better, bar });
    return [
      mk("综合评分", cat("overall"), null, "high", true),
      mk("已验证评分", cat("verified"), null, "high", true),
      mk("场景", null, [fmtScen(a.scen), fmtScen(b.scen)], null, false),
      mk("智能体", cat("agentic"), null, "high", true),
      mk("编程", cat("coding"), null, "high", true),
      mk("推理", cat("reasoning"), null, "high", true),
      mk("多模态", cat("multimodal"), null, "high", true),
      mk("知识", cat("knowledge"), null, "high", true),
      mk("速度", [numOf(a.speed), numOf(b.speed)], [disp(a.speed), disp(b.speed)], "high", false),
      mk("首字延迟 TTFT", [numOf(a.ttft), numOf(b.ttft)], [disp(a.ttft), disp(b.ttft)], "low", false),
      mk("上下文窗口", [ctxNum(a.ctx), ctxNum(b.ctx)], [disp(a.ctx), disp(b.ctx)], "high", false),
      mk("输入价格", [priceNum(a.input), priceNum(b.input)], [disp(a.input), disp(b.input)], "low", false),
      mk("输出价格", [priceNum(a.output), priceNum(b.output)], [disp(a.output), disp(b.output)], "low", false),
      mk("性价比（分/$）", [valueOf(a), valueOf(b)], [disp(valueOf(a)), disp(valueOf(b))], "high", false),
      mk("开源 / 闭源", null, [disp(a.source), disp(b.source)], null, false),
      mk("发布时间", null, [disp(a.released), disp(b.released)], null, false)
    ];
  }

  function winnerClass(row, idx) {
    if (!row.better || !row.num) return "";
    const x = row.num[0], y = row.num[1];
    if (x === null || x === undefined || y === null || y === undefined || x === y) return "";
    const aWins = row.better === "high" ? x > y : x < y;
    return (idx === 0) === aWins ? " model-compare__win" : " model-compare__lose";
  }

  function barHtml(n) {
    if (n === null || n === undefined) return "";
    const w = Math.max(0, Math.min(100, n));
    return '<span class="model-compare__bar"><i style="width:' + w + '%"></i></span>';
  }

  function modelTitle(m, which) {
    const link = m.url ? '<a href="' + m.url + '">' + m.id + "</a>" : m.id;
    return "<strong>" + link + "</strong><small>" + m.vendor + " · " + m.series + " · " + which + "</small>";
  }

  function render() {
    const a = currentModel("a");
    const b = currentModel("b");
    let body = "";
    rows(a, b).forEach((row) => {
      const d0 = row.disp ? disp(row.disp[0]) : disp(row.num ? row.num[0] : null);
      const d1 = row.disp ? disp(row.disp[1]) : disp(row.num ? row.num[1] : null);
      const barA = row.bar ? barHtml(row.num ? row.num[0] : null) : "";
      const barB = row.bar ? barHtml(row.num ? row.num[1] : null) : "";
      body +=
        "<tr>" +
        '<th scope="row">' + row.label + "</th>" +
        '<td class="' + winnerClass(row, 0).trim() + '">' + d0 + barA + "</td>" +
        '<td class="' + winnerClass(row, 1).trim() + '">' + d1 + barB + "</td>" +
        "</tr>";
    });
    resultEl.innerHTML =
      '<table class="model-compare__table hf-table">' +
      "<thead><tr>" +
      "<th>指标</th>" +
      "<th>" + modelTitle(a, "A") + "</th>" +
      "<th>" + modelTitle(b, "B") + "</th>" +
      "</tr></thead><tbody>" + body + "</tbody></table>";
  }

  // 初始化：填充厂商下拉，默认选综合评分最高的两个模型（不同厂商优先）
  fillVendor("a"); fillVendor("b");
  const sorted = [];
  vendors.forEach(function (v, vi) {
    v.series.forEach(function (s, si) {
      s.models.forEach(function (m, mi) {
        m._vi = vi; m._si = si; m._mi = mi;
        sorted.push(m);
      });
    });
  });
  sorted.sort(function (x, y) {
    const sx = x.scores && x.scores.overall !== undefined ? x.scores.overall : 0;
    const sy = y.scores && y.scores.overall !== undefined ? y.scores.overall : 0;
    return sy - sx;
  });
  // 支持 /compare/?model=<slug>：把指定模型预选为 A
  const urlSlug = new URLSearchParams(location.search).get("model");
  const first = (urlSlug && sorted.find(function (m) { return m.slug === urlSlug; })) || sorted[0];
  const second = sorted.find(function (m) { return m._vi !== first._vi; }) || sorted[1] || first;
  setModel("a", first._vi, first._si, first._mi);
  setModel("b", second._vi, second._si, second._mi);

  // 级联：厂商 → 系列 → 模型
  ["a", "b"].forEach(function (w) {
    sel[w + "Vendor"].addEventListener("change", function () {
      fillSeries(w);
      fillModel(w);
      render();
    });
    sel[w + "Series"].addEventListener("change", function () {
      fillModel(w);
      render();
    });
    sel[w + "Model"].addEventListener("change", render);
  });

  // 交换 A / B
  root.querySelector("[data-swap]").addEventListener("click", function () {
    const av = sel.aVendor.value, as = sel.aSeries.value, am = sel.aModel.value;
    setModel("a", +sel.bVendor.value, +sel.bSeries.value, +sel.bModel.value);
    setModel("b", +av, +as, +am);
    render();
  });

  render();
})();
