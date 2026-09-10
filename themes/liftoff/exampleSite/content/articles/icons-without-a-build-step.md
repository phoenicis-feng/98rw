---
title: "Icons without a build step"
date: 2026-06-12
author: "Kevin"
description: "Why Liftoff fetches icons from Iconify at build time instead of shipping a font or a sprite sheet."
tags: ["icons", "performance"]
categories: ["Design notes"]
---

Icon fonts ship every glyph to every visitor. Sprite sheets need a
build step and a naming convention nobody remembers. Liftoff takes a
third route: it fetches each icon from the Iconify API while Hugo
builds, and inlines the SVG.

```go-html-template
{{ partial "icon.html" "simple-icons:codeberg" }}
```

Any set on Iconify works, addressed as `set:name`. A bare name falls
back to Material Design Icons, so `check` and `mdi:check` are the same
icon.

The trade-off is honest: your build needs network access the first time
it sees an icon. After that Hugo's file cache answers, so repeat builds
and CI runs with a warm cache stay offline. If you need fully hermetic
builds, drop SVGs into `assets/icons/` and reference them as
`local:name`.

What you get is a page that carries exactly the glyphs it uses,
inlined, with no extra request and no flash of missing icons.
