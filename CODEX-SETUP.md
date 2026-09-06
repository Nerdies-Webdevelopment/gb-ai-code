# CODEX-SETUP.md

## Verify instruction loading

From the repository root, start a fresh Codex session and ask it to summarize the active instructions.

A useful CLI check is:

```bash
codex "Summarize the current project instructions and list the GenerateBlocks skills you can use."
```

## Verify skills

The repository skills live under:

```text
.agents/skills/
```

Use `/skills` or skill mentions in Codex when available.

For a Visual-to-Code job, the main workflow skill is:

```text
$generateblocks-visual-to-code
```

## Recommended workflow for complex work

For a single section conversion, normal task execution is usually sufficient.

For larger tasks such as:

- plugin-version migration
- reference-library overhaul
- many-family refactor
- systematic runtime revalidation

use a plan first and keep the working plan in `PLANS.md`.

## Static tool checks

```bash
python tools/validate_all.py --installed
```

For a newly generated file:

```bash
python tools/validate_gb_block.py --strict path/to/file.html
```

## Runtime note

Static scripts cannot prove Gutenberg save compatibility or frontend interaction. Use actual WordPress/browser checks when those environments are available.

## Project directory

Open the actual WordPress root containing AGENTS.md, wp-admin and wp-content.
No specific folder name is required. See README.md for the complete setup.
Keep backups outside the web root and merge existing project instructions.

Instruction discovery: [official OpenAI documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
