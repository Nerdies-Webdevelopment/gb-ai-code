---
name: generatepress-premium
description: Use GP Premium Elements, Menu Plus and theme modules for GeneratePress headers, footers, hooks, layouts and archives. Use when a task affects theme placement or settings beyond page post_content.
---

# generatepress-premium

All project paths below are relative to the package root (the directory containing AGENTS.md).

Read `PLUGIN-FEATURES.md` section GP Premium and project context/rules. Inspect the relevant installed GP Premium module and, for theme integration, the packaged child theme instructions. Module presence does not prove activation.

Choose the narrowest integration: normal page content, Block Element, Hook Element, Layout Element, Header Element or an existing theme setting. For Elements inspect `elements/class-block.php`, the relevant renderer and `class-conditions.php`. Keep content separate from `gp_elements` type, placement/hook, priority, display rules and exclusions. Do not encode GP post meta as GB block attributes.

For header/footer replacement verify existing Elements and theme output to avoid duplicates. Distinguish Content Template for individual entries from Loop Template for the loop and choose query inheritance accordingly. For theme navigation prefer the requested existing Menu Plus/Secondary Nav settings; route block navigation to `generateblocks-navigation`.

Only configure modules relevant to the request. WooCommerce needs the actual shop plugin; Site Library import is not implied by a block request. Legacy Hooks/Page Header/Sections and compatibility-only Colors/Typography are not default modern choices. Keep fonts consistent with the theme and project no-external-font rule.

Project PHP/CSS belongs in the child theme; never edit plugin or parent-theme code. Validate changed block/theme files, then check actual placement and display/exclusion contexts when runtime is available. Report any settings that still require application independently of the generated post_content.
