---
name: generateblocks-footer
description: Build or review GenerateBlocks footer compositions and local link hover/focus effects. Use for footer grids, contact/legal links, hover underlines, and accessible focus styling.
---

# Footer

## Required project sources

Read:

- `PROJECT-CONTEXT.md`
- `PROJECT-RULES.md`
- `GenerateBlocks-Master-Formula-v2.md`
- `EXAMPLE-INDEX.md`

Primary reference:

```text
references/footer/instantvolt-footer-hover01.html
```

Supplementary reference:

```text
none
```

Do not load unrelated references.

## Structural orientation

```text
footer/div wrapper
└── project inner container
    └── footer grid
        ├── brand/contact
        ├── link groups
        └── legal/meta
```

This tree is orientation only. Exact version-dependent attributes/classes/save markup must come from the current local implementation or the strongest compatible reference.

## Family rules

- Use hover/focus technique without copying brand data or font family.
- Do not copy real-looking phone/email/media IDs/URLs unless the task explicitly owns those values.
- Use current project container contract for new work.
- Preserve visible focus.

## Universal checks

- Apply `GB-SERIAL-*`, `GB-RESP-001`, `GB-A11Y-001`, and `GB-VALID-001`.
- Normalize project container width to the current theme contract.
- Keep `styles` and `css` synchronized.
- Preserve semantic responsive reading order.
- Do not invent IDs, URLs, hidden content, or Pro serialization.
- Run `python tools/validate_gb_block.py` on created/changed HTML when applicable.
