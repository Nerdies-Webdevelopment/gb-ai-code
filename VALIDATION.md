# VALIDATION.md

## Validation levels

### 1. Static

Can be performed without WordPress runtime:

- block JSON parses
- Gutenberg comments are balanced
- `uniqueId` values are unique
- obvious ID/CSS inconsistencies
- `tagName` vs saved tag when determinable
- hard badge rule
- placeholder/local URL warnings
- fixed legacy project-width warnings
- suspicious internal scrolling
- common reference hygiene

Command:

```bash
python tools/validate_gb_block.py path/to/file.html
```

### 2. Project-source based

Requires current repository/theme/plugin source inspection:

- actual installed versions
- current Child Theme tokens
- current editor-style integration
- version-dependent registered attributes
- exact Pro save/render implementation

Do not call this runtime testing.

### 3. WordPress runtime

When WordPress is available:

- run `parse_blocks()`
- insert/open in Gutenberg
- confirm no invalid/recovery warning
- save
- reload
- compare serialized `post_content`

### 4. Browser/frontend

When browser tooling is available:

Check relevant widths, including the documented project test widths.

Verify:

- no page-level horizontal overflow
- no clipped visible content
- no ordinary card scroll containers
- focus-visible states
- interaction behavior
- responsive reading order
- component geometry
- editor/frontend parity at equal effective component width

### 5. Accessibility

Static accessibility review is not the same as runtime accessibility testing.

Check, where tooling exists:

- keyboard operation
- focus order
- accessible names
- semantics
- ARIA relationships
- contrast
- reduced motion behavior if animations are used

## Reporting format

Always distinguish:

```text
Executed:
- ...

Static:
- ...

Project-source based:
- ...

Open:
- ...
```

Never collapse an unexecuted check into “passed”.

## Reference-library validation

```bash
python tools/validate_reference_library.py
```

This command checks manifest/file consistency and runs the static validator across all references.

Warnings are expected in legacy references because the project explicitly documents older values such as fixed widths, placeholders, `localhost`, or old breakpoints.

A warning is not automatic proof that the historical reference is invalid.

## Strict mode

For newly generated block files, use:

```bash
python tools/validate_gb_block.py --strict path/to/new-block.html
```

Strict mode treats warnings as a non-zero result.

Do not use strict-mode cleanliness as a reason to rewrite historical technical references unless reference maintenance is the task.


## Child Theme validation

The corrected Child Theme is packaged at:

```text
wp-content/themes/generatepress_child/
```

Run:

```bash
python tools/validate_child_theme.py
```

The static validator checks:

- `Template: generatepress`
- required GenerateBlocks project tokens
- no reintroduction of high-specificity `body .fs-*` / `body .gb-button`
- editor-style registration
- no `@import` parent stylesheet
- suspicious duplicate frontend enqueue
- PHP syntax with `php -l` when PHP CLI is available

A successful static validation does **not** prove:

- the theme activates correctly on the live WordPress site
- Gutenberg/frontend parity
- the `gblocks_templates` admin hooks still match the installed plugin
- GenerateBlocks Pro runtime behavior

Those remain runtime checks.

## Complete package check

```bash
python tools/validate_all.py --installed
```

Runs all validator tests, the Child Theme validator, the reference validator,
and the installed-source version check. Runs all groups even if one fails and
returns a nonzero exit code if any group fails. Works independently of the
calling directory. Omit `--installed` for a standalone package without plugins.

`python tools/check_environment.py` compares the installed source headers with
`PROJECT-CONTEXT.md` without loading WordPress or accessing the database.
A mismatch requires review; it does not automatically update the snapshot.
Legacy reference warnings remain visible and are not promoted to runtime passes.

## Checks added in v3.1.2

`validate_gb_block.py` now detects malformed/truncated Gutenberg comments,
non-object JSON attributes, mismatched saved HTML closing tags and wrong
native Core classes. Classless unstyled blocks remain allowed. Pro wrappers
are not guessed from block names.

Structured styles are compared against CSS declarations for the same native
selector and media/supports/container/layer context, including descendant and
pseudo selectors. Common box shorthands, decimal minification and shortened
hex colors are normalized. Unsupported syntax/shorthand comparisons produce
warnings, which fail `--strict`; they are not silently declared equivalent.
Since v3.1.3, comparison also flags CSS-only declarations per selector and
responsive context as review warnings (rejected by --strict). Basic named/hex/RGB
colors and zero lengths are compared conservatively. This does not model the
browser cascade, inherited styles, CSS variables or mathematical equivalence. It does not replace Gutenberg/browser validation.

Manifest roots/entries must be objects, IDs and paths non-empty strings,
and reference files readable HTML within `references/`. Invalid input reports
an error with a nonzero exit code rather than crashing.

## Isolated typography browser check

```powershell
node tools/check_typography.cjs
```

Requires an available `playwright` Node package and Chromium. If necessary set
`PLAYWRIGHT_CHROMIUM_EXECUTABLE` to an existing Chrome executable. This optional
check is run explicitly; it is not part of the dependency-free Python suite.
It checks heading/paragraph/span size utilities and native class overrides at
1440, 768 and 390px. This is an isolated browser test, not a live WordPress test.

The Child Theme tests also verify that the current v0.4 ZIP matches its source.

## Plugin source inventory

`python tools/inspect_plugin_features.py --root <wordpress-root>` reads local
metadata only; `--json` outputs a portable report without installation paths.
Missing/malformed source returns exit code 1. The suite includes scanner tests;
a real installation scan remains an explicit separate command. The snapshot is
not proof of activation, complete registry coverage or save-markup correctness.
New feature skills have no runtime-validated HTML examples. Check dependent
records, save/render implementations and Gutenberg/browser behavior for outputs.
