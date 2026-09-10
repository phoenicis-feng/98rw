---
title: "Installation"
description: "Add Liftoff to a Hugo site as a module or submodule."
category: "Setup"
weight: 10
---

Liftoff can be consumed in two ways. Pick the one that matches how the
rest of your dependencies live.

## As a Hugo module

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

> [!NOTE]
> Hugo modules require Go to be installed locally. The module proxy
> handles vendoring on first build.

## As a git submodule

```bash
git submodule add https://codeberg.org/head1328/hugo-liftoff.git themes/liftoff
echo 'theme = "liftoff"' >> hugo.toml
```

> [!WARNING]
> Submodules need a manual `git submodule update --remote` to pick up
> upstream changes. Hugo modules use semver and resolve automatically.

## Minimum Hugo version

Liftoff targets Hugo `0.146.0` and newer. The theme leans on the
simplified layout lookup introduced in that release.
