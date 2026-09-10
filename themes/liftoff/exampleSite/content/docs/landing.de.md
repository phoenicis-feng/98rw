---
title: "Landingpages"
description: "Eine Get-Started-Seite aus Shortcodes und Partials zusammensetzen."
category: "Inhalte"
weight: 30
---

Eine Landingpage kombiniert einen Hero, Inhalts-Sektionen aus
Shortcodes und einen abschließenden CTA. Der Hero wird im Front Matter
gesteuert, alles andere ist Markdown.

## Hero aus dem Front Matter

```yaml
hero:
  title: "Von Null zur"
  titleAccent: "fertigen Seite."
  subtitle: "Plattform wählen, Theme einbinden, Inhalte schreiben."
  highlights:
    - icon: "mdi:code-tags"
      label: "Jede Sprache"
    - icon: "mdi:translate"
      label: "Mehrsprachig"
  primary:
    label: "Installieren"
    url: "#install"
  secondary:
    label: "Blueprints ansehen"
    url: "/blueprints"
  code:
    language: bash
    content: |
      hugo server
```

| Feld | Bedeutung |
| --- | --- |
| `title` | Überschrift, wird als `h1` der Seite ausgegeben |
| `titleAccent` | Zweiter Teil der Überschrift, in der Akzentfarbe |
| `subtitle` | Einleitungsabsatz, wird als Markdown geparst |
| `highlights` | Liste aus `{ icon, label }`, erscheint als Pills |
| `primary` / `secondary` | Buttons, jeweils `{ label, url }` |
| `code` | Einzelner Codeblock: `{ language, content }` |
| `code.tabs` | Mehrere Codeblöcke, siehe unten |

`url`-Werte laufen durch `relLangURL`. Sie gehören also ohne
Sprachpräfix notiert: `/docs`, nicht `/de/docs`.

Statt eines einzelnen `code`-Blocks kann der Hero OS-Tabs zeigen. Ist
`code.tabs` gesetzt, werden `code.language` und `code.content`
ignoriert.

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
> Alle Shortcodes funktionieren auf jeder Seite, nicht nur auf der
> Startseite. Mische sie nach Bedarf in Doku oder Blog.

### OS-Tabs

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

### Feature-Grid

```markdown
{{</* feature-grid */>}}
  {{</* feature-card title="Klares YAML" */>}}
  Beschreibe deinen Workflow deklarativ.
  {{</* /feature-card */>}}
{{</* /feature-grid */>}}
```

### Integrationen

```markdown
{{</* icon-grid data="integrations" */>}}
```

Liest `data/integrations.yaml`. Jeder Eintrag besteht aus
`{ name, icon, url }`, wobei `icon` ein Iconify-Bezeichner ist. Ohne
`icon` bleibt die Kachel leer.

### Pricing

```markdown
{{</* pricing data="editions" */>}}
```

### Testimonial

```markdown
{{</* testimonial author="Jane Doe" role="VP, Acme" */>}}
Zitat-Text.

metrics:
- 80% Zeit gespart
- 40+ Teams onboarded
{{</* /testimonial */>}}
```

### CTA

```markdown
{{</* cta title="Bereit, zu skalieren?" primary="Demo buchen|/demo" secondary="Mit uns sprechen|/contact" */>}}
Optionaler Untertitel als Markdown.
{{</* /cta */>}}
```
