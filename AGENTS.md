# AGENTS.md — GenerateBlocks / Codex

## Mission

Build, repair, and review portable GenerateBlocks/Gutenberg `post_content` for this repository.

A screenshot or mockup is a **visual geometry contract**. It determines layout, proportions, spacing, colors, visible typography, shapes, and visible states. It does **not** determine GenerateBlocks serialization.

Technical structure comes from the current project, local plugin/theme implementation, and the closest family reference.

The goal is not a similar HTML prototype. The goal is valid, editor-compatible GenerateBlocks/Gutenberg code that matches the project and installed versions.

## Instruction strategy

Keep this file short. Do not copy all family rules into `AGENTS.md`.

For GenerateBlocks work, load detail only when needed:

1. `PROJECT-CONTEXT.md` — current documented project facts.
2. `PROJECT-RULES.md` — binding project rules.
3. `GenerateBlocks-Master-Formula-v2.md` — general construction and acceptance formula.
4. `EXAMPLE-INDEX.md` — route to the closest technical reference.
5. `CAPABILITIES.md` — whether a family is safely supported.
6. A matching skill in `.agents/skills/`.
7. Only the selected reference file(s) under `references/`.

Do not load every reference unless the task is explicitly about reference-library maintenance.

## Source precedence

When technical sources conflict:

1. direct user instruction
2. specific project rule in this repository
3. currently installed local GenerateBlocks / GenerateBlocks Pro / GeneratePress implementation
4. a reference explicitly validated against that local version
5. the matching family skill
6. `GenerateBlocks-Master-Formula-v2.md`
7. other relevant references
8. inference

A more specific rule may override a general one.

The visual reference remains authoritative for appearance. The technical precedence above determines how that appearance is serialized.

## Task routing

### Visual-to-Code

Use `$generateblocks-visual-to-code`.

Then route to the matching family skill when applicable:

- Tabs → `$generateblocks-tabs`
- Accordion / FAQ → `$generateblocks-accordion`
- Carousel → `$generateblocks-carousel`
- Query / Looper → `$generateblocks-query-loop`
- Pricing / legacy GB button → `$generateblocks-pricing-button`
- Table → `$generateblocks-table`
- Hero → `$generateblocks-hero`
- Content section → `$generateblocks-content-section`
- Feature section → `$generateblocks-feature`
- CTA → `$generateblocks-cta`
- Process / steps → `$generateblocks-process`
- Contact / form surroundings → `$generateblocks-contact`
- Footer / hover-focus patterns → `$generateblocks-footer`

If no visual reference is available for an explicitly visual conversion task, ask exactly:

> Welches Bild soll ich in GenerateBlocks-Code umwandeln?  
> Which image should I convert into GenerateBlocks code?

Do not invent visual geometry before the image is supplied.

### Additional plugin features

For native features beyond the HTML references, read only the relevant section
of `PLUGIN-FEATURES.md` and use the focused skill:

- Navigation / Mega Menu → `$generateblocks-navigation`
- Native Pro Forms → `$generateblocks-forms`
- Overlays / display conditions → `$generateblocks-display`
- Global classes / patterns / assets → `$generateblocks-global-styles`
- GP Premium Elements / theme modules → `$generatepress-premium`
- Dynamic tags / meta repeaters / pagination → `$generateblocks-query-loop`

These are source workflows, not runtime-validated templates. A read-only inventory
is available via `python tools/inspect_plugin_features.py --root <wordpress-root>`.
Source presence/defaults do not prove activation.

### Existing block repair

Preserve valid IDs, content, hierarchy, and project conventions unless the requested fix requires a change. Prefer a focused repair over a rewrite.

### Reference-library maintenance

Read `references/REFERENCE-MANIFEST.json`, `EXAMPLE-INDEX.md`, `VALIDATION.md`, and the affected family skill. Do not promote a reference to `validated` without evidence from the required runtime checks.

## Non-negotiable GenerateBlocks invariants

For every changed block, keep these relationships consistent:

```text
uniqueId in block JSON
= unique native class identifier
= identifier used by the block CSS selector

styles
= same visual statement as css

tagName
= saved opening tag
= saved closing tag

htmlAttributes
= attributes present in saved markup
```

Also require:

- parseable block JSON
- complete Gutenberg open/close comments
- no duplicate `uniqueId`
- synchronized responsive states in `styles` and `css`
- no invented version-dependent Pro attributes, wrappers, classes, state attributes, ARIA relationships, or save markup

## Hard project constraints

- Prefer native GenerateBlocks blocks.
- Do not replace a native GenerateBlocks/Pro feature with Raw HTML or custom JavaScript.
- Do not modify GenerateBlocks, GenerateBlocks Pro, GeneratePress parent theme, WordPress core, or unrelated third-party plugin files.
- Project theme code belongs in the packaged GeneratePress Child Theme at `wp-content/themes/generatepress_child/`.
- Never invent WordPress post IDs, page IDs, attachment/media IDs, form IDs, company data, phone numbers, email addresses, or final production URLs.
- `href="#"` is not a final target. Use a clearly marked portable placeholder such as `https://example.com/ziel/` only when a URL is required but unknown.
- Do not add external frameworks, external fonts, icon CDNs, or tracking scripts.
- Do not repair ordinary cards or panels with internal vertical scrolling.
- Do not clip visible content to force screenshot height.
- Do not claim browser, Gutenberg, WordPress, parser, responsive, accessibility, or frontend testing unless it was actually executed.

