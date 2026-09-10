---
title: "Über Design-Tokens"
date: 2026-05-02
author: "Kevin"
description: "Warum Liftoff Palette und Spacing als CSS-Variablen offenlegt."
tags: ["design", "css"]
---

Liftoff legt seine Palette, sein Spacing und die Typografie als CSS
Custom Properties auf `:root` offen. Konsument:innen können das Theme
anpassen, ohne es zu forken.

## Override-Pattern

Lege eine kleine CSS-Datei in `assets/css/` deiner Seite ab und binde
sie nach dem Theme-Bundle ein.

```css
:root {
  --color-accent: #ff7a59;
  --color-bg: #0d0a0a;
}
```

Der Light-Mode ist Opt-in über `data-theme="light"` am `<html>`-Element.
Der eingebaute Toggle merkt sich die Wahl in `localStorage`, Fallback
ist `prefers-color-scheme`.

## Warum nicht Tailwind

Für ein Theme, das als Hugo-Modul ausgeliefert wird, ist eine
Node-Toolchain Reibung. Reines CSS mit Variablen bringt keine
Abhängigkeiten und bleibt lesbar.
