---
title: "Konfiguration"
description: "Site-Params, Menüs, Sprachen und Theme-Overrides."
category: "Setup"
weight: 20
---

Liftoff liest konventionelle Hugo-Konfiguration. Wenige Extras schalten
das Landing-Chrome scharf.

## Pflicht-Einstellung für Markup

Die Shortcodes geben HTML aus, Goldmark muss es also durchlassen. Fehlt
das, erscheinen Feature-Cards und Hinweisboxen als escapter Text.

```toml
[markup.goldmark.renderer]
  unsafe = true
```

## Site-Params

```toml
[params]
  description     = "Was deine Seite leistet, in einem Satz."
  tagline         = "Im Footer-Brand-Block sichtbar."
  ogImage         = "/images/og.png"
  accent          = "cyan"
  copyrightOwner  = "ACME"
  copyrightSuffix = "Alle Rechte vorbehalten."
```

| Param             | Wird genutzt für              | Standard     |
| ----------------- | ----------------------------- | ------------ |
| `description`     | Meta-Description, Open Graph  | keiner       |
| `tagline`         | Footer-Brand-Block            | keiner       |
| `ogImage`         | Bild für Open Graph und Twitter Card | keiner |
| `accent`          | Farbschema, siehe unten       | `cyan`       |
| `copyrightOwner`  | Copyright-Zeile im Footer     | `site.Title` |
| `copyrightSuffix` | Text hinter der Copyright-Zeile | keiner     |

### Farbschemata

`accent` tauscht die beiden Markenfarben aus. Flächen, Schrift und die
semantischen Farben bleiben unverändert, und jedes Schema bringt eine
passende Light-Mode-Variante mit. Der Umschalter funktioniert also in
beiden Fällen weiter.

| Wert     | Markenfarben       | Wirkung                            |
| -------- | ------------------ | ---------------------------------- |
| `cyan`   | Cyan und Violett   | Standard. Produkt und Developer-Tools |
| `ember`  | Orange und Pink    | Warm, energisch                    |
| `forest` | Smaragd und Cyan   | Ruhig, nach Infrastruktur          |
| `indigo` | Indigo und Magenta | Klassisches SaaS                   |
| `mono`   | Nur Grautöne       | Fast neutral, Inhalt zuerst        |

Die beiden Farben liegen jeweils weit genug auseinander, damit die
Verläufe in der Hero-Überschrift, im CTA-Band und im Brandmark als
Verlauf erkennbar bleiben. `mono` ist die bewusste Ausnahme: Dort ist
der Abstand minimal, und genau das ist die Absicht.

Der Wert landet auf `<html data-accent="...">`. Für eine eigene Palette
überschreibst du stattdessen direkt die Tokens, siehe
[Anpassung](/docs/customization).

Jeder dieser Werte lässt sich pro Sprache unter
`[languages.<code>.params]` überschreiben.

### Repository-Statistik

Zeigt die Sternezahl im Header. Unterstützt sind ausschließlich
`codeberg` und `github`. Der Wert wird im Browser geladen und eine
Stunde im `localStorage` zwischengespeichert, kostet also keine
Build-Zeit.

```toml
[params.repo]
  host  = "codeberg"
  owner = "head1328"
  name  = "liftoff"
```

### Social-Links

Erscheinen im Footer. `icon` ist ein Iconify-Bezeichner. Interne Pfade
werden sprachbewusst aufgelöst, externe URLs bleiben unverändert.

```toml
[[params.social]]
  icon = "simple-icons:codeberg"
  name = "Codeberg"
  url  = "https://codeberg.org/head1328"
```

### Adresse im Footer

Wird als Markdown geparst, Links und Zeilenumbrüche funktionieren also.

```toml
[params.footer]
  address = """
ACME
Musterstadt
[hello@acme.example](mailto:hello@acme.example)
"""
```

## Seitenweise Ausgabe

Die Artikelliste und die Taxonomie-Seiten nutzen Hugos Paginator.

```toml
[pagination]
  pagerSize = 6
```

## Sprachen

```toml
defaultContentLanguage = "en"
defaultContentLanguageInSubdir = true

[languages.en]
  label  = "English"
  locale = "en"
  weight = 1
[languages.de]
  label  = "Deutsch"
  locale = "de"
  weight = 2
```

## Menüs

```toml
[[menus.main]]
  name    = "Docs"
  pageRef = "/docs"
  weight  = 10
```

Footer-Spalten sind Top-Level-Einträge mit Kindern:

```toml
[[menus.footer]]
  identifier = "product"
  name       = "Produkt"
[[menus.footer]]
  parent = "product"
  name   = "Loslegen"
  url    = "/get-started"
```

Nimm für interne Ziele `pageRef` statt `url`. Der Verweis läuft über
Hugos Seiten-Lookup, ein Fehler lässt damit den Build scheitern, statt
einen 404 auszuliefern. Footer-Einträge mit festem `url` werden nicht
geprüft.

## Front Matter

Felder, die das Theme zusätzlich zu Hugos Standards liest.

| Feld          | Bereich             | Bedeutung                            |
| ------------- | ------------------- | ------------------------------------ |
| `hero`        | Listen und Seiten   | Rendert den Hero, siehe [Landingpages](/docs/landing) |
| `description` | alle                | Kartentext und Meta-Description      |
| `image`       | alle                | Open-Graph-Bild der Seite, überschreibt `params.ogImage` |
| `author`      | Artikel             | Erscheint in der Meta-Zeile          |
| `weight`      | Doku                | Reihenfolge im Index und Vor/Zurück  |
| `tags`        | Artikel, Doku       | Taxonomie-Begriffe, verlinkt         |
| `categories`  | Artikel             | Taxonomie-Begriffe, verlinkt         |
| `mark`        | Blueprints          | Kürzel auf der Karte, sonst die ersten zwei Zeichen des Titels |
| `filters`     | Blueprints          | Filter-Buttons im Index, keine Taxonomie |
| `startFrom`   | Blueprints          | Optionaler Link zur passenden Referenzseite |
