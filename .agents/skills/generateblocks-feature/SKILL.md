---
name: generateblocks-feature
description: Build GenerateBlocks feature sections and decorative panels. Use for feature panels, gradients, GenerateBlocks shapes, cards, and responsive panel geometry.
---

# Feature

## Required project sources

Read:

- `PROJECT-CONTEXT.md`
- `PROJECT-RULES.md`
- `GenerateBlocks-Master-Formula-v2.md`
- `EXAMPLE-INDEX.md`

Primary reference:

```text
references/feature/feature01.html
```

Supplementary reference:

```text
none
```

Do not load unrelated references.

## Structural orientation

```text
section
└── project inner container
    └── feature panel
        ├── content
        ├── cards / CTAs
        └── optional shape
```

This tree is orientation only. Exact version-dependent attributes/classes/save markup must come from the current local implementation or the strongest compatible reference.

## Family rules

- Use the reference for panel/shape technique, not brand styling.
- Normalize fixed heights when content or responsive flow requires it.
- Replace final `href="#"` patterns; historical reference warnings are not project defaults.

## Universal checks

- Apply `GB-SERIAL-*`, `GB-RESP-001`, `GB-A11Y-001`, and `GB-VALID-001`.
- Normalize project container width to the current theme contract.
- Keep `styles` and `css` synchronized.
- Preserve semantic responsive reading order.
- Do not invent IDs, URLs, hidden content, or Pro serialization.
- Run `python tools/validate_gb_block.py` on created/changed HTML when applicable.
