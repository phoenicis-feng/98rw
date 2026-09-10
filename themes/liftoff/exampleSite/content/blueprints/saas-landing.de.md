---
title: "SaaS-Landingpage"
description: "Hero, Features, Pricing, Testimonial, CTA. Die kanonische Form."
mark: "S1"
filters: ["landing", "commercial"]
weight: 10
startFrom: "/docs/shortcodes"
---

Die häufigste Produktseite: überzeugen, belegen, bepreisen,
abschließen. Kopiere Front Matter und Body nach `content/_index.md` und
ersetze die Beispieltexte durch deine eigenen.

## Front Matter

Der Hero wird konfiguriert, nicht geschrieben. Alles darunter ist
Markdown.

```yaml
---
title: "Acme"
description: "Der erste Workflow läuft in fünf Minuten."
hero:
  title: "Automatisiere die langweilige Hälfte"
  titleAccent: "deiner Deployments."
  subtitle: "Eine Konfigurationsdatei. Keine Agents zu installieren."
  highlights:
    - icon: "mdi:lightning-bolt-outline"
      label: "Ohne Ausfall"
    - icon: "mdi:lock-outline"
      label: "SOC 2"
  primary:
    label: "Kostenlos starten"
    url: "/signup"
  secondary:
    label: "Zur Doku"
    url: "/docs"
  code:
    language: yaml
    content: |
      deploy:
        target: production
        strategy: rolling
---
```

## Body

```markdown
{{</* section */>}}
## Alles, was zum Ausliefern fehlt

{{</* feature-grid */>}}
  {{</* feature-card title="Rollbacks" icon="mdi:backup-restore" */>}}
  Ein Befehl zurück zum letzten funktionierenden Release.
  {{</* /feature-card */>}}
  {{</* feature-card title="Audit-Log" icon="mdi:history" */>}}
  Jede Änderung nachvollziehbar, exportierbar als JSON.
  {{</* /feature-card */>}}
  {{</* feature-card title="Secrets" icon="mdi:key-outline" */>}}
  Verschlüsselt gespeichert, zur Laufzeit eingespielt.
  {{</* /feature-card */>}}
{{</* /feature-grid */>}}
{{</* /section */>}}

{{</* section width="narrow" */>}}
## Passt zu deinem Stack

{{</* icon-grid data="integrations" */>}}
{{</* /section */>}}

{{</* section */>}}
## Preise

{{</* pricing data="editions" */>}}
{{</* /section */>}}

{{</* section width="narrow" */>}}
{{</* testimonial author="Jana Dohm" role="VP Engineering, Northwind" */>}}
Drei interne Tools sind dafür rausgeflogen, und seitdem denkt hier
niemand mehr über Deployments nach.

metrics:
- 80% weniger Deploy-Zeit
- 40+ Teams angebunden
{{</* /testimonial */>}}
{{</* /section */>}}

{{</* cta title="Bereit für schnellere Releases?" primary="Kostenlos starten|/signup" secondary="Vertrieb kontaktieren|/contact" */>}}
Ohne Kreditkarte. Jederzeit kündbar.
{{</* /cta */>}}
```

## Was du anpassen musst

| Baustein                 | Ersetzen durch                                |
| ------------------------ | --------------------------------------------- |
| `hero.code.content`      | Deine echte Konfiguration oder dein CLI-Aufruf |
| `feature-card`           | Drei bis sechs Karten, je ein Nutzen           |
| `data/integrations.yaml` | Die Tools, die deine Kundschaft ohnehin nutzt  |
| `data/editions.yaml`     | Zwei bis drei Pläne, einer als `featured`      |

> [!TIP]
> Der CTA wiederholt die Primäraktion aus dem Hero mit Absicht. Wer die
> ganze Seite gelesen hat, soll zum Handeln nicht zurückscrollen müssen.
