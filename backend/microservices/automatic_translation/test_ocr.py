"""Test script for OCR extraction on local image files."""

import os
from pathlib import Path
from OCR_model import run_ocr

# Path to test image - find the first image in ocr_file folder
ocr_folder = Path(__file__).parent / "ocr_file"
image_files = list(ocr_folder.glob("*.jpg")) + list(ocr_folder.glob("*.png"))

if not image_files:
    print(f"[ERROR] No image files found in {ocr_folder}")
    exit(1)

image_path = image_files[0]
print(f"[TEST] Loading image from: {image_path}")

if not image_path.exists():
    print(f"[ERROR] Image not found at {image_path}")
    exit(1)

# Read image bytes
with open(image_path, "rb") as f:
    image_bytes = f.read()

print(f"[TEST] Image loaded: {len(image_bytes)} bytes")
print("[TEST] Running OCR extraction via HF API...")
print("-" * 80)

try:
    extracted_text = run_ocr(image_bytes)
    print(extracted_text)
    print("-" * 80)
    print(f"[SUCCESS] Extracted {len(extracted_text)} characters")
    
    # Optionally save to file
    output_path = Path(__file__).parent / "ocr_file" / "extracted_text.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)
    print(f"[SAVED] Text saved to: {output_path}")
    
except Exception as exc:
    print(f"[ERROR] {exc}")
    raise
