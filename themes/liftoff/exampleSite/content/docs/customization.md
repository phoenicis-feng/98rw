---
title: "Customization"
description: "Override theme styles, scripts, partials, layouts and i18n strings without forking."
category: "Authoring"
weight: 25
---

Liftoff is designed to be customized without forking. Hugo's theme
lookup falls through to the site project first, so anything you place
under your project's `assets/`, `layouts/`, `i18n/` or `static/` wins
over the theme. This page lists the seams that exist and how to use
them.

## Custom CSS

Place a stylesheet at `assets/css/custom.css` in your project. The
theme's head includes loads it *after* the main bundle, so any rule
you write here overrides the theme.

```css
/* assets/css/custom.css */
:root {
  --color-accent: #ff5c8a;
}

.hero__title {
  font-family: "Inter", system-ui, sans-serif;
}
```

The file is minified and fingerprinted in production builds. If the
file does not exist, no extra `<link>` is rendered.

## Design tokens

Almost everything visual is a custom property on `:root`, defined in
the theme's `tokens.css`. Overriding tokens is the intended way to
rebrand Liftoff: no forking, no fighting specificity.

| Group        | Count | Examples                                        |
| ------------ | ----- | ----------------------------------------------- |
| `--color-*`  | 35    | `--color-bg`, `--color-accent`, `--color-border` |
| `--space-*`  | 11    | `--space-1` through `--space-9`                 |
| `--text-*`   | 9     | `--text-sm`, `--text-base`, `--text-4xl`        |
| `--shadow-*` | 8     | `--shadow-sm`, `--shadow-lg`                    |
| `--radius-*` | 6     | `--radius-sm`, `--radius-md`, `--radius-pill`   |
| `--font-*`   | 3     | `--font-sans`, `--font-display`, `--font-mono`  |
| `--container-*` | 3  | `--container`, `--container-narrow`             |

The colour tokens that matter most:

```css
:root {
  --color-bg: #0b1020;          /* page background */
  --color-bg-surface: #131a2e;  /* cards, callouts */
  --color-text: #e6edf7;        /* body copy */
  --color-text-muted: #a8b8d0;  /* summaries, captions */
  --color-accent: #22d3ee;      /* links, buttons, marks */
  --color-border: #22304d;      /* hairlines */
}
```

Light mode is the same set, redefined under `[data-theme="light"]`.
Override both if you change the palette:

```css
:root { --color-accent: #ff5c8a; }
[data-theme="light"] { --color-accent: #d81b60; }
```

### Your own accent preset

Five presets ship with the theme and are selected with `params.accent`
(see [configuration](/docs/configuration)). Defining your own follows
the same shape: six tokens per scheme, with the light rule carrying
both attributes so it outranks the dark one.

```css
/* assets/css/custom.css */
[data-accent="sunset"] {
  --color-accent: #fb7185;
  --color-accent-strong: #fda4af;
  --color-accent-soft: rgba(251, 113, 133, 0.12);
  --color-secondary: #fbbf24;
  --color-secondary-soft: rgba(251, 191, 36, 0.14);
  --shadow-glow: 0 0 24px rgba(251, 113, 133, 0.25);
}

[data-theme="light"][data-accent="sunset"] {
  --color-accent: #be123c;
  --color-accent-strong: #9f1239;
  --color-accent-soft: rgba(190, 18, 60, 0.1);
  --color-secondary: #b45309;
  --color-secondary-soft: rgba(180, 83, 9, 0.1);
  --shadow-glow: 0 0 24px rgba(190, 18, 60, 0.2);
}
```

Then set `accent = "sunset"` in your config.

> [!WARNING]
> In dark mode `--color-accent-strong` is the *lighter* variant,
> because it is the link hover colour and has to stay readable on a
> dark surface. In light mode it is the darker one. Getting this
> backwards makes links vanish on hover.

If you only want to recolour everything without a preset, skip
`data-accent` entirely and override the tokens on `:root` as shown
above.

> [!TIP]
> Read the theme's `assets/css/tokens.css` for the full list. Copy the
> lines you want to change into your own `custom.css` rather than
> redefining the whole file, so you keep future additions.

## Custom JS

