# GenerateBlocks Master Formula — Codex Edition

## Purpose

This file is the general construction formula for GenerateBlocks/Gutenberg work.

Project-specific values belong in `PROJECT-CONTEXT.md` and binding project behavior belongs in `PROJECT-RULES.md`.

Family-specific serialization belongs in `.agents/skills/` plus the closest technical reference.

## General formula

```text
New block
= purpose
+ visual geometry contract
+ current project contract
+ semantic structure
+ native block selection
+ version-correct serialization
+ unique identities
+ synchronized styles/css
+ responsive states
+ content-fit strategy
+ editor/frontend parity
+ accessibility
+ portability
+ honest validation
```

Technically:

```text
GB block
= Gutenberg wrapper(
    block name,
    attributes(
        uniqueId,
        tagName,
        styles,
        css,
        globalClasses,
        htmlAttributes,
        family-specific attributes
    ),
    saved markup,
    optional child blocks
)
```

## Core invariants

```text
uniqueId in JSON
= ID represented by native unique class
= ID represented by CSS selector
```

```text
styles
= same visual behavior as css
```

```text
tagName in JSON
= saved opening tag
= saved closing tag
```

```text
htmlAttributes
= saved HTML attributes
```

If one side differs, the block is unfinished.

## Reference model

Always distinguish:

```text
visual reference
= appearance and geometry

technical reference
= serialization and family structure

project context
= current documented facts

project rules
= binding implementation constraints
```

Do not let an example silently become a project rule.

## Production algorithm

### 1. Identify the job

Determine:

- section purpose
- semantic meaning
- block family
- interaction model
- dynamic/static data
- visible states
- whether the task modifies existing valid code or creates a new block

### 2. Analyze geometry before CSS

From the visual reference derive:

- outer bounds
- content container
- columns/rows
- relative proportions
- card widths/heights
- gaps and whitespace
- alignment
- overlap
- radii
- shapes
- reading order
- visible interaction states

Do not begin by guessing CSS values before the geometry is understood.

### 3. Route to one primary technical reference

Use `EXAMPLE-INDEX.md`.

Prefer one primary same-family reference.

Use a secondary reference only for a clearly bounded subproblem.

Do not merge unrelated example attributes opportunistically.

### 4. Inspect current runtime sources when needed

For version-sensitive GenerateBlocks/Pro behavior, inspect the actually installed plugin/theme implementation when available.

A documented version snapshot is not stronger than the current installation.

### 5. Build the semantic block tree first

Example:

```text
section
└── inner container
    └── layout
        ├── content
        │   ├── badge / eyebrow
        │   ├── heading
        │   ├── copy
        │   └── CTA group
        └── media / visual / cards
```

Only add wrappers with a distinct semantic or visual responsibility.

### 6. Select native blocks

Prefer native GenerateBlocks Core blocks.

Use Pro components only when their native interaction is required and their structure is supported by current evidence.

### 7. Assign identities

Use unique, readable family prefixes.

When repairing existing code, retain current valid IDs unless a change is necessary.

### 8. Implement desktop geometry

Desktop is the base state.

Use robust track sizing where content could overflow:

```text
minmax(0,1fr)
min-width:0
```

### 9. Add responsive transformations

Add only values that change.

Project breakpoints come from `PROJECT-CONTEXT.md`.

Desktop-only fixed geometry should normally reset to robust flow on smaller viewports.

### 10. Synchronize executable CSS

Derive `css` from the same intended state represented by `styles`.

Do not leave stale CSS after changing structured styles.

### 11. Synchronize saved markup

Confirm:

- tags
- classes
- IDs
- attributes
- state/ARIA values
- content

match the block attributes and family structure.

### 12. Validate honestly

Run static validation.

If WordPress is available, parse and reopen/save in Gutenberg.

If browser tooling is available, compare at relevant widths and verify interaction/focus.

Report only what actually ran.

## Component geometry

### Full-width outer section

Use the current project contract from `PROJECT-CONTEXT.md`.

### Inner container

Use the current project container source.

Do not learn the site width from an old example.

### Irregular/mosaic layouts

Desktop:

```text
visual proportions
+ independent card geometry
+ intentional offsets
+ controlled gaps
```

Tablet/mobile:

```text
semantic order
+ auto height
+ no desktop-only offsets
+ no content clipping
+ no internal scroll repair
```

### Local visual geometry

Prefer:

```text
local relative parent
+ local percentages / sizes
```

over internal viewport-driven positioning.

## Typography

Hierarchy follows document semantics.

Visual scale can be supplied by project typography classes/variables.

A local typography cap is acceptable for a truly constrained component, but not as a substitute for:

- wrong container width
- wrong layout
- unsuitable copy length
- clipped content

## CTA formula

For small CTA groups:

```text
flex
+ wrap
+ local gap
+ intrinsic button widths
```

Avoid distributing two simple CTAs with `space-between/around/evenly` unless the visual reference explicitly requires it.

## Full-card link formula

If the entire card has one destination:

```text
semantic outer link
+ no nested interactive controls
+ visible focus
+ accessible name
```

If the card has multiple actions, the outer card is not a link.

## Media formula

Content image:

```text
generateblocks/media
+ meaningful alt
+ stable responsive sizing
+ appropriate object-fit
+ real or clearly portable source
```

Decorative image:

```text
alt=""
```

Never invent a WordPress media ID.

## Accessibility formula

```text
native semantics
+ understandable accessible name
+ keyboard operability
+ visible focus
+ correct relationships
+ sufficient contrast
+ responsive semantic order
```

Pro interactions require correct family-specific relationships.

## Pro components

The following are family structures, not sufficient serialization proof.

### Accordion

```text
accordion
└── accordion-item
    ├── accordion-toggle
    │   └── optional accordion-toggle-icon
    └── accordion-content
```

### Tabs

```text
tabs
├── tabs-menu
│   └── tab-menu-item
└── tab-items
    └── tab-item
```

### Carousel

```text
carousel
├── carousel-items
│   └── carousel-item
├── optional pagination
└── optional controls
```

Always obtain exact attributes/classes/save markup from current implementation or the strongest compatible local reference.

## Badge formula

A simple single badge is:

```text
generateblocks/text
tagName: span
```

It is not a `generateblocks/element <span>` with InnerBlocks.

## Portability formula

Portable block:

```text
complete Gutenberg serialization
+ block-local styles/css
+ real or clearly portable media/links
+ no hidden DOM repair
+ no invented runtime IDs
+ no plugin-core edits
```

## Acceptance formula

```text
complete
= parseable block JSON
AND complete Gutenberg structure
AND unique identities
AND styles/css synchronization
AND tag/attribute synchronization
AND supported family serialization
AND robust responsive geometry
AND no horizontal page overflow by design
AND no clipped visible content
AND no scroll-as-repair
AND semantic responsive reading order
AND accessible interaction
AND portable serialization
AND honest validation report
```

Runtime-dependent checks remain open until they are actually executed.

## Features with dependencies beyond post_content

Use `PLUGIN-FEATURES.md` for navigation, forms, overlays/conditions, shared styles
and GP Premium placement. Model the result as block content plus required real
records, definitions and settings. Preserve native interaction and validate the
save/render contract; source inventory alone is not serialization proof.
