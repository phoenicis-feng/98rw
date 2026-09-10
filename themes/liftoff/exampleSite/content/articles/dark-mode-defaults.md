---
title: "Dark mode that respects the system"
date: 2026-05-08
author: "Kevin"
description: "Liftoff opens in the visitor's preferred scheme and only remembers a choice once it is made."
tags: ["design", "css"]
categories: ["Design notes"]
---

A theme toggle that defaults to dark for everyone is a preference
disguised as a feature. Liftoff reads `prefers-color-scheme` first, and
only writes to `localStorage` once someone actually picks a scheme.

```js
const stored = localStorage.getItem("liftoff.theme");
const system = matchMedia("(prefers-color-scheme: light)").matches;
```

That ordering matters. A visitor whose system is light gets a light
page on first load, without a flash of dark. A visitor who then picks
dark keeps dark, even if their system changes later, because an
explicit choice outranks an inferred one.

Both schemes are defined as tokens. Dark is the default on `:root`,
light overrides it under `[data-theme="light"]`, and every component
reads variables rather than literal colours.

```css
[data-theme="light"] {
  --color-bg: #ffffff;
  --color-text: #0b1020;
}
```

Which means adding a third scheme is a block of variables, not a pass
through every stylesheet.
