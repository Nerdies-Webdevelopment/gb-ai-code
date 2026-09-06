# CHANGELOG — Codex v2

## Structural changes

- Reduced root `AGENTS.md` from an all-in-one handbook to an operational router.
- Moved reusable workflows into repository skills under `.agents/skills/`.
- Separated current project facts (`PROJECT-CONTEXT.md`) from binding rules (`PROJECT-RULES.md`).
- Reworked Master Formula as a general construction/acceptance document.
- Reorganized references by block family.
- Added machine-readable `references/REFERENCE-MANIFEST.json`.
- Added `CAPABILITIES.md` to prevent unsupported family hallucination.
- Added `VALIDATION.md`.
- Added zero-dependency static validator scripts and unit tests.
- Added `PLANS.md` for long multi-step maintenance/migrations.
- Preserved the supplied final Visual-to-Code prompt in `docs/source/`.

## Rule preservation

Preserved core source behavior:

- visual reference = geometry/design contract
- technical reference = serialization structure
- project rules = global/current implementation constraints
- local installed versions outrank documented snapshots
- do not invent Pro serialization
- do not copy example values as project defaults
- no invented IDs/content/runtime tests
- responsive/editor/frontend/accessibility/portability requirements
- simple badge uses `generateblocks/text` + `span`, not `generateblocks/element <span>` with InnerBlocks
- missing visual input question in German and English
