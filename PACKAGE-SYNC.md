# Optionale parallele Paketpflege

Der Paketordner ist die Standardquelle. Es gibt kein fest eingebautes Ziel.
Quelle und Ziel müssen getrennte Verzeichnisse sein. In einer vorhandenen
lokalen `.package-sync.local.json` können `source` und `destination` gespeichert
werden; diese Datei wird nicht synchronisiert oder veröffentlicht.

```powershell
python tools/validate_all.py --installed
python tools/build_release.py
python tools/sync_package.py --destination C:/paketkopie --apply
python tools/sync_package.py --destination C:/paketkopie
python C:/paketkopie/tools/validate_all.py
```

Mit lokaler Konfiguration kann `--destination` entfallen. Relative Konfigurationspfade
beziehen sich auf den Paketordner, explizite CLI-Pfade auf das Arbeitsverzeichnis.
Ohne `--apply` nur Vergleich: Exitcode 0 bedeutet Gleichstand, 1 Unterschiede/Fehler.
Bei --recover ohne lokale Konfiguration dieselben expliziten Pfade mitgeben.

`TREE.txt` enthält das explizite Dateiinventar. Fremde Dateien und unabhängige
Änderungen werden nicht überschrieben. Inventarentfernungen verlangen bewusste
Prüfung. WordPress-Core, Plugins, Uploads, Datenbank und lokale Konfiguration sind
ausgeschlossen. `.package-sync.json` speichert ausschließlich den lokalen Abgleichstand.
Es gibt keinen Hintergrunddienst. Die Desktop-Paketkopie ohne --installed prüfen.

## Sicherungen und Wiederherstellung ab v3.1.3

Der Abgleich hält eine Betriebssystem-Sperre gegen parallele Schreibzugriffe.
Er bereitet neue Dateien vor, sichert alle zu ersetzenden Dateien einschließlich
des bisherigen Abgleichstands und schreibt ein Wiederherstellungsjournal.
Erst anschließend ersetzt er einzelne Dateien atomar und prüft die Hashes.
Der gesamte Dateisatz wird dabei schrittweise ersetzt; er ist keine atomare Einheit.

Bei gewöhnlichen Schreibfehlern wird der vorherige Stand zurückgespielt.
Nach Prozessabbruch oder einer unterbrochenen Wiederherstellung stoppen weitere
Abgleiche. Beende andere Sync-Prozesse und führe im WordPress-Ordner aus:

```powershell
python tools/sync_package.py --recover
python tools/sync_package.py --apply
```

`--recover` stellt zuerst den Stand vor dem abgebrochenen Abgleich wieder her
und vergleicht danach nur. Exitcode 1 kann dann regulär verbleibende Unterschiede
anzeigen. Später manuell bearbeitete Dateien werden auch bei der Wiederherstellung
nicht überschrieben; die Meldung benennt den Konflikt. Journal und Sicherungen
bleiben bei Fehlern für die gezielte Klärung erhalten.

Vorbereitung, Journal und dauerhaft aufbewahrte Sicherungen liegen neben dem
Zielordner: `.<Zielordner>.package-sync-transaction` bzw.
`.<Zielordner>.package-sync-backup-<Kennung>` im übergeordneten Ordner des Ziels.
Sie werden nicht in das Paket oder das Download-ZIP aufgenommen. Nach Prüfung
können alte Sicherungsordner bewusst entfernt werden; es gibt keine automatische
Bereinigung. Fehlende Zieldateien werden wie bisher aus der Quelle wiederhergestellt.
Bei Datenträgerverlust kann auch eine Sicherung auf demselben Datenträger verloren
gehen; das Journal ersetzt kein externes Backup.
