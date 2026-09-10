---
title: "Dark Mode, der das System respektiert"
date: 2026-05-08
author: "Kevin"
description: "Liftoff startet im bevorzugten Farbschema und merkt sich eine Wahl erst, wenn sie getroffen wurde."
tags: ["design", "css"]
categories: ["Design-Notizen"]
---

Ein Umschalter, der für alle erst mal dunkel startet, ist eine
Geschmacksfrage im Gewand eines Features. Liftoff liest zuerst
`prefers-color-scheme` und schreibt erst dann nach `localStorage`, wenn
jemand tatsächlich ein Schema wählt.

```js
const stored = localStorage.getItem("liftoff.theme");
const system = matchMedia("(prefers-color-scheme: light)").matches;
```

Diese Reihenfolge ist der Punkt. Wer sein System hell eingestellt hat,
bekommt eine helle Seite, ohne dass kurz Dunkel aufblitzt. Wer danach
bewusst auf Dunkel wechselt, behält Dunkel, auch wenn sich das System
später ändert: Eine ausdrückliche Wahl schlägt eine abgeleitete.

Beide Schemata liegen als Tokens vor. Dunkel ist der Standard auf
`:root`, Hell überschreibt es unter `[data-theme="light"]`, und jede
Komponente liest Variablen statt fester Farbwerte.

```css
[data-theme="light"] {
  --color-bg: #ffffff;
  --color-text: #0b1020;
}
```

Ein drittes Schema ist damit ein Block Variablen und kein Durchgang
durch sämtliche Stylesheets.
