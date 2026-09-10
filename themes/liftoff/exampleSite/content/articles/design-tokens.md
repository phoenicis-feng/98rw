---
title: "On design tokens"
date: 2026-05-02
author: "Kevin"
description: "Why Liftoff exposes its palette and spacing as CSS variables."
tags: ["design", "css"]
---

Liftoff exposes its palette, spacing scale, and typography as CSS
custom properties on `:root`. Consumers can theme the site without
forking the theme.

## Override pattern

Drop a small CSS file into your site's `assets/css/` and import it
after the theme's bundle.

```css
:root {
  --color-accent: #ff7a59;
  --color-bg: #0d0a0a;
}
```

Light mode is opt-in by setting `data-theme="light"` on `<html>`. The
built-in toggle remembers the user's choice in `localStorage` with
`prefers-color-scheme` as the fallback.

## Why not Tailwind

For a theme distributed as a Hugo module, a Node toolchain is
friction. Plain CSS with variables ships zero dependencies and stays
readable.
