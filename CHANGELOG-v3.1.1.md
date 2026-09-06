# GenerateBlocks Codex v3.1.1 — local package maintenance

Date: 2026-09-06. Target: `C:/xampp/htdocs/nerdies2000`.

## Changes

- Fixed the Child Theme validator's default path for the WordPress root layout.
- Corrected current documentation and theme instructions that used the old path.
  Historical changelogs and source documents retain their original wording.
- Corrected the README package revision and installation/setup commands.
- Recorded installed source headers: GeneratePress 3.6.1, GP Premium 2.5.6,
  GenerateBlocks 2.4.1, GenerateBlocks Pro 2.7.1.
- Distinguished installed source presence from plugin/theme activation and
  runtime compatibility; retained the original reference validation status.
- Added `tools/check_environment.py` to detect version drift or missing sources
  without loading WordPress, reading wp-config.php, or accessing the database.
- Added `tools/validate_all.py --installed` as one entry point for tests,
  theme checks, reference checks and installed source inspection. Failures
  are preserved even when a later check succeeds.
- Added regression coverage for the WordPress theme path and version inspection.

## Verification

The prepared package passed 12 unit tests, Child Theme checks including PHP
syntax lint, and validation of all 15 reference files (0 errors, 24 pre-existing
warnings). The source inspection correctly detected the old documented
GenerateBlocks versions in the unchanged installation before transfer.

Gutenberg save/reopen, frontend behavior, activation and visual parity have
not been tested by this maintenance update. No reference is promoted to
runtime-validated. Theme PHP/CSS and block reference contents are unchanged.

## Routine check

```powershell
cd C:/xampp/htdocs/nerdies2000
python tools/validate_all.py --installed
```

Review a version mismatch against the installed implementation. Updating a
version entry is documentation maintenance, not proof of block compatibility.

During verification the installed plugin sources changed from 2.4.0 / 2.7.0
to 2.4.1 / 2.7.1. The new check detected this drift. The final version headers
and constants were inspected again and the source snapshot was updated;
no block compatibility certification is implied.
