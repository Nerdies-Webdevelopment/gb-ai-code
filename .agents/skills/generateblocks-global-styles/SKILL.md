---
name: generateblocks-global-styles
description: Reuse GenerateBlocks Pro global classes, local patterns and assets while preserving portable exports. Use for shared style systems or pattern-library tasks, not ordinary one-off styling.
---

# generateblocks-global-styles

All project paths below are relative to the package root (the directory containing AGENTS.md).

Read `PLUGIN-FEATURES.md` section Globale Klassen, Muster und Assets and the project typography/container rules. Inspect current `generateblocks-pro/includes/styles/` and only the relevant pattern/asset-library implementation.

Inventory actual classes and definitions before reusing them. Match serialized `globalClasses`, saved classes and available CSS. Keep current `gblocks_styles` distinct from legacy global styles. Do not migrate unrelated styles or create guessed database IDs.

For a portable result, provide the referenced style definitions and setup or use equivalent block-local styles/css. A class name or copied pattern alone does not transfer database-backed styling or promise synchronized content. Retain `--gb-container-width` and inherited typography; avoid duplicating site tokens.

Compare shared and local styles, responsive states and focus states. Check definition import/availability and CSS loading in the target installation when runtime exists. Report external style/pattern/asset dependencies explicitly; distribute no premium plugin code.
