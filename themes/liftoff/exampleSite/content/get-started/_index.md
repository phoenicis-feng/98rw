---
title: "Get started"
description: "Install Liftoff and ship your first page in five minutes."
---

{{< hero title="From zero to a" titleAccent="running site." subtitle="Pick your platform, drop in the theme, write content. Liftoff stays out of your way." >}}

{{< code language="zsh" featured="true" >}}
hugo new site mysite && cd mysite
hugo mod init example.com/mysite
hugo mod get codeberg.org/head1328/hugo-liftoff
hugo server
{{< /code >}}

{{< buttons >}}
{{< button href="#start" variant="primary" size="lg" >}}Start{{< /button >}}
{{< button href="/blueprints" variant="ghost" size="lg" >}}See blueprints{{< /button >}}
{{< /buttons >}}

{{< /hero >}}

{{< section >}}

## Up and running in 3 steps {#start}

{{< tabs >}}

{{< tab name="macOS" icon="simple-icons:apple" >}}
{{< steps >}}

{{< step number="1" title="Install Hugo" >}}
```zsh
brew install hugo
```
{{< /step >}}

{{< step number="2" title="Wire the theme" >}}
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

{{< step number="3" title="Pick a starting point" >}}
The pieces are independent. Use what you need.

{{< feature-grid >}}
{{< feature-card title="Landing" icon="mdi:rocket-launch" >}}
Hero, OS tabs, code demo, feature grid, integrations, pricing, CTA.
{{< /feature-card >}}
{{< feature-card title="Docs" icon="mdi:book-open-page-variant" >}}
Sidebar-free layout, on-this-page TOC, render hooks, prev/next.
{{< /feature-card >}}
{{< feature-card title="Articles" icon="mdi:newspaper-variant-outline" >}}
Listing cards and article view with a comfortable reading width.
{{< /feature-card >}}
{{< /feature-grid >}}
{{< /step >}}

{{< /steps >}}
{{< /tab >}}

{{< tab name="Linux" icon="simple-icons:linux" >}}
{{< steps >}}

{{< step number="1" title="Install Hugo" >}}
```bash
sudo apt install hugo
```
{{< /step >}}

{{< step number="2" title="Wire the theme" >}}
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

{{< step number="3" title="Pick a starting point" >}}
The pieces are independent. Use what you need.

{{< feature-grid >}}
{{< feature-card title="Landing" icon="mdi:rocket-launch" >}}
Hero, OS tabs, code demo, feature grid, integrations, pricing, CTA.
{{< /feature-card >}}
{{< feature-card title="Docs" icon="mdi:book-open-page-variant" >}}
Sidebar-free layout, on-this-page TOC, render hooks, prev/next.
{{< /feature-card >}}
{{< feature-card title="Articles" icon="mdi:newspaper-variant-outline" >}}
Listing cards and article view with a comfortable reading width.
{{< /feature-card >}}
{{< /feature-grid >}}
{{< /step >}}

{{< /steps >}}
{{< /tab >}}

{{< tab name="Windows" icon="mdi:microsoft-windows" >}}
{{< steps >}}

{{< step number="1" title="Install Hugo" >}}
```powershell
winget install Hugo.Hugo.Extended
```
{{< /step >}}

{{< step number="2" title="Wire the theme" >}}
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

{{< step number="3" title="Pick a starting point" >}}
The pieces are independent. Use what you need.

{{< feature-grid >}}
{{< feature-card title="Landing" icon="mdi:rocket-launch" >}}
Hero, OS tabs, code demo, feature grid, integrations, pricing, CTA.
{{< /feature-card >}}
{{< feature-card title="Docs" icon="mdi:book-open-page-variant" >}}
Sidebar-free layout, on-this-page TOC, render hooks, prev/next.
{{< /feature-card >}}
{{< feature-card title="Articles" icon="mdi:newspaper-variant-outline" >}}
Listing cards and article view with a comfortable reading width.
{{< /feature-card >}}
{{< /feature-grid >}}
{{< /step >}}

{{< /steps >}}
{{< /tab >}}

{{< /tabs >}}

{{< /section >}}

{{< section >}}

## Run on any platform

{{< icon-grid data="integrations" >}}

## Consulting

{{< pricing data="consulting" >}}

## What people say

{{< testimonial author="Jane Doe" role="Platform Lead" >}}
We rebuilt our docs and landing in a weekend. The defaults are sensible,
the override points are obvious.

metrics:
- 80% time saved
- 6 sites shipped
{{< /testimonial >}}

{{< /section >}}