## Badge rule

A simple badge / eyebrow / pill label is a single text block:

```text
generateblocks/text
tagName: span
```

Do **not** use:

```text
generateblocks/element
tagName: span
with InnerBlocks
```

This is a hard project rule.

## Project layout contract

Read current values from `PROJECT-CONTEXT.md`.

For the documented current project:

```css
/* full-width section */
width: 100%;
max-width: 100%;
box-sizing: border-box;

/* direct inner container */
width: 100%;
max-width: var(--gb-container-width, 1280px);
margin-left: auto;
margin-right: auto;
```

Do not copy fixed `1200px` or `1280px` inner-container values from older references when `--gb-container-width` is available.

Default documented responsive states:

```text
Desktop: base values
Tablet:  @media (max-width:1024px)
Mobile:  @media (max-width:767px)
```

`768px` is an important test width, not automatically the mobile CSS breakpoint.

## Geometry and content-fit

Prefer robust layout primitives:

```text
minmax(0,1fr)
min-width:0
```

Reset desktop-only fixed heights and offsets on smaller viewports unless the visual contract explicitly requires them there.

For irregular or mosaic desktop layouts, preserve independent proportions and offsets instead of forcing an equal-height grid. Tablet/mobile should return to semantically sensible reading order and robust auto-height flow.

Internal shapes and local component geometry should normally be positioned relative to a local `position:relative` parent. Avoid viewport units for internal geometry when local percentages/sizes can preserve editor/frontend parity.

## Accessibility

Prefer native semantics before ARIA.

Require where applicable:

- meaningful heading hierarchy
- real links/buttons for interaction
- visible `:focus-visible`
- meaningful alt text for content images
- `alt=""` for decorative images
- no nested interactive elements
- accessible names for icon-only controls
- correct unique ARIA/state relationships for Pro components
- semantic reading order on responsive layouts

## Reference discipline

A reference primarily supplies technical structure:

- block names
- parent/child hierarchy
- native classes
- save markup
- state/ARIA relationships
- version-dependent attributes

Do not automatically copy:

- colors
- copy
- URLs
- IDs
- container widths
- breakpoints
- font families
- spacing
- media values
- placeholders
- local brand values

If a reference is not explicitly marked `validated`, treat it as a strong technical reference, not proof of current runtime correctness.

## Local installation preflight

At the start of version-sensitive block work run `python tools/check_environment.py`.
A version mismatch requires source inspection and review of the affected family;
updating the version text alone is not compatibility validation.
For routine assumptions, continue using the documented project defaults.

## Validation commands

For changed HTML reference/block files, run:

```bash
python tools/validate_gb_block.py path/to/file.html
```

For the reference library, run:

```bash
python tools/validate_reference_library.py
```

For Child Theme changes, run:

```bash
python tools/validate_child_theme.py
```

For the full local check suite (including validator tests):

```bash
python tools/validate_all.py --installed
```

Omit `--installed` only when checking a standalone package without plugins.

Warnings from old references may be expected. Errors are not.

If WordPress access exists, additionally use `parse_blocks()` and reopen/save in Gutenberg without recovery warnings.

If browser access exists, additionally verify the visual contract at relevant widths and compare editor/frontend at the same effective component width.

See `VALIDATION.md`.

## Change discipline

Before editing:

- inspect `git status` if Git is available
- when theme tokens/editor integration are relevant, inspect `wp-content/themes/generatepress_child/`
- do not overwrite unrelated uncommitted changes
- identify the smallest relevant file set
- inspect the current local plugin/theme implementation if serialization is version-dependent

After editing:

- review the diff
- run applicable validation
- report only tests actually run
- list unresolved placeholders/runtime checks

## Completion report

Separate:

- **Executed:** checks actually run
- **Static:** checks performed without runtime
- **Project-source based:** conclusions derived from repository facts/references
- **Open:** Gutenberg/browser/runtime checks not available

For Visual-to-Code output, unless the user requests a different format, provide:

1. short reference analysis
2. actual reference basis used
3. essential technical decisions
4. assumptions/placeholders
5. compact block tree
6. complete GenerateBlocks `post_content` with no omissions
7. validation status
8. values still requiring replacement

## Code Review Rules

Flag as blocking issues:

- invented Pro serialization
- duplicate `uniqueId`
- inconsistent `styles` vs `css`
- inconsistent `tagName` or saved attributes
- forbidden badge wrapper pattern
- final `href="#"`
- invented WordPress/form/media IDs
- nested interactive controls
- ordinary card content repaired by internal vertical scroll
- fixed project inner width copied from a reference instead of the theme variable
- claimed tests that were not executed
- edits to plugin core or the GeneratePress parent theme

## Portable package and local copies

The package root is the directory containing this AGENTS.md, regardless of its
name, operating system or location. Never infer a different machine's paths.
Use `python tools/setup_project.py` to check a WordPress installation.

If `.package-sync.local.json` exists, it describes this machine's authorized
source/destination copy relationship. Maintain both copies after package changes:
validate the source, rebuild the release, run `python tools/sync_package.py --apply`,
compare again, and validate the destination. Otherwise require an explicit sync
destination; normal package use does not require synchronization.

`TREE.txt` is the package inventory. Never package WordPress core, plugins, uploads,
database data, local configuration or secrets. Do not overwrite independent edits.
Do not publish local sync files or `.local/`. See PACKAGE-SYNC.md and README.md.
