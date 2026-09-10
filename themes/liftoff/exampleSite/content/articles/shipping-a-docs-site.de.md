---
title: "Eine Doku-Seite an einem Nachmittag"
date: 2026-06-28
author: "Kevin"
description: "Einmal komplett durch: Modul einbinden, Inhalte strukturieren, Navigation aufsetzen. Und die zwei Entscheidungen, die später am meisten Zeit kosten."
tags: ["doku", "tutorial"]
categories: ["Anleitungen"]
---

Die meisten Doku-Seiten scheitern an der Struktur, nicht am Text. Der
erste Nachmittag geht für den Generator drauf, der zweite für die
Navigation, und nach dem dritten stehen vier Seiten und die Lust ist
weg. Diese Anleitung springt direkt zu dem Teil, in dem du schreibst.

## Als Modul einbinden, nicht forken

Binde Liftoff als Hugo-Modul ein, statt es nach `themes/` zu kopieren.
So bleiben Updates möglich, und dein Repository bleibt überschaubar.

```toml
# hugo.toml
[module]
  [[module.imports]]
    path = "codeberg.org/head1328/hugo-liftoff"
```

```bash
hugo mod get codeberg.org/head1328/hugo-liftoff
hugo mod tidy
```

Ein Fork lohnt sich genau in einem Fall: wenn du das Markup ändern
willst, nicht die Optik. Alles Visuelle liegt in CSS Custom Properties,
und die überschreibst du aus deiner eigenen Seite heraus, ohne das
Theme anzufassen.

## Inhalte nach Fragen gliedern, nicht nach Features

Verbreitet ist eine Doku, die die Architektur der Software abbildet. Das
ist bequem für die Person, die sie geschrieben hat, und nutzlos für
alle anderen. Benenne Seiten danach, was jemand vorhat.

```text
content/
  docs/
    _index.md
    installation.md
    configuration.md
    customization.md
```

Jede Seite bekommt ein `weight`, und das steuert sowohl die Reihenfolge
im Index als auch die Vor/Zurück-Links am Seitenende. Eine Sortierung
nach Titel sieht ordentlich aus und liest sich wie ein Aktenschrank.

```yaml
---
title: "Konfiguration"
description: "Site-Params, Menüs und Sprachen."
weight: 20
---
```

> [!TIP]
> Lass Lücken zwischen den Gewichten: 10, 20, 30. Eine Seite später
> dazwischenzuschieben ist dann eine Zeile Änderung statt einer
> Neunummerierung.

## Navigation ist ein Menü, keine Sidebar

Liftoff zeigt den Doku-Index als Kartenraster und gibt jeder Seite ein
Inhaltsverzeichnis. Eine dauerhafte Sidebar gibt es bewusst nicht:
Sidebars verleiten zu vierzig Seiten, wo acht gereicht hätten.

```toml
[[menus.main]]
  name = "Doku"
  pageRef = "/docs"
  weight = 10
```

Nimm `pageRef` statt `url`. Der Verweis läuft über Hugos Seiten-Lookup,
ein Tippfehler wird damit zum Build-Fehler statt zu einem 404, den
deine Leser:innen vor dir finden.

## Die zwei teuersten Entscheidungen

**Sprachen erst klären, wenn Inhalte da sind.** Eine zweite Sprache
nachzurüsten heißt: jede Datei anfassen, jeden Menüeintrag, jede
Data-Datei. Wenn eine zweite Sprache auch nur denkbar ist, richte die
Struktur am ersten Tag ein, zunächst mit einer einzigen Sprache. Es
kostet einen Config-Block.

**Beispielbefehle in den Fließtext schreiben.** Jeder Befehl, den
jemand ausführen könnte, gehört in einen Codeblock mit Copy-Button,
nicht mitten in einen Satz. Gelesen wird nach grauen Kästen. Text
dazwischen ist Kontext, Text, der einen Befehl versteckt, wird zur
Rückfrage.

## Ausliefern

Jeder Static-Host funktioniert, das Ergebnis ist schließlich ein
Verzeichnis voller Dateien.

```bash
hugo --minify
```

Host auf `public/` zeigen lassen, fertig. Keine Laufzeitumgebung, keine
Datenbank, nichts, was du nachts um zwei patchen musst.

> [!NOTE]
> Setze `baseURL` vor dem ersten Deploy auf die endgültige Adresse.
> Relative Links lösen dagegen auf. Ein falscher Wert ergibt eine
> Seite, die lokal läuft und in Produktion bricht.

## Womit anfangen

Nicht mit der Einleitung. Schreib zuerst die Installationsseite, danach
die Seite zu der Frage, die dir am häufigsten gestellt wird.
Einleitungen schreiben sich leicht, sobald klar ist, was sie einleiten,
und das ist meistens erst der Fall, wenn der Rest steht.
