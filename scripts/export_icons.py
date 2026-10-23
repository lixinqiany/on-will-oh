#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Export approved ONWILO artwork into frontend icon formats.

This script resizes and packages the artwork; it does not redraw the logo.
Run from any directory: python3 scripts/export_icons.py
"""

from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "brand" / "original"
PUBLIC = ROOT / "public"
SIZES = (16, 32, 48, 64, 128, 180, 192, 256, 512, 1024)
THEMES = {
    "light": {"background": "#F0FBFA", "background_rgb": (240, 251, 250)},
    "dark": {"background": "#08314B", "background_rgb": (8, 49, 75)},
}
ICO_SIZES = ((16, 16), (32, 32), (48, 48))


def write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def export_maskable(image: Image.Image, size: int, background: tuple) -> Image.Image:
    # The complete square artwork fits inside the central 80%-diameter circle.
    # A square with side 0.8/sqrt(2) of the canvas fits that circle.
    artwork_size = math.floor(size * 0.8 / math.sqrt(2)) - 2
    artwork = image.resize((artwork_size, artwork_size), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), background)
    offset = (size - artwork_size) // 2
    canvas.paste(artwork, (offset, offset))
    return canvas


def manifest(theme: str, metadata: dict) -> dict:
    return {
        "id": "./",
        "name": "ONWILO · 由行",
        "short_name": "ONWILO",
        "description": "按自己的节奏，去喜欢的地方。",
        "lang": "zh-CN",
        "start_url": "./",
        "scope": "./",
        "display": "standalone",
        "background_color": metadata["background"],
        "theme_color": metadata["background"],
        "icons": [
            {
                "src": f"brand/{theme}/onwilo-{size}.png",
                "sizes": f"{size}x{size}",
                "type": "image/png",
                "purpose": "any",
            }
            for size in (192, 512)
        ] + [
            {
                "src": f"brand/{theme}/onwilo-maskable-{size}.png",
                "sizes": f"{size}x{size}",
                "type": "image/png",
                "purpose": "maskable",
            }
            for size in (192, 512)
        ],
    }


def main() -> None:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    brand = {
        "name": "ONWILO",
        "chineseName": "由行",
        "repositoryName": "on-will-oh",
        "tagline": "按自己的节奏，去喜欢的地方。",
        "assetVersion": "0.1.0",
        "themes": {},
    }
    for theme, metadata in THEMES.items():
        output = PUBLIC / "brand" / theme
        output.mkdir(parents=True, exist_ok=True)
        with Image.open(SOURCE / f"onwilo-{theme}.png") as original:
            image = original.convert("RGB")
        for size in SIZES:
            image.resize((size, size), Image.Resampling.LANCZOS).save(
                output / f"onwilo-{size}.png", optimize=True
            )
        image.resize((256, 256), Image.Resampling.LANCZOS).save(
            output / "favicon.ico", format="ICO", sizes=ICO_SIZES
        )
        for size in (192, 512):
            export_maskable(image, size, metadata["background_rgb"]).save(
                output / f"onwilo-maskable-{size}.png", optimize=True
            )
        brand["themes"][theme] = {
            "background": metadata["background"],
            "icons": {
                str(size): f"/brand/{theme}/onwilo-{size}.png"
                for size in SIZES
            },
            "favicon": f"/brand/{theme}/favicon.ico",
            "appleTouchIcon": f"/brand/{theme}/onwilo-180.png",
            "maskable": {
                str(size): f"/brand/{theme}/onwilo-maskable-{size}.png"
                for size in (192, 512)
            },
        }
        manifest_name = "site.webmanifest" if theme == "light" else "site-dark.webmanifest"
        write_json(PUBLIC / manifest_name, manifest(theme, metadata))

    shutil.copyfile(
        PUBLIC / "brand" / "light" / "favicon.ico",
        PUBLIC / "favicon.ico",
    )
    shutil.copyfile(
        PUBLIC / "brand" / "light" / "onwilo-180.png",
        PUBLIC / "apple-touch-icon.png",
    )
    write_json(PUBLIC / "brand" / "brand.json", brand)
    files = [path for path in PUBLIC.rglob("*") if path.is_file()]
    print(json.dumps({
        "themes": list(THEMES),
        "png_sizes": list(SIZES),
        "public_files": len(files),
        "public_bytes": sum(path.stat().st_size for path in files),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
