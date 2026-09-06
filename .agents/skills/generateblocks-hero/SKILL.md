---
name: generateblocks-hero
description: Build complex GenerateBlocks hero sections from visual references. Use for full-width heroes, split layouts, decorative pseudo-elements, local shapes, and responsive hero geometry.
---

# Hero

## Required project sources

Read:

- `PROJECT-CONTEXT.md`
- `PROJECT-RULES.md`
- `GenerateBlocks-Master-Formula-v2.md`
- `EXAMPLE-INDEX.md`

Primary reference:

```text
references/hero/hero03.html
```

Supplementary reference:

```text
references/content/contentblock04.html or references/feature/feature01.html only for clearly bounded techniques
```

Do not load unrelated references.

## Structural orientation

```text
full-width section
└── project inner container
    └── hero layout
        ├── content
        └── visual / shapes / cards
```

This tree is orientation only. Exact version-dependent attributes/classes/save markup must come from the current local implementation or the strongest compatible reference.

## Family rules

- Derive geometry from the screenshot, not the example.
- Keep internal shapes local-container-relative where possible.
- Reset desktop-only min-heights/offsets on smaller viewports unless visually required.
- Use project typography rather than reference-local font assumptions.

## Universal checks

- Apply `GB-SERIAL-*`, `GB-RESP-001`, `GB-A11Y-001`, and `GB-VALID-001`.
- Normalize project container width to the current theme contract.
- Keep `styles` and `css` synchronized.
- Preserve semantic responsive reading order.
- Do not invent IDs, URLs, hidden content, or Pro serialization.
- Run `python tools/validate_gb_block.py` on created/changed HTML when applicable.
