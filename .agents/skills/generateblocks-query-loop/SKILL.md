---
name: generateblocks-query-loop
description: Build or repair GenerateBlocks Query/Looper structures, including post grids and query-driven carousels. Use when content is dynamic, post-based, paginated, or looped.
---

# Query / Looper

## Required project sources

Read:

- `PROJECT-CONTEXT.md`
- `PROJECT-RULES.md`
- `GenerateBlocks-Master-Formula-v2.md`
- `EXAMPLE-INDEX.md`

Primary reference:

```text
references/query/post-grid01.html for classic grids; references/query/query-loop01.html for dynamic carousel composition
```

Supplementary reference:

```text
matching carousel skill/reference when Pro carousel interaction is present
```

Do not load unrelated references.

## Structural orientation

```text
query
└── looper
    └── loop-item
        └── dynamic card content
+ optional pagination / no-results
+ optional Pro carousel composition
```

This tree is orientation only. Exact version-dependent attributes/classes/save markup must come from the current local implementation or the strongest compatible reference.

## Family rules

- Query parameters must come from the task, not from the reference.
- Use semantic `article` for post loop items where appropriate.
- Preserve dynamic placeholders only when they match the actual data model.
- Do not invent post IDs or data sources.

## Universal checks

- Apply `GB-SERIAL-*`, `GB-RESP-001`, `GB-A11Y-001`, and `GB-VALID-001`.
- Normalize project container width to the current theme contract.
- Keep `styles` and `css` synchronized.
- Preserve semantic responsive reading order.
- Do not invent IDs, URLs, hidden content, or Pro serialization.
- Run `python tools/validate_gb_block.py` on created/changed HTML when applicable.
