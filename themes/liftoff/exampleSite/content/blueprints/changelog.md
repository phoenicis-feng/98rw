---
title: "Public changelog"
description: "A dated section reframed as a release log, with one page per release."
mark: "C1"
filters: ["articles", "oss"]
weight: 40
startFrom: "/docs/configuration"
---

A changelog is the articles layout with different vocabulary: one page
per release, newest first, tagged by change type. Point it at its own
section so your actual writing stays separate.

## Section front matter

Create `content/releases/_index.md`. The articles layout is reused by
matching the section name in your own `layouts/` folder, or by keeping
the content under `content/articles/` if you have no blog.

```yaml
---
title: "Releases"
description: "Every change to Widget, newest first."
hero:
  title: "What changed, and"
  titleAccent: "when it changed."
  subtitle: "Every release since 1.0, with upgrade notes."
  highlights:
    - icon: "mdi:tag-outline"
      label: "Semantic versioning"
    - icon: "mdi:rss"
      label: "RSS feed"
---
```

## One page per release

Name the file after the version. The date drives the ordering, the tags
drive the filtering.

```yaml
---
title: "2.4.0"
date: 2026-07-02
description: "Parallel task execution and a smaller binary."
tags: ["feature", "performance"]
---
```

```markdown
## Added

- Tasks declared in the same group now run in parallel
- `widget run --dry` prints the resolved plan without executing

## Fixed

- Exit code was 0 when a task timed out

## Breaking

- `widget.toml` now rejects unknown keys instead of ignoring them
```

## Conventions worth keeping

| Tag        | Use for                                       |
| ---------- | --------------------------------------------- |
| `feature`  | New capability someone asked for              |
| `fix`      | Behaviour that was wrong and now is not       |
| `security` | Anything with a CVE or an advisory            |
| `breaking` | Requires the reader to change something       |

> [!TIP]
> Give `breaking` its own heading in the body, not just a tag. People
> skim changelogs for exactly one question: will this upgrade cost me
> an afternoon?

Sorting is newest-first by date, which the articles layout already
does. The RSS feed comes for free, and it is the reason to publish a
changelog as pages rather than as a single long markdown file.
