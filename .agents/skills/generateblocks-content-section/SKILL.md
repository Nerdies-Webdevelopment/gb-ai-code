---
name: generateblocks-content-section
description: Build standard or decorative GenerateBlocks content sections. Use for text-led sections, gradient backgrounds, pseudo-elements, and constrained content containers.
---

# Content Section

## Required project sources

Read:

- `PROJECT-CONTEXT.md`
- `PROJECT-RULES.md`
- `GenerateBlocks-Master-Formula-v2.md`
- `EXAMPLE-INDEX.md`

Primary reference:

```text
references/content/contentblock04.html
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
    └── content group
```

This tree is orientation only. Exact version-dependent attributes/classes/save markup must come from the current local implementation or the strongest compatible reference.

## Family rules

- Use the reference for pseudo-element/editor-compatible decorative technique.
- Do not copy its colors, content, or fixed site width.
- Avoid extra wrappers without a separate visual/semantic responsibility.

## Universal checks

- Apply `GB-SERIAL-*`, `GB-RESP-001`, `GB-A11Y-001`, and `GB-VALID-001`.
- Normalize project container width to the current theme contract.
- Keep `styles` and `css` synchronized.
- Preserve semantic responsive reading order.
- Do not invent IDs, URLs, hidden content, or Pro serialization.
- Run `python tools/validate_gb_block.py` on created/changed HTML when applicable.
