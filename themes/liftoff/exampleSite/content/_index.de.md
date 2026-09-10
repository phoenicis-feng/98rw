---
title: "Liftoff"
description: "Ein Hugo-Theme für Produkt-Landingpages, Docs, Artikel und Showcase."
---

{{< hero title="Produktseiten zum Abheben." titleAccent="Im Nu." subtitle="Landingpage, Doku, Artikel und Showcase: reduziert, ausdrucksstark, sofort startklar als Hugo-Theme. Einklinken, Inhalte pflegen, ausrollen." >}}

{{< pills >}}
{{< pill icon="mdi:code-tags" >}}Jede Sprache{{< /pill >}}
{{< pill icon="mdi:book-open-page-variant" >}}Doku inklusive{{< /pill >}}
{{< pill icon="mdi:web" >}}Mehrsprachig{{< /pill >}}
{{< pill icon="mdi:package-variant-closed" >}}Hugo-Modul{{< /pill >}}
{{< /pills >}}

{{< tabs featured="true" >}}
{{< tab name="macOS" icon="simple-icons:apple" >}}
```zsh
brew install hugo
hugo new site mysite && cd mysite
hugo mod init example.com/mysite
hugo mod get codeberg.org/head1328/hugo-liftoff
hugo server
```
{{< /tab >}}
{{< tab name="Linux" icon="simple-icons:linux" >}}
```bash
sudo apt install hugo
hugo new site mysite && cd mysite
hugo mod init example.com/mysite
hugo mod get codeberg.org/head1328/hugo-liftoff
hugo server
```
{{< /tab >}}
{{< tab name="Windows" icon="mdi:microsoft-windows" >}}
```powershell
winget install Hugo.Hugo.Extended
hugo new site mysite; cd mysite
hugo mod init example.com/mysite
hugo mod get codeberg.org/head1328/hugo-liftoff
hugo server
```
{{< /tab >}}
{{< /tabs >}}

{{< buttons >}}
{{< button href="/docs" variant="primary" size="lg" icon="mdi:arrow-right" iconPosition="right" >}}Doku lesen{{< /button >}}
{{< button href="/blueprints" variant="ghost" size="lg" >}}Blueprints ansehen{{< /button >}}
{{< /buttons >}}

{{< /hero >}}

{{< section >}}
{{< feature-grid >}}
{{< feature-card title="Dokumentation" icon="mdi:book-open-page-variant" url="/docs" >}}
Doku-Layout ohne Sidebar, mit Breadcrumb, Inhaltsverzeichnis pro
Seite, Render-Hooks für Code und Hinweise, Vor/Zurück.
{{< /feature-card >}}
{{< feature-card title="Shortcodes" icon="mdi:code-tags" url="/docs/shortcodes" >}}
Eine handvoll Shortcodes zum Zusammenstecken: Hero, Tabs, Pills,
Buttons, Feature-Grids, Pricing, Testimonials, CTA.
{{< /feature-card >}}
{{< feature-card title="Open Source" icon="simple-icons:codeberg" url="https://codeberg.org/head1328/hugo-liftoff" >}}
MIT-lizenziert, gehostet auf Codeberg. Stern dalassen, forken,
Issues aufmachen, Patches schicken.
{{< /feature-card >}}
{{< feature-card title="Mehrsprachig" icon="mdi:web" url="/docs/configuration" >}}
Deutsch und Englisch sind ab Werk dabei. Weitere Sprachen über eine
YAML-Datei in `i18n/`.
{{< /feature-card >}}
{{< feature-card title="Fira Code" icon="mdi:format-letter-case" url="/docs/configuration" >}}
Programmierfont mit Ligaturen ist eingebaut. Code-Blöcke lesen sich
wie im Editor, nicht wie ein generischer Monospace-Fallback.
{{< /feature-card >}}
{{< feature-card title="Icons" icon="mdi:emoticon-outline" url="https://icon-sets.iconify.design/" >}}
Jedes Icon aus Iconify funktioniert inline: Simple Icons, Material
Design, Heroicons, Tabler und mehr. Wird beim Build geladen und
direkt ins HTML eingebettet.
{{< /feature-card >}}
{{< /feature-grid >}}
{{< /section >}}
