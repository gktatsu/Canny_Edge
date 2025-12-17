# Canny Edge Processor

Batch Canny edge detection for images in a directory while preserving the original directory structure. Processing parameters are recorded in a JSON log for reproducibility.

## Features

- **Batch Processing**: Process all images in a directory at once
- **Structure Preservation**: Maintains input directory hierarchy in the output
- **Skip Existing**: Existing files are skipped without overwriting
- **Detailed Logging**: Records processing parameters and results in JSON log for reproducibility
- **Flexible Configuration**: Customizable thresholds, Gaussian blur, and target file extensions

## Installation

```bash
pip install .
```

For development (editable mode):

```bash
pip install -e .
```

## Dependencies

- Python >= 3.9
- opencv-python >= 4.8.0
- numpy >= 1.24.0

## Usage

### Basic Example

```bash
canny-edge \
  --input-dir /path/to/images \
  --output-dir /path/to/output \
  --lower-threshold 50 \
  --upper-threshold 150
```

### Full Options Example

```bash
canny-edge \
  --input-dir /path/to/images \
  --output-dir /path/to/output \
  --lower-threshold 50 \
  --upper-threshold 150 \
  --gaussian-ksize 7 \
  --gaussian-sigma 1.5 \
  --log-path /path/to/custom_log.json \
  --extensions .png .jpg .bmp
```

## Command Line Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--input-dir` | ✓ | - | Directory containing source images |
| `--output-dir` | ✓ | - | Directory where edge images will be stored |
| `--lower-threshold` | ✓ | - | Lower hysteresis threshold for Canny edge detection |
| `--upper-threshold` | ✓ | - | Upper hysteresis threshold for Canny edge detection |
| `--gaussian-ksize` | - | 5 | Kernel size for Gaussian blur (must be odd) |
| `--gaussian-sigma` | - | auto | Sigma for Gaussian blur (auto-calculated by OpenCV if omitted) |
| `--log-path` | - | `<output-dir>/processing_log.json` | Path for the JSON log file |
| `--extensions` | - | `.png .jpg .jpeg .tif .tiff` | File extensions to process |

## Processing Pipeline

1. Recursively collect images with target extensions from input directory
2. For each image:
   - Convert color image to grayscale
   - Apply Gaussian blur
   - Perform Canny edge detection
   - Binarize and save as PNG
3. Record processing results in JSON log

## Output

- **Edge Images**: Binary PNG images (pixel values 0 or 255)
- **Processing Log**: JSON format containing:
  - Timestamp
  - Input/output directories
  - Processing parameters
  - List of processed files
  - List of skipped files (with reasons)

## Notes

- `lower_threshold` must be less than `upper_threshold`
- `gaussian-ksize` must be a positive odd integer
- Existing output files are skipped without overwriting
- If the log file already exists, new records are appended

## Help

To see all available options:

```bash
canny-edge --help
```

Or:

```bash
python -m canny_edge.cli --help
```
