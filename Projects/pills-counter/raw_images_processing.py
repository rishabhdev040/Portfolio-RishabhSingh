"""Convert images from a raw folder to uniquely named JPG files.

Original files are preserved unless --delete-originals is explicitly supplied.
"""

from __future__ import annotations

import argparse
import itertools
import secrets
from pathlib import Path
from typing import Callable

from PIL import Image, UnidentifiedImageError
import pillow_avif  # Registers AVIF support with Pillow.

SUPPORTED_SUFFIXES = {
    ".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp", ".avif"
}


def get_unique_id():
    """Yield increasing IDs from a random starting point."""
    seed = secrets.randbelow(2**32)
    return itertools.count(seed)


def change_format_to_jpg(
    raw_image_save_path: Path,
    image_save_path: Path,
    *,
    delete_originals: bool = False,
    quality: int = 95,
    progress_callback: Callable[[int, int, str], None] | None = None,
    log_callback: Callable[[str, str], None] | None = None,
) -> int:
    """Convert supported images and return the number successfully converted."""
    raw_image_save_path = Path(raw_image_save_path)
    image_save_path = Path(image_save_path)

    if not raw_image_save_path.is_dir():
        raise FileNotFoundError(f"Input directory does not exist: {raw_image_save_path}")
    if not 1 <= quality <= 100:
        raise ValueError("JPEG quality must be between 1 and 100.")

    image_save_path.mkdir(parents=True, exist_ok=True)
    ids = get_unique_id()
    converted = 0
    candidates = [
        path for path in sorted(raw_image_save_path.iterdir())
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    ]
    total = len(candidates)

    for index, raw_image_path in enumerate(candidates, start=1):
        try:
            with Image.open(raw_image_path) as image:
                converted_image = image.convert("RGB")
                while True:
                    new_path = image_save_path / f"{next(ids)}.jpg"
                    if not new_path.exists():
                        break
                converted_image.save(new_path, format="JPEG", quality=quality)

            converted += 1
            message = f"Saved: {new_path} (from {raw_image_path.name})"
            print(message)
            if log_callback:
                log_callback("success", message)

            if delete_originals:
                raw_image_path.unlink()
                message = f"Deleted original: {raw_image_path}"
                print(message)
                if log_callback:
                    log_callback("warning", message)

        except (OSError, UnidentifiedImageError, ValueError) as exc:
            message = f"Skipped {raw_image_path}: {exc}"
            print(message)
            if log_callback:
                log_callback("error", message)

        if progress_callback:
            progress_callback(index, total, raw_image_path.name)

    return converted


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert raw images to JPG.")
    parser.add_argument("--input-dir", type=Path, default=Path("raw-data"))
    parser.add_argument("--output-dir", type=Path, default=Path("data"))
    parser.add_argument("--quality", type=int, default=95, help="JPEG quality (1-100).")
    parser.add_argument(
        "--delete-originals",
        action="store_true",
        help="Delete an original only after its JPG conversion succeeds.",
    )
    args = parser.parse_args()

    count = change_format_to_jpg(
        args.input_dir,
        args.output_dir,
        delete_originals=args.delete_originals,
        quality=args.quality,
    )
    print(f"Converted {count} image(s).")


if __name__ == "__main__":
    main()
