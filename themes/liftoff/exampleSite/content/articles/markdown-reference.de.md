---
title: "Alle Markdown-Elemente auf einer Seite"
date: 2026-07-10
author: "Kevin"
description: "Ein Referenzartikel, der jedes Element durchspielt, das Liftoff gestaltet. Jeder Abschnitt zeigt erst den Quelltext, dann das Ergebnis."
tags: ["referenz", "design"]
categories: ["Referenz"]
image: "/img/pipeline.svg"
---

<!-- markdownlint-configure-file {
  "MD010": false,
  "MD014": false,
  "MD028": false,
  "MD029": false,
  "MD040": false
} -->

Dieser Artikel darf ruhig überladen wirken, das ist Absicht. Er spielt
jedes Markdown-Element durch, das im Theme gestaltet ist. Damit lassen
sich Typografie, Abstände und der Kontrast im Dark Mode an einer Stelle
prüfen. Was hier schief aussieht, sieht auch in deinen Inhalten schief
aus.

Jeder Abschnitt zeigt zuerst den Quelltext, darunter das Ergebnis.

<!--more-->

## Überschriften

Das `h1` ist dem Artikeltitel vorbehalten, Fließtext beginnt deshalb
bei `h2`.

```markdown
## Zweite Ebene
### Dritte Ebene
#### Vierte Ebene
##### Fünfte Ebene
###### Sechste Ebene in Versalien
```

### Dritte Ebene

Ab der dritten Ebene bringt weitere Verschachtelung selten etwas.

#### Vierte Ebene

##### Fünfte Ebene

###### Sechste Ebene in Versalien

## Auszeichnungen im Fließtext

```markdown
Normaler Text mit **fett**, *kursiv*, ***beidem***, `Inline-Code`,
~~durchgestrichen~~ und <mark>hervorgehoben</mark>.

Abkürzungen wie <abbr title="Static Site Generator">SSG</abbr> bekommen
eine gepunktete Unterstreichung. Mit <kbd>Strg</kbd> + <kbd>C</kbd>
kopierst du.

Zwei Leerzeichen am Zeilenende  
erzwingen einen Umbruch ohne neuen Absatz.
```

Normaler Text mit **fett**, *kursiv*, ***beidem***, `Inline-Code`,
~~durchgestrichen~~ und <mark>hervorgehoben</mark>.

Abkürzungen wie <abbr title="Static Site Generator">SSG</abbr> bekommen
eine gepunktete Unterstreichung. Mit <kbd>Strg</kbd> + <kbd>C</kbd>
kopierst du.

Zwei Leerzeichen am Zeilenende  
erzwingen einen Umbruch ohne neuen Absatz.

## Links

```markdown
Ein [Link im Text](/docs), einer [mit Titel](/docs "Theme-Doku"), ein
nackter Autolink <https://gohugo.io/> und ein [Referenz-Link][hugo].

[hugo]: https://gohugo.io/
```

Ein [Link im Text](/docs), einer [mit Titel](/docs "Theme-Doku"), ein
nackter Autolink <https://gohugo.io/> und ein [Referenz-Link][hugo].

[hugo]: https://gohugo.io/

Links ab Wurzel werden sprachbewusst aufgelöst. Schreib also `/docs`,
nicht `/de/docs`.

## Listen

```markdown
- Design-Tokens liegen in `tokens.css`
- Komponenten liegen in `assets/css/components/`
  - Eine Datei pro Komponente
  - Eingebunden über `main.css`
- Schriften werden außerhalb des Bundles geladen
```

- Design-Tokens liegen in `tokens.css`
- Komponenten liegen in `assets/css/components/`
  - Eine Datei pro Komponente
  - Eingebunden über `main.css`
- Schriften werden außerhalb des Bundles geladen

```markdown
1. Theme als Modul einbinden
2. Eine Blueprint nach `content/` kopieren
3. Den Beispieltext durch eigenen ersetzen
4. Ausliefern
```

1. Theme als Modul einbinden
2. Eine Blueprint nach `content/` kopieren
3. Den Beispieltext durch eigenen ersetzen
4. Ausliefern

Eine nummerierte Liste darf beliebig anfangen:

```markdown
7. Siebtens
8. Achtens
```

7. Siebtens
8. Achtens

Aufgabenlisten verlieren den Aufzählungspunkt und zeigen eine
deaktivierte Checkbox:

```markdown
- [x] Layout steht
- [x] Doku steht
- [ ] Suchindex steht
```

- [x] Layout steht
- [x] Doku steht
- [ ] Suchindex steht

Definitionslisten:

```markdown
Hugo
: Der Static-Site-Generator, für den dieses Theme gebaut ist.

Iconify
: Die Icon-API, aus der das Theme beim Build lädt.
```

Hugo
: Der Static-Site-Generator, für den dieses Theme gebaut ist.

Iconify
: Die Icon-API, aus der das Theme beim Build lädt.

## Zitate

```markdown
> Ein Theme soll ein Startpunkt sein, kein Käfig. Wer es forken muss,
> um eine Farbe zu ändern, hat es falsch gebaut.
>
> > Zitate lassen sich schachteln, sinnvoll ist es selten.
```

