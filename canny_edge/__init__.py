"""Canny edge detection package."""

from .config import CannySettings
from .processor import CannyBatchProcessor

__all__ = ["CannySettings", "CannyBatchProcessor"]
