---
name: generateblocks-contact
description: Build GenerateBlocks contact/form-surrounding layouts. Use for two-column contact sections, content beside a form shortcode, and responsive form embedding surroundings.
---

# Contact

## Required project sources

Read:

- `PROJECT-CONTEXT.md`
- `PROJECT-RULES.md`
- `GenerateBlocks-Master-Formula-v2.md`
- `EXAMPLE-INDEX.md`

Primary reference:

```text
references/contact/contactblock13.html
```

Supplementary reference:

```text
none
```

Do not load unrelated references.

## Structural orientation

```text
section
└── inner layout
    ├── contact content
    └── form embedding area
```

This tree is orientation only. Exact version-dependent attributes/classes/save markup must come from the current local implementation or the strongest compatible reference.

## Family rules

- Treat the supplied file as a layout reference, not a source of form IDs.
- Never invent Contact Form 7 or other form IDs.
- Do not submit forms during visual checks.
- Normalize the old fixed 1200px layout to the current project container contract for new work.

## Universal checks

- Apply `GB-SERIAL-*`, `GB-RESP-001`, `GB-A11Y-001`, and `GB-VALID-001`.
- Normalize project container width to the current theme contract.
- Keep `styles` and `css` synchronized.
- Preserve semantic responsive reading order.
- Do not invent IDs, URLs, hidden content, or Pro serialization.
- Run `python tools/validate_gb_block.py` on created/changed HTML when applicable.

## Native Pro form option

For native fields/actions use `generateblocks-forms` and the Forms section of
`PLUGIN-FEATURES.md`. This skill handles the surrounding layout. Preserve an
existing shortcode when requested. Pro Forms require the feature and a real form
record; the contact reference does not require all projects to use a third-party
form plugin.
