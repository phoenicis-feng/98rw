---
title: "Hello, Liftoff"
date: 2026-04-15
author: "Kevin"
description: "Why I built a Hugo theme for product-landing pages."
tags: ["release", "design"]
---

I kept rebuilding the same scaffold for every small product page: a
hero with a code block, OS-specific install tabs, a feature grid, a
docs section, and a closing CTA. Liftoff bundles those pieces into one
Hugo theme with sensible dark-first defaults.

## What's in the first cut

- Hero partial driven by front matter
- OS tabs as a CSS-light shortcode
- Code blocks with copy buttons
- Feature, integrations, pricing, testimonial, and CTA shortcodes
- Docs layout with card index, on-this-page TOC, and prev/next navigation
- Blog and showcase sections

## Where it's going

Internationalisation strings ship for German and English. More
languages are a `i18n/<lang>.yaml` file away.

> [!TIP]
> Browse the [blueprints](/blueprints) to see how the pieces compose
> for different shapes of pages.
