# Startseite: Paket installieren und nutzen

`homepage-package-guide.html` enthält die vollständige Anleitung mit Downloads
als 95 native GenerateBlocks-Container- und Textblöcke, direkt unter dem Hero.
Der Export stammt aus dem am 06.09.2026 in Gutenberg gespeicherten Seiteninhalt.
Der lokale Hero verlinkt „Installation & Nutzung“ auf `#paket-anleitung`.

## Inhalt

Gesamtpaket/Child-Theme-Downloads und SHA-256-Datei; Voraussetzungen,
Installation im WordPress-Hauptordner, Codex-Einrichtung, Blockcode einsetzen,
Prüfungen sowie Updates und parallele Paketpflege.

## Wiederverwenden

Vollständigen HTML-Code zwischen vollständigen Blöcken im Gutenberg-Code-Editor
einfügen. Danach visuell prüfen und speichern. Der Export enthält ausschließlich
die Anleitung; Hero und Footer sind nicht enthalten. Bei mehrfacher Verwendung
IDs und Sprungmarken eindeutig anpassen. Die drei Download-Pfade beginnen mit
`/dist/` für eine Installation an der Domain-Wurzel. Für Unterordner erzeugt
`python tools/export_homepage_guide.py --site-url DEINE_URL` die passende Kopie
unter `.local/homepage-package-guide.html`. Die ZIPs gehören ebenfalls an diesen Ort.

## Ausgeführte Prüfungen

- Strenge statische Prüfung des exportierten Abschnitts: 0 Fehler, 0 Warnungen.
- WordPress `parse_blocks()`: gesamte Home-Seite mit 103 registrierten Blöcken,
  eindeutigen IDs und erwarteter Hero-/Anleitungsstruktur gespeichert.
- Gutenberg im angemeldeten Chrome: visuell geöffnet, „Speichern“ ausgeführt,
  Meldung „Die Seite wurde aktualisiert.“ und nach Neuladen keine Meldung zur
  Block-Wiederherstellung. Anleitung und Downloads bleiben native Blöcke.
- Frontend: Hero-Sprungziel funktioniert; alle lokalen Sprungmarken vorhanden.
  Desktop- und Smartphone-Ansicht visuell betrachtet; kein horizontaler
  Seitenüberlauf bei 360, 390, 768, 1024 und 1920 Pixeln.
- Download-Ziele im gerenderten Frontend zeigen auf die lokale Paketablage.

Diese Prüfung gilt für die konkrete Home-Anleitung und den vorhandenen Hero,
nicht pauschal für sämtliche historischen Referenzen oder Pro-Komponenten.
Eine vollständige Barrierefreiheitsprüfung wurde nicht durchgeführt.

```powershell
python tools/validate_gb_block.py --strict docs/examples/homepage-package-guide.html
```

Seiteninhalte liegen in der WordPress-Datenbank. Die Paketsynchronisierung
überträgt diesen Export und importiert ihn nicht automatisch auf anderen Seiten.

## Portabler Stand 3.2.0

Downloadversion auf 3.2.0 aktualisiert und lokale Installationspfade aus der
Vorlage entfernt. Die oben aufgeführten Gutenberg-Prüfungen betreffen die
zugrunde liegende Struktur aus 3.1.3; neue Exportpfade werden statisch getestet.
