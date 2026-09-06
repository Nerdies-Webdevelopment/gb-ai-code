---
name: generateblocks-cta
description: Build compact GenerateBlocks CTA sections. Use for call-to-action boxes, text plus button compositions, and responsive CTA alignment.
---

# CTA

## Required project sources

Read:

- `PROJECT-CONTEXT.md`
- `PROJECT-RULES.md`
- `GenerateBlocks-Master-Formula-v2.md`
- `EXAMPLE-INDEX.md`

Primary reference:

```text
references/cta/cta03.html
```

Supplementary reference:

```text
references/pricing/pricing01.html only when classic button serialization is needed
```

Do not load unrelated references.

## Structural orientation

```text
section
└── project inner container
    └── CTA box
        ├── content
        └── action
```

This tree is orientation only. Exact version-dependent attributes/classes/save markup must come from the current local implementation or the strongest compatible reference.

## Family rules

- Prefer Flex + Gap for small CTA groups.
- Keep button widths intrinsic unless the visual reference requires full width.
- Do not copy example colors/copy/URLs.

## Universal checks

- Apply `GB-SERIAL-*`, `GB-RESP-001`, `GB-A11Y-001`, and `GB-VALID-001`.
- Normalize project container width to the current theme contract.
- Keep `styles` and `css` synchronized.
- Preserve semantic responsive reading order.
- Do not invent IDs, URLs, hidden content, or Pro serialization.
- Run `python tools/validate_gb_block.py` on created/changed HTML when applicable.
