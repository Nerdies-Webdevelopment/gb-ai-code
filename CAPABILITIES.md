# CAPABILITIES.md

## Purpose

This file tells Codex what this package can support safely **from repository evidence alone**.

`validated` means a reference has explicit runtime evidence recorded in the manifest. None of the supplied references were documented as fully runtime-validated, so this package does not promote them beyond their source status.

| Family | Type | Primary reference | Skill | Package support | Runtime validation |
|---|---|---|---|---|---|
| Tabs | GenerateBlocks Pro | `references/tabs/vertical-tabs01.html` | `generateblocks-tabs` | strong technical reference | unconfirmed |
| Accordion / FAQ | GenerateBlocks Pro | `references/accordion/faq01.html` | `generateblocks-accordion` | strong technical reference | unconfirmed |
| Accordion + image | GenerateBlocks Pro + Core | `references/accordion/faq-accordion01.html` | `generateblocks-accordion` | supplementary reference | unconfirmed |
| Carousel | GenerateBlocks Pro | `references/carousel/carousel03.html` | `generateblocks-carousel` | strong technical reference | unconfirmed |
| Query / dynamic carousel | Core + Pro | `references/query/query-loop01.html` | `generateblocks-query-loop` | strong technical reference | unconfirmed |
| Post grid | Core Query/Looper | `references/query/post-grid01.html` | `generateblocks-query-loop` | technical reference | unconfirmed |
| Pricing / classic GB button | Core | `references/pricing/pricing01.html` | `generateblocks-pricing-button` | preferred button reference | unconfirmed |
| Responsive table | Core | `references/table/table01.html` | `generateblocks-table` | technical reference | unconfirmed |
| Contact / form surroundings | Core + shortcode | `references/contact/contactblock13.html` | `generateblocks-contact` | layout reference only | unconfirmed |
| Hero | Core | `references/hero/hero03.html` | `generateblocks-hero` | visual/technical reference | unconfirmed |
| Content section | Core | `references/content/contentblock04.html` | `generateblocks-content-section` | visual/technical reference | unconfirmed |
| Feature | Core | `references/feature/feature01.html` | `generateblocks-feature` | visual/technical reference | unconfirmed |
| CTA | Core | `references/cta/cta03.html` | `generateblocks-cta` | core reference | unconfirmed |
| Process / steps | Core | `references/process/process01.html` | `generateblocks-process` | core reference | unconfirmed |
| Footer / link hover-focus | Core | `references/footer/instantvolt-footer-hover01.html` | `generateblocks-footer` | special reference | unconfirmed |
| Navigation / Mega Menu | GenerateBlocks Pro | none | none | **unsupported from package alone** | none |

## Decision rule

If a requested family is marked unsupported:

1. inspect the current local installed implementation, or
2. obtain a known-good local saved block/export from the same version.

Do not invent serialization to fill the gap.

## Promotion to validated

A reference may only be promoted when evidence is recorded for the relevant checks, for example:

- JSON/static structure
- WordPress `parse_blocks()`
- Gutenberg opens without recovery
- save/reopen round trip
- frontend interaction
- relevant responsive behavior
- editor/frontend parity where applicable

Record results in `references/REFERENCE-MANIFEST.json`.

## Local version delta (2026-09-06)

The installed sources are GenerateBlocks 2.4.1 / Pro 2.7.1, while the original
package documented 2.2.1 / Pro 2.5.0. The support table describes reference
availability, not verified compatibility with the installed versions.
Use local implementation evidence before producing version-sensitive markup.
No reference has been promoted to runtime-validated by this package update.
