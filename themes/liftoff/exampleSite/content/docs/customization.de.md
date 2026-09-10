---
title: "Anpassen"
description: "Styles, Skripte, Partials, Layouts und i18n-Strings überschreiben, ohne das Theme zu forken."
category: "Inhalte"
weight: 25
---

Liftoff ist so gebaut, dass du es ohne Fork anpassen kannst. Hugo
schaut zuerst im Site-Projekt nach Templates und Assets, danach erst
im Theme. Was du also unter `assets/`, `layouts/`, `i18n/` oder
`static/` ablegst, gewinnt. Die folgenden Nahtstellen stehen bereit.

## Eigenes CSS

Lege eine Stylesheet-Datei unter `assets/css/custom.css` im Projekt
ab. Das Theme lädt sie *nach* dem Haupt-Bundle, jede Regel hier
überschreibt also Theme-Styles.

```css
/* assets/css/custom.css */
:root {
  --color-accent: #ff5c8a;
}

.hero__title {
  font-family: "Inter", system-ui, sans-serif;
}
```

In Produktion wird die Datei minifiziert und mit Fingerprint versehen.
Existiert die Datei nicht, wird kein zusätzlicher `<link>` gerendert.

## Design-Tokens

Fast alles Visuelle ist eine Custom Property auf `:root`, definiert in
der `tokens.css` des Themes. Tokens zu überschreiben ist der vorgesehene
Weg zum eigenen Erscheinungsbild: kein Fork, kein Kampf mit
Spezifität.

| Gruppe          | Anzahl | Beispiele                                       |
| --------------- | ------ | ----------------------------------------------- |
| `--color-*`     | 35     | `--color-bg`, `--color-accent`, `--color-border` |
| `--space-*`     | 11     | `--space-1` bis `--space-9`                     |
| `--text-*`      | 9      | `--text-sm`, `--text-base`, `--text-4xl`        |
| `--shadow-*`    | 8      | `--shadow-sm`, `--shadow-lg`                    |
| `--radius-*`    | 6      | `--radius-sm`, `--radius-md`, `--radius-pill`   |
| `--font-*`      | 3      | `--font-sans`, `--font-display`, `--font-mono`  |
| `--container-*` | 3      | `--container`, `--container-narrow`             |

Die wichtigsten Farb-Tokens:

```css
:root {
  --color-bg: #0b1020;          /* Seitenhintergrund */
  --color-bg-surface: #131a2e;  /* Karten, Hinweisboxen */
  --color-text: #e6edf7;        /* Fließtext */
  --color-text-muted: #a8b8d0;  /* Kurztexte, Bildunterschriften */
  --color-accent: #22d3ee;      /* Links, Buttons, Hervorhebungen */
  --color-border: #22304d;      /* Trennlinien */
}
```

Der Light-Mode ist derselbe Satz, neu definiert unter
`[data-theme="light"]`. Wer die Palette ändert, passt beides an:

```css
:root { --color-accent: #ff5c8a; }
[data-theme="light"] { --color-accent: #d81b60; }
```

### Eigenes Farbschema

Das Theme bringt fünf Schemata mit, ausgewählt über `params.accent`
(siehe [Konfiguration](/docs/configuration)). Ein eigenes folgt
derselben Form: sechs Tokens pro Modus, wobei die Light-Regel beide
Attribute trägt und damit die Dark-Regel schlägt.

```css
/* assets/css/custom.css */
[data-accent="sunset"] {
  --color-accent: #fb7185;
  --color-accent-strong: #fda4af;
  --color-accent-soft: rgba(251, 113, 133, 0.12);
  --color-secondary: #fbbf24;
  --color-secondary-soft: rgba(251, 191, 36, 0.14);
  --shadow-glow: 0 0 24px rgba(251, 113, 133, 0.25);
}

[data-theme="light"][data-accent="sunset"] {
  --color-accent: #be123c;
  --color-accent-strong: #9f1239;
  --color-accent-soft: rgba(190, 18, 60, 0.1);
  --color-secondary: #b45309;
  --color-secondary-soft: rgba(180, 83, 9, 0.1);
  --shadow-glow: 0 0 24px rgba(190, 18, 60, 0.2);
}
```

Danach `accent = "sunset"` in der Konfiguration setzen.

> [!WARNING]
> Im Dark Mode ist `--color-accent-strong` die *hellere* Variante, denn
> es ist die Hover-Farbe für Links und muss auf dunklem Grund lesbar
> bleiben. Im Light Mode ist es die dunklere. Wer das vertauscht, lässt
> Links beim Hovern verschwinden.

Wer einfach alles umfärben will, ohne ein Schema anzulegen, lässt
`data-accent` weg und überschreibt die Tokens direkt auf `:root`.

> [!TIP]
> Die vollständige Liste steht in `assets/css/tokens.css` des Themes.
> Kopiere nur die Zeilen in deine `custom.css`, die du ändern willst,
> statt die ganze Datei neu zu definieren. So bekommst du spätere
> Ergänzungen weiterhin mit.

## Eigenes JS

Lege Skripte unter `assets/js/custom.js` ab. Das Bundle wird per
esbuild nach dem Theme-Bundle gebaut und mit `defer` eingebunden.
Nutze es für Analytics, Chat-Widgets oder eigenes DOM-Verhalten.

