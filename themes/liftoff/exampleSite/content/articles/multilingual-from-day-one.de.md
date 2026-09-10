---
title: "Zweisprachig ab dem ersten Tag"
date: 2026-05-24
author: "Kevin"
description: "Eine zweite Sprache kostet jetzt einen Config-Block und später ein Wochenende."
tags: ["i18n", "doku"]
categories: ["Anleitungen"]
---

Eine zweite Sprache nachzurüsten sieht nach einem Nachmittag aus und
wird ein Wochenende. Jede Inhaltsdatei braucht ein Gegenstück, jeder
Menüeintrag eine Übersetzung, jede Data-Datei eine Variante, und jedes
fest verdrahtete Datumsformat entpuppt sich als englisch.

Vorab konfiguriert kostet es fast nichts, selbst wenn es bei einer
Sprache bleibt.

```toml
defaultContentLanguage = "de"
defaultContentLanguageInSubdir = true

[languages]
  [languages.de]
    label = "Deutsch"
    weight = 1
```

Die Sprache steckt danach im Dateinamen: `about.md` und `about.en.md`
liegen nebeneinander, Hugo verknüpft sie von selbst.

> [!WARNING]
> Achte in eigenen Templates auf `relURL`. Die Funktion ignoriert das
> Sprachpräfix. Ein Link, der in der Hauptsprache stimmt, zeigt in
> jeder anderen still auf die falsche Seite. Nimm `relLangURL`.

Die Strings des Themes liegen in `i18n/`, und deine Seite überschreibt
jeden davon mit einer gleichnamigen Datei. Niemand zwingt dich, die
zweite Sprache heute anzulegen. Sie hört nur auf, teuer zu sein.