> Ein Theme soll ein Startpunkt sein, kein Käfig. Wer es forken muss,
> um eine Farbe zu ändern, hat es falsch gebaut.
>
> > Zitate lassen sich schachteln, sinnvoll ist es selten.

## Hinweisboxen

Ein Zitat, das mit einer Alert-Markierung beginnt, wird zur
Hinweisbox. Die Beschriftung ist übersetzt und folgt der Sprache der
Seite.

```markdown
> [!NOTE]
> Neutraler Kontext. Für Hintergrund, den man auch überspringen kann.

> [!TIP]
> Eine Abkürzung oder der bessere Weg zum Ziel.

> [!WARNING]
> Etwas, das später Ärger macht, wenn man es jetzt ignoriert.

> [!DANGER]
> Etwas, das den Build sofort zerlegt.
```

> [!NOTE]
> Neutraler Kontext. Für Hintergrund, den man auch überspringen kann.

> [!TIP]
> Eine Abkürzung oder der bessere Weg zum Ziel.

> [!WARNING]
> Etwas, das später Ärger macht, wenn man es jetzt ignoriert.

> [!DANGER]
> Etwas, das den Build sofort zerlegt.

`[!CAUTION]` gilt als Alias für `[!DANGER]`.

## Code

Ein Block mit Sprachangabe bekommt ein Label und einen Copy-Button.

````markdown
```bash
hugo server --source exampleSite --themesDir ../..
```
````

```bash
hugo server --source exampleSite --themesDir ../..
```

Eine andere Sprache, um das Highlighting zu prüfen:

````markdown
```go
func main() {
	site := hugo.New()
	site.Render()
}
```
````

```go
func main() {
	site := hugo.New()
	site.Render()
}
```

Ohne Sprachangabe fällt der Block auf reinen Text zurück:

````markdown
```
$ hugo mod get codeberg.org/head1328/hugo-liftoff
```
````

```
$ hugo mod get codeberg.org/head1328/hugo-liftoff
```

Eine lange Zeile, um das horizontale Scrollen zu prüfen:

```json
{"module":{"imports":[{"path":"codeberg.org/head1328/hugo-liftoff","disable":false,"ignoreConfig":false,"ignoreImports":false}]}}
```

Diffs behalten ihre Vorzeichen:

```diff
-  --color-accent: #22d3ee;
+  --color-accent: #f97316;
```

## Tabellen

Doppelpunkte in der Trennzeile steuern die Ausrichtung.

```markdown
| Token            | Zweck                        | Light Mode |
| :--------------- | :--------------------------: | ---------: |
| `--color-bg`     | Seitenhintergrund            |         ja |
| `--color-accent` | Links, Buttons, Hervorhebung |         ja |
| `--space-4`      | Vertikaler Standardabstand   |       nein |
```

| Token            | Zweck                        | Light Mode |
| :--------------- | :--------------------------: | ---------: |
| `--color-bg`     | Seitenhintergrund            |         ja |
| `--color-accent` | Links, Buttons, Hervorhebung |         ja |
| `--space-4`      | Vertikaler Standardabstand   |       nein |

## Bilder

Ein einfaches Bild steht in einer eigenen Zeile. Für eine
Bildunterschrift packst du es in ein `figure`.

```markdown
![Das content-Verzeichnis speist die Layouts, daraus entsteht public](/img/pipeline.svg)

<figure>
  <img src="/img/pipeline.svg" alt="Das content-Verzeichnis speist die Layouts, daraus entsteht public">
  <figcaption>Markdown rein, statisches HTML raus.</figcaption>
</figure>
```

<figure>
  <img src="/img/pipeline.svg" alt="Das content-Verzeichnis speist die Layouts, daraus entsteht public">
  <figcaption>Markdown rein, statisches HTML raus.</figcaption>
</figure>

> [!NOTE]
> Dieses SVG ist ein Platzhalter aus der Demo. Ersetze es durch eine
> eigene Datei unter `static/` oder in einem Page Bundle.

## Aufklappbare Abschnitte

```markdown
<details>
  <summary>Warum gibt es keine Suche?</summary>

Eine Suche braucht einen Index im Browser oder einen gehosteten Dienst.

</details>
```

<details>
  <summary>Warum gibt es keine Suche?</summary>

Eine Suche braucht entweder einen Index im Browser oder einen
gehosteten Dienst. Beides ist eine Entscheidung, die in deine Seite
gehört und nicht ins Theme.

</details>

## Fußnoten

```markdown
Liftoff lädt Icons beim Build.[^1]

[^1]: Hugo cached die geladenen SVGs.
```

Liftoff lädt Icons beim Build, statt einen Icon-Font mitzuliefern.[^1]
So landen nur die Glyphen im Output, die eine Seite wirklich braucht.

## Trennlinie und Maskierung

```markdown
---

Ein Zeichen maskierst du mit Backslash: \*nicht kursiv\*, \# keine
Überschrift.
```

---

Ein Zeichen maskierst du mit Backslash: \*nicht kursiv\*, \# keine
Überschrift.

Wenn bis hierhin alles sauber zu lesen war, macht die Typografie ihren
Job.

[^1]: Hugo cached die geladenen SVGs, wiederholte Builds gehen also
    nicht erneut ins Netz.
