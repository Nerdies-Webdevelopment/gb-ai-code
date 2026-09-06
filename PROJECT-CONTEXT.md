# PROJECT-CONTEXT.md

## Purpose

This file contains **documented and inspected project facts**, not workflow rules.

Rules belong in `PROJECT-RULES.md`. General construction principles belong in
`GenerateBlocks-Master-Formula-v2.md`. Reference routing belongs in
`EXAMPLE-INDEX.md`.

## Context status

```yaml
context_schema: 3
last_source_inspection: 2026-09-06
package_revision: 3.2.0
last_packaged: 2026-09-06

child_theme:
  packaged_source: wp-content/themes/generatepress_child/
  source_inspected: true
  corrected_package_version: 0.4
  php_syntax_checked: true
  static_validation_passed: true
  wordpress_runtime_verified: false
  gutenberg_editor_verified: false
  generateblocks_admin_column_runtime_verified: false

plugin_theme_snapshot:
  status: local_source_headers_inspected
  actual_installed_source_included_in_package: false
  source_installation: local_reference_installation_not_distributed
  actual_installed_source_present_at_source: true
  activation_verified: false
```

The corrected Child Theme source **is included** in this repository and has
been statically inspected.

The inspected reference installation contains the GeneratePress / GenerateBlocks /
GenerateBlocks Pro / GP Premium sources. Their version headers were read on
2026-09-06. The Desktop package copy does not bundle these plugins; these facts describe
the source installation, not plugin presence in every package copy.
This inspection does not establish active plugins, the active theme, or
Gutenberg compatibility. Run `python tools/check_environment.py` after updates.

If the actual local installation differs, the actual installation wins.

## Project

```text
Project family: GenerateBlocks / GeneratePress Block Library
Child theme:    GeneratePress Child (present; activation not checked)
Parent theme:   GeneratePress
Child source:   wp-content/themes/generatepress_child/
Block library:  GB-Blöcke/
```

Project-specific theme code belongs in the GeneratePress Child Theme.

GenerateBlocks, GenerateBlocks Pro, GeneratePress parent theme, and WordPress
core are technical sources, not project-edit targets.

## Inspected local plugin/theme source versions

```text
GeneratePress:       3.6.1
GP Premium:          2.5.6
GenerateBlocks:      2.4.1
GenerateBlocks Pro:  2.7.1
```

Sources: `wp-content/themes/generatepress/style.css`,
`wp-content/plugins/gp-premium/gp-premium.php`,
`wp-content/plugins/generateblocks/plugin.php`, and
`wp-content/plugins/generateblocks-pro/plugin.php`.

The original package documented GenerateBlocks 2.2.1 / Pro 2.5.0.
Existing references are not thereby validated against 2.4.1 / Pro 2.7.1.
Inspect the installed family implementation before version-sensitive work.
Do not infer a newer or different version from memory.

## Inspected Child Theme contract

The packaged v0.4 `style.css` defines:

```css
:root {
    --gb-container-width: 1280px;

    --fs-h1: clamp(2.15rem, 1.625rem + 2.625vi, 3.6rem);
    --fs-h2: clamp(1.75rem, 1.4045rem + 1.7273vi, 2.7rem);
    --fs-h3: clamp(1.45rem, 1.1591rem + 1.4545vi, 2.25rem);
    --fs-h4: clamp(1.25rem, 1.05rem + 1vi, 1.8rem);
    --fs-h5: clamp(1.1rem, 0.9545rem + 0.7273vi, 1.5rem);
    --fs-h6: clamp(1rem, 0.8727rem + 0.6364vi, 1.35rem);
    --fs-p: clamp(0.95rem, 0.9318rem + 0.0909vi, 1rem);
}
```

The packaged `functions.php` registers:

```php
add_theme_support( 'editor-styles' );
add_editor_style( 'style.css' );
```

## Typography specificity contract

Semantic defaults use element selectors such as:

```css
body :where(h1)
body :where(h2)
body :where(p)
```

