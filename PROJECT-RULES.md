# PROJECT-RULES.md

## Purpose and terminology

This is the single authoritative file for project-specific implementation rules.

Keywords:

- **MUST** — required
- **MUST NOT** — prohibited
- **SHOULD** — preferred unless a more specific technical reason overrides it
- **MAY** — allowed

The current local plugin/theme implementation remains authoritative for version-dependent save/render behavior.

## GB-SOURCE-001 — Source precedence

MUST resolve technical conflicts in this order:

1. direct user instruction
2. specific project rule
3. current local plugin/theme implementation
4. reference validated against the current local version
5. matching family skill
6. Master Formula
7. other references
8. inference

The visual reference controls appearance. The technical hierarchy controls serialization.

## GB-SOURCE-002 — Reference boundaries

A technical reference SHOULD supply:

- block names
- hierarchy
- native classes
- save markup
- state/ARIA relationships
- version-dependent attributes

MUST NOT automatically copy:

- colors
- text
- URLs
- IDs
- fixed container widths
- breakpoints
- font families
- spacing
- media values
- placeholders
- local brand values

An unvalidated reference is evidence, not proof of current runtime correctness.

## GB-CONT-001 — Full-width section

New full-width sections MUST use the equivalent of:

```css
width: 100%;
max-width: 100%;
box-sizing: border-box;
```

## GB-CONT-002 — Project inner container

The direct project inner container MUST use the project container source rather than duplicating a fixed site width:

```css
width: 100%;
max-width: var(--gb-container-width, 1280px);
margin-left: auto;
margin-right: auto;
```

MUST NOT copy fixed `1200px`/`1280px` site-width values from references when `--gb-container-width` is available.

## GB-SERIAL-001 — Identity invariant

MUST maintain:

```text
uniqueId in JSON
= native unique class identifier
= ID represented by the block CSS selector
```

MUST NOT introduce duplicate `uniqueId`.

## GB-SERIAL-002 — Style invariant

`styles` and `css` MUST express the same visual behavior, including responsive states.

## GB-SERIAL-003 — Markup invariant

MUST maintain:

```text
tagName
= saved opening tag
= saved closing tag
```

and:

```text
htmlAttributes
= saved HTML attributes
```

## GB-SERIAL-004 — Gutenberg structure

Every block opening MUST have the correct closing comment unless the block is legitimately self-closing.

JSON MUST be parseable.

MUST NOT introduce damaged Unicode escapes or damaged Gutenberg comment prefixes.

## GB-NATIVE-001 — Native blocks first

SHOULD prefer:

```text
generateblocks/element
generateblocks/text
generateblocks/media
generateblocks/shape
generateblocks/button
generateblocks/query
generateblocks/looper
generateblocks/loop-item
```

MUST NOT use Raw HTML or custom JavaScript as a substitute for an available native GenerateBlocks/Pro feature.

## GB-BADGE-001 — Single badge

A simple badge / eyebrow / pill label MUST use:

```text
generateblocks/text
tagName: span
```

MUST NOT use:

```text
generateblocks/element
tagName: span
with InnerBlocks
```

## GB-TYPE-001 — Theme typography

Font family SHOULD inherit from the theme.

SHOULD use documented `fs-h1` … `fs-h6` and `fs-p` classes/variables when appropriate.

Semantic heading level MUST follow content hierarchy rather than visual size.

A local font-size cap MAY be used for a genuinely constrained component, but MUST NOT hide a wrong container width or unsuitable content length.

## GB-RESP-001 — Responsive states

Default project states:

```text
Desktop: base
Tablet:  max-width:1024px
Mobile:  max-width:767px
```

MUST keep breakpoint behavior synchronized between `styles` and `css`.

MUST NOT mix 767px and 768px arbitrarily inside the same block family.

## GB-LAYOUT-001 — Robust grid/flex sizing

SHOULD use:

```text
minmax(0,1fr)
min-width:0
```

where necessary to prevent content-driven overflow.

Desktop-only fixed heights/offsets MUST reset on smaller viewports unless the visual reference requires them.

## GB-LAYOUT-002 — No scroll-as-repair

Ordinary cards/panels MUST NOT use internal `overflow-y:auto` or `overflow-y:scroll` merely to fit content into a screenshot-sized box.

Visible content MUST NOT be clipped as a geometry repair.

## GB-LAYOUT-003 — Irregular layouts

An asymmetric/mosaic desktop reference SHOULD preserve independent proportions and intentional offsets rather than being normalized into a generic equal-height grid.

Tablet/mobile MUST return to robust flow and semantically sensible reading order unless the visual reference states otherwise.

## GB-GEOM-001 — Local geometry

Internal shapes and component geometry SHOULD use a local `position:relative` parent plus local percentages/sizes.

