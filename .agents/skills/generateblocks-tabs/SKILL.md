---
name: generateblocks-tabs
description: Build or repair GenerateBlocks Pro tabs using the supplied tabs reference. Use for horizontal or vertical tab interfaces, tab ARIA/state relationships, and screenshot-to-tabs reconstruction.
---

# Tabs

## Required project sources

Read:

- `PROJECT-CONTEXT.md`
- `PROJECT-RULES.md`
- `GenerateBlocks-Master-Formula-v2.md`
- `EXAMPLE-INDEX.md`

Primary reference:

```text
references/tabs/vertical-tabs01.html
```

Supplementary reference:

```text
none
```

Do not load unrelated references.

## Structural orientation

```text
tabs
├── tabs-menu
│   └── tab-menu-item
└── tab-items
    └── tab-item
```

This tree is orientation only. Exact version-dependent attributes/classes/save markup must come from the current local implementation or the strongest compatible reference.

## Family rules

- Use the reference for parent/child hierarchy, native classes, state/open attributes, IDs, ARIA relationships, and save markup.
- Do not inherit the reference's vertical geometry when the screenshot requires horizontal tabs.
- Do not invent content for hidden tab states; use real supplied content or clearly marked neutral placeholders.
- Treat exact Pro serialization as version-sensitive.

## Universal checks

- Apply `GB-SERIAL-*`, `GB-RESP-001`, `GB-A11Y-001`, and `GB-VALID-001`.
- Normalize project container width to the current theme contract.
- Keep `styles` and `css` synchronized.
- Preserve semantic responsive reading order.
- Do not invent IDs, URLs, hidden content, or Pro serialization.
- Run `python tools/validate_gb_block.py` on created/changed HTML when applicable.
