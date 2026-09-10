---
title: "SaaS landing page"
description: "Hero, features, pricing, testimonial, CTA. The canonical shape."
mark: "S1"
filters: ["landing", "commercial"]
weight: 10
startFrom: "/docs/shortcodes"
---

The most common product page: convince, prove, price, close. Copy the
front matter and the body below into `content/_index.md`, then replace
the copy with your own.

## Front matter

The hero is configured, not written. Everything below it is markdown.

```yaml
---
title: "Acme"
description: "Ship your first workflow in five minutes."
hero:
  title: "Automate the boring half of"
  titleAccent: "your deployments."
  subtitle: "One config file. No agents to install."
  highlights:
    - icon: "mdi:lightning-bolt-outline"
      label: "Zero downtime"
    - icon: "mdi:lock-outline"
      label: "SOC 2"
  primary:
    label: "Start free"
    url: "/signup"
  secondary:
    label: "Read the docs"
    url: "/docs"
  code:
    language: yaml
    content: |
      deploy:
        target: production
        strategy: rolling
---
```

## Body

```markdown
{{</* section */>}}
## Everything you need to ship

{{</* feature-grid */>}}
  {{</* feature-card title="Rollbacks" icon="mdi:backup-restore" */>}}
  One command back to the last known good release.
  {{</* /feature-card */>}}
  {{</* feature-card title="Audit log" icon="mdi:history" */>}}
  Every change attributed, exportable as JSON.
  {{</* /feature-card */>}}
  {{</* feature-card title="Secrets" icon="mdi:key-outline" */>}}
  Encrypted at rest, injected at runtime.
  {{</* /feature-card */>}}
{{</* /feature-grid */>}}
{{</* /section */>}}

{{</* section width="narrow" */>}}
## Works with your stack

{{</* icon-grid data="integrations" */>}}
{{</* /section */>}}

{{</* section */>}}
## Pricing

{{</* pricing data="editions" */>}}
{{</* /section */>}}

{{</* section width="narrow" */>}}
{{</* testimonial author="Jane Doe" role="VP Engineering, Northwind" */>}}
We replaced three internal tools with this and stopped thinking about
deploys entirely.

metrics:
- 80% less deploy time
- 40+ teams onboarded
{{</* /testimonial */>}}
{{</* /section */>}}

{{</* cta title="Ready to ship faster?" primary="Start free|/signup" secondary="Talk to sales|/contact" */>}}
No credit card. Cancel whenever.
{{</* /cta */>}}
```

## What to change

| Piece                   | Replace with                                |
| ----------------------- | ------------------------------------------- |
| `hero.code.content`     | Your actual config or CLI invocation        |
| `feature-card`          | Three to six cards, one benefit each        |
| `data/integrations.yaml`| The tools your customers already run        |
| `data/editions.yaml`    | Two or three plans, one marked `featured`   |

> [!TIP]
> The CTA repeats the hero's primary action on purpose. Visitors who
> scrolled the whole page should not have to scroll back up to act.