Place scripts at `assets/js/custom.js` in your project. The bundle is
built with esbuild after the theme's main bundle and loaded with
`defer`. Use it for analytics, chat widgets, or custom DOM behavior.

```js
// assets/js/custom.js
document.addEventListener("DOMContentLoaded", () => {
  console.log("Liftoff site ready");
});
```

ES modules work; `import` statements are resolved against your site's
`assets/` tree.

## Override partials

Every partial under `layouts/_partials/` in the theme can be replaced
by a file with the same path in your project. Common targets:

| Partial                         | What it controls                              |
|---------------------------------|-----------------------------------------------|
| `_partials/header.html`         | Top navigation, branding, social icons.       |
| `_partials/footer.html`         | Footer brand block, columns, bottom bar.      |
| `_partials/head.html`           | `<head>` meta, OG/Twitter, canonical, feeds.  |
| `_partials/social-icons.html`   | Renders icons from `[[params.social]]`.       |
| `_partials/repo-stats.html`     | Codeberg/GitHub star count badge.             |
| `_partials/icon.html`           | The icon resolver (Iconify + `local:`).       |

Copy the theme file into your project at the same path as a starting
point, then edit. Do not include the file in production unless you
actually want the override.

## Override layouts

Same rule for full layouts. The theme ships:

- `home.html` for the homepage
- `page.html` for regular pages
- `section.html` for section index pages
- `articles/list.html` and `articles/single.html`
- `docs/list.html` and `docs/single.html`
- `blueprints/list.html` and `blueprints/single.html`
- `taxonomy.html` and `term.html`

Place a file at the same path in your project's `layouts/` to take
over rendering for that template.

## Override i18n strings

The theme bundles English and German labels in `i18n/en.yaml` and
`i18n/de.yaml`. To change a label, create the same file in your
project's `i18n/` and override just the keys you care about. Hugo
merges site and theme i18n; site wins on conflicts.

```yaml
# i18n/en.yaml in your project
on_this_page: Contents
back_to_top: Top
```

## Configure the theme

Almost everything visible is driven by `hugo.toml`:

- `params.tagline`, `params.description`, `params.copyrightOwner`,
  `params.copyrightSuffix`
- `params.footer.address`
- `params.repo` for the star badge
- `[[params.social]]` for icon links
- `[menus.main]` and `[menus.footer]` for navigation
- `[languages.<code>]` for per-language overrides of any of the
  above

See `exampleSite/hugo.toml` for the full set.

## Where to put assets

| Project path                | Theme path                  | Lookup order      |
|-----------------------------|-----------------------------|-------------------|
| `assets/css/custom.css`     | (none)                      | site only         |
| `assets/js/custom.js`       | (none)                      | site only         |
| `assets/icons/<name>.svg`   | `assets/icons/<name>.svg`   | site first        |
| `layouts/_partials/...`     | `layouts/_partials/...`     | site first        |
| `layouts/<template>.html`   | `layouts/<template>.html`   | site first        |
| `i18n/<lang>.yaml`          | `i18n/<lang>.yaml`          | merged, site wins |
| `data/<name>.yaml`          | (theme can ship samples)    | site first        |
| `static/favicon.*`          | (none)                      | see below         |

### Favicons

The head links each of these only when the file exists, so you can
ship as few or as many as you like. `assets/` is checked first, then
`static/`.

| File                   | Purpose                                   |
| ---------------------- | ----------------------------------------- |
| `favicon.svg`          | Scalable, preferred by modern browsers    |
| `favicon.ico`          | Legacy fallback, ideally 16/32/48         |
| `apple-touch-icon.png` | 180x180, needs an opaque background       |
| `site.webmanifest`     | References `icon-192.png`, `icon-512.png` |

Hugo cannot rasterise SVG, so the PNG sizes have to be generated
outside the build. With ImageMagick and `rsvg-convert` installed:

```bash
magick -background none -density 1536 favicon.svg -resize 512x512 icon-512.png
magick -background none -density 576  favicon.svg -resize 192x192 icon-192.png
magick -background none -density 540  favicon.svg -resize 180x180 apple-touch-icon.png
```

Rendering each size natively from the SVG, rather than downscaling one
large PNG, keeps small sizes crisp. The density is `96 * target / 32`
for a 32-unit viewBox.
