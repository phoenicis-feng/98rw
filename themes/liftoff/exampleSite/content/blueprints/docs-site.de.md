---
title: "Reine Doku-Seite"
description: "Wenn das Projekt die Dokumentation ist. Kurze Startseite, tiefe Doku."
mark: "D1"
filters: ["docs", "oss"]
weight: 30
startFrom: "/docs/configuration"
---

Manche Projekte sind ihre Dokumentation. Die Startseite existiert dann
nur, um in die Doku zu führen, alles Übrige aus dem Theme fliegt raus.

## Front Matter

Ein knapper Hero, kein Codeblock. Die Startseite ist ein Wegweiser,
kein Verkaufsgespräch.

```yaml
---
title: "Widget Handbuch"
description: "Alles, was Widget kann, an einer Stelle."
hero:
  title: "Das vollständige"
  titleAccent: "Widget-Handbuch."
  subtitle: "Installieren, konfigurieren, erweitern. Aktuell zu jedem Release."
  primary:
    label: "Loslesen"
    url: "/docs/installation"
  secondary:
    label: "Quellcode"
    url: "https://codeberg.org/you/widget"
---
```

## Body

```markdown
{{</* section width="narrow" */>}}
{{</* feature-grid */>}}
  {{</* feature-card title="Installieren" icon="mdi:download-outline" url="/docs/installation" */>}}
  Paketmanager, Binaries und der Weg über den Quellcode.
  {{</* /feature-card */>}}
  {{</* feature-card title="Konfigurieren" icon="mdi:cog-outline" url="/docs/configuration" */>}}
  Jede Option, mit Standardwert und Beispiel.
  {{</* /feature-card */>}}
  {{</* feature-card title="Erweitern" icon="mdi:puzzle-outline" url="/docs/plugins" */>}}
  Ein Plugin in ungefähr dreißig Zeilen.
  {{</* /feature-card */>}}
{{</* /feature-grid */>}}
{{</* /section */>}}
```

## Die anderen Bereiche entfernen

Einen Inhaltsordner zu löschen ist nur die halbe Miete. Die
Menüeinträge überleben und werden zu toten Links, also müssen sie mit
weg.

```bash
rm -r content/articles content/blueprints
```

```toml
# hugo.toml: die passenden Einträge löschen
[[menus.main]]
  name = "Artikel"       # entfernen
  pageRef = "/articles"

[[menus.footer]]
  parent = "resources"
  name = "Artikel"       # entfernen
  url = "/articles"
```

> [!WARNING]
> Footer-Einträge nutzen ein festes `url`, Hugo warnt also nicht, wenn
> das Ziel verschwindet. Hauptmenü-Einträge mit `pageRef` lassen den
> Build scheitern, und genau das ist erwünscht. Prüfe die Konfiguration
> auf beide Varianten.

## Reihenfolge der Doku

Der Doku-Index und die Vor/Zurück-Links lesen beide `weight`. Ohne
diesen Wert sortiert Hugo nach Titel.

```yaml
---
title: "Installation"
weight: 10
---
```
