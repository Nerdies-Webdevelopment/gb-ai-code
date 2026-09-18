---
name: generateblocks-display
description: Configure GenerateBlocks Pro overlay panels and display conditions. Use for popups, off-canvas panels, conditional blocks or menu visibility; not for generic CSS visibility.
---

# generateblocks-display

All project paths below are relative to the package root (the directory containing AGENTS.md).

Read `PLUGIN-FEATURES.md` section Overlays and Anzeigebedingungen plus project rules. Inspect only the relevant local `generateblocks-pro/includes/overlays/`, `includes/conditions/` and `includes/extend/block-conditions.php` or `menu-item-conditions.php` implementation.

Choose native overlays/conditions for these tasks. Preserve real `gblocks_overlay` and `gblocks_condition` dependencies. Describe record setup, trigger target and conditions separately from portable page content. Derive close/trigger attributes from current save/runtime code; do not invent overlay block types or a parallel JavaScript controller.

`gbBlockCondition` is a string ID and `gbBlockConditionInvert` a boolean in the inspected implementation. Missing/unpublished condition records can leave content visible. Treat conditions as presentation rules, never authorization for confidential content. Consider cache behavior when output depends on user, time or request.

Confirm the feature setting, actual rule, exclusions and referenced records. Test opening/closing, Escape, focus return, scroll restoration and reduced motion for overlays; test both matching and nonmatching contexts for conditions. Record source evidence separately from actual runtime results.
