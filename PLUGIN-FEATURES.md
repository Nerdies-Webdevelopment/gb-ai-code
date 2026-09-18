# Zusätzliche Plugin-Funktionen

Quellprüfung vom 18.09.2026: GenerateBlocks 2.4.1, GenerateBlocks Pro 2.7.1,
GP Premium 2.5.6. Dies erweitert die Arbeitsanleitungen des Pakets; es aktiviert
keine Funktionen auf der Website. Plugin-Aktivierung und gespeicherte Einstellungen
wurden nicht geprüft. Alle Quellpfade unten sind relativ zur WordPress-Installation.

## Auswahl nach Aufgabe

| Aufgabe | Native Lösung | Arbeitsanleitung |
|---|---|---|
| Header, mobile Navigation, Untermenüs, Mega Menu | Pro-Navigationsblöcke; bei klassischem Theme-Header GP Menu Plus | `generateblocks-navigation` |
| Kontaktformular mit eigenen Feldern | Optionale Pro Forms; vorhandene Formulare weiterverwenden | `generateblocks-forms` |
| Popup, Off-canvas, bedingte Inhalte | Pro Overlays und Conditions | `generateblocks-display` |
| Wiederkehrende Klassen, lokale Muster und Assets | Pro Global Styles, Pattern Library, Asset Library | `generateblocks-global-styles` |
| Archiv, Beitragsraster, Meta-Repeater, dynamische Texte | Core Query/Dynamic Tags + Pro-Erweiterungen | `generateblocks-query-loop` |
| Website-Header/Footer ersetzen, Hooks, Layout-Regeln | GP Premium Elements | `generatepress-premium` |

Dies sind quellbasierte Arbeitsabläufe. Für neue interaktive Familien gibt es
noch keinen geprüften Gutenberg-Export. Schema, Save-Funktion und PHP-Renderer
zusammen prüfen oder einen aktuellen gespeicherten Export verwenden. `block.json`
allein beweist keine gültige Speicherung. Keine Referenz erhält durch diese
Bestandsaufnahme den Status `validated`.

## GenerateBlocks: Query und dynamische Inhalte

Quellen unter `wp-content/plugins/generateblocks/`:

- `dist/blocks/query/block.json`: `queryType` (Standard `WP_Query`), `query`,
  `inheritQuery` und `paginationType` (`standard` oder `instant`).
- `dist/blocks/query-page-numbers/block.json` und
  `dist/blocks/query-no-results/block.json`: native Seitennummern und Leerzustände.
- `includes/blocks/class-query.php`: Abfragekontext und geerbte Hauptabfrage.
- `includes/dynamic-tags/class-dynamic-tags.php`: registriert u. a. `post_title`,
  `post_permalink`, `post_excerpt`, `post_date`, `post_meta`, `featured_image`,
  `term_list`, Autorendaten sowie Links zur vorherigen/nächsten Ergebnisseite.
- `includes/dynamic-tags/class-dynamic-tag-callbacks.php`: Ausgabeverhalten;
  `includes/class-dynamic-tag-security.php`: Zugriffsbeschränkungen.

Dynamische Texte als native Tags verwenden; Syntax und Optionen aus dem jeweiligen
Callback bzw. gespeichertem Export übernehmen. Keine erfundenen Metaschlüssel oder
IDs. Fehlende Werte, Beitragskontext und verlinkte Bilder berücksichtigen.
`inheritQuery` nur für die beabsichtigte Hauptabfrage einsetzen. Für unabhängige
Listen eigene Parameter verwenden; mehrere paginierte Queries getrennt halten.
Instant Pagination auch mit Fokus, Zurück-Navigation und Leerzustand prüfen.

Pro ergänzt unter `wp-content/plugins/generateblocks-pro/`:

- `includes/extend/query/class-query.php`: Query-Typen `post_meta` und `option`;
  `includes/extend/looper/class-looper.php`: Ausgabe ihrer Einträge.
