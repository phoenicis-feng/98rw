---
title: "Liftoff"
description: "A Hugo theme for product-landing, docs, articles and showcase sites."
---

{{< hero title="Get product sites off the ground." titleAccent="Fast." subtitle="Liftoff bundles a landing page, docs, articles and showcase set into one minimal, expressive Hugo theme. Drop it in, write content, ship." >}}

{{< pills >}}
{{< pill icon="mdi:code-tags" >}}Any language{{< /pill >}}
{{< pill icon="mdi:book-open-page-variant" >}}Docs included{{< /pill >}}
{{< pill icon="mdi:web" >}}Multilingual{{< /pill >}}
{{< pill icon="mdi:package-variant-closed" >}}Hugo module{{< /pill >}}
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
{{< button href="/docs" variant="primary" size="lg" icon="mdi:arrow-right" iconPosition="right" >}}Read the docs{{< /button >}}
{{< button href="/blueprints" variant="ghost" size="lg" >}}Browse blueprints{{< /button >}}
{{< /buttons >}}

{{< /hero >}}

{{< section >}}
{{< feature-grid >}}
{{< feature-card title="Documentation" icon="mdi:book-open-page-variant" url="/docs" >}}
Sidebar-free docs layout with breadcrumb, on-this-page TOC, render
hooks for code and callouts, prev/next pagination.
{{< /feature-card >}}
{{< feature-card title="Shortcodes" icon="mdi:code-tags" url="/docs/shortcodes" >}}
A small set of composable shortcodes for hero, tabs, pills,
buttons, feature grids, pricing, testimonials and CTAs.
{{< /feature-card >}}
{{< feature-card title="Open source" icon="simple-icons:codeberg" url="https://codeberg.org/head1328/hugo-liftoff" >}}
MIT-licensed. Hosted on Codeberg. Star, fork, file issues, send
patches.
{{< /feature-card >}}
{{< feature-card title="Multilingual" icon="mdi:web" url="/docs/configuration" >}}
German and English i18n strings shipped. Add more languages by
dropping a YAML file into `i18n/`.
{{< /feature-card >}}
{{< feature-card title="Fira Code" icon="mdi:format-letter-case" url="/docs/configuration" >}}
Bundled programming font with ligatures. Code blocks read like the
editor you write them in, not like a generic monospaced fallback.
{{< /feature-card >}}
{{< feature-card title="Icons" icon="mdi:emoticon-outline" url="https://icon-sets.iconify.design/" >}}
Any icon from Iconify works inline. Simple Icons, Material Design,
Heroicons, Tabler and more, fetched and inlined at build time.
{{< /feature-card >}}
{{< /feature-grid >}}
{{< /section >}}
