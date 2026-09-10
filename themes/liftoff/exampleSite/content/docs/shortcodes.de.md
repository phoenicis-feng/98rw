---
title: "Shortcodes"
description: "Referenz aller Shortcodes, die das Theme mitbringt."
category: "Inhalte"
weight: 40
---

Liftoff bringt eine kompakte Sammlung von Shortcodes mit, die du frei
kombinieren kannst. Jeder Eintrag listet Parameter, ein Code-Beispiel
und eine Live-Vorschau.

Zwei Dinge kommen ganz ohne Shortcode aus, weil sie über
Markdown-Render-Hooks laufen: Hinweisboxen und Codeblöcke.

## Hinweisboxen {#callouts}

Ein Zitat, das mit einer Alert-Markierung beginnt, wird zur
Hinweisbox. Die Beschriftung läuft über `i18n` und richtet sich damit
nach der Sprache der Seite.

```markdown
> [!NOTE]
> Neutraler Hintergrund.

> [!TIP]
> Eine Abkürzung oder der bessere Weg.

> [!WARNING]
> Etwas, das später Ärger macht.

> [!DANGER]
> Etwas, das den Build sofort zerlegt.
```

`[!CAUTION]` gilt als Alias für `[!DANGER]`. Ein Zitat ohne Markierung
bleibt ein normales Zitat.

> [!TIP]
> So sieht eine Hinweisbox aus. Die vier Typen unterscheiden sich nur
> in Farbe und Beschriftung.

## Codeblöcke {#code-blocks}

Codeblöcke mit Backticks bekommen automatisch ein Sprachlabel und einen
Copy-Button. Dafür braucht es keinen Shortcode.

````markdown
```bash
hugo server --source exampleSite --themesDir ../..
```
````