Project typography utilities deliberately use low specificity:

```css
body :where(.fs-h1)
body :where(.fs-h2)
...
body :where(.fs-p)
body :where(.gb-button)
```

Defaults and utilities both have specificity (0,0,1). All semantic defaults
precede all size utilities. Native unique classes have specificity (0,1,0),
so they retain priority in either stylesheet order. Typography was checked
in isolated Chromium at 1440, 768 and 390px; Gutenberg parity remains unverified.

Do not reintroduce:

```css
body .fs-h1
body .fs-p
body .gb-button
```

without an explicit project decision.

## Container facts

Current packaged project container source:

```text
--gb-container-width
```

Current packaged value:

```text
1280px
```

Preferred current inner-container expression:

```css
max-width: var(--gb-container-width, 1280px);
```

Older references may contain fixed `1200px` or `1280px`. Those values are not
automatically current project facts.

## Typography facts

Font family is inherited from the active GeneratePress / Child Theme unless a
specific current project requirement says otherwise.

Current project classes/tokens:

```text
--fs-h1 / fs-h1
--fs-h2 / fs-h2
--fs-h3 / fs-h3
--fs-h4 / fs-h4
--fs-h5 / fs-h5
--fs-h6 / fs-h6
--fs-p  / fs-p
```

Semantic tag and visual scale are independent.

## Responsive facts

Documented primary states:

```text
Desktop: base styles
Tablet:  @media (max-width:1024px)
Mobile:  @media (max-width:767px)
```

Important test widths:

```text
wide desktop
normal desktop
1024px
768px
~440px
~412px
~393px
~360px
```

`768px` is a test width, not automatically the mobile CSS breakpoint.

## GenerateBlocks facts

Typical Core blocks used by the project:

```text
generateblocks/element
generateblocks/text
generateblocks/media
generateblocks/shape
generateblocks/query
generateblocks/looper
generateblocks/loop-item
generateblocks/button
```

A locally appropriate classic GenerateBlocks button reference may use:

```text
blockVersion: 4
```

GenerateBlocks Pro structures must be derived from the installed version
and/or the closest reliable local reference.

Known Pro families in the project context:

```text
Accordion
Tabs
Carousel
Navigation / Mega Menu
```

Navigation / Mega Menu currently has no reference in this package and is not
considered safely serializable from the package alone. See `CAPABILITIES.md`.

## GenerateBlocks admin integration in the Child Theme

The packaged Child Theme contains admin-column hooks for:

```text
gblocks_templates
```

This integration has been statically inspected but is **runtime-dependent** on
the installed GenerateBlocks implementation.

After a relevant GenerateBlocks upgrade, confirm the actual post type/hook
contract before changing the code.

## Editor/frontend geometry facts

WordPress editor chrome is not part of component geometry.

Editor/frontend parity is evaluated at the same effective component/content
width.

Internal component geometry should generally be local-container-relative
rather than viewport-relative when this affects parity.

## Known legacy/reference differences

Older references may include:

```text
fixed 1200px or 1280px containers
768px CSS breakpoints
local font-family values
localhost URLs
placeholder media
old colors
example-specific IDs
brand-specific content
href="#"
```

These are not automatically current project values.

## Unknown runtime facts

Do not invent without current verification:

```text
WordPress patch version
PHP runtime used by the live site
production domain
post/page IDs
media/attachment IDs
form IDs
final external URLs
current installed plugin versions if they differ from the snapshot
live Gutenberg/editor behavior
live GenerateBlocks template post type after upgrades
```

## Update triggers

Update this file when any of these change:

```text
GeneratePress version
GP Premium version
GenerateBlocks version
GenerateBlocks Pro version
Child Theme source
--gb-container-width
fluid typography
specificity contract
breakpoints
editor-style integration
GenerateBlocks template admin integration
reference-library support matrix
```

When GenerateBlocks or GenerateBlocks Pro changes version, revalidate
version-dependent save/render structures and Child Theme integration before
promoting validation status.
