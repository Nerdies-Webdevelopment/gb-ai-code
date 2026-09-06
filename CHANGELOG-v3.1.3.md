# GenerateBlocks Codex 3.1.3

- Vollständiges versioniertes Projekt-ZIP mit SHA-256-Datei und reproduzierbarem
  Build aus dem expliziten Inventar. Das ZIP enthält keine weiteren Gesamtpaket-ZIPs,
  WordPress-Konfiguration, Plugins, Uploads oder Datenbankinhalte. Sein TREE.txt
  beschreibt ausschließlich den tatsächlichen Archivinhalt.
- Startseiten-Anleitung mit getrennten Downloads für Gesamtpaket und Child Theme;
  der lokale Hero-Link führt zu „Installation & Nutzung“.
- Stilprüfung in beide Richtungen: CSS-Zusätze werden pro Selektor/Kontext als
  Warnungen angezeigt und scheitern im strengen Modus. Grundlegende Farbnotationen
  und Null-Längen werden als gleichwertig erkannt. Benutzerdefinierte CSS-Variablen
  bleiben wörtlich verglichen. Keine vollständige Browser-Cascade-Simulation.
- Synchronisierung mit Vorbereitung, überprüften Sicherungen, Betriebssystem-Sperre,
  atomarem Ersetzen einzelner Dateien, Journal und expliziter Abbruch-Wiederherstellung.
- Zusätzliche Tests für CSS-Zusätze, gleichwertige Werte, Release-Inhalt/Reproduzierbarkeit,
  Schreibfehler, Abbrüche, spätere Benutzeränderungen und parallele Sync-Aufrufe.

Prüfstand: 45 Python-Tests; Child Theme weiterhin 0.4. Die 15 historischen Referenzen
haben 0 statische Fehler und jetzt 77 Warnungen: 24 bisherige Hinweise sowie
53 neu sichtbare Gruppen von CSS-Zusätzen. Ihre Inhalte wurden nicht pauschal
umgeschrieben oder als Gutenberg-validiert hochgestuft.

Der aktuelle Laufzeit-Prüfstand der Anleitung steht in
`docs/examples/homepage-package-guide.md`.
