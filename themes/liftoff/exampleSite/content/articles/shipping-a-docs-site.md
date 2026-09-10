---
title: "Shipping a docs site in an afternoon"
date: 2026-06-28
author: "Kevin"
description: "A start-to-finish walkthrough: module setup, content structure, navigation, and the two decisions that cost the most time later."
tags: ["docs", "tutorial"]
categories: ["Guides"]
---

Most documentation sites die of structure, not of prose. You spend the
first afternoon on the generator, the second on navigation, and by the
third you have written four pages and lost interest. This walkthrough
skips to the part where you are writing.

## Start from the module, not from a fork

Add Liftoff as a Hugo module rather than copying it into `themes/`. You
keep the ability to update, and your repository stays small enough to
read.

```toml
# hugo.toml
[module]
  [[module.imports]]
    path = "codeberg.org/head1328/hugo-liftoff"
```

```bash
hugo mod get codeberg.org/head1328/hugo-liftoff
hugo mod tidy
```

Forking is the right call exactly once: when you want to change the
markup, not the styling. Everything visual is a CSS custom property,
and those you can override from your own site without touching the
theme.

## Structure content around questions, not features

The most common docs layout mirrors the software's architecture. That
is convenient for the person who wrote the software and useless for
everyone else. Name pages after what a reader is trying to do.

```text
content/
  docs/
    _index.md
    installation.md
    configuration.md
    customization.md
```

Each page gets a `weight`, and that weight drives both the ordering on
the index and the prev/next links at the bottom of every page. Ordering
by title looks tidy and reads like a filing cabinet.

```yaml
---
title: "Configuration"
description: "Site params, menus, and language setup."
weight: 20
---
```

> [!TIP]
> Leave gaps in your weights: 10, 20, 30. Inserting a page between two
> neighbours later is then a one-line change instead of a renumbering.

## Navigation is a menu, not a sidebar

Liftoff renders the docs index as a card grid and gives each page an
on-this-page table of contents. There is no persistent sidebar, which
is a deliberate constraint: sidebars encourage forty pages where eight
would do.

```toml
[[menus.main]]
  name = "Docs"
  pageRef = "/docs"
  weight = 10
```

Use `pageRef` rather than `url`. It resolves through Hugo's page
lookup, which means a typo becomes a build error instead of a 404 your
readers find first.

## The two decisions that cost the most later

**Deciding on languages after you have content.** Retrofitting a second
language means touching every file, every menu entry, and every data
file. If there is any chance of a second language, set it up on day one
with a single language configured. The cost is one config block.

**Putting example commands in prose.** Every command a reader might run
belongs in a fenced code block with a copy button, not inline in a
sentence. Readers skim for the grey boxes. Prose between them is
context; prose that hides a command is a support ticket.

## Deploy

Any static host works, because the output is a directory of files.

```bash
hugo --minify
```

Point your host at `public/` and you are done. No runtime, no database,
nothing to patch at two in the morning.

> [!NOTE]
> Set `baseURL` to the final URL before the first deploy. Relative
> links resolve against it, and getting it wrong produces a site that
> works locally and breaks in production.

## What to write first

Not the introduction. Write the installation page, then the page that
answers the question you get asked most often. Introductions are easiest
to write once you know what you are introducing, which is usually after
the rest exists.
