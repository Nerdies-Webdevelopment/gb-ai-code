---
name: generateblocks-table
description: Build responsive GenerateBlocks table-like structures using the supplied table reference. Use for comparisons, product matrices, desktop/mobile alternate layouts, and table accessibility review.
---

# Responsive Table

## Required project sources

Read:

- `PROJECT-CONTEXT.md`
- `PROJECT-RULES.md`
- `GenerateBlocks-Master-Formula-v2.md`
- `EXAMPLE-INDEX.md`

Primary reference:

```text
references/table/table01.html
```

Supplementary reference:

```text
none
```

Do not load unrelated references.

## Structural orientation

```text
section
└── inner container
    ├── intro
    └── table composition
        ├── desktop representation
        └── optional mobile stacked representation
```

This tree is orientation only. Exact version-dependent attributes/classes/save markup must come from the current local implementation or the strongest compatible reference.

## Family rules

- Preserve identical data meaning across desktop and mobile variants.
- Do not default to horizontal scroll as the only mobile repair.
- Use roles/schema only when semantically justified.
- Do not copy the reference's sample data.

## Universal checks

- Apply `GB-SERIAL-*`, `GB-RESP-001`, `GB-A11Y-001`, and `GB-VALID-001`.
- Normalize project container width to the current theme contract.
- Keep `styles` and `css` synchronized.
- Preserve semantic responsive reading order.
- Do not invent IDs, URLs, hidden content, or Pro serialization.
- Run `python tools/validate_gb_block.py` on created/changed HTML when applicable.
