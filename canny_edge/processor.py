"""Core processing logic for the Canny edge batch tool."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import cv2
import numpy as np

from .config import CannySettings


class CannyBatchProcessor:
    """Apply Canny edge detection to every supported image in a directory."""

    def __init__(self, settings: CannySettings) -> None:
        self.settings = settings
        self._allowed_extensions = {
            ext.lower() for ext in self.settings.allowed_extensions
        }

    def run(self) -> Dict[str, object]:
        """Process all eligible images and write a JSON log."""
        file_pairs = list(self._collect_file_pairs())
        processed: List[Dict[str, str]] = []
        skipped: List[Dict[str, str]] = []

        for source_path, output_path in file_pairs:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if output_path.exists():
                skipped.append(
                    {
                        "input": str(source_path),
                        "output": str(output_path),
                        "reason": "output already exists",
                    }
                )
                continue

            image = cv2.imread(str(source_path), cv2.IMREAD_COLOR)
            if image is None:
                skipped.append(
                    {
                        "input": str(source_path),
                        "output": str(output_path),
                        "reason": "failed to read image",
                    }
                )
                continue

            edge_image = self._compute_edges(image)
            write_success = cv2.imwrite(str(output_path), edge_image)
            if not write_success:
                skipped.append(
                    {
                        "input": str(source_path),
                        "output": str(output_path),
                        "reason": "failed to write output",
                    }
                )
                continue

            processed.append(
                {"input": str(source_path), "output": str(output_path)}
            )

        log_record = self._build_log(processed=processed, skipped=skipped)
        self._write_log(log_record)
        return log_record

    def _collect_file_pairs(self) -> Iterable[Tuple[Path, Path]]:
        """Yield matching source and destination paths for supported files."""
        for source_path in self.settings.input_dir.rglob("*"):
            if not source_path.is_file():
                continue
            if source_path.suffix.lower() not in self._allowed_extensions:
                continue
            relative_path = source_path.relative_to(self.settings.input_dir)
            output_root = self.settings.output_dir / relative_path
            output_path = output_root.with_suffix(".png")
            yield source_path, output_path

    def _compute_edges(self, image: np.ndarray) -> np.ndarray:
        """Convert an image to binary edges using Canny."""
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(
            grayscale,
            ksize=(self.settings.gaussian_ksize, self.settings.gaussian_ksize),
            sigmaX=self.settings.gaussian_sigma or 0.0,
        )
        edges = cv2.Canny(
            blurred,
            threshold1=self.settings.lower_threshold,
            threshold2=self.settings.upper_threshold,
        )
        # Ensure the result is a binary image (0 or 255 values only).
        _, binary_edges = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY)
        return binary_edges

    def _build_log(
        self,
        processed: List[Dict[str, str]],
        skipped: List[Dict[str, str]],
    ) -> Dict[str, object]:
        parameters = asdict(self.settings)
        parameters["input_dir"] = str(self.settings.input_dir)
        parameters["output_dir"] = str(self.settings.output_dir)
        if parameters.get("log_path") is not None:
            parameters["log_path"] = str(self.settings.resolved_log_path)

        return {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "input_dir": str(self.settings.input_dir),
            "output_dir": str(self.settings.output_dir),
            "parameters": parameters,
            "processed_files": processed,
            "skipped_files": skipped,
        }

    def _write_log(self, log_record: Dict[str, object]) -> None:
        """Write or append the log record to the configured JSON file."""
        log_path = self.settings.resolved_log_path
        log_path.parent.mkdir(parents=True, exist_ok=True)

        if log_path.exists():
            try:
                with log_path.open("r", encoding="utf-8") as existing_file:
                    existing_data = json.load(existing_file)
            except (json.JSONDecodeError, OSError):
                existing_data = []

            if isinstance(existing_data, list):
                existing_data.append(log_record)
                data_to_write = existing_data
            else:
                data_to_write = [existing_data, log_record]
        else:
            data_to_write = [log_record]

        with log_path.open("w", encoding="utf-8") as log_file:
            json.dump(data_to_write, log_file, indent=2, ensure_ascii=False)
