---
name: generateblocks-process
description: Build GenerateBlocks process/steps sections. Use for numbered workflows, repeated process cards, responsive step grids, and ordered explanatory sections.
---

# Process

## Required project sources

Read:

- `PROJECT-CONTEXT.md`
- `PROJECT-RULES.md`
- `GenerateBlocks-Master-Formula-v2.md`
- `EXAMPLE-INDEX.md`

Primary reference:

```text
references/process/process01.html
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
    ├── intro
    └── repeated process cards / steps
```

This tree is orientation only. Exact version-dependent attributes/classes/save markup must come from the current local implementation or the strongest compatible reference.

## Family rules

- Preserve semantic step order on smaller viewports.
- Use robust grid tracks and auto-height content.
- Do not copy example text/colors.

## Universal checks

- Apply `GB-SERIAL-*`, `GB-RESP-001`, `GB-A11Y-001`, and `GB-VALID-001`.
- Normalize project container width to the current theme contract.
- Keep `styles` and `css` synchronized.
- Preserve semantic responsive reading order.
- Do not invent IDs, URLs, hidden content, or Pro serialization.
- Run `python tools/validate_gb_block.py` on created/changed HTML when applicable.
