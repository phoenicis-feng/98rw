---
title: "Multilingual from day one"
date: 2026-05-24
author: "Kevin"
description: "Setting up a second language costs one config block now and a weekend later."
tags: ["i18n", "docs"]
categories: ["Guides"]
---

Retrofitting a second language is the kind of task that looks like an
afternoon and turns into a weekend. Every content file needs a
counterpart, every menu entry needs a translation, every data file
needs a variant, and every hardcoded date format turns out to be
English.

Configuring it up front costs almost nothing, even if you only ever
ship one language.

```toml
defaultContentLanguage = "en"
defaultContentLanguageInSubdir = true

[languages]
  [languages.en]
    label = "English"
    weight = 1
```

Content files then carry their language in the filename:
`about.md` and `about.de.md` sit side by side and Hugo pairs them
automatically.

> [!WARNING]
> Watch out for `relURL` in your own templates. It ignores the language
> prefix, so a link that works in your default language quietly points
> at the wrong page in every other one. Use `relLangURL`.

The theme's own strings live in `i18n/`, and your site can override any
of them by shipping a file with the same name. Nothing forces you to
add the second language today. It just stops being expensive.
