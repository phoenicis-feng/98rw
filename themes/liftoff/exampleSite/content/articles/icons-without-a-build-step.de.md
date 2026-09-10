---
title: "Icons ohne Build-Schritt"
date: 2026-06-12
author: "Kevin"
description: "Warum Liftoff Icons beim Build von Iconify lädt, statt einen Font oder ein Sprite-Sheet auszuliefern."
tags: ["icons", "performance"]
categories: ["Design-Notizen"]
---

Icon-Fonts liefern jede Glyphe an jeden Besucher aus. Sprite-Sheets
brauchen einen Build-Schritt und eine Namenskonvention, die sich
niemand merkt. Liftoff geht einen dritten Weg: Jedes Icon wird während
des Hugo-Builds von der Iconify-API geladen und als SVG eingebettet.

```go-html-template
{{ partial "icon.html" "simple-icons:codeberg" }}
```

Jedes Set auf Iconify funktioniert, adressiert als `set:name`. Ein
Name ohne Präfix landet bei den Material Design Icons, `check` und
`mdi:check` sind also dasselbe Icon.

Der Haken ist überschaubar: Beim ersten Kontakt mit einem Icon braucht
der Build Netzzugriff. Danach antwortet Hugos Dateicache, wiederholte
Builds und CI-Läufe mit warmem Cache bleiben offline. Wer vollständig
abgeschottete Builds braucht, legt SVGs in `assets/icons/` und
referenziert sie als `local:name`.

Am Ende trägt eine Seite genau die Glyphen, die sie nutzt, direkt im
HTML, ohne zusätzlichen Request und ohne kurz aufblitzende Leerstellen.
