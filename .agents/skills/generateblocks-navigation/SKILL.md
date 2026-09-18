---
name: generateblocks-navigation
description: Build or repair GenerateBlocks Pro navigation, site headers, menu toggles and mega menus. Use for block navigation; distinguish GeneratePress Menu Plus theme settings.
---

# generateblocks-navigation

All project paths below are relative to the package root (the directory containing AGENTS.md).

Read `PLUGIN-FEATURES.md` sections Navigation and Overlays plus project context/rules.
Inspect the local `generateblocks-pro/dist/blocks/{site-header,navigation,menu-toggle,menu-container,classic-menu,classic-menu-item,classic-sub-menu}` metadata and save functions; pair them with the PHP renderers under `includes/blocks/`.

Determine whether the task targets the theme header or a block header. For theme Menu Plus or GP Elements placement, use `generatepress-premium`. Derive block hierarchy, native classes, ARIA and responsive toggle targets from a current export or implementation. The package has no runtime-validated navigation HTML reference; do not fabricate one from block names.

Mega menus also use WordPress menu-item metadata and overlay records. Read `includes/mega-menus/class-mega-menus.php`; preserve actual menu/overlay IDs and list required setup separately from post_content. Do not invent a mega-menu block or custom menu JavaScript.

Keep navigation semantic and keyboard-accessible. Verify mobile toggles, submenus, Escape, focus return, touch and multiple menus when runtime access exists. Run the block validator on produced HTML; source inspection alone does not prove a Gutenberg round trip.
