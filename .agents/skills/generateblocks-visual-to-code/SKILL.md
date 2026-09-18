---
name: generateblocks-visual-to-code
description: Convert screenshots, mockups, or visual web references into valid GenerateBlocks/Gutenberg post_content using this repository's project rules and technical reference library. Use for requests such as “convert this screenshot to GenerateBlocks”, “rebuild this section”, or visual-to-code repair.
---

# GenerateBlocks Visual-to-Code

## Required inputs

A visual reference is required for a visual reconstruction.

If none is available, ask exactly:

> Welches Bild soll ich in GenerateBlocks-Code umwandeln?  
> Which image should I convert into GenerateBlocks code?

## Read before implementation

From repository root read:

1. `PROJECT-CONTEXT.md`
2. `PROJECT-RULES.md`
3. `GenerateBlocks-Master-Formula-v2.md`
4. `EXAMPLE-INDEX.md`
5. `CAPABILITIES.md`

Then select the matching family skill and only the needed technical reference.

For version-sensitive Pro structures, inspect current installed plugin implementation when available.

## Workflow

1. Treat the visual as a geometry contract.
2. Identify purpose, block family, interaction model, dynamic/static data, visible states.
3. Analyze container edges, proportions, gaps, cards, overlap, radii, shapes, reading order.
4. Select one primary technical reference.
5. Build the semantic block tree without styling.
6. Assign unique IDs.
7. Implement desktop geometry.
8. Add only necessary responsive changes.
9. Synchronize `styles`, `css`, tags, classes, and attributes.
10. Run static validation.
11. If available, run WordPress/Gutenberg/browser checks.
12. Report only tests actually executed.

## Hard checks

- simple badge = `generateblocks/text` + `span`
- never `generateblocks/element <span>` with InnerBlocks for a simple badge
- no invented IDs, Pro attributes, hidden state content, or final URLs
- no raw HTML/custom JS substitute for native interaction
- no clipped visible content or internal card scroll repair
- use current project inner-container contract
- preserve semantic responsive order

## Default result structure

1. Reference analysis
2. Reference basis actually used
3. Essential technical decisions
4. Assumptions/placeholders
5. Compact block tree
6. Complete GenerateBlocks `post_content`
7. Validation status
8. Values still to replace

## Additional native features

For navigation, native forms, overlays, conditions, shared classes or theme-level
placement, follow the corresponding route in `EXAMPLE-INDEX.md` and read only
that section of `PLUGIN-FEATURES.md`. Use its focused skill and current save/render
evidence. These workflows are not validated HTML references. List record/settings
dependencies separately from the visual reconstruction.
