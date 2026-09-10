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

    const picks = {};
    wrap.querySelectorAll("select[data-pick]").forEach((sel, i) => {
      sel.innerHTML = models
        .map((m, j) => `<option value="${j}">${esc(m.name)}</option>`)
        .join("");
      sel.value = String(i % Math.min(2, models.length));
      picks[sel.dataset.pick] = sel;
    });

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
})();
