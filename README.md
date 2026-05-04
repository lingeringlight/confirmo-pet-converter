# Confirmo Pet Converter

Codex skill for converting desktop pet sprite packages downloaded from
<https://sprites.confirmo.love/sprite> into Codex-recognizable local pet packages.

It converts the common Confirmo package format:

```text
manifest.json
sprite.png
```

into:

```text
pet.json
spritesheet.webp
```

The generated atlas is `1536x1872`, with `8x9` cells at `192x208`, and the magenta/pink chroma-key background is removed.

## Install

Copy this repository folder into your Codex skills directory:

```bash
cp -R confirmo-pet-converter "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart Codex if the skill list does not refresh immediately.

## Usage

Convert one downloaded pet package:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/confirmo-pet-converter/scripts/convert_confirmo_pet.py" \
  --pet-dir "${CODEX_HOME:-$HOME/.codex}/pets/ikun"
```

Convert all Confirmo-style packages under the Codex pets folder:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/confirmo-pet-converter/scripts/convert_confirmo_pet.py" \
  --all "${CODEX_HOME:-$HOME/.codex}/pets"
```

## License

MIT
