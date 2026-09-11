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

  // /models/ 总索引：勾选两个模型卡片，跳转到 /compare/ 页面查看对比（最多勾 2 个）
  document.querySelectorAll(".model-select").forEach((wrap) => {
    let models;
    try { models = JSON.parse(wrap.dataset.models); } catch { return; }
    if (!Array.isArray(models) || models.length < 2) return;

    const byUrl = new Map(models.map((m) => [m.url, m]));
    const boxes = Array.from(wrap.querySelectorAll('input[type="checkbox"][data-model]'));
    const result = wrap.querySelector(".model-select__result");
    if (!result) return;

    const update = () => {
      const picked = boxes
        .filter((b) => b.checked)
        .map((b) => byUrl.get(b.dataset.model))
        .filter(Boolean);
      // 只能对比 2 个：勾满后禁用其余勾选框
      const full = picked.length >= 2;
      boxes.forEach((b) => { if (!b.checked) b.disabled = full; });
      if (!full) {
        result.innerHTML =
          "<p>勾选上方两个模型卡片，即可前往对比页面对比规格与跑分。</p>";
        return;
      }
      const href = "/compare/?models=" +
        picked.slice(0, 2).map((m) => encodeURIComponent(m.url)).join(",");
      result.innerHTML =
        `<a class="model-select__go" href="${href}">前往对比这 2 个模型 →</a>`;
    };

    boxes.forEach((b) => b.addEventListener("change", update));
    update();
  });
})();

/* ===== 模型推荐页面：分类 Tab 切换 ===== */
(() => {
  "use strict";
  const recSection = document.querySelector(".rec-section");
  if (!recSection) return;

  const tabs = recSection.querySelectorAll(".rec-tab");
  const categories = recSection.querySelectorAll("[data-category]");

  function switchTab(tabId) {
    tabs.forEach((t) => t.classList.remove("rec-tab--active"));
    categories.forEach((c) => c.classList.remove("rec-category--active"));

    const activeTab = recSection.querySelector(`.rec-tab[data-tab="${tabId}"]`);
    const activeCat = recSection.querySelector(`[data-category][id="rec-${tabId}"]`);
    if (activeTab) activeTab.classList.add("rec-tab--active");
    if (activeCat) activeCat.classList.add("rec-category--active");
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => switchTab(tab.dataset.tab));
  });

  // 默认激活第一个
  if (tabs.length > 0) switchTab(tabs[0].dataset.tab);
})();

/* ===== 模型推荐页面：卡片排序 ===== */
(() => {
  "use strict";
  const recSection = document.querySelector(".rec-section");
  if (!recSection) return;

  // 从类似 "$5/M" 或 "¥2/M" 中提取数值
  function parsePrice(str) {
    if (!str) return 0;
    const match = str.match(/[\d.]+/);
    return match ? parseFloat(match[0]) : 0;
  }

  recSection.addEventListener("change", (e) => {
    if (!e.target.matches("[data-sort]")) return;
    const select = e.target;
    const grid = select.closest(".rec-category").querySelector(".rec-grid");
    if (!grid) return;
    const cards = Array.from(grid.querySelectorAll(".rec-card"));
    const sortBy = select.value;

    cards.sort((a, b) => {
      if (sortBy === "default") {
        // 按原始 rank 顺序排列
        const ra = parseInt(a.querySelector(".rec-card__rank")?.textContent?.replace("#", "") || "0");
        const rb = parseInt(b.querySelector(".rec-card__rank")?.textContent?.replace("#", "") || "0");
        return ra - rb;
      }
      const rawA = a.dataset[sortBy] || "0";
      const rawB = b.dataset[sortBy] || "0";
      const va = sortBy === "price" ? parsePrice(rawA) : (parseFloat(rawA) || 0);
      const vb = sortBy === "price" ? parsePrice(rawB) : (parseFloat(rawB) || 0);
      // 价格升序，其他降序
      return sortBy === "price" ? va - vb : vb - va;
    });

    cards.forEach((card) => grid.appendChild(card));
  });
})();

/* ===== OpenRouter 模型列表：搜索 + 筛选 + 排序 ===== */
(() => {
  "use strict";
  const section = document.querySelector(".openrouter-section");
  if (!section) return;

  const searchInput = document.getElementById("openrouter-search");
  const vendorSelect = document.getElementById("openrouter-vendor");
  const categorySelect = document.getElementById("openrouter-category");
  const sortSelect = document.getElementById("openrouter-sort");
  const grid = document.getElementById("openrouter-grid");
  const emptyState = document.querySelector(".openrouter-empty");

  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll(".openrouter-card"));

  function parsePrice(str) {
    if (!str || str === "免费") return 0;
    const match = str.match(/[\d.]+/);
    return match ? parseFloat(match[0]) : 0;
  }

  function getContextNum(ctx) {
    if (!ctx) return 0;
    const match = ctx.match(/(\d+)/);
    if (!match) return 0;
    const num = parseFloat(match[1]);
    if (ctx.includes("M")) return num * 1000000;
    if (ctx.includes("K")) return num * 1000;
    return num;
  }

  function filterAndSort() {
    const q = (searchInput?.value || "").toLowerCase().trim();
    const vendor = vendorSelect?.value || "";
    const category = categorySelect?.value || "";
    const sortBy = sortSelect?.value || "default";

    let visible = 0;
    cards.forEach((card) => {
      const name = (card.dataset.name || "").toLowerCase();
      const cardVendor = (card.dataset.vendor || "").toLowerCase();
      const cardCat = (card.dataset.category || "").toLowerCase();

      const matchesSearch = !q || name.includes(q) || cardVendor.includes(q);
      const matchesVendor = !vendor || cardVendor === vendor.toLowerCase();
      const matchesCategory = !category || cardCat === category.toLowerCase();

      const show = matchesSearch && matchesVendor && matchesCategory;
      card.style.display = show ? "" : "none";
      if (show) visible++;
    });

    // 空状态
    if (emptyState) emptyState.style.display = visible === 0 ? "block" : "none";

    // 排序
    const sorted = cards
      .filter((c) => c.style.display !== "none")
      .sort((a, b) => {
        if (sortBy === "default") return 0;
        if (sortBy === "context") {
          return getContextNum(b.dataset.context) - getContextNum(a.dataset.context);
        }
        if (sortBy === "price_input") {
          return parsePrice(a.dataset.priceInput) - parsePrice(b.dataset.priceInput);
        }
        if (sortBy === "price_output") {
          return parsePrice(a.dataset.priceOutput) - parsePrice(b.dataset.priceOutput);
        }
        if (sortBy === "name") {
          return a.dataset.name.localeCompare(b.dataset.name);
        }
        if (sortBy === "vendor") {
          return a.dataset.vendor.localeCompare(b.dataset.vendor);
        }
        return 0;
      });

    sorted.forEach((card) => grid.appendChild(card));
  }

  searchInput?.addEventListener("input", filterAndSort);
  vendorSelect?.addEventListener("change", filterAndSort);
  categorySelect?.addEventListener("change", filterAndSort);
  sortSelect?.addEventListener("change", filterAndSort);

  // 初始执行
  filterAndSort();
})();