Ohne Sprachangabe fällt der Block auf `text` zurück. Für die Varianten
`wide` und `featured` nimmst du stattdessen den
[`code`](#code)-Shortcode.

## hero {#hero}

Hero in Sektionsbreite mit optionalem Akzent in der Headline. Beliebige
weitere Blöcke (Code, Buttons, Pills) kommen in den Body und landen in
der Hero-Spalte.

| Param         | Typ      | Beschreibung                                                |
|---------------|----------|-------------------------------------------------------------|
| `title`       | string   | Hauptüberschrift.                                           |
| `titleAccent` | string   | Zweiter Teil der Überschrift im Akzentfarbton.              |
| `subtitle`    | string   | Lead unter der Überschrift. Markdown erlaubt.               |
| _body_        | markdown | Freier Slot: Code-Blöcke, Buttons, Pills, alles.            |

```markdown
{{</* hero title="In fünf Minuten" titleAccent="online." subtitle="Plattform aussuchen, Theme einklinken, Inhalte pflegen." */>}}

{{</* buttons */>}}
  {{</* button href="/docs" variant="primary" size="lg" */>}}Zur Doku{{</* /button */>}}
{{</* /buttons */>}}

{{</* /hero */>}}
```

{{< hero title="In fünf Minuten" titleAccent="online." subtitle="Plattform aussuchen, Theme einklinken, Inhalte pflegen." >}}

{{< buttons >}}
  {{< button href="/docs" variant="primary" size="lg" >}}Zur Doku{{< /button >}}
{{< /buttons >}}

{{< /hero >}}

---

## pills / pill {#pills--pill}

Kompakte Reihe mit Highlight-Tags für Hero- oder Section-Intros. Jeder
`pill` nimmt optional ein Iconify-Icon.

| Param        | Typ    | Beschreibung                              |
|--------------|--------|-------------------------------------------|
| pill `icon`  | string | Iconify-Identifier, z. B. `mdi:code-tags`. |
| pill _body_  | text   | Label.                                    |

```markdown
{{</* pills */>}}
  {{</* pill icon="mdi:code-tags" */>}}Jede Sprache{{</* /pill */>}}
  {{</* pill icon="mdi:translate" */>}}Mehrsprachig{{</* /pill */>}}
  {{</* pill icon="mdi:flash" */>}}Static & schnell{{</* /pill */>}}
{{</* /pills */>}}
```

{{< pills >}}
  {{< pill icon="mdi:code-tags" >}}Jede Sprache{{< /pill >}}
  {{< pill icon="mdi:translate" >}}Mehrsprachig{{< /pill >}}
  {{< pill icon="mdi:flash" >}}Static & schnell{{< /pill >}}
{{< /pills >}}

---

## buttons / button {#buttons--button}

`buttons` legt eine umbrechende Reihe; `button` rendert einen einzelnen
Link im Button-Stil. Interne `href`s laufen durch `relLangURL`; URLs
mit `http(s)://` oder `mailto:` bleiben unverändert.

| Param          | Typ    | Beschreibung                                              |
|----------------|--------|-----------------------------------------------------------|
| `href`         | string | Linkziel.                                                 |
| `target`       | string | HTML-`target`, z. B. `_blank`. Setzt `rel=noopener noreferrer`. |
| `variant`      | enum   | `primary` (default), `secondary`, `ghost`.                |
| `size`         | enum   | `sm`, `md` (default), `lg`.                               |
| `icon`         | string | Iconify-Identifier.                                       |
| `iconPosition` | enum   | `left` (default) oder `right`.                            |
| _body_         | text   | Label.                                                    |

```markdown
{{</* buttons */>}}
  {{</* button href="/docs" variant="primary" size="lg" icon="mdi:rocket-launch" */>}}Loslegen{{</* /button */>}}
  {{</* button href="/docs" variant="ghost" size="lg" icon="mdi:arrow-right" iconPosition="right" */>}}Zur Doku{{</* /button */>}}
{{</* /buttons */>}}
```

{{< buttons >}}
  {{< button href="/docs" variant="primary" size="lg" icon="mdi:rocket-launch" >}}Loslegen{{< /button >}}
  {{< button href="/docs" variant="ghost" size="lg" icon="mdi:arrow-right" iconPosition="right" >}}Zur Doku{{< /button >}}
{{< /buttons >}}

---

## code {#code}

Eigenständiger Code-Block mit derselben Optik wie der Markdown-Render-
Hook: Sprach-Label, Copy-Button und optional ein animierter Verlaufs-
Rahmen für die Hero-Platzierung.

| Param      | Typ    | Beschreibung                                              |
|------------|--------|-----------------------------------------------------------|
| `language` | string | Chroma-Sprach-ID. Default `text`.                         |
| `wide`     | bool   | `true` hebt die Hero-Breitenbegrenzung auf.               |
| `featured` | bool   | `true` zeichnet einen animierten Verlaufs-Rahmen.         |
| _body_     | text   | Roher Code. Keine Backticks nötig.                        |

```markdown
{{</* code language="zsh" featured="true" */>}}
hugo new site mysite && cd mysite
hugo mod init example.com/mysite
hugo mod get codeberg.org/head1328/hugo-liftoff
hugo server
{{</* /code */>}}
```

{{< code language="zsh" featured="true" >}}
hugo new site mysite && cd mysite
hugo mod init example.com/mysite
hugo mod get codeberg.org/head1328/hugo-liftoff
hugo server
{{< /code >}}

---

## tabs / tab {#tabs--tab}

Tab-Panels. `tabs` umschließt einen oder mehrere `tab`-Shortcodes. Der
erste Tab ist per Default aktiv. Inhalte werden als Markdown gerendert,
Code-Fences und verschachtelte Shortcodes funktionieren also.

| Param           | Typ      | Beschreibung                                       |
|-----------------|----------|----------------------------------------------------|
| tabs `wide`     | bool     | `true` hebt die Hero-Breitenbegrenzung auf.        |
| tabs `featured` | bool     | `true` zeichnet einen animierten Verlaufs-Rahmen.  |
| tab `name`      | string   | Label auf dem Tab-Button.                          |
| tab `icon`      | string   | Iconify-Identifier links neben dem Label.          |
| tab _body_      | markdown | Panel-Inhalt. Code-Fences und Shortcodes erlaubt.  |

````markdown
{{</* tabs */>}}
  {{</* tab name="macOS" icon="simple-icons:apple" */>}}
  ```zsh
  brew install hugo
  ```
  {{</* /tab */>}}
  {{</* tab name="Linux" icon="simple-icons:linux" */>}}
  ```bash
  sudo apt install hugo
  ```
  {{</* /tab */>}}
  {{</* tab name="Windows" icon="mdi:microsoft-windows" */>}}
  ```powershell
  winget install Hugo.Hugo.Extended
  ```
  {{</* /tab */>}}
{{</* /tabs */>}}
````

{{< tabs >}}
  {{< tab name="macOS" icon="simple-icons:apple" >}}
  ```zsh
  brew install hugo
  ```
  {{< /tab >}}
  {{< tab name="Linux" icon="simple-icons:linux" >}}
  ```bash
  sudo apt install hugo
  ```
  {{< /tab >}}
  {{< tab name="Windows" icon="mdi:microsoft-windows" >}}
  ```powershell
  winget install Hugo.Hugo.Extended
  ```
  {{< /tab >}}
{{< /tabs >}}

---

## steps / step {#steps--step}

Vertikaler, nummerierter Onboarding-Flow. `steps` ist der Container;
jeder `step` ist eine eigenständige Karte mit Step-N-Titel-Header
und einem Markdown-Body, der verschachtelte Shortcodes akzeptiert.

| Param           | Typ      | Beschreibung                                            |
|-----------------|----------|---------------------------------------------------------|
| step `number`   | string   | Im Header angezeigte Nummer.                            |
| step `title`    | string   | Titel des Schritts.                                     |
| step _body_     | markdown | Inhalt. Code, Tabs, feature-grid: alles möglich.        |

````markdown
{{</* steps */>}}

{{</* step number="1" title="Hugo installieren" */>}}
```zsh
brew install hugo
```
{{</* /step */>}}

{{</* step number="2" title="Theme einklinken" */>}}
Den Modul-Import in der `hugo.toml` ergänzen, dann:

```zsh
hugo mod tidy
hugo server
```
{{</* /step */>}}

{{</* /steps */>}}
````

{{< steps >}}

{{< step number="1" title="Hugo installieren" >}}
```zsh
brew install hugo
```
{{< /step >}}

{{< step number="2" title="Theme einklinken" >}}
Den Modul-Import in der `hugo.toml` ergänzen, dann:

```zsh
hugo mod tidy
hugo server
```
{{< /step >}}

{{< /steps >}}

Die Stärke der Steps zeigt sich in Kombination mit anderen Shortcodes.
Wickelt man die ganze Sequenz in `tabs`, bekommt jedes OS seinen
eigenen, unabhängigen Step-Flow. Anzahl und Inhalt der Schritte
dürfen sich pro Tab unterscheiden.

`````markdown
{{</* tabs */>}}
  {{</* tab name="macOS" icon="simple-icons:apple" */>}}
  {{</* steps */>}}
  {{</* step number="1" title="Hugo installieren" */>}}
  ```zsh
  brew install hugo
  ```
  {{</* /step */>}}
  {{</* step number="2" title="Server starten" */>}}
  ```zsh
  hugo server
  ```
  {{</* /step */>}}
  {{</* step number="3" title="Startpunkt wählen" */>}}
  {{</* feature-grid */>}}
  {{</* feature-card title="Landing" icon="mdi:rocket-launch" */>}}
  Hero, OS-Tabs, Code-Demo, Feature-Grid, Pricing, CTA.
  {{</* /feature-card */>}}
  {{</* feature-card title="Doku" icon="mdi:book-open-page-variant" */>}}
  Layout ohne Sidebar, On-this-page-TOC, Render-Hooks.
  {{</* /feature-card */>}}
  {{</* /feature-grid */>}}
  {{</* /step */>}}
  {{</* /steps */>}}
  {{</* /tab */>}}
  {{</* tab name="Linux" icon="simple-icons:linux" */>}}
  {{</* steps */>}}
  {{</* step number="1" title="Hugo installieren" */>}}
  ```bash
  sudo apt install hugo
  ```
  {{</* /step */>}}
  {{</* /steps */>}}
  {{</* /tab */>}}
{{</* /tabs */>}}
`````

{{< tabs >}}
  {{< tab name="macOS" icon="simple-icons:apple" >}}
  {{< steps >}}
  {{< step number="1" title="Hugo installieren" >}}
  ```zsh
  brew install hugo
  ```
  {{< /step >}}
  {{< step number="2" title="Server starten" >}}
  ```zsh
  hugo server
  ```
  {{< /step >}}
  {{< step number="3" title="Startpunkt wählen" >}}
  {{< feature-grid >}}
  {{< feature-card title="Landing" icon="mdi:rocket-launch" >}}
  Hero, OS-Tabs, Code-Demo, Feature-Grid, Pricing, CTA.
  {{< /feature-card >}}
  {{< feature-card title="Doku" icon="mdi:book-open-page-variant" >}}
  Layout ohne Sidebar, On-this-page-TOC, Render-Hooks.
  {{< /feature-card >}}
  {{< /feature-grid >}}
  {{< /step >}}
  {{< /steps >}}
  {{< /tab >}}
  {{< tab name="Linux" icon="simple-icons:linux" >}}
  {{< steps >}}
  {{< step number="1" title="Hugo installieren" >}}
  ```bash
  sudo apt install hugo
  ```
  {{< /step >}}
  {{< /steps >}}
  {{< /tab >}}
{{< /tabs >}}

---

## section {#section}

Einfacher Container mit Standard-Inhaltsbreite. Praktisch, um auf
shortcode-getriebenen Seiten Sektionen zu gruppieren und Prosa zentriert
zu halten.

| Param   | Typ      | Beschreibung                                       |
|---------|----------|----------------------------------------------------|
| `width` | enum     | `wide` (default) oder `narrow`.                    |
| _body_  | markdown | Inhalt. Überschriften, Prosa, Shortcodes.          |

```markdown
{{</* section */>}}

## Läuft überall

{{</* icon-grid data="integrations" */>}}

{{</* /section */>}}
```

---

## feature-grid / feature-card {#feature-grid--feature-card}

Responsives Grid aus Feature-Cards. `feature-grid` umschließt beliebig
viele verschachtelte `feature-card`-Shortcodes.

| Param          | Typ      | Beschreibung                                  |
|----------------|----------|-----------------------------------------------|
| card `title`   | string   | Karten-Überschrift.                           |
| card `icon`    | string   | Iconify-Identifier.                           |
| card `url`     | string   | Macht die ganze Karte anklickbar.             |
| card _body_    | markdown | Karten-Body.                                  |

```markdown
{{</* feature-grid */>}}
  {{</* feature-card title="Landing" icon="mdi:rocket-launch" url="/get-started" */>}}
  Hero, OS-Tabs, Code-Demo, Feature-Grid, Integrationen, Pricing, CTA.
  {{</* /feature-card */>}}
  {{</* feature-card title="Doku" icon="mdi:book-open-page-variant" url="/docs" */>}}
  Layout ohne Sidebar, On-this-page-TOC, Render-Hooks, Vor/Zurück.
  {{</* /feature-card */>}}
  {{</* feature-card title="Artikel" icon="mdi:newspaper-variant-outline" url="/articles" */>}}
  Listenkarten und Artikelseite mit angenehmer Leseweite.
  {{</* /feature-card */>}}
{{</* /feature-grid */>}}
```

{{< feature-grid >}}
  {{< feature-card title="Landing" icon="mdi:rocket-launch" url="/get-started" >}}
  Hero, OS-Tabs, Code-Demo, Feature-Grid, Integrationen, Pricing, CTA.
  {{< /feature-card >}}
  {{< feature-card title="Doku" icon="mdi:book-open-page-variant" url="/docs" >}}
  Layout ohne Sidebar, On-this-page-TOC, Render-Hooks, Vor/Zurück.
  {{< /feature-card >}}
  {{< feature-card title="Artikel" icon="mdi:newspaper-variant-outline" url="/articles" >}}
  Listenkarten und Artikelseite mit angenehmer Leseweite.
  {{< /feature-card >}}
{{< /feature-grid >}}

---

## icon-grid {#icon-grid}

Kachel-Grid aus einer Daten-Datei. Praktisch für Integrations-Logos und
Deployment-Ziele. Einträge mit Iconify-`icon` rendern als Inline-SVG;
ohne `icon` bleibt die Kachel leer.

| Param  | Typ      | Beschreibung                                      |
|--------|----------|---------------------------------------------------|
| `data` | string   | Name einer YAML-/TOML-Datei unter `data/`.        |

```yaml
# data/integrations.yaml
- name: Docker
  icon: simple-icons:docker
  url: "#"
- name: Kubernetes
  icon: simple-icons:kubernetes
  url: "#"
```

```markdown
{{</* icon-grid data="integrations" */>}}
```

{{< icon-grid data="integrations" >}}

---

## pricing {#pricing}

Vergleich gestaffelter Angebote aus einer Daten-Datei. Rendert eine
Karte pro Eintrag; der Eintrag mit `featured: true` bekommt Akzent-
Rahmen und Banner.

| Param  | Typ    | Beschreibung                                          |
|--------|--------|-------------------------------------------------------|
| `data` | string | Name einer YAML-/TOML-Datei unter `data/`.            |

```yaml
# data/consulting.yaml
- name: Entwicklung
  tagline: Das fehlende Stück bauen.
  price: ab 800 EUR/Tag
  features: ["Neue Features", "Migrationen", "Code-Review"]
  cta:
    label: Anfrage stellen
    url: "#"
- name: Beratung
  featured: true
  tag: Häufig gebucht
  price: 150 EUR/h
  features: ["Architektur-Audits", "Workshops"]
  cta: { label: Termin buchen, url: "#", primary: true }
```

```markdown
{{</* pricing data="consulting-de" */>}}
```

{{< pricing data="consulting-de" >}}

---

## testimonial {#testimonial}

Zitat-Block mit optionalem Autor, Rolle und Metriken. Die Metriken
werden aus einer `metrics:`-Liste am Ende des Bodys geparst.

| Param      | Typ      | Beschreibung                                       |
|------------|----------|----------------------------------------------------|
| `author`   | string   | Autor:innen-Name.                                  |
| `role`     | string   | Rolle.                                             |
| _body_     | markdown | Zitat, optional gefolgt von `metrics:`-Liste.      |

```markdown
{{</* testimonial author="Jane Doe" role="Platform Lead, Acme" */>}}
Doku und Landingpage haben wir an einem Wochenende neu aufgesetzt.
Die Voreinstellungen passen, und wo man Hand anlegen muss, sieht man
sofort.

metrics:
- 80 % Zeit gespart
- 6 Seiten live
{{</* /testimonial */>}}
```

{{< testimonial author="Jane Doe" role="Platform Lead, Acme" >}}
Doku und Landingpage haben wir an einem Wochenende neu aufgesetzt.
Die Voreinstellungen passen, und wo man Hand anlegen muss, sieht man
sofort.

metrics:
- 80 % Zeit gespart
- 6 Seiten live
{{< /testimonial >}}

---

## cta {#cta}

Auffälliger Call-to-Action-Block mit optionalem Titel, optionalem
Untertitel (dem Shortcode-Body) und bis zu zwei Aktions-Buttons.

| Param       | Typ          | Beschreibung                                       |
|-------------|--------------|----------------------------------------------------|
| `title`     | string       | Überschrift als H2.                                |
| `primary`   | `label\|url` | Primärer Button, pipe-separiert.                   |
| `secondary` | `label\|url` | Sekundärer Button, pipe-separiert.                 |
| _body_      | markdown     | Untertitel unter der Überschrift.                  |

```markdown
{{</* cta title="Bereit, zu skalieren?" primary="Loslegen|/get-started" secondary="Zur Doku|/docs" */>}}
Wähle ein Blueprint und passe es an. Fünf Minuten vom Klonen zum Deploy.
{{</* /cta */>}}
```

{{< cta title="Bereit, zu skalieren?" primary="Loslegen|/get-started" secondary="Zur Doku|/docs" >}}
Wähle ein Blueprint und passe es an. Fünf Minuten vom Klonen zum Deploy.
{{< /cta >}}