```js
// assets/js/custom.js
document.addEventListener("DOMContentLoaded", () => {
  console.log("Liftoff-Site bereit");
});
```

ES-Module funktionieren; `import`-Statements werden gegen den
`assets/`-Baum deines Projekts aufgelöst.

## Partials überschreiben

Jedes Partial unter `layouts/_partials/` im Theme lässt sich durch
eine Datei mit demselben Pfad im Projekt ersetzen. Häufige
Kandidaten:

| Partial                         | Was es steuert                                |
|---------------------------------|-----------------------------------------------|
| `_partials/header.html`         | Top-Navigation, Branding, Social-Icons.       |
| `_partials/footer.html`         | Footer-Brand, Spalten, Bottom-Bar.            |
| `_partials/head.html`           | `<head>`-Meta, OG/Twitter, Canonical, Feeds.  |
| `_partials/social-icons.html`   | Rendert Icons aus `[[params.social]]`.        |
| `_partials/repo-stats.html`     | Codeberg-/GitHub-Star-Badge.                  |
| `_partials/icon.html`           | Der Icon-Resolver (Iconify + `local:`).       |

Kopiere die Theme-Datei als Startpunkt unter denselben Pfad in dein
Projekt und passe sie an. Lass die Datei nur dort liegen, wenn du
tatsächlich überschreiben willst.

## Layouts überschreiben

Dieselbe Regel für komplette Layouts. Das Theme bringt mit:

- `home.html` für die Startseite
- `page.html` für reguläre Seiten
- `section.html` für Sektions-Index-Seiten
- `articles/list.html` und `articles/single.html`
- `docs/list.html` und `docs/single.html`
- `blueprints/list.html` und `blueprints/single.html`
- `taxonomy.html` und `term.html`

Eine Datei unter demselben Pfad in `layouts/` deines Projekts
übernimmt das Rendering für dieses Template.

## i18n-Strings überschreiben

Das Theme bringt englische und deutsche Labels in `i18n/en.yaml` und
`i18n/de.yaml` mit. Um ein Label zu ändern, leg dieselbe Datei in
`i18n/` deines Projekts an und überschreib nur die Keys, die du
willst. Hugo merged Site- und Theme-i18n; Site gewinnt bei
Konflikten.

```yaml
# i18n/en.yaml im Projekt
on_this_page: Contents
back_to_top: Top
```

## Theme konfigurieren

Fast alles Sichtbare lässt sich über `hugo.toml` steuern:

- `params.tagline`, `params.description`, `params.copyrightOwner`,
  `params.copyrightSuffix`
- `params.footer.address`
- `params.repo` für den Star-Badge
- `[[params.social]]` für Social-Icon-Links
- `[menus.main]` und `[menus.footer]` für Navigation
- `[languages.<code>]` für sprachspezifische Overrides

Vollständiges Beispiel: `exampleSite/hugo.toml`.

## Wohin mit welchem Asset

| Projekt-Pfad                | Theme-Pfad                  | Lookup            |
|-----------------------------|-----------------------------|-------------------|
| `assets/css/custom.css`     | (keine)                     | nur Site          |
| `assets/js/custom.js`       | (keine)                     | nur Site          |
| `assets/icons/<name>.svg`   | `assets/icons/<name>.svg`   | Site zuerst       |
| `layouts/_partials/...`     | `layouts/_partials/...`     | Site zuerst       |
| `layouts/<template>.html`   | `layouts/<template>.html`   | Site zuerst       |
| `i18n/<lang>.yaml`          | `i18n/<lang>.yaml`          | merged, Site gewinnt |
| `data/<name>.yaml`          | (Theme kann Samples liefern) | Site zuerst      |
| `static/favicon.*`          | (keine)                     | siehe unten       |

### Favicons

Der Head verlinkt jede dieser Dateien nur, wenn sie existiert. Du
kannst also so wenige oder so viele mitliefern, wie du willst. Zuerst
wird in `assets/` gesucht, danach in `static/`.

| Datei                  | Zweck                                       |
| ---------------------- | ------------------------------------------- |
| `favicon.svg`          | Skalierbar, von aktuellen Browsern bevorzugt |
| `favicon.ico`          | Fallback für Altbrowser, idealerweise 16/32/48 |
| `apple-touch-icon.png` | 180x180, braucht einen deckenden Hintergrund |
| `site.webmanifest`     | Verweist auf `icon-192.png` und `icon-512.png` |

Hugo kann SVG nicht rastern, die PNG-Größen müssen also außerhalb des
Builds entstehen. Mit ImageMagick und installiertem `rsvg-convert`:

```bash
magick -background none -density 1536 favicon.svg -resize 512x512 icon-512.png
magick -background none -density 576  favicon.svg -resize 192x192 icon-192.png
magick -background none -density 540  favicon.svg -resize 180x180 apple-touch-icon.png
```

Jede Größe direkt aus dem SVG zu rendern, statt ein großes PNG
herunterzuskalieren, hält die kleinen Varianten scharf. Die Density
ergibt sich als `96 * Zielgröße / 32` bei einer viewBox von 32.
