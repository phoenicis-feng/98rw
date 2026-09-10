---
title: "Docs-only site"
description: "When the project is the documentation. Short home page, deep docs section."
mark: "D1"
filters: ["docs", "oss"]
weight: 30
startFrom: "/docs/configuration"
---

Some projects are the documentation. The home page exists only to get
people into the docs, and everything else in the theme comes off.

## Front matter

A short hero, no code block. The landing page is a signpost, not a
pitch.

```yaml
---
title: "Widget Handbook"
description: "Everything Widget can do, in one place."
hero:
  title: "The complete"
  titleAccent: "Widget handbook."
  subtitle: "Install, configure, extend. Updated with every release."
  primary:
    label: "Start reading"
    url: "/docs/installation"
  secondary:
    label: "Source"
    url: "https://codeberg.org/you/widget"
---
```

## Body

```markdown
{{</* section width="narrow" */>}}
{{</* feature-grid */>}}
  {{</* feature-card title="Install" icon="mdi:download-outline" url="/docs/installation" */>}}
  Package managers, binaries, and building from source.
  {{</* /feature-card */>}}
  {{</* feature-card title="Configure" icon="mdi:cog-outline" url="/docs/configuration" */>}}
  Every option, with defaults and examples.
  {{</* /feature-card */>}}
  {{</* feature-card title="Extend" icon="mdi:puzzle-outline" url="/docs/plugins" */>}}
  Write a plugin in about thirty lines.
  {{</* /feature-card */>}}
{{</* /feature-grid */>}}
{{</* /section */>}}
```

## Removing the other sections

Deleting a content folder is only half the job. The menu entries
survive and turn into dead links, so remove those too.

```bash
rm -r content/articles content/blueprints
```

```toml
# hugo.toml: delete the matching entries
[[menus.main]]
  name = "Articles"      # remove
  pageRef = "/articles"

[[menus.footer]]
  parent = "resources"
  name = "Articles"      # remove
  url = "/articles"
```

> [!WARNING]
> Footer entries use a hard `url`, so Hugo will not warn you when the
> target disappears. Main-menu entries use `pageRef` and do fail the
> build, which is the behaviour you want. Grep your config for both.

## Ordering the docs

The docs index and the prev/next links both read `weight`. Set it on
every page or the order falls back to titles.

```yaml
---
title: "Installation"
weight: 10
---
```
