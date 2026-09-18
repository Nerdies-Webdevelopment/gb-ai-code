---
name: generateblocks-forms
description: Build or embed native GenerateBlocks Pro forms with their saved form records. Use for fields, labels and form actions; use generateblocks-contact for layout around an existing shortcode.
---

# generateblocks-forms

All project paths below are relative to the package root (the directory containing AGENTS.md).

Read `PLUGIN-FEATURES.md` section Native Pro Forms and project rules. Inspect `generateblocks-pro/includes/feature-settings.php`, `includes/form/bootstrap.php` and the selected form block metadata/save/render files.

Forms are optional and default off in the inspected source. Confirm the actual feature setting before using them. Separate form-definition work (`gblocks_form`, native form/field/label/control blocks) from page embedding (`generateblocks-pro/form-render`, integer `formId`). The embed does not carry field definitions, actions or integration configuration.

Reuse existing real form IDs and providers when requested. Do not invent a numeric placeholder or replace an existing third-party form automatically. If an ID is missing, finish the surrounding layout and field specification, and identify the required form record rather than claiming a working embed. For field serialization use current saved exports or the local save implementation; no validated form HTML reference is bundled.

Keep visible labels, suitable input types/autocomplete, required indications and accessible errors. Read form action/schema classes before configuring delivery. Do not put credentials in exports or infer recipients, webhook URLs or consent. Visual tests must not submit forms; actual delivery requires an explicitly requested test. Report definition, embed and action configuration separately, including missing activation/runtime checks.
