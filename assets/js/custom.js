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
  let currentCategory = "all";

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
    if (currentCategory !== "all") {
      const category = row.dataset.category || "待确认";
      if (category !== currentCategory) return false;
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
      case "category":
        return (row.dataset.category || "").toLowerCase();
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

  // 事件委托：表头排序 / 场景筛选 / 类型筛选
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
    // 类型筛选
    const categoryBtn = e.target.closest("[data-category]");
    if (categoryBtn) {
      currentCategory = categoryBtn.dataset.category;
      recSection.querySelectorAll("[data-category]").forEach((b) => b.classList.remove("rec-filter-btn--active"));
      categoryBtn.classList.add("rec-filter-btn--active");
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
  const seriesFilterEl = document.getElementById("hf-series-filter");
  const tbody = document.getElementById("hf-model-tbody");
  const countEl = document.getElementById("hf-count");
  const paginationEl = document.getElementById("hf-pagination");
  const searchInput = document.getElementById("hf-search");

  // 任务类型中文标签（服务端注入的 JSON，键为 HF pipeline_tag）
  const tableEl = tbody.closest("table");
  let TASK_LABELS = {};
  try { TASK_LABELS = JSON.parse(tableEl.dataset.taskLabels || "{}"); } catch { TASK_LABELS = {}; }

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
    series: r.dataset.hfSeries,
    search: (r.dataset.search || "").toLowerCase()
  }));

  // 任务类型列：英文键 → 中文标签；更新时间列：绝对时间 → 相对时间
  allRows.forEach((r) => {
    const taskTd = r.querySelector(".hf-table__task");
    const tag = taskTd && taskTd.querySelector(".rec-scenario-tag");
    if (tag && TASK_LABELS[tag.textContent.trim()]) tag.textContent = TASK_LABELS[tag.textContent.trim()];
    const timeTd = r.querySelector(".hf-table__time");
    if (timeTd) {
      const label = relTime(timeTd.textContent.trim());
      if (label) timeTd.textContent = label;
    }
  });

  // 分组：厂商索引 -> {series: Map(系列名 -> 数量)}
  const vendorMap = new Map();
  models.forEach((m) => {
    if (!vendorMap.has(m.vendor)) vendorMap.set(m.vendor, { series: new Map() });
    const v = vendorMap.get(m.vendor);
    v.series.set(m.series, (v.series.get(m.series) || 0) + 1);
  });

  const PAGE_SIZES = [30, 50, 100];
  const state = { vendor: "all", series: "all", search: "", page: 1, pageSize: 50 };

  function fmt(n) { return n.toLocaleString("en-US"); }

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function scrollToTop() {
    section.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  /* ---------- 系列筛选按钮：随厂商级联刷新 ---------- */
  function renderSeriesFilter() {
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
    if (state.search) {
      const q = state.search.toLowerCase();
      list = list.filter((m) => m.search.indexOf(q) !== -1);
    }
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
      div.textContent = "没有匹配的模型，换个筛选条件或关键词试试。";
      tableAnchor().insertBefore(div, tableAnchor().firstChild);
    }

    countEl.textContent = "共 " + fmt(total) + " 个模型" +
      (totalPages > 1 ? " \u00b7 第 " + state.page + " / " + totalPages + " 页" : "");

    renderPagination(totalPages);
  }

  function tableAnchor() {
    return tbody.closest(".hf-table-wrap").parentNode;
  }

  /* ---------- 渲染：分页控件 ---------- */
  function renderPagination(totalPages) {
    if (totalPages <= 1) {
      paginationEl.innerHTML = "";
      return;
    }
    let html = '<button type="button" class="hf-page-btn" data-page="prev"' + (state.page === 1 ? " disabled" : "") + '>\u2039 上一页</button>';
    const pages = [];
    const addPage = (p) => { if (pages.indexOf(p) === -1) pages.push(p); };
    const pushRange = (a, b) => { for (let i = a; i <= b; i++) addPage(i); };
    if (totalPages <= 7) {
      pushRange(1, totalPages);
    } else {
      addPage(1);
      if (state.page > 3) pages.push("\u2026");
      pushRange(Math.max(2, state.page - 1), Math.min(totalPages - 1, state.page + 1));
      if (state.page < totalPages - 2) pages.push("\u2026");
      addPage(totalPages);
    }
    pages.forEach((p) => {
      if (p === "\u2026") {
        html += '<span class="hf-page-ellipsis">\u2026</span>';
      } else {
        html += '<button type="button" class="hf-page-btn' + (p === state.page ? " hf-page-btn--active" : "") + '" data-page="' + p + '">' + p + '</button>';
      }
    });
    html += '<button type="button" class="hf-page-btn" data-page="next"' + (state.page === totalPages ? " disabled" : "") + '>下一页 \u203a</button>';
    html += '<span class="hf-page-size">每页 <select id="hf-page-size">' +
      PAGE_SIZES.map((s) => '<option value="' + s + '"' + (s === state.pageSize ? " selected" : "") + '>' + s + '</option>').join("") +
      '</select> 条</span>';
    paginationEl.innerHTML = html;
  }

  function render() {
    renderSeriesFilter();
    renderTable();
  }

  /* ---------- 事件：厂商 / 系列级联 ---------- */
  section.addEventListener("click", (e) => {
    const vendorBtn = e.target.closest("[data-hf-vendor]");
    if (vendorBtn) {
      state.vendor = vendorBtn.dataset.hfVendor;
      state.series = "all";
      state.page = 1;
      vendorFilterEl.querySelectorAll("[data-hf-vendor]").forEach((b) => b.classList.remove("rec-filter-btn--active"));
      vendorBtn.classList.add("rec-filter-btn--active");
      render();
      return;
    }
    const seriesBtn = e.target.closest("[data-hf-series]");
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

  paginationEl.addEventListener("change", (e) => {
    if (e.target.id === "hf-page-size") {
      state.pageSize = parseInt(e.target.value, 10) || 50;
      state.page = 1;
      renderTable();
    }
  });

  let searchTimer = null;
  searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      state.search = searchInput.value.trim();
      state.page = 1;
      renderTable();
    }, 200);
  });

  // 初始渲染
  render();
})();
