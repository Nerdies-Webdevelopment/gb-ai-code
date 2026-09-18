# EXAMPLE-INDEX.md

## Purpose

Route Codex to the **smallest relevant technical reference set**.

The visual reference defines appearance. A technical reference defines structure. `PROJECT-RULES.md` defines binding project behavior.

Do not load every example for ordinary Visual-to-Code work.

Machine-readable metadata is in:

```text
references/REFERENCE-MANIFEST.json
```

## Matrix

| Family | Primary | Supplementary | Use for | Do not copy automatically |
|---|---|---|---|---|
| Tabs | `references/tabs/vertical-tabs01.html` | — | Pro hierarchy, menu/items, state/ARIA/save structure | vertical geometry, colors, URLs, fixed width |
| Accordion / FAQ | `references/accordion/faq01.html` | `references/accordion/faq-accordion01.html` | accordion hierarchy, toggle/content, FAQ patterns | copy, colors, fixed width, 768px legacy values, placeholder image |
| Carousel | `references/carousel/carousel03.html` | `references/query/query-loop01.html` for dynamic content | carousel hierarchy, items, pagination | copy, colors, fixed width, local values |
| Query / Looper | `references/query/post-grid01.html` | `references/query/query-loop01.html` | query attributes, looper/loop item, dynamic fields | query parameters, content, fixed width |
| Button / Pricing | `references/pricing/pricing01.html` | — | classic GB button serialization, pricing-card patterns | products, prices, copy, colors, fixed width |
| Table | `references/table/table01.html` | — | responsive desktop/mobile table composition | data, colors, fixed width |
| Contact | `references/contact/contactblock13.html` | — | content/form surroundings | form ID, 1200px width, copy, colors |
| Hero | `references/hero/hero03.html` | feature/content refs only for bounded techniques | complex hero geometry, pseudo-elements | exact decoration, min heights, fixed width |
| Content | `references/content/contentblock04.html` | — | gradient/pseudo-element content section | colors, copy, fixed width |
| Feature | `references/feature/feature01.html` | — | panel, shape, responsive geometry | brand colors, fixed heights, fixed width |
| CTA | `references/cta/cta03.html` | pricing button ref when button serialization is needed | compact CTA composition | copy, colors, fixed width |
| Process | `references/process/process01.html` | — | repeated cards, numbered responsive grid | copy, colors, fixed width |
| Footer | `references/footer/instantvolt-footer-hover01.html` | — | hover/focus link behavior, footer composition | font family, brand data, links, media IDs, fixed width |

## Family routing

### Tabs

Use:

```text
$generateblocks-tabs
references/tabs/vertical-tabs01.html
```

If the screenshot is horizontal, keep the technical tabs structure but derive horizontal geometry from the screenshot.

### Accordion

Use:

```text
$generateblocks-accordion
references/accordion/faq01.html
```

Add `faq-accordion01.html` only for image + accordion composition.

### Carousel

Use:

```text
$generateblocks-carousel
references/carousel/carousel03.html
```

For dynamic posts also route through `$generateblocks-query-loop` and read `query-loop01.html`.

### Query / Looper

Classic post grid:

```text
references/query/post-grid01.html
```

Dynamic carousel/combined interaction:

```text
references/query/query-loop01.html
```

### Button

Use `pricing01.html` as the preferred supplied classic GenerateBlocks button reference, but only if its button structure is compatible with the actual installed version.

### Hero / visually complex static sections

Choose the closest geometry technique:

- Hero → `hero03.html`
- gradient content → `contentblock04.html`
- panel/shape composition → `feature01.html`

Do not blend all three without a specific need.

## Conflict normalization

If a reference conflicts with a current project rule:

1. keep relevant serialization evidence
2. discard the conflicting example design/project value
3. normalize to the current project rule
4. mention the conflict only when it materially affects the implementation

Common legacy conflicts:

```text
768px reference breakpoint
vs
767px current project mobile breakpoint

fixed 1200px/1280px example width
vs
--gb-container-width

local font-family
vs
theme inheritance

localhost / foreign upload path
vs
portable project media

fixed example colors
vs
current design target/tokens
```

## Validation status

No reference in this supplied set is promoted to runtime-validated unless `references/REFERENCE-MANIFEST.json` explicitly records the required evidence.

A technically useful reference may still contain legacy warnings.

## Additional plugin workflows

Read the relevant section of `PLUGIN-FEATURES.md` for these tasks:

| Task | Skill | Required evidence |
|---|---|---|
| Navigation / Mega Menu | `generateblocks-navigation` | Current save/render + menu/overlay records |
| Native Forms | `generateblocks-forms` | Feature enabled + form record + real embedding ID |
| Overlays / Conditions | `generateblocks-display` | Current trigger/render contract + real records |
| Global classes / Patterns / Assets | `generateblocks-global-styles` | Actual definitions + transfer dependencies |
| Dynamic tags / pagination / repeaters | `generateblocks-query-loop` | Current callbacks + real query/field schema |
| GP Premium Elements / modules | `generatepress-premium` | Active module + placement/display metadata |

These are source notes, not new HTML reference entries. Existing reference
statuses in `references/REFERENCE-MANIFEST.json` remain unchanged.
