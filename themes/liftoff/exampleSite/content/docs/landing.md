---
title: "Landing pages"
description: "Compose a get-started style page from shortcodes and partials."
category: "Authoring"
weight: 30
---

A landing page combines a hero, content sections built from shortcodes,
and a closing CTA. The hero is driven by front matter; everything else
is markdown.

## Hero from front matter

```yaml
hero:
  title: "From zero to"
  titleAccent: "a running site."
  subtitle: "Pick your platform, drop in the theme, write content."
  highlights:
    - icon: "mdi:code-tags"
      label: "Any language"
    - icon: "mdi:translate"
      label: "Multilingual"
  primary:
    label: "Install"
    url: "#install"
  secondary:
    label: "See blueprints"
    url: "/blueprints"
  code:
    language: bash
    content: |
      hugo server
```

| Field | Purpose |
| --- | --- |
| `title` | Headline, rendered as the page `h1` |
| `titleAccent` | Second half of the headline, in the accent colour |
| `subtitle` | Lead paragraph, parsed as markdown |
| `highlights` | List of `{ icon, label }` pills below the subtitle |
| `primary` / `secondary` | Buttons, each `{ label, url }` |
| `code` | Single code block: `{ language, content }` |
| `code.tabs` | Multiple code blocks, see below |

`url` values are resolved with `relLangURL`, so write them without a
language prefix: `/docs`, not `/en/docs`.

Instead of a single `code` block, the hero can show OS tabs. When
`code.tabs` is present, `code.language` and `code.content` are ignored.

```yaml
hero:
  code:
    tabs:
      - name: "macOS"
        icon: "simple-icons:apple"
        language: bash
        content: |
          brew install yourapp
      - name: "Linux"
        icon: "simple-icons:linux"
        language: bash
        content: |
          apt install yourapp
```

## Shortcodes

> [!TIP]
> All shortcodes work in any page, not just the home page. Mix them
> into docs or articles as needed.

### OS tabs

````markdown
{{</* tabs */>}}
  {{</* tab name="macOS" */>}}
  ```bash
  brew install yourapp
  ```
  {{</* /tab */>}}
  {{</* tab name="Linux" */>}}
  ```bash
  apt install yourapp
  ```
  {{</* /tab */>}}
{{</* /tabs */>}}
````

### Feature grid

```markdown
{{</* feature-grid */>}}
  {{</* feature-card title="Plain YAML" */>}}
  Describe your workflow declaratively.
  {{</* /feature-card */>}}
{{</* /feature-grid */>}}
```

### Integrations

```markdown
{{</* icon-grid data="integrations" */>}}
```

Reads `data/integrations.yaml`. Each entry is `{ name, icon, url }`,
where `icon` is an Iconify identifier. Entries without an `icon` render
an empty tile.

### Pricing

```markdown
{{</* pricing data="editions" */>}}
```

### Testimonial

```markdown
{{</* testimonial author="Jane Doe" role="VP, Acme" */>}}
Quote text.

metrics:
- 80% time saved
- 40+ teams onboarded
{{</* /testimonial */>}}
```

### CTA

```markdown
{{</* cta title="Ready to scale?" primary="Book demo|/demo" secondary="Talk to us|/contact" */>}}
Optional subtitle markdown.
{{</* /cta */>}}
```
