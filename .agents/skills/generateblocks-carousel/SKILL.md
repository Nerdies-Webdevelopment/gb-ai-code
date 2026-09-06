---
name: generateblocks-carousel
description: Build or repair GenerateBlocks Pro carousels using the supplied carousel reference. Use for sliders, carousel items, pagination/controls, and responsive slide geometry.
---

# Carousel

## Required project sources

Read:

- `PROJECT-CONTEXT.md`
- `PROJECT-RULES.md`
- `GenerateBlocks-Master-Formula-v2.md`
- `EXAMPLE-INDEX.md`

Primary reference:

```text
references/carousel/carousel03.html
```

Supplementary reference:

```text
references/query/query-loop01.html when the carousel is dynamic/query-driven
```

Do not load unrelated references.

## Structural orientation

```text
carousel
├── carousel-items
│   └── carousel-item
├── optional carousel-pagination
└── optional carousel-controls
```

This tree is orientation only. Exact version-dependent attributes/classes/save markup must come from the current local implementation or the strongest compatible reference.

## Family rules

- Use the reference for Pro hierarchy and saved state relationships.
- Use the query-loop skill in addition when content is dynamic.
- Do not invent slides that are not visible or supplied.
- Do not add custom JS initialization for native carousel behavior.

## Universal checks

- Apply `GB-SERIAL-*`, `GB-RESP-001`, `GB-A11Y-001`, and `GB-VALID-001`.
- Normalize project container width to the current theme contract.
- Keep `styles` and `css` synchronized.
- Preserve semantic responsive reading order.
- Do not invent IDs, URLs, hidden content, or Pro serialization.
- Run `python tools/validate_gb_block.py` on created/changed HTML when applicable.
