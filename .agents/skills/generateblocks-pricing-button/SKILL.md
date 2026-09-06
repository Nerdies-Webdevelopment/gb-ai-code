---
name: generateblocks-pricing-button
description: Build pricing/card sections or use the supplied classic GenerateBlocks button serialization. Use for pricing tables, package cards, and simple CTA buttons when the local version supports the reference pattern.
---

# Pricing / Button

## Required project sources

Read:

- `PROJECT-CONTEXT.md`
- `PROJECT-RULES.md`
- `GenerateBlocks-Master-Formula-v2.md`
- `EXAMPLE-INDEX.md`

Primary reference:

```text
references/pricing/pricing01.html
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
    └── pricing/cards
        └── optional generateblocks/button
```

This tree is orientation only. Exact version-dependent attributes/classes/save markup must come from the current local implementation or the strongest compatible reference.

## Family rules

- The supplied reference demonstrates a classic GenerateBlocks button with `blockVersion:4`.
- Use it only when compatible with the actual installed version.
- Do not copy prices, products, colors, or example URLs.
- A simple text-like CTA may still be a semantic link if that is the intended element.

## Universal checks

- Apply `GB-SERIAL-*`, `GB-RESP-001`, `GB-A11Y-001`, and `GB-VALID-001`.
- Normalize project container width to the current theme contract.
- Keep `styles` and `css` synchronized.
- Preserve semantic responsive reading order.
- Do not invent IDs, URLs, hidden content, or Pro serialization.
- Run `python tools/validate_gb_block.py` on created/changed HTML when applicable.
