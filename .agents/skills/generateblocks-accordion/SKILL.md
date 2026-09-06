---
name: generateblocks-accordion
description: Build or repair GenerateBlocks Pro Accordion/FAQ structures. Use for FAQs, accordions, accordion-with-image sections, toggle/content relationships, and FAQ schema patterns.
---

# Accordion / FAQ

## Required project sources

Read:

- `PROJECT-CONTEXT.md`
- `PROJECT-RULES.md`
- `GenerateBlocks-Master-Formula-v2.md`
- `EXAMPLE-INDEX.md`

Primary reference:

```text
references/accordion/faq01.html
```

Supplementary reference:

```text
references/accordion/faq-accordion01.html for image + accordion composition
```

Do not load unrelated references.

## Structural orientation

```text
accordion
└── accordion-item
    ├── accordion-toggle
    │   └── optional accordion-toggle-icon
    └── accordion-content
```

This tree is orientation only. Exact version-dependent attributes/classes/save markup must come from the current local implementation or the strongest compatible reference.

## Family rules

- Use `faq01.html` as the primary hierarchy/save reference.
- Use `faq-accordion01.html` only when image + accordion composition is needed.
- FAQ schema is allowed only when the real content is actually FAQ content.
- Do not copy the supplementary reference's 768px breakpoint as a new project default.
- Do not invent answers for unseen accordion states.

## Universal checks

- Apply `GB-SERIAL-*`, `GB-RESP-001`, `GB-A11Y-001`, and `GB-VALID-001`.
- Normalize project container width to the current theme contract.
- Keep `styles` and `css` synchronized.
- Preserve semantic responsive reading order.
- Do not invent IDs, URLs, hidden content, or Pro serialization.
- Run `python tools/validate_gb_block.py` on created/changed HTML when applicable.