- `includes/extend/dynamic-tags/class-register.php`: `archive_title`,
  `archive_description`, `option`, `term_meta`, `user_meta`, `current_year`,
  `site_title`, `site_tagline`, `site_logo_url`, `site_url`, `loop_index`, `loop_item`.
- `includes/extend/dynamic-tags/class-acf.php`: ACF-Anbindung; vorhandenes ACF und
  echtes Feldschema prüfen. Eine Pro-Installation belegt keine ACF-Installation.
- `includes/extend/query-loop/class-related-*.php`: Beziehungen zu Beitrag,
  Parent, Autor und Terms. Alte Query-Loop-Erweiterungen nicht ungeprüft auf die
  aktuellen Query-Attribute übertragen.

Repeater benötigen reale Feld-/Optionsnamen und passende Array-Daten. Nur für
öffentliche Ausgabe bestimmte Werte verwenden; Plugin-Zugriffsprüfungen erhalten.

## Navigation und Mega Menu

Unter `generateblocks-pro/dist/blocks/` sind `site-header`, `navigation`,
`menu-toggle`, `menu-container`, `classic-menu`, `classic-menu-item` und
`classic-sub-menu` vorhanden. Die gleichnamigen Verzeichnisse unter
`includes/blocks/` enthalten die PHP-Renderer; die jeweiligen `index.js`-Dateien
enthalten Editor-/Save-Implementierungen.

`navigation/block.json` führt u. a. `subMenuType` (Standard `hover`) und
`htmlAttributes` als Kontext. Daraus keine vollständige Blockhierarchie oder
ARIA-Verknüpfung ableiten. Wrapper, responsive Umschaltung, Ziele des Toggles und
Save-Markup am konkreten Export bzw. an der Implementierung prüfen.

`includes/mega-menus/class-mega-menus.php` registriert am WordPress-Menüeintrag
`nav_menu_item` die Metadaten `_gb_mega_menu` (number) und
`_gb_mega_menu_anchor` (string). Diese Daten liegen außerhalb des Seiteninhalts.
Die zugehörige Overlay-Konfiguration ebenfalls übertragen; keine fiktiven IDs
oder erfundenen `generateblocks-pro/mega-menu`-Blöcke erzeugen.

Bei Header-Aufgaben zuerst bestimmen, ob der GeneratePress-Theme-Header oder ein
Block-Header bearbeitet wird. GP Menu Plus und Pro Navigation sind getrennte Wege.
Tastaturbedienung, Touch, Escape, Fokus-Rückkehr, kleine Breiten und mehrere Menüs
auf derselben Seite gehören zu den erforderlichen Laufzeitprüfungen.

## Native Pro Forms

`includes/feature-settings.php` setzt `enable_forms` im Quellcode auf `false`.
`init.php` und `includes/blocks/blocks.php` laden das Formularsystem nur bei
aktiviertem Schalter. Dies sagt nichts über den aktuellen gespeicherten Wert aus.

- Formular-Datensatz: `gblocks_form`, definiert in
  `includes/form/class-form-post-type.php`.
- Formularaufbau: `generateblocks-pro/form`, `form-field`, `form-field-label`,
  `form-field-control`; genaue Struktur aus den entsprechenden `dist/blocks/`
  und `includes/blocks/`-Dateien ableiten.
- Seiteneinbettung: `generateblocks-pro/form-render`; dessen `block.json`
  deklariert `formId` als Integer. Der PHP-Renderer verwendet den gespeicherten
  Formular-Datensatz. Felder und Aktionen werden nicht mit einer bloßen
  Seitenreferenz transportiert.
- `includes/form/bootstrap.php` lädt E-Mail, Bestätigungs-E-Mail,
  Newsletter-Anmeldung, Webhooks, Spam-/Turnstile-Unterstützung und Submissions.
  Eingebaute Integrationen liegen unter `includes/form/integrations/`.

