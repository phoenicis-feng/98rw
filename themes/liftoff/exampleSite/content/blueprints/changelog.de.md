---
title: "Öffentliches Changelog"
description: "Ein datierter Bereich als Release-Log, mit einer Seite pro Release."
mark: "C1"
filters: ["articles", "oss"]
weight: 40
startFrom: "/docs/configuration"
---

Ein Changelog ist das Artikel-Layout mit anderem Vokabular: eine Seite
pro Release, neueste zuerst, verschlagwortet nach Art der Änderung. Gib
ihm einen eigenen Bereich, damit deine Texte davon getrennt bleiben.

## Front Matter des Bereichs

Lege `content/releases/_index.md` an. Das Artikel-Layout lässt sich
über einen gleichnamigen Ordner in deinem `layouts/` wiederverwenden.
Wer keinen Blog hat, lässt die Inhalte einfach unter
`content/articles/`.

```yaml
---
title: "Releases"
description: "Jede Änderung an Widget, neueste zuerst."
hero:
  title: "Was sich geändert hat,"
  titleAccent: "und wann."
  subtitle: "Alle Releases seit 1.0, mit Hinweisen zum Umstieg."
  highlights:
    - icon: "mdi:tag-outline"
      label: "Semantic Versioning"
    - icon: "mdi:rss"
      label: "RSS-Feed"
---
```

## Eine Seite pro Release

Benenne die Datei nach der Version. Das Datum steuert die Reihenfolge,
die Tags steuern die Filterung.

```yaml
---
title: "2.4.0"
date: 2026-07-02
description: "Tasks laufen parallel, die Binary ist kleiner."
tags: ["feature", "performance"]
---
```

```markdown
## Neu

- Tasks derselben Gruppe laufen jetzt parallel
- `widget run --dry` zeigt den aufgelösten Plan, ohne ihn auszuführen

## Behoben

- Der Exit-Code war 0, wenn ein Task ins Timeout lief

## Breaking Changes

- `widget.toml` weist unbekannte Schlüssel ab, statt sie zu ignorieren
```

## Konventionen, die sich lohnen

| Tag        | Wofür                                            |
| ---------- | ------------------------------------------------ |
| `feature`  | Neue Funktion, nach der gefragt wurde            |
| `fix`      | Verhalten, das falsch war und es jetzt nicht ist |
| `security` | Alles mit CVE oder Advisory                      |
| `breaking` | Erfordert eine Änderung auf der Gegenseite       |

> [!TIP]
> Gib Breaking Changes eine eigene Überschrift im Text, nicht nur einen
> Tag. Changelogs werden nach genau einer Frage überflogen: Kostet
> mich dieses Update einen Nachmittag?

Sortiert wird nach Datum absteigend, das macht das Artikel-Layout schon
von selbst. Der RSS-Feed fällt nebenbei ab, und genau deshalb lohnt es
sich, ein Changelog als Seiten zu führen statt als eine lange
Markdown-Datei.
