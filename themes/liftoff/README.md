# Liftoff

A Hugo theme for product-landing, docs, articles and showcase sites.
Dark UI, code-first hero, designed for get-started style pages.

![Liftoff](https://codeberg.org/head1328/hugo-liftoff/raw/branch/main/images/tn.png)

The visual language borrows from modern developer-product sites: dark
navy surfaces, a cyan accent, geometric sans, monospaced code with copy
buttons, OS tabs and card grids. Liftoff copies no particular one of
them; it ships a generic set of building blocks for the genre.

[Demo site](https://hugo-liftoff.kevinhorst.de)

## Requirements

Hugo extended, 0.146.0 or newer.

## Use

### Via Hugo Modules (recommended)

```toml
# hugo.toml
[module]
  [[module.imports]]
    path = "codeberg.org/head1328/hugo-liftoff"
```

```bash
hugo mod get codeberg.org/head1328/hugo-liftoff
hugo mod tidy
hugo server
```

### As Git submodule

```bash
git submodule add https://codeberg.org/head1328/hugo-liftoff.git themes/liftoff
echo 'theme = "liftoff"' >> hugo.toml
```

## Sections covered

- Product landing (hero with code block, OS tabs, feature cards,
  integrations grid, pricing comparison, CTA)
- Docs (card index, on-this-page TOC, code/note/warning render hooks,
  prev/next navigation)
- Articles (listing with tags, categories, reading time, pagination)
- Blueprints (copyable page recipes in a filterable card grid)

## Shortcodes

Seventeen shortcodes cover the landing-page vocabulary: `hero`,
`section`, `feature-grid`, `feature-card`, `icon-grid`, `pricing`,
`testimonial`, `cta`, `tabs`, `code`, `steps`, `buttons`, `pills` and
their children. Callouts and code-block chrome come from markdown
render hooks and need no shortcode at all.

Full reference with live previews: `/docs/shortcodes` on the demo site.

## Theming

Every colour, space and type step is a CSS custom property on `:root`,
so a site can rebrand the theme without forking it. Five accent presets
ship out of the box:

```toml
[params]
  accent = "cyan"  # cyan, ember, forest, indigo, mono
```

Light mode is included for all of them and is switched at runtime,
defaulting to the visitor's `prefers-color-scheme`.

## Languages

German (`de`) and English (`en`) i18n strings ship with the theme, and
the demo site is authored in both. Internal links, dates and plurals
are language-aware.

## Icons

Icons are fetched from the [Iconify](https://iconify.design/) API at
build time and inlined, addressed as `set:name`. Local SVGs under
`assets/icons/` are available as `local:name`.

## Demo

The `exampleSite/` directory is a full Hugo site that consumes the
theme and doubles as its documentation.

The repository is named `hugo-liftoff`, the theme itself `liftoff`, so
clone into a matching directory. `--themesDir` resolves the theme by
directory name, not by repository name.

```bash
git clone https://codeberg.org/head1328/hugo-liftoff.git liftoff
cd liftoff
hugo server --source exampleSite --themesDir ../..
```

## Authors

This project is maintained by the Liftoff contributors.
See the [AUTHORS](./AUTHORS) file for details.

## License

MIT, see [LICENSE](./LICENSE).
