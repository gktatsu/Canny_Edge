"""Command line interface for the Canny edge batch processor."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .config import CannySettings
from .processor import CannyBatchProcessor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Batch Canny edge extraction with directory preservation",
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="Directory that contains source images.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where edge images will be stored.",
    )
    parser.add_argument(
        "--lower-threshold",
        type=float,
        required=True,
        help="Lower hysteresis threshold for Canny.",
    )
    parser.add_argument(
        "--upper-threshold",
        type=float,
        required=True,
        help="Upper hysteresis threshold for Canny.",
    )
    parser.add_argument(
        "--gaussian-ksize",
        type=int,
        default=5,
        help="Odd kernel size for Gaussian blur (default: 5).",
    )
    parser.add_argument(
        "--gaussian-sigma",
        type=float,
        default=None,
        help="Sigma for Gaussian blur (default: auto).",
    )
    parser.add_argument(
        "--log-path",
        type=Path,
        default=None,
        help="Optional path for the JSON log file.",
    )
    parser.add_argument(
        "--extensions",
        type=str,
        nargs="+",
        default=None,
        help=(
            "File extensions to include (default: .png .jpg .jpeg .tif .tiff)."
        ),
    )
    return parser


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = build_parser()
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    namespace = parse_args(argv if argv is not None else sys.argv[1:])

    input_dir = namespace.input_dir.expanduser().resolve()
    output_dir = namespace.output_dir.expanduser().resolve()
    if namespace.log_path:
        log_path = namespace.log_path.expanduser().resolve()
    else:
        log_path = None

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    settings_kwargs = dict(
        input_dir=input_dir,
        output_dir=output_dir,
        lower_threshold=namespace.lower_threshold,
        upper_threshold=namespace.upper_threshold,
        gaussian_ksize=namespace.gaussian_ksize,
        gaussian_sigma=namespace.gaussian_sigma,
        log_path=log_path,
    )
    if namespace.extensions:
        settings_kwargs["allowed_extensions"] = namespace.extensions

    settings = CannySettings(**settings_kwargs)

    processor = CannyBatchProcessor(settings)
    log_record = processor.run()

    print(f"Processed {len(log_record['processed_files'])} files.")
    print(f"Skipped {len(log_record['skipped_files'])} files.")
    print(f"Log written to: {settings.resolved_log_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