Ein vorhandenes Drittanbieterformular nicht automatisch ersetzen. Für ein neues
natives Formular zunächst Felder, Beschriftungen, Pflichtangaben und gewünschte
Aktionen bestimmen. Eine echte veröffentlichte Formular-ID erst nach Einrichtung
verwenden. Keine Schlüssel, Empfängeradressen oder Webhook-Ziele erfinden oder
in portable Exporte übernehmen. Turnstile/externe Dienste nicht nebenbei einbauen.
Visuelle Prüfungen senden keine Formulare ab; Versand und Integrationen benötigen
einen gesondert beauftragten Funktionstest. Fehlermeldungen, Labels, Fokus und
Bestätigungszustand ohne echte Übermittlung prüfen, soweit die Umgebung das erlaubt.

## Overlays und Anzeigebedingungen

Quellen unter `generateblocks-pro/`:

- `includes/overlays/class-overlay-post-type.php`: `gblocks_overlay`.
- `includes/overlays/class-overlays.php` und `class-overlay.php`: Einstellungen
  und Ausgabe; u. a. Typ, Auslöser, Position, Backdrop, Animation, Zeit-/Scroll-
  Auslösung sowie Escape, Außenklick und Scroll-Sperre je nach Overlay-Typ.
- `includes/conditions/class-conditions-post-type.php`: `gblocks_condition`.
- `includes/conditions/conditions/`: Bedingungen für Ort, Benutzerrolle,
  Post-/User-Meta, Optionen, Datum/Zeit, Gerät, Sprache, Cookie, Referrer,
  Query-Argumente und Autor. Verfügbarkeit aus der Registry überprüfen.
- `includes/extend/block-conditions.php`: Blockattribute `gbBlockCondition`
  (string) und `gbBlockConditionInvert` (boolean), Verweis auf `_gb_conditions`.
- `includes/extend/menu-item-conditions.php`: Bedingungen für Menüeinträge.

Quell-Standardwerte: `enable_overlay_panels=true`, `enable_block_conditions=true`.
Live-Einstellungen können abweichen. Overlays und Conditions sind eigene Datensätze;
portables `post_content` allein überträgt sie nicht. Reale IDs und Abhängigkeiten
im Ergebnis aufführen. Trigger/Schließen-Beziehungen vom Plugin übernehmen.

Bedingungen steuern Anzeige. Insbesondere gibt der Block-Renderer bei fehlender
oder unveröffentlichter Bedingung den ursprünglichen Inhalt zurück. Daher keine
Zugriffssicherung für vertrauliche Inhalte daraus ableiten. Bei benutzer-, geräte-
oder zeitabhängigen Bedingungen auch den Seiten-Cache berücksichtigen. Overlay-
Tests umfassen Öffnen/Schließen, Fokus, Escape, Scroll und reduzierte Bewegung.

## Globale Klassen, Muster und Assets

Quellen unter `generateblocks-pro/`:

- `includes/styles/class-styles-post-type.php`: aktuelle globale Styles unter
  `gblocks_styles`; `class-styles.php` und `class-styles-enqueue.php`: Verwendung
  und CSS-Ausgabe. Blockattribute können `globalClasses` führen.
- `includes/class-global-styles.php`: ältere globale Styles; nicht mit dem
  aktuellen System gleichsetzen oder ungefragt migrieren.
- `includes/pattern-library/class-patterns-post-type.php` und
  `class-pattern-library.php`: lokale Pattern Library.
- `includes/class-asset-library.php`: Asset Library.

Für konsistente wiederkehrende Elemente vorhandene globale Klassen bevorzugen,
wenn deren Definitionen in der Zielinstallation existieren. Klasse, Definition,
responsive Zustände und Übertragungsweg zusammen dokumentieren. Ein Klassenname
allein transportiert kein Styling. Eigenständige Exporte benötigen mitgelieferte
Definitionen oder gleichwertige blocklokale Styles/CSS. Bestehende Theme-Tokens
weiterverwenden. Muster sind keine pauschale Zusicherung synchronisierter Inhalte.
Keine Premium-Plugin-Dateien oder fremden Bibliotheksinhalte ins Paket kopieren.

