---
name: confirmo-pet-converter
description: Convert downloaded desktop pet sprite packages from https://sprites.confirmo.love/sprite into Codex-recognizable local pet packages. Use when a user has a folder containing manifest.json and sprite.png from sprites.confirmo.love and wants it imported as a Codex desktop pet with transparent background, pet.json, spritesheet.webp, and validation previews.
---

# Confirmo Pet Converter

## Overview

Use this skill to convert pet image packs downloaded from `https://sprites.confirmo.love/sprite` into Codex desktop pet packages.

Source packages usually look like:

```text
<pet folder>/
  manifest.json
  sprite.png
```

Codex local pet packages should include:

```text
<pet folder>/
  pet.json
  spritesheet.webp
```

The converter handles the common Confirmo sprite format: `8x7` rows, opaque magenta/pink chroma-key background, and `manifest.json` metadata. It outputs a Codex atlas: `1536x1872`, `8x9`, `192x208` cells, transparent background.

## Workflow

1. Confirm the package folder contains `manifest.json` and `sprite.png`.
2. Run the bundled converter:

```bash
python /Users/jintaoguo/.codex/skills/confirmo-pet-converter/scripts/convert_confirmo_pet.py \
  --pet-dir /absolute/path/to/pet-folder
```

For all Confirmo packages under the default Codex pets folder:

```bash
python /Users/jintaoguo/.codex/skills/confirmo-pet-converter/scripts/convert_confirmo_pet.py \
  --all /Users/jintaoguo/.codex/pets
```

3. Validate with the hatch-pet atlas validator when available:

```bash
python /Users/jintaoguo/.codex/skills/hatch-pet/scripts/validate_atlas.py \
  /absolute/path/to/pet-folder/spritesheet.webp \
  --json-out /absolute/path/to/pet-folder/_conversion_qa/validation-foreground-only.json
```

4. Generate a contact sheet preview when available:

```bash
python /Users/jintaoguo/.codex/skills/hatch-pet/scripts/make_contact_sheet.py \
  /absolute/path/to/pet-folder/spritesheet.webp \
  --output /absolute/path/to/pet-folder/_conversion_qa/contact-sheet-foreground-only.png
```

5. Tell the user to restart Codex App or reopen the desktop pet picker if the new pet is not visible immediately.

## Mapping

Confirmo packages commonly have 7 rows. Codex expects 9 rows. Preserve the original rows and fill missing Codex rows with sensible fallbacks:

```text
idle          <- source row 0
running-right <- source row 1
running-left  <- source row 2
waving        <- source row 3
jumping       <- source row 4
failed        <- source row 5
waiting       <- source row 6
running       <- source row 1
review        <- source row 0
```

Unused frame cells in Codex rows must remain transparent.

## Notes

- Do not delete the original `manifest.json` or `sprite.png`; keep them as source material.
- The converter removes magenta/pink chroma-key backgrounds using HSV thresholds. This works for the downloaded Confirmo packs seen so far.
- If foreground pixels are also magenta/pink, inspect the contact sheet and adjust thresholds or rerun without aggressive removal.
- The converter writes QA files under `_conversion_qa/`, including the cleaned source sprite and a conversion report.
