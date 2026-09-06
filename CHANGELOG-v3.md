# CHANGELOG — Codex v3

## Child Theme integration

- Added the actual corrected GeneratePress Child Theme source under
  `child-theme/generatepress_child/`.
- Updated Child Theme version from 0.2 to 0.3.
- Replaced high-specificity typography utilities such as `body .fs-p` with
  low-specificity `:where(.fs-p)` equivalents.
- Kept semantic `body h1` ... `body h6` / `body p` defaults.
- Standardized PHP function prefixes to `gpc_`.
- Internationalized the GenerateBlocks template column title.
- Added explicit lazy/async image attributes in the admin thumbnail output.
- Added nested Child Theme `AGENTS.md`.
- Added static Child Theme validator and unit tests.
- Added installable `dist/generatepress-child-v0.3.zip`.
- Preserved the user-supplied v0.2 ZIP under `docs/source/` for provenance.

## Project-context accuracy

`PROJECT-CONTEXT.md` now distinguishes:

```text
Child Theme source inspected: yes
Child Theme PHP syntax checked: yes/no based on executed validator
WordPress runtime verified: no
Gutenberg verified: no
GenerateBlocks admin hook runtime verified: no
```

This avoids calling static source inspection a runtime test.

## Codex structure

The v2 Codex architecture remains:

- concise root `AGENTS.md`
- progressive-disclosure `.agents/skills/`
- family-organized references
- capability matrix
- machine-readable reference manifest
- deterministic static validation

v3 adds a nested theme-specific `AGENTS.md` so Codex gets closer-scope
instructions when modifying the Child Theme.
