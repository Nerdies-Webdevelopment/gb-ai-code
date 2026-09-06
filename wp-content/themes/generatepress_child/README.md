# GeneratePress Child – v0.4

## Zweck

Dieses Child Theme stellt den aktuellen dokumentierten Theme-Contract für das
GenerateBlocks-/Codex-Projekt bereit.

## Enthalten

### `style.css`

- `--gb-container-width: 1280px`
- Fluid-Typografie `--fs-h1` bis `--fs-h6`
- `--fs-p`
- `fs-*`-Utility-Klassen
- GenerateBlocks-Button-Typografie
- bewusst niedrige Utility-Spezifität über `:where(...)`

### `functions.php`

- registriert `style.css` per `add_editor_style()` für den Block-Editor
- bindet das Child-Stylesheet **nicht** redundant über `wp_enqueue_scripts()` ein
- behält die GenerateBlocks-Template-Vorschaubildspalte bei
- nutzt konsistente `gpc_`-Funktionspräfixe
- internationalisiert den Spaltentitel
- escaped dynamische Bildwerte

## Spezifitätskorrektur gegenüber v0.2

v0.2 verwendete unter anderem:

```css
body .fs-p
body .fs-h1
body .gb-button
```

Diese Utility-Selektoren waren unnötig stark.

v0.4 verwendet:

```css
body :where(.fs-p)
body :where(.fs-h1)
body :where(.gb-button)
```

Damit bleiben die Projektklassen Defaults, während eine bewusst gesetzte
GenerateBlocks-Unique-Class wie `.gb-text-abc123` eine lokale Typografie
überschreiben kann.

Die semantischen Defaults bleiben elementbasiert:

```css
body :where(h1)
body :where(h2)
...
body :where(p)
```

und sind damit weiterhin schwächer als eine GenerateBlocks-Klasse.

## Container-Contract

Für neue Full-Width-Sections:

```css
/* Outer section */
width: 100%;
max-width: 100%;
box-sizing: border-box;

/* Direct inner container */
width: 100%;
max-width: var(--gb-container-width, 1280px);
margin-left: auto;
margin-right: auto;
```

## GeneratePress

GeneratePress als Parent Theme installiert lassen.

Das Parent-Stylesheet weder per `@import` noch durch eine zusätzliche
projektseitige Frontend-Einbindung duplizieren.

Für echte Full-Width-GenerateBlocks-Sections muss der relevante
GeneratePress-Seiten-/Content-Container ebenfalls so konfiguriert sein, dass
das Theme die Section nicht zusätzlich begrenzt.

## Runtime-Hinweis

Die Admin-Hooks:

```text
manage_gblocks_templates_posts_columns
manage_gblocks_templates_posts_custom_column
```

setzen voraus, dass die installierte GenerateBlocks-Version weiterhin den
Post Type `gblocks_templates` verwendet.

Die PHP-Datei kann statisch validiert werden. Die tatsächliche Admin-
Integration muss nach relevanten GenerateBlocks-Upgrades in WordPress
runtime-validiert werden.

## Installation

1. GeneratePress installiert lassen.
2. Das mitgelieferte `dist/generatepress-child-v0.4.zip` über
   **Design → Themes → Hinzufügen → Theme hochladen** installieren.
3. Child Theme aktivieren.
4. GeneratePress-/Customizer-Einstellungen kontrollieren.
5. Gutenberg und Frontend bei derselben effektiven Komponentenbreite vergleichen.
6. Die GenerateBlocks-Template-Vorschaubildspalte im Admin prüfen.

## Korrektur v0.4

Semantische Defaults stehen vor allen Größenklassen. Beide verwenden
`body :where(...)` mit Spezifität (0,0,1). So setzt `h2.fs-h1` die H1-Größe,
während eine GenerateBlocks-Unique-Class mit (0,1,0) Vorrang behält.
Das Archiv v0.3 bleibt ausschließlich als historischer Stand erhalten.
