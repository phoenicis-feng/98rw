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

/* ===== 推荐页面：分类 Tab 切换 + 卡片排序（联动） ===== */
(() => {
  "use strict";
  const recSection = document.querySelector(".rec-section");
  if (!recSection) return;

  const tabs = recSection.querySelectorAll(".rec-tab");
  const categories = recSection.querySelectorAll("[data-category]");
  let currentSortType = "comprehensive";

  function parsePrice(str) {
    if (!str) return 0;
    const match = str.match(/[\d.]+/);
    return match ? parseFloat(match[0]) : 0;
  }

  function sortGrid(grid, sortType) {
    const cards = Array.from(grid.querySelectorAll(".rec-card"));
    cards.sort((a, b) => {
      if (sortType === "price") {
        const va = parsePrice(a.dataset.price || "0");
        const vb = parsePrice(b.dataset.price || "0");
        return va - vb;
      }
      if (sortType === "strongest") {
        const va = parseFloat(a.dataset.reasoning || "0");
        const vb = parseFloat(b.dataset.reasoning || "0");
        return vb - va;
      }
      const weights = { reasoning: 0.3, coding: 0.3, chinese: 0.2, longtext: 0.2 };
      let scoreA = 0, scoreB = 0;
      for (const [key, w] of Object.entries(weights)) {
        const va = parseFloat(a.dataset[key] || "0");
        const vb = parseFloat(b.dataset[key] || "0");
        scoreA += va * w;
        scoreB += vb * w;
      }
      return scoreB - scoreA;
    });

    // 将排序后的完整候选池写回 DOM（候选池可能大于展示上限）
    cards.forEach((card) => grid.appendChild(card));

    // 只展示排名靠前的卡片（默认前 5 名），其余隐藏，并重新编号
    const limit = parseInt(grid.dataset.limit || "6", 10);
    const displayLimit = Number.isNaN(limit) || limit <= 0 ? 6 : limit;
    cards.forEach((card, i) => {
      card.style.display = i < displayLimit ? "" : "none";
      const rankEl = card.querySelector(".rec-card__rank");
      rankEl && (rankEl.textContent = "#" + (i + 1));
    });

    renderComparison(grid, displayLimit);
  }

  // 依当前展示的卡片，动态生成“TOP N 对比”表
  function escapeHtml(str) {
    return String(str == null ? "" : str)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function renderComparison(grid, displayLimit) {
    const cat = grid.closest("[data-category]");
    const comp = cat && cat.querySelector("[data-comparison]");
    if (!comp) return;

    const title = comp.querySelector(".rec-comparison__title");
    const box = comp.querySelector(".rec-comparison__table");
    if (!title || !box) return;

    const modelCards = Array.from(grid.querySelectorAll(".rec-card"))
      .filter((c) => c.style.display !== "none")
      .slice(0, displayLimit);

    // 不足 2 个时不展示对比表
    if (modelCards.length < 2) {
      box.className = "rec-comparison__table rec-comparison__table--empty";
      box.innerHTML = "";
      return;
    }

    title.textContent = "TOP " + modelCards.length + " 对比";
    box.className = "rec-comparison__table";

    const getName = (c) => {
      const el = c.querySelector(".rec-card__name");
      return el ? el.textContent.trim() : "—";
    };

    // 转置：每个模型一行，维度作为列
    const dims = [
      ["推理", (c) => c.dataset.reasoning],
      ["编码", (c) => c.dataset.coding],
      ["中文", (c) => c.dataset.chinese],
      ["长文本", (c) => c.dataset.longtext],
      ["输入价格", (c) => c.dataset.price],
      ["上下文", (c) => c.dataset.context],
      ["模态", (c) => c.dataset.modalities],
    ];

    let html = "<table><thead><tr><th>模型</th>";
    dims.forEach(([label]) => { html += "<th>" + escapeHtml(label) + "</th>"; });
    html += "</tr></thead><tbody>";

    modelCards.forEach((c, i) => {
      html += '<tr><td class="rec-comparison__label">#' + (i + 1) + " " + escapeHtml(getName(c)) + "</td>";
      dims.forEach(([, getter]) => { html += "<td>" + escapeHtml(getter(c)) + "</td>"; });
      html += "</tr>";
    });

    html += "</tbody></table>";
    box.innerHTML = html;
  }

  function getActiveCategory() {
    return recSection.querySelector("[data-category].rec-category--active");
  }

  function applySortToActive() {
    const activeCat = getActiveCategory();
    if (!activeCat) return;
    const activeBtn = activeCat.querySelector(`.rec-sort-btn[data-sort="${currentSortType}"]`);
    activeCat.querySelectorAll(".rec-sort-btn").forEach((b) => b.classList.remove("rec-sort-btn--active"));
    if (activeBtn) activeBtn.classList.add("rec-sort-btn--active");
    recSection.querySelectorAll(".rec-grid").forEach((grid) => sortGrid(grid, currentSortType));
  }

  function switchTab(tabId) {
    tabs.forEach((t) => {
      if (!t.classList.contains("free-filter")) t.classList.remove("rec-tab--active");
    });
    categories.forEach((c) => c.classList.remove("rec-category--active"));

    const activeTab = recSection.querySelector(`.rec-tab[data-tab="${tabId}"]`);
    const activeCat = recSection.querySelector(`[data-category][id="rec-${tabId}"]`);
    if (activeTab) activeTab.classList.add("rec-tab--active");
    if (activeCat) activeCat.classList.add("rec-category--active");

    applySortToActive();
  }

  recSection.addEventListener("click", (e) => {
    const btn = e.target.closest(".rec-sort-btn");
    if (!btn) return;
    const sortType = btn.dataset.sort;

    currentSortType = sortType;
    recSection.querySelectorAll(".rec-sort-btn").forEach((b) => b.classList.remove("rec-sort-btn--active"));
    btn.classList.add("rec-sort-btn--active");
    recSection.querySelectorAll(".rec-grid").forEach((grid) => sortGrid(grid, sortType));
  });

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      if (!tab.classList.contains("free-filter")) switchTab(tab.dataset.tab);
    });
  });

  if (tabs.length > 0) {
    switchTab(tabs[0].dataset.tab);
  }
})();
