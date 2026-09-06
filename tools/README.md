# Static tooling

## `validate_gb_block.py`

Zero-dependency static validator.

Checks include:

- Gutenberg block comment balance
- JSON parsing
- duplicate `uniqueId`
- common ID/CSS consistency hints
- `tagName` vs saved tag where determinable
- hard badge rule
- `href="#"`
- localhost URLs
- fixed legacy width warnings
- suspicious internal scrolling
- mixed 767/768 breakpoint warning
- selected external CDN warnings

This is not a WordPress parser and does not prove Gutenberg runtime compatibility.

Usage:

```bash
python tools/validate_gb_block.py path/to/file.html
python tools/validate_gb_block.py --strict path/to/new-file.html
```

## `validate_reference_library.py`

Checks the machine manifest, file presence, duplicate entries, unlisted reference HTML, and runs the static validator on every reference.

```bash
python tools/validate_reference_library.py
```

## Tests

```bash
python -m unittest discover -s tools -t .
```

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
