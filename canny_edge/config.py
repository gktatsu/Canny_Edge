"""Configuration models for the Canny edge processor."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass(frozen=True)
class CannySettings:
    """User-facing settings for Canny edge detection."""

    input_dir: Path
    output_dir: Path
    lower_threshold: float
    upper_threshold: float
    gaussian_ksize: int = 5
    gaussian_sigma: Optional[float] = None
    log_path: Optional[Path] = None
    allowed_extensions: List[str] = field(
        default_factory=lambda: [".png", ".jpg", ".jpeg", ".tif", ".tiff"]
    )

    def __post_init__(self) -> None:
        if self.lower_threshold < 0 or self.upper_threshold < 0:
            raise ValueError("Thresholds must be non-negative.")
        if self.lower_threshold >= self.upper_threshold:
            raise ValueError(
                "Lower threshold must be less than upper threshold."
            )
        if self.gaussian_ksize <= 0 or self.gaussian_ksize % 2 == 0:
            raise ValueError(
                "Gaussian kernel size must be a positive odd integer."
            )

    @property
    def resolved_log_path(self) -> Path:
        if self.log_path is not None:
            return self.log_path
        return self.output_dir / "processing_log.json"