## GP Premium: Module und Elements

`wp-content/plugins/gp-premium/gp-premium.php` lädt Module abhängig von Optionen
bzw. Konstanten. Ein vorhandenes Modul ist nicht automatisch aktiv.

| Modul | Aufgabe / Grenze |
|---|---|
| Elements | Block-, Hook-, Layout- und Header-Elements mit Anzeigeregeln |
| Menu Plus | Theme-Navigation; Sticky-/mobile Header und Off-canvas-Menü |
| Secondary Nav | Zweite Theme-Navigation |
| Blog | Blog-/Archivdarstellung und Beitragsmetadaten |
| Spacing / Backgrounds | Theme-Abstände und Hintergründe |
| Disable Elements | Ausgewählte Theme-Bestandteile ausblenden |
| Copyright | Footer-Copyright konfigurieren |
| Font Library | Schriftverwaltung; Projekt nutzt Theme-Schrift, keine ungefragten externen Fonts |
| WooCommerce | Shop-Anpassungen; zusätzlich aktives WooCommerce erforderlich |
| Site Library | Site-Import; keine notwendige Aktion für einzelne Blockaufgaben |

`hooks`, `page-header` und `sections` stehen im Loader als veraltete Module.
`colors` wird nur bei älteren Parent-Themes geladen, `typography` nur ohne aktive
dynamische Typografie. Für GeneratePress 3.6.1 nicht einfach alle gefundenen
Modulnamen als moderne oder aktive Funktionen darstellen.

Elements-Quellen: `elements/class-post-type.php` (`gp_elements`),
`elements/elements.php`, `class-block.php`, `class-layout.php`, `class-hooks.php`,
`class-hero.php` und `class-conditions.php`.

Block-Elements verwenden u. a. `_generate_element_type`, `_generate_block_type`
und Hook-/Anzeigemetadaten. `class-block.php` behandelt `site-header`,
`site-footer`, `content-template` und `loop-template`. Ein normaler Seitenblock
ersetzt den Theme-Header nicht. Inhalt plus Element-Typ, Platzierung, Priorität,
Anzeigeregeln und Ausschlüsse getrennt angeben. Content Template formt einzelne
Einträge; Loop Template ersetzt die Schleifenausgabe und braucht passende Query-
Vererbung. Bestehende Header/Footer und Archivregeln auf Doppel-Ausgabe prüfen.
Keine GP-Optionen oder Post-Meta als GenerateBlocks-Attribute erfinden.

## Wiederholbare Quellprüfung

```powershell
python tools/check_environment.py --profile full
python tools/inspect_plugin_features.py
python tools/inspect_plugin_features.py --root C:/pfad/zur/wordpress-installation --json
```

`docs/plugin-source-inventory.json` ist der portable Snapshot dieser Prüfung:
9 Core- und 27 Pro-Blockmetadaten, 15 Core- und 12 Pro-Tags aus den untersuchten
Registrierungsdateien sowie 16 GP-Modulschalter (einschließlich Legacy).
Der Scanner liest nur Quelltext, keine Datenbank, Konfiguration oder Zugangsdaten.
Er erkennt Metadaten-Dateien, keine tatsächlich aktive Block-Registry. Legacy-
Blöcke, per PHP/Filter ergänzte Attribute und weitere Tag-Registrierungen können
fehlen. Der Snapshot ist kein Save-Markup-Vertrag und kein Aktivierungsnachweis.

Nach einem Plugin-Update Scanner und Versionscheck erneut ausführen, betroffene
Save-/Render-Pfade prüfen und dann diesen Snapshot bewusst erneuern. Statische
Tests prüfen Scannerfehler; Gutenberg-Roundtrip und Browser-Interaktionen bleiben
eigenständige Prüfungen für konkret erzeugte Blöcke.
