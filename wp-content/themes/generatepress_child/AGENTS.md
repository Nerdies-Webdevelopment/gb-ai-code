# AGENTS.md — GeneratePress Child Theme

These instructions apply when working inside this Child Theme and supplement
the repository-root `AGENTS.md`.

## Edit boundary

Project-specific theme code belongs here.

Do not edit:

- GeneratePress parent theme
- GenerateBlocks Core
- GenerateBlocks Pro
- WordPress Core

## Theme contract

Preserve the project tokens unless the task explicitly updates the project
contract:

```text
--gb-container-width
--fs-h1 ... --fs-h6
--fs-p
```

When a token changes, also update `PROJECT-CONTEXT.md`.

## CSS specificity rule

Typography utilities are project defaults, not hard overrides.

MUST NOT reintroduce selectors such as:

```css
body .fs-h1
body .fs-p
body .gb-button
```

Prefer low-specificity utility selectors such as:

```css
body :where(.fs-h1)
body :where(.fs-p)
body :where(.gb-button)
```

Local GenerateBlocks unique-class CSS must remain able to override a utility
when a component has a justified local typography requirement.

## Editor parity

Keep:

```php
add_theme_support( 'editor-styles' );
add_editor_style( 'style.css' );
```

Do not add a duplicate frontend enqueue merely to load this Child Theme's
`style.css`.

## GenerateBlocks template admin column

The `gblocks_templates` post-type hooks are version-dependent integration
points.

Do not change the hook/post-type names from memory. If GenerateBlocks is
upgraded or the column stops working, inspect the actual registered post type
and hooks before changing this code.

## Validation

After changing this Child Theme run:

```bash
python tools/validate_child_theme.py
```

If PHP CLI is available, the validator also executes:

```bash
php -l wp-content/themes/generatepress_child/functions.php
```

WordPress activation, Gutenberg parity, and the admin template column remain
runtime checks and must not be claimed without execution.

## Typography cascade

Use `body :where(h1)` through `body :where(h6)` and `body :where(p)`
before all `body :where(.fs-*)` utilities. Both have specificity (0,0,1);
size utilities win by order, native unique classes win by specificity.
After changing typography run `node tools/check_typography.cjs` when Playwright
and Chromium are available; see VALIDATION.md. Rebuild the current installable
Child Theme ZIP and verify it matches the source.
