---
title: "Loslegen"
description: "Liftoff installieren und in fünf Minuten die erste Seite ausliefern."
---

{{< hero title="In fünf Minuten" titleAccent="online." subtitle="Plattform aussuchen, Theme einklinken, Inhalte pflegen. Liftoff hält sich im Hintergrund." >}}

{{< code language="zsh" featured="true" >}}
hugo new site mysite && cd mysite
hugo mod init example.com/mysite
hugo mod get codeberg.org/head1328/hugo-liftoff
hugo server
{{< /code >}}

{{< buttons >}}
{{< button href="#start" variant="primary" size="lg" >}}Loslegen{{< /button >}}
{{< button href="/blueprints" variant="ghost" size="lg" >}}Blueprints ansehen{{< /button >}}
{{< /buttons >}}

{{< /hero >}}

{{< section >}}

## In drei Schritten startklar {#start}

{{< tabs >}}

{{< tab name="macOS" icon="simple-icons:apple" >}}
{{< steps >}}

{{< step number="1" title="Hugo installieren" >}}
```zsh
brew install hugo
```
{{< /step >}}

{{< step number="2" title="Theme einklinken" >}}
```toml
# hugo.toml
[module]
  [[module.imports]]
    path = "codeberg.org/head1328/hugo-liftoff"
```
```zsh
hugo mod tidy
hugo server
```
{{< /step >}}

{{< step number="3" title="Startpunkt wählen" >}}
Die Bausteine stehen einzeln. Pick dir raus, was du gerade brauchst.

{{< feature-grid >}}
{{< feature-card title="Landing" icon="mdi:rocket-launch" >}}
Hero, OS-Tabs, Code-Demo, Feature-Grid, Integrationen, Pricing, CTA.
{{< /feature-card >}}
{{< feature-card title="Doku" icon="mdi:book-open-page-variant" >}}
Layout ohne Sidebar, On-this-page-TOC, Render-Hooks, Vor/Zurück.
{{< /feature-card >}}
{{< feature-card title="Artikel" icon="mdi:newspaper-variant-outline" >}}
Listenkarten und Artikelseite mit angenehmer Leseweite.
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

{{< step number="2" title="Theme einklinken" >}}
```toml
# hugo.toml
[module]
  [[module.imports]]
    path = "codeberg.org/head1328/hugo-liftoff"
```
```bash
hugo mod tidy
hugo server
```
{{< /step >}}

{{< step number="3" title="Startpunkt wählen" >}}
Die Bausteine stehen einzeln. Pick dir raus, was du gerade brauchst.

{{< feature-grid >}}
{{< feature-card title="Landing" icon="mdi:rocket-launch" >}}
Hero, OS-Tabs, Code-Demo, Feature-Grid, Integrationen, Pricing, CTA.
{{< /feature-card >}}
{{< feature-card title="Doku" icon="mdi:book-open-page-variant" >}}
Layout ohne Sidebar, On-this-page-TOC, Render-Hooks, Vor/Zurück.
{{< /feature-card >}}
{{< feature-card title="Artikel" icon="mdi:newspaper-variant-outline" >}}
Listenkarten und Artikelseite mit angenehmer Leseweite.
{{< /feature-card >}}
{{< /feature-grid >}}
{{< /step >}}

{{< /steps >}}
{{< /tab >}}

{{< tab name="Windows" icon="mdi:microsoft-windows" >}}
{{< steps >}}

{{< step number="1" title="Hugo installieren" >}}
```powershell
winget install Hugo.Hugo.Extended
```
{{< /step >}}

{{< step number="2" title="Theme einklinken" >}}
```toml
# hugo.toml
[module]
  [[module.imports]]
    path = "codeberg.org/head1328/hugo-liftoff"
```
```powershell
hugo mod tidy
hugo server
```
{{< /step >}}

{{< step number="3" title="Startpunkt wählen" >}}
Die Bausteine stehen einzeln. Pick dir raus, was du gerade brauchst.

{{< feature-grid >}}
{{< feature-card title="Landing" icon="mdi:rocket-launch" >}}
Hero, OS-Tabs, Code-Demo, Feature-Grid, Integrationen, Pricing, CTA.
{{< /feature-card >}}
{{< feature-card title="Doku" icon="mdi:book-open-page-variant" >}}
Layout ohne Sidebar, On-this-page-TOC, Render-Hooks, Vor/Zurück.
{{< /feature-card >}}
{{< feature-card title="Artikel" icon="mdi:newspaper-variant-outline" >}}
Listenkarten und Artikelseite mit angenehmer Leseweite.
{{< /feature-card >}}
{{< /feature-grid >}}
{{< /step >}}

{{< /steps >}}
{{< /tab >}}

{{< /tabs >}}

{{< /section >}}

{{< section >}}

## Läuft überall

{{< icon-grid data="integrations" >}}

## Beratung & Entwicklung

{{< pricing data="consulting-de" >}}

## Stimmen

{{< testimonial author="Jane Doe" role="Platform Lead" >}}
Doku und Landingpage haben wir an einem Wochenende neu aufgesetzt.
Die Voreinstellungen passen, und wo man Hand anlegen muss, sieht man
sofort.

metrics:
- 80 % Zeit gespart
- 6 Seiten live
{{< /testimonial >}}

{{< /section >}}
