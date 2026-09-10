---
title: "Icons"
description: "Die 200.000+ Iconify-Icons nutzen oder eigene SVGs mitliefern."
category: "Inhalte"
weight: 27
---

Liftoff hat ein einziges Icon-Partial, das drei Quellen auflöst: den
Iconify-Katalog, das Material-Design-Icons-Set als Shortcut und
lokale SVGs aus deinem Projekt. Überall dort, wo ein Shortcode oder
Partial einen `icon`-Parameter nimmt, läuft der Wert durch diesen
Resolver.

## Iconify-Icons

Iconify stellt 200.000+ Icons aus 150+ Sets unter einem einheitlichen
Schema bereit: `set:name`. Liftoff holt das SVG einmalig zur Build-
Zeit und cached es.

```markdown
{{</* pill icon="mdi:flash" */>}}Schnell{{</* /pill */>}}
{{</* feature-card title="Doku" icon="mdi:book-open-page-variant" */>}}...{{</* /feature-card */>}}
{{</* button href="/docs" icon="simple-icons:codeberg" */>}}Source{{</* /button */>}}
```

Katalog durchsuchen: [icon-sets.iconify.design](https://icon-sets.iconify.design/).
Auf ein Icon klicken zeigt den Identifier; den `set:name`-Teil
kopieren.

Häufig genutzte Sets:

| Set                 | Katalog                                                   |
|---------------------|-----------------------------------------------------------|
| `mdi`               | Material Design Icons. Große, gleichmäßige Strichstärke.   |
| `simple-icons`      | Brand-Logos (Codeberg, Mastodon, GitHub, Docker, ...).    |
| `lucide`            | Klare Line-Icons im Feather-Stil.                          |
| `tabler`            | Tabler-Set, ähnlich zu Lucide.                             |
| `heroicons`         | Tailwinds Icon-Set.                                        |

Namen ohne Präfix landen automatisch in `mdi:`. `icon="rocket"` ist
also dasselbe wie `icon="mdi:rocket"`. Den Präfix nur dort setzen, wo
du ein anderes Set willst.

## Lokale SVGs

Zwei Fälle brauchen ein lokales SVG: ein eigenes Logo oder ein Glyph,
den es in keinem Iconify-Set gibt.

1. SVG unter `assets/icons/<name>.svg` im Projekt ablegen.
2. Als `local:<name>` referenzieren.

```markdown
{{</* feature-card title="Eigenes" icon="local:my-logo" */>}}
Diese Karte nutzt assets/icons/my-logo.svg als Icon.
{{</* /feature-card */>}}
```

Die Datei muss ein einzelnes `<svg>`-Element sein. Inline-Styles und
`<defs>` funktionieren; externe Referenzen nicht. `width`/`height`
weglassen, damit CSS die Größe über `currentColor` und `font-size`
steuern kann.

Ein kompakter Startpunkt zum Kopieren nach `assets/icons/`:

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 2 2 22h20L12 2z"/>
</svg>
```

## Wo Icons gerendert werden

Shortcodes mit `icon`-Parameter:

- `button` (`icon`, `iconPosition`)
- `feature-card`
- `pill`
- `tab`

Eigene Partials und Layouts können den Resolver direkt aufrufen:

```go-html-template
{{ partial "icon.html" "mdi:rocket-launch" }}
{{ partial "icon.html" "local:my-logo" }}
```

Die Ausgabe ist Inline-SVG, Farben und Größen folgen CSS.

## Caching und Offline-Builds

Iconify-SVGs werden einmal per `resources.GetRemote` geholt und in
Hugos Resource-Cache (`resources/_gen/`) abgelegt. Spätere Builds
nutzen den Cache; commit `resources/_gen/`, wenn der Build voll
reproduzierbar ohne Netzwerk laufen soll.

Findet Hugo einen Iconify-Identifier nicht, gibt es eine Warnung zur
Build-Zeit, die Seite rendert aber trotzdem ohne das fehlende Icon.
