# DEPLOYMENT-NOTES.md

## Bestehende Installation

Diese Paketstruktur ist für eine bestehende WordPress-Installation gedacht.

Vor dem Kopieren:

- Backup erstellen
- vorhandenes `wp-content/themes/generatepress_child/` prüfen
- vorhandene Root-`AGENTS.md` / `.agents/` / `tools/` / `references/` prüfen
- bei bestehenden eigenen Änderungen zuerst Diff/Merge statt blindem Überschreiben

## Nicht enthalten

Nicht enthalten sind:

- WordPress Core
- GeneratePress Parent Theme
- GenerateBlocks
- GenerateBlocks Pro
- GP Premium
- produktive Uploads
- Datenbank

WordPress, GeneratePress und GenerateBlocks sind die Basis. Pro-Erweiterungen
und weitere Plugins werden nur bei Verwendung der jeweiligen Funktion benötigt.
Die vollständige Abhängigkeitstabelle steht in README.md.

## Codex

Codex sollte aus dem WordPress-/Git-Projektroot gestartet werden, damit die
Root-`AGENTS.md` und die Repository-Skills unter `.agents/skills/` verfügbar
sind.

Für Änderungen im Child Theme gilt zusätzlich die dort liegende
`wp-content/themes/generatepress_child/AGENTS.md`.
