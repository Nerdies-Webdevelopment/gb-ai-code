# GenerateBlocks Codex v3.1.2 — four correctness fixes

Date: 2026-09-06. Child Theme: 0.4.

- Fixed typography precedence: semantic defaults and size utilities now use
  `body :where(...)` at specificity (0,0,1), with all utilities after the defaults.
  Native GenerateBlocks unique classes retain higher priority in either order.
- Block comment scanning now reports malformed/truncated comments and rejects
  non-object JSON attributes instead of silently skipping them.
- Added saved-HTML closing-tag checks and native Core class checks. Unstyled
  blocks may legitimately omit a unique class, as confirmed in installed
  GenerateBlocks 2.4.1 Text save logic. Pro class names are not inferred.
- Added comparison of structured styles against CSS declarations in matching
  selectors, pseudo states and responsive contexts. Common margin/padding/border
  shorthands and harmless minification are normalized. Unsupported comparisons
  produce warnings; strict mode treats warnings as failure.
- Manifest validation now reports malformed root/entry/field types and invalid
  reference paths as errors instead of raising AttributeError/TypeError.
- Added regression tests and an optional isolated Chromium typography check.
- Rebuilt `dist/generatepress-child-v0.4.zip`; a test checks byte-for-byte parity
  with the four source theme files. The v0.3 archive remains historical.

## Verification

The reference library retains its original content and validation status.
Static validation finds 0 errors and the same 24 existing warnings across
15 references. Chromium checks typography at 1440, 768 and 390px, including
block CSS loaded before and after the theme stylesheet.

No Gutenberg save/reopen or full site/editor parity validation is implied.

## Commands

```powershell
python tools/validate_all.py --installed
node tools/check_typography.cjs
python tools/sync_package.py --apply
```

The Node check requires Playwright and Chromium. An existing Chrome executable
can be selected with the `PLAYWRIGHT_CHROMIUM_EXECUTABLE` environment variable.
The Python suite remains dependency-free.
