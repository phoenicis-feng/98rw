---
title: "Icons"
description: "Use any of the 200,000+ Iconify icons or ship your own SVGs."
category: "Authoring"
weight: 27
---

Liftoff has a single icon partial that resolves three things: the
Iconify catalog, the Material Design Icons set as a shortcut, and
local SVGs you ship with your site. Anywhere a shortcode or partial
takes an `icon` parameter, the value goes through this resolver.

## Iconify icons

Iconify exposes 200,000+ icons from 150+ sets under a uniform naming
scheme: `set:name`. Liftoff fetches the SVG once at build time and
caches it.

```markdown
{{</* pill icon="mdi:flash" */>}}Fast{{</* /pill */>}}
{{</* feature-card title="Docs" icon="mdi:book-open-page-variant" */>}}...{{</* /feature-card */>}}
{{</* button href="/docs" icon="simple-icons:codeberg" */>}}Source{{</* /button */>}}
```

Browse and search the catalog: [icon-sets.iconify.design](https://icon-sets.iconify.design/).
Click an icon to see its identifier; copy the `set:name` portion.

Common sets used by the example site:

| Set                 | Catalog                                                    |
|---------------------|------------------------------------------------------------|
| `mdi`               | Material Design Icons. Large, uniform stroke weight.        |
| `simple-icons`      | Brand logos (Codeberg, Mastodon, GitHub, Docker, ...).     |
| `lucide`            | Clean line icons, Feather-style.                            |
| `tabler`            | Tabler icon set, similar feel to Lucide.                    |
| `heroicons`         | Tailwind's icon set.                                        |

Bare names without a prefix resolve to `mdi:`. So `icon="rocket"` is
the same as `icon="mdi:rocket"`. Use the prefix when you want a
different set.

## Local SVGs

Two cases need a local SVG instead of Iconify: a custom logo or a
glyph that does not exist in any Iconify set.

1. Drop the SVG at `assets/icons/<name>.svg` in your project.
2. Reference it as `local:<name>`.

```markdown
{{</* feature-card title="Custom" icon="local:my-logo" */>}}
This card uses assets/icons/my-logo.svg as the icon.
{{</* /feature-card */>}}
```

The file must be a single `<svg>` element. Inline styles and `<defs>`
work; external references do not. Strip width/height attributes so
CSS can size it via `currentColor` and font-size.

A small starting point you can copy into `assets/icons/`:

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 2 2 22h20L12 2z"/>
</svg>
```

## Where icons render

Shortcodes that accept an `icon` parameter:

- `button` (`icon`, `iconPosition`)
- `feature-card`
- `pill`
- `tab`

Plus any partial or layout you write yourself can call the resolver
directly:

```go-html-template
{{ partial "icon.html" "mdi:rocket-launch" }}
{{ partial "icon.html" "local:my-logo" }}
```

The output is raw inline SVG, so colors and sizes follow CSS.

## Caching and offline builds

Iconify SVGs are fetched once via `resources.GetRemote` and stored in
Hugo's resource cache (`resources/_gen/`). Subsequent builds use the
cache; commit `resources/_gen/` if you want fully reproducible builds
without network access at build time.

If an Iconify identifier cannot be resolved, Hugo emits a warning at
build time but the page still renders without the missing icon.
