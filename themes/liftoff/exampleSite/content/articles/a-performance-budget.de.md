---
title: "Ein Performance-Budget, das man einhält"
date: 2026-05-15
author: "Kevin"
description: "Drei Zahlen, die auf einer statischen Seite Verteidigung lohnen, und wofür Liftoff sie ausgibt."
tags: ["performance", "css"]
categories: ["Design-Notizen"]
---

Ein Performance-Budget funktioniert nur, wenn es kurz genug ist, um im
Kopf zu bleiben. Für eine Inhaltsseite reichen drei Zahlen.

| Budget            | Zielwert      | Was es sprengt          |
| ----------------- | ------------- | ----------------------- |
| Requests pro Seite | unter 10     | Webfonts, Analytics     |
| CSS               | unter 30 kB   | Utility-Frameworks      |
| JavaScript        | unter 10 kB   | alles mit Build-Schritt |

Liftoff gibt sein JavaScript für drei Dinge aus: den Theme-Umschalter,
die Copy-Buttons an Codeblöcken und den Blueprint-Filter. Alle drei
bleiben ohne Skripte benutzbar, und nur deshalb dürfen sie überhaupt
existieren.

Teuer sind die Schriften. Fira Code kommt als zwei woff2-Dateien, auf
Latin reduziert und ausschließlich für Code. Der Fließtext nutzt den
System-Font-Stack: kostet nichts und wirkt auf jeder Plattform
heimisch.

> [!TIP]
> Bevor eine Abhängigkeit dazukommt, prüfe, ob der Browser es schon
> kann. Details und Summary ergeben Akkordeons, Dialog ergibt Modals,
> und beides braucht kein Kilobyte.

Nichts davon ist raffiniert. Es ist eine Liste dessen, was nicht
gemacht wurde.
