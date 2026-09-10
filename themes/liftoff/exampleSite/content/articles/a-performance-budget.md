---
title: "A performance budget you can actually keep"
date: 2026-05-15
author: "Kevin"
description: "Three numbers worth defending on a static site, and what Liftoff spends them on."
tags: ["performance", "css"]
categories: ["Design notes"]
---

A performance budget only works if it is short enough to remember.
Three numbers are enough for a content site.

| Budget            | Target        | What breaks it        |
| ----------------- | ------------- | --------------------- |
| Requests per page | Under 10      | Web fonts, analytics  |
| CSS               | Under 30 kB   | Utility frameworks    |
| JavaScript        | Under 10 kB   | Anything with a build |

Liftoff spends its JavaScript on three things: the theme toggle, the
copy buttons on code blocks, and the blueprint filter. All three
degrade to something usable when scripting is off, which is the only
reason they are allowed to exist at all.

The fonts are the expensive part. Fira Code is loaded as two woff2
files, subset to Latin, and only for code. Body text uses the system
font stack, which costs nothing and looks native on every platform.

> [!TIP]
> Before adding a dependency, check whether the browser already does
> it. Details and summary give you accordions, dialog gives you modals,
> and neither needs a kilobyte.

Nothing here is clever. It is just a list of things not done.
