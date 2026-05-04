#!/usr/bin/env python3
"""Convert sprites.confirmo.love pet packages into Codex local pet packages."""

from __future__ import annotations

import argparse
import colorsys
import hashlib
import json
import re
from pathlib import Path

from PIL import Image, ImageFilter

CELL_WIDTH = 192
CELL_HEIGHT = 208
COLUMNS = 8
ROWS = 9

ROW_SPECS = [
    ("idle", 0, 6),
    ("running-right", 1, 8),
    ("running-left", 2, 8),
    ("waving", 3, 4),
    ("jumping", 4, 5),
    ("failed", 5, 8),
    ("waiting", 6, 6),
    ("running", 7, 6),
    ("review", 8, 6),
]

SOURCE_ROW_FOR_TARGET = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 1,
    8: 0,
}


def slugify(value: str, fallback: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or fallback


def bounds(index: int, total_pixels: int, count: int) -> tuple[int, int]:
    return round(index * total_pixels / count), round((index + 1) * total_pixels / count)


def is_confirmo_key_pixel(r: int, g: int, b: int) -> bool:
    hue, saturation, _value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    hue_degrees = hue * 360
    return (
        285 <= hue_degrees <= 335
        and saturation > 0.28
        and r > 115
        and b > 105
        and g < 155
        and (r - g) > 55
        and (b - g) > 45
    )


def remove_chroma_key(image: Image.Image, median_filter: bool) -> tuple[Image.Image, int]:
    cleaned = image.convert("RGBA")
    pixels = cleaned.load()
    removed = 0
    for y in range(cleaned.height):
        for x in range(cleaned.width):
            r, g, b, a = pixels[x, y]
            if a and is_confirmo_key_pixel(r, g, b):
                pixels[x, y] = (r, g, b, 0)
                removed += 1
    if median_filter:
        cleaned.putalpha(cleaned.getchannel("A").filter(ImageFilter.MedianFilter(size=3)))
    return cleaned, removed


def compose_codex_atlas(source: Image.Image, source_rows: int, source_columns: int) -> Image.Image:
    atlas = Image.new("RGBA", (CELL_WIDTH * COLUMNS, CELL_HEIGHT * ROWS), (0, 0, 0, 0))
    for _state, target_row, used_frames in ROW_SPECS:
        source_row = min(SOURCE_ROW_FOR_TARGET[target_row], source_rows - 1)
        y0, y1 = bounds(source_row, source.height, source_rows)
        for column in range(used_frames):
            source_column = column % source_columns
            x0, x1 = bounds(source_column, source.width, source_columns)
            frame = source.crop((x0, y0, x1, y1))
            frame.thumbnail((CELL_WIDTH, CELL_HEIGHT), Image.Resampling.LANCZOS)
            left = column * CELL_WIDTH + (CELL_WIDTH - frame.width) // 2
            top = target_row * CELL_HEIGHT + (CELL_HEIGHT - frame.height) // 2
            atlas.alpha_composite(frame, (left, top))
    return atlas


def convert_pet_dir(pet_dir: Path, force_id: str | None, median_filter: bool) -> dict[str, object]:
    pet_dir = pet_dir.expanduser().resolve()
    manifest_path = pet_dir / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"manifest.json not found: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_path = pet_dir / manifest.get("spriteFile", "sprite.png")
    if not source_path.exists():
        raise SystemExit(f"sprite file not found: {source_path}")

    source = Image.open(source_path).convert("RGBA")
    source_rows = int(manifest.get("rows", 7))
    source_columns = int(manifest.get("columns", 8))
    display_name = manifest.get("name") or pet_dir.name
    pet_id = force_id or slugify(display_name, manifest.get("id") or pet_dir.name)
    description = manifest.get("description") or (
        "Converted from a sprites.confirmo.love pet package with transparent background."
    )

    qa_dir = pet_dir / "_conversion_qa"
    qa_dir.mkdir(parents=True, exist_ok=True)

    cleaned, removed_pixels = remove_chroma_key(source, median_filter=median_filter)
    clean_source_path = qa_dir / "sprite-foreground-only.png"
    cleaned.save(clean_source_path)

    atlas = compose_codex_atlas(cleaned, source_rows=source_rows, source_columns=source_columns)
    qa_atlas_path = qa_dir / "spritesheet-foreground-only.png"
    spritesheet_path = pet_dir / "spritesheet.webp"
    atlas.save(qa_atlas_path)
    atlas.save(spritesheet_path, format="WEBP", lossless=True, quality=100, method=6)

    pet_manifest = {
        "id": pet_id,
        "displayName": display_name,
        "description": description,
        "spritesheetPath": "spritesheet.webp",
    }
    pet_json_path = pet_dir / "pet.json"
    pet_json_path.write_text(
        json.dumps(pet_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    report = {
        "ok": True,
        "source_url": "https://sprites.confirmo.love/sprite",
        "pet_dir": str(pet_dir),
        "source": str(source_path),
        "source_size": [source.width, source.height],
        "source_rows": source_rows,
        "source_columns": source_columns,
        "removed_pixels_before_median": removed_pixels,
        "clean_source": str(clean_source_path),
        "pet_json": str(pet_json_path),
        "spritesheet": str(spritesheet_path),
        "qa_png": str(qa_atlas_path),
        "target_size": [CELL_WIDTH * COLUMNS, CELL_HEIGHT * ROWS],
        "row_mapping": {state: SOURCE_ROW_FOR_TARGET[row] for state, row, _ in ROW_SPECS},
        "sha256": hashlib.sha256(spritesheet_path.read_bytes()).hexdigest(),
    }
    (qa_dir / "foreground-removal-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


def find_pet_dirs(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.expanduser().resolve().iterdir()
        if path.is_dir() and (path / "manifest.json").exists() and (path / "sprite.png").exists()
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--pet-dir", help="One sprites.confirmo.love pet folder to convert.")
    source.add_argument("--all", help="Root folder containing multiple pet folders.")
    parser.add_argument("--id", help="Override the generated pet id. Only valid with --pet-dir.")
    parser.add_argument(
        "--no-median-filter",
        action="store_true",
        help="Skip the alpha median filter used to soften chroma-key speckles.",
    )
    args = parser.parse_args()

    if args.id and not args.pet_dir:
        raise SystemExit("--id can only be used with --pet-dir")

    pet_dirs = [Path(args.pet_dir)] if args.pet_dir else find_pet_dirs(Path(args.all))
    reports = [
        convert_pet_dir(path, force_id=args.id, median_filter=not args.no_median_filter)
        for path in pet_dirs
    ]
    print(json.dumps(reports[0] if len(reports) == 1 else reports, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
