---
title: "Configuration"
description: "Site params, menus, languages, and theme overrides."
category: "Setup"
weight: 20
---

Liftoff reads conventional Hugo configuration. A few extras enable the
landing-style chrome.

## Required markup setting

The shortcodes emit HTML, so Goldmark must be allowed to pass it
through. Without this, feature cards and callouts render as escaped
text.

```toml
[markup.goldmark.renderer]
  unsafe = true
```

## Site params

```toml
[params]
  description     = "What your site does in one line."
  tagline         = "Used in the footer brand block."
  ogImage         = "/images/og.png"
  accent          = "cyan"
  copyrightOwner  = "ACME"
  copyrightSuffix = "All rights reserved."
```

| Param             | Used by            | Default      |
| ----------------- | ------------------ | ------------ |
| `description`     | Meta description, Open Graph | none |
| `tagline`         | Footer brand block | none         |
| `ogImage`         | Open Graph and Twitter card image | none |
| `accent`          | Colour preset, see below | `cyan` |
| `copyrightOwner`  | Footer copyright line | `site.Title` |
| `copyrightSuffix` | Text after the copyright line | none |

### Colour presets

`accent` swaps the two brand colours. Surfaces, text and the semantic
colours stay the same, and every preset ships a matching light-mode
variant, so the theme toggle keeps working either way.

| Value    | Brand colours     | Reads as                        |
| -------- | ----------------- | ------------------------------- |
| `cyan`   | Cyan and violet   | Default. Product and developer tooling |
| `ember`  | Orange and pink   | Warm, high energy               |
| `forest` | Emerald and cyan  | Calm, infrastructure-flavoured  |
| `indigo` | Indigo and magenta| Conservative SaaS               |
| `mono`   | Slate only        | Near-neutral, content-first     |

The two colours sit far enough apart on the wheel that the gradients
in the hero headline, the CTA band and the brand mark stay legible as
gradients. `mono` is the deliberate exception: it has almost no
contrast between the two, which is the point.

The value lands on `<html data-accent="...">`. For a palette of your
own, override the tokens directly instead, see
[customization](/docs/customization).

Any of these can be overridden per language under
`[languages.<code>.params]`.

### Repository stats

Renders a star count in the header. Only `codeberg` and `github` are
supported as hosts. The count is fetched in the browser and cached in
`localStorage` for an hour, so it costs nothing at build time.

```toml
[params.repo]
  host  = "codeberg"
  owner = "head1328"
  name  = "liftoff"
```

### Social links

Rendered in the footer. `icon` is an Iconify identifier. Internal paths
are resolved per language, external URLs are left alone.

```toml
[[params.social]]
  icon = "simple-icons:codeberg"
  name = "Codeberg"
  url  = "https://codeberg.org/head1328"
```

### Footer address

Parsed as markdown, so links and line breaks work.

```toml
[params.footer]
  address = """
ACME
Anytown, Germany
[hello@acme.example](mailto:hello@acme.example)
"""
```

## Pagination

The articles listing and taxonomy term pages both use Hugo's paginator.

```toml
[pagination]
  pagerSize = 6
```

## Languages

```toml
defaultContentLanguage = "en"
defaultContentLanguageInSubdir = true

[languages.en]
  label  = "English"
  locale = "en"
  weight = 1
[languages.de]
  label  = "Deutsch"
  locale = "de"
  weight = 2
```

## Menus

```toml
[[menus.main]]
  name    = "Docs"
  pageRef = "/docs"
  weight  = 10
```

Footer columns are top-level menu entries with children:

```toml
[[menus.footer]]
  identifier = "product"
  name       = "Product"
[[menus.footer]]
  parent = "product"
  name   = "Get started"
  url    = "/get-started"
```

Prefer `pageRef` over `url` for internal targets. It resolves through
Hugo's page lookup, so a broken reference fails the build instead of
shipping a 404. Footer entries with a hard `url` are not checked.

## Front matter

Fields the theme reads on top of Hugo's built-ins.

| Field         | Sections            | Purpose                              |
| ------------- | ------------------- | ------------------------------------ |
| `hero`        | any list or page    | Renders the hero, see [landing pages](/docs/landing) |
| `description` | all                 | Card summary and meta description    |
| `image`       | all                 | Per-page Open Graph image, overrides `params.ogImage` |
| `author`      | articles            | Shown in the article meta line       |
| `weight`      | docs                | Index order and prev/next links      |
| `tags`        | articles, docs      | Taxonomy terms, linked               |
| `categories`  | articles            | Taxonomy terms, linked               |
| `mark`        | blueprints          | Short label on the card, falls back to the first two title characters |
| `filters`     | blueprints          | Filter buttons on the index, not a taxonomy |
| `startFrom`   | blueprints          | Optional link to the matching reference page |