Viewport units MAY be used for intentionally viewport-wide effects, but SHOULD NOT drive internal geometry when doing so harms editor/frontend parity.

## GB-CTA-001 — CTA groups

Small CTA groups SHOULD use Flex + Gap:

```css
display: flex;
flex-wrap: wrap;
align-items: center;
justify-content: flex-start;
gap: 1rem;
width: fit-content;
max-width: 100%;
```

Buttons SHOULD remain intrinsic width unless the visual reference requires another layout.

## GB-LINK-001 — Real interaction

Interactive actions MUST be real links/buttons.

Final code MUST NOT use `href="#"`.

Unknown required URLs MAY use a clearly identified portable placeholder such as:

```text
https://example.com/ziel/
```

and the completion report must list it for replacement.

## GB-LINK-002 — Full-card link

If a card has exactly one target, the outer card MAY be a link.

MUST NOT nest other links/buttons inside an interactive outer card.

With multiple independent actions, the outer card MUST remain non-interactive.

## GB-MEDIA-001 — Media IDs and URLs

MUST NOT invent WordPress media/attachment IDs.

Content images SHOULD have meaningful alt text and appropriate responsive sizing.

Decorative images MUST use empty alt text.

MUST NOT copy localhost/final foreign upload paths as portable project media without explicit intent.

## GB-SHAPE-001 — Decorative elements

Decorative shapes MAY use `generateblocks/shape` or local pseudo-elements.

Decorative elements SHOULD use `pointer-events:none`.

Decorative SVGs SHOULD be hidden from assistive technology with appropriate attributes.

MUST NOT add external icon CDNs.

## GB-A11Y-001 — Native semantics

SHOULD prefer native semantic elements before ARIA:

```text
section
article
nav
header
footer
figure
a
button
h1-h6
p
```

MUST provide visible focus for interactive elements.

MUST NOT create nested interactive elements.

Pro component ARIA/state relationships MUST come from a trustworthy version-compatible structure.

## GB-PRO-001 — Version-sensitive Pro components

Tabs, Accordion, Carousel, Navigation/Mega Menu, and other version-sensitive Pro structures MUST be derived from:

1. current local implementation when available,
2. a validated matching reference,
3. otherwise the strongest matching technical reference plus explicit unvalidated status.

MUST NOT invent unknown Pro wrappers, attributes, classes, states, IDs, ARIA relationships, or save markup.

MUST NOT add a parallel custom JavaScript initializer for native Pro functionality.

## GB-QUERY-001 — Dynamic content

Query/Looper parameters MUST match the task.

MUST NOT copy query values simply because they exist in a reference.

Loop items representing posts SHOULD use semantic `article` where appropriate.

## GB-TABLE-001 — Responsive tables

MUST preserve tabular meaning.

SHOULD NOT default to horizontal-scroll repair when a stable desktop/mobile alternative is appropriate.

Desktop table + mobile stacked/card rendering MAY be used when both present the same data.

## GB-FORM-001 — Forms

MUST NOT invent form IDs.

Contact Form 7 IDs must come from the actual installation or explicit user input.

Visual tests MUST NOT submit forms.

## GB-SCHEMA-001 — Structured data

Schema MUST only be added when the real content supports it.

MUST NOT fabricate Product/Offer/Review values.

## GB-PORT-001 — Portability

Final block code MUST NOT depend exclusively on:

- post-specific generated CSS outside the serialization
- DOM repair scripts
- localhost paths
- invented IDs
- hidden global hooks
- external frameworks/fonts/icon CDNs/tracking

Block-specific geometry and responsive rules SHOULD live with the serialized block.

## GB-EDIT-001 — Existing code

When modifying valid existing GenerateBlocks code:

- SHOULD preserve IDs
- SHOULD preserve content not requested for change
- SHOULD preserve valid hierarchy
- SHOULD make the smallest safe change

MUST NOT globally replace IDs without checking every dependent selector/attribute.

## GB-UNKNOWN-001 — Unknown content

MUST NOT invent unreadable screenshot text or hidden content for tabs, accordion items, slides, or other states.

Use clearly labeled neutral placeholders only when necessary.

Small visual uncertainty SHOULD be resolved with a documented reasonable assumption.

Ask only when missing information materially changes block type, interaction model, data source, Pro structure, save serialization, or a required real ID.

## GB-VALID-001 — Honest validation

Only actually executed checks may be reported as executed.

Report separately:

```text
static
project-source based
runtime executed
open
```

WordPress/Gutenberg/browser/accessibility checks MUST NOT be claimed without execution.

## GB-EDITTARGET-001 — Allowed edit targets

MUST NOT modify:

- GenerateBlocks Core
- GenerateBlocks Pro
- GeneratePress parent theme
- WordPress core
- unrelated third-party plugins

Project-specific theme changes belong in the GeneratePress Child theme.
