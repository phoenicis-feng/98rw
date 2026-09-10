(() => {
  "use strict";

  const root = document.documentElement;
  const storageKey = "liftoff.theme";

  /* Theme: initial selection from storage or prefers-color-scheme. */

  const getInitialTheme = () => {
    const stored = localStorage.getItem(storageKey);
    if (stored === "light" || stored === "dark") return stored;
    return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  };

  const applyTheme = (theme) => {
    root.setAttribute("data-theme", theme);
  };

  applyTheme(getInitialTheme());

  /* Tabs */

  document.querySelectorAll(".tabs").forEach((tabs) => {
    const buttons = tabs.querySelectorAll('[role="tab"]');
    const panels = tabs.querySelectorAll(".tabs__panel");
    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const target = btn.getAttribute("data-tab");
        buttons.forEach((b) => b.setAttribute("aria-selected", b === btn ? "true" : "false"));
        panels.forEach((p) => {
          p.hidden = p.getAttribute("data-panel") !== target;
        });
      });
      btn.addEventListener("keydown", (e) => {
        const list = Array.from(buttons);
        const idx = list.indexOf(btn);
        if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
          e.preventDefault();
          const dir = e.key === "ArrowRight" ? 1 : -1;
          const next = list[(idx + dir + list.length) % list.length];
          next.click();
          next.focus();
        }
      });
    });
  });

  /* Repo stats: client-side fetch with 1h localStorage cache. */

  const fetchRepoStats = async (el) => {
    const { repoHost, repoOwner, repoName } = el.dataset;
    if (!repoOwner || !repoName) return;
    const cacheKey = `liftoff.repo.${repoHost}.${repoOwner}.${repoName}`;
    const now = Date.now();
    const ttlMs = 60 * 60 * 1000;
    let data = null;
    try {
      const cached = JSON.parse(localStorage.getItem(cacheKey) || "null");
      if (cached && now - cached.t < ttlMs) data = cached.d;
    } catch (e) { /* ignore */ }

    if (!data) {
      const url = repoHost === "github"
        ? `https://api.github.com/repos/${repoOwner}/${repoName}`
        : `https://codeberg.org/api/v1/repos/${repoOwner}/${repoName}`;
      try {
        const res = await fetch(url, { headers: { accept: "application/json" } });
        if (!res.ok) return;
        data = await res.json();
        localStorage.setItem(cacheKey, JSON.stringify({ t: now, d: data }));
      } catch (e) { return; }
    }

    const stars = data.stargazers_count ?? data.stars_count;
    if (typeof stars === "number") {
      const target = el.querySelector('[data-stat="stars"]');
      if (target) target.textContent = stars.toLocaleString();
    }
  };

  document.querySelectorAll(".repo-stats").forEach(fetchRepoStats);

  /* Click-outside closes the language dropdown. */

  document.addEventListener("click", (event) => {
    document.querySelectorAll("details.lang-switcher[open]").forEach((d) => {
      if (!d.contains(event.target)) d.removeAttribute("open");
    });
  });

  /* Click delegation: theme toggle, mobile menu, code copy, blueprint filter. */

  document.addEventListener("click", (event) => {
    const themeToggle = event.target.closest('[data-action="toggle-theme"]');
    if (themeToggle) {
      const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      localStorage.setItem(storageKey, next);
      applyTheme(next);
      return;
    }

    const menuToggle = event.target.closest('[data-action="toggle-menu"]');
    if (menuToggle) {
      const header = menuToggle.closest(".site-header");
      if (!header) return;
      const open = header.getAttribute("data-menu-open") === "true";
      header.setAttribute("data-menu-open", open ? "false" : "true");
      menuToggle.setAttribute("aria-expanded", open ? "false" : "true");
      return;
    }

    const copyBtn = event.target.closest('[data-action="copy-code"]');
    if (copyBtn) {
      const block = copyBtn.closest(".codeblock");
      const code = block && block.querySelector("pre");
      if (!code || !navigator.clipboard) return;
      navigator.clipboard.writeText(code.innerText).then(() => {
        const original = copyBtn.textContent;
        copyBtn.setAttribute("data-state", "copied");
        copyBtn.textContent = copyBtn.getAttribute("data-copied-label") || "Copied";
        setTimeout(() => {
          copyBtn.removeAttribute("data-state");
          copyBtn.textContent = original;
        }, 1500);
      });
      return;
    }

    const filterBtn = event.target.closest("[data-blueprint-filter]");
    if (filterBtn) {
      const tag = filterBtn.getAttribute("data-blueprint-filter");
      const group = filterBtn.closest(".blueprints");
      if (!group) return;
      group.querySelectorAll("[data-blueprint-filter]").forEach((b) => {
        const active = b === filterBtn;
        b.setAttribute("data-active", active ? "true" : "false");
        b.setAttribute("aria-pressed", active ? "true" : "false");
      });
      group.querySelectorAll(".blueprint-card").forEach((card) => {
        const tags = (card.getAttribute("data-tags") || "").split(",");
        const show = tag === "*" || tags.includes(tag);
        card.setAttribute("data-hidden", show ? "false" : "true");
      });
    }
  });
})();
