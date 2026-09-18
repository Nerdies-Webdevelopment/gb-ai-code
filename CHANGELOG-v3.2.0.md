# 3.2.0 – portables WordPress-Projektpaket

- Vollständige deutsche README: Installation durch Kopieren, Abhängigkeiten,
  Arbeitsweise, Codex-Aufträge, Gutenberg, Werkzeuge, Updates und Fehlerbehebung.
- Paketordner automatisch erkennen; keine festen Benutzer- oder Sync-Zielpfade.
  Lokale Kopierbeziehungen bleiben in einer nicht verteilten Konfiguration.
- Read-only Einrichtungscheck und optionaler Windows-Doppelklickstart.
- Basisprofil mit GeneratePress/GenerateBlocks; Premium-Plugins nur im Vollprofil erforderlich.
- Nativen Anleitungs-Export an beliebige Website-Unterordner anpassen.
- Git-Abgrenzung für reine Paketdateien und GitHub-Workflow für Windows/Linux.
- Neue Tests für fremde Installationsnamen, Profile, Sync-Konfiguration und Exportpfade.
- Windows-Kurzpfade vor Transaktionspfad-Vergleichen normalisieren.
- Release 3.2.0 mit SHA-256; Child Theme unverändert 0.4.

## Regelaktualisierung vom 18.09.2026

Die überarbeitete Vorgabe zu Shapes und Icons wurde aus der bereitgestellten
PROJECT-RULES.md in GB-SHAPE-001 übernommen. Komplexe dekorative Referenzformen
werden als native GenerateBlocks-Shapes mit Inline-SVG umgesetzt; vereinfachte
CSS-Borders und Pseudo-Elemente dürfen ihre erkennbare Linienführung nicht ersetzen.
Einfache Flächen, Kreise und Overlays dürfen weiterhin Pseudo-Elemente verwenden.
Bestehende Regel-IDs und übrige Paketregeln bleiben erhalten.
