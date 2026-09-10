---
title: "Open-Source-Projektseite"
description: "Installieren, Features, Doku, Mitmachen. Kein Pricing, kein Testimonial."
mark: "O1"
filters: ["landing", "oss"]
weight: 20
startFrom: "/docs/shortcodes"
---

Eine Open-Source-Projektseite hat eine Aufgabe: von "was ist das?" zur
laufenden Installation, bevor das Interesse kippt. Alles, was dem nicht
dient, fliegt raus.

## Front Matter

Der Installationsbefehl gehört in den Hero. Er ist der meistkopierte
Text der ganzen Seite.

```yaml
---
title: "Widget"
description: "Ein Task-Runner als einzelne Binary, für kleine Teams."
hero:
  title: "Tasks ausführen ohne"
  titleAccent: "den YAML-Wildwuchs."
  subtitle: "Eine Binary, keine Laufzeitumgebung, MIT-Lizenz."
  highlights:
    - icon: "mdi:package-variant-closed"
      label: "Eine Binary"
    - icon: "mdi:scale-balance"
      label: "MIT"
  primary:
    label: "Loslegen"
    url: "/docs/installation"
  secondary:
    label: "Quellcode"
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
## Was es macht

{{</* feature-grid */>}}
  {{</* feature-card title="Kein Daemon" icon="mdi:power-plug-off-outline" */>}}
  Läuft und beendet sich. Nichts bleibt auf dem Rechner zurück.
  {{</* /feature-card */>}}
  {{</* feature-card title="Lesbare Konfiguration" icon="mdi:file-document-outline" */>}}
  Zwanzig Zeilen TOML statt zweihundert Zeilen YAML.
  {{</* /feature-card */>}}
  {{</* feature-card title="Doku" icon="mdi:book-open-page-variant" url="/docs" */>}}
  Jedes Flag dokumentiert, mit Beispielen.
  {{</* /feature-card */>}}
{{</* /feature-grid */>}}
{{</* /section */>}}

{{</* section width="narrow" */>}}
## Ausprobieren

{{</* steps */>}}
  {{</* step number="1" title="Installieren" */>}}
  Plattform oben auswählen.
  {{</* /step */>}}
  {{</* step number="2" title="Einrichten" */>}}
  `widget init` im Projektverzeichnis ausführen.
  {{</* /step */>}}
  {{</* step number="3" title="Ausführen" */>}}
  `widget run build` starten und sauber beenden lassen.
  {{</* /step */>}}
{{</* /steps */>}}
{{</* /section */>}}

{{</* cta title="Etwas hakt?" primary="Good First Issues|https://codeberg.org/you/widget/issues" secondary="Leitfaden zum Mitmachen|/docs/contributing" */>}}
Auch ein Bugreport ist ein Beitrag.
{{</* /cta */>}}
```

> [!NOTE]
> Pricing- und Testimonial-Shortcodes bleiben hier draußen. Eine
> Preistabelle auf einem MIT-lizenzierten Projekt wirkt wie ein
> Lockangebot, selbst wenn nur das Hosting Geld kostet.

## Was du anpassen musst

| Baustein         | Ersetzen durch                                    |
| ---------------- | ------------------------------------------------- |
| `hero.code.tabs` | Die Plattformen, für die du wirklich baust        |
| `secondary.url`  | Dein Repository, keine Doku-Seite                 |
| CTA-Links        | Dein Issue-Label und dein Leitfaden zum Mitmachen |
