---
title: "Open source project page"
description: "Install, features, docs, contribute. No pricing, no testimonial."
mark: "O1"
filters: ["landing", "oss"]
weight: 20
startFrom: "/docs/shortcodes"
---

An open source project page has one job: get someone from "what is
this" to a working install before they lose interest. Cut everything
that does not serve that.

## Front matter

Put the install command in the hero. It is the single most-copied
string on the page.

```yaml
---
title: "Widget"
description: "A single-binary task runner for small teams."
hero:
  title: "Task running without"
  titleAccent: "the YAML sprawl."
  subtitle: "One binary, no runtime, MIT licensed."
  highlights:
    - icon: "mdi:package-variant-closed"
      label: "Single binary"
    - icon: "mdi:scale-balance"
      label: "MIT"
  primary:
    label: "Get started"
    url: "/docs/installation"
  secondary:
    label: "Source"
    url: "https://codeberg.org/you/widget"
  code:
    tabs:
      - name: "macOS"
        icon: "simple-icons:apple"
        language: bash
        content: |
          brew install widget
      - name: "Linux"
        icon: "simple-icons:linux"
        language: bash
        content: |
          curl -sSf https://widget.dev/install.sh | sh
---
```

## Body

```markdown
{{</* section */>}}
## What it does

{{</* feature-grid */>}}
  {{</* feature-card title="No daemon" icon="mdi:power-plug-off-outline" */>}}
  Runs and exits. Nothing left behind on your machine.
  {{</* /feature-card */>}}
  {{</* feature-card title="Readable config" icon="mdi:file-document-outline" */>}}
  Twenty lines of TOML, not two hundred of YAML.
  {{</* /feature-card */>}}
  {{</* feature-card title="Docs" icon="mdi:book-open-page-variant" url="/docs" */>}}
  Every flag documented, with examples.
  {{</* /feature-card */>}}
{{</* /feature-grid */>}}
{{</* /section */>}}

{{</* section width="narrow" */>}}
## Try it

{{</* steps */>}}
  {{</* step number="1" title="Install" */>}}
  Pick your platform above.
  {{</* /step */>}}
  {{</* step number="2" title="Initialise" */>}}
  Run `widget init` in your project root.
  {{</* /step */>}}
  {{</* step number="3" title="Run" */>}}
  Run `widget run build` and watch it exit cleanly.
  {{</* /step */>}}
{{</* /steps */>}}
{{</* /section */>}}

{{</* cta title="Found a rough edge?" primary="Good first issues|https://codeberg.org/you/widget/issues" secondary="Contributing guide|/docs/contributing" */>}}
Bug reports are contributions too.
{{</* /cta */>}}
```

> [!NOTE]
> Skip the pricing and testimonial shortcodes here. A pricing table on
> an MIT-licensed project reads as a bait and switch, even when the
> paid tier is only hosting.

## What to change

| Piece            | Replace with                                    |
| ---------------- | ----------------------------------------------- |
| `hero.code.tabs` | The platforms you actually publish builds for   |
| `secondary.url`  | Your repository, not a docs page                |
| CTA links        | Your issue label and contributing guide         |
