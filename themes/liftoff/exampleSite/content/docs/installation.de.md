---
title: "Installation"
description: "Liftoff als Modul oder Submodule in eine Hugo-Seite einbinden."
category: "Setup"
weight: 10
---

Liftoff lässt sich auf zwei Wegen einbinden. Nimm den, der zu deinem
restlichen Dependency-Management passt.

## Als Hugo Modul

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
> Hugo Modules brauchen lokal eine Go-Installation. Der Modul-Proxy
> kümmert sich beim ersten Build um das Vendoring.

## Als Git-Submodule

```bash
git submodule add https://codeberg.org/head1328/hugo-liftoff.git themes/liftoff
echo 'theme = "liftoff"' >> hugo.toml
```

> [!WARNING]
> Submodules brauchen ein manuelles `git submodule update --remote`,
> um Updates upstream zu übernehmen. Hugo Modules nutzen semver und
> lösen automatisch auf.

## Mindestversion

Liftoff zielt auf Hugo `0.146.0` oder neuer. Das Theme nutzt den
vereinfachten Layout-Lookup aus dieser Version.
