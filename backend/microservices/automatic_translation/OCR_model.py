"""OCR service helpers for the automatic_translation microservice.

This module exposes a reusable `run_ocr` function that calls the Hugging Face
Router API with vision-capable models. Image bytes are encoded to base64 and
sent via OpenAI-compatible client.
"""

from __future__ import annotations

import base64
import io
import os
import logging

from openai import OpenAI
from PIL import Image, UnidentifiedImageError
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


class ModelLoadError(RuntimeError):
    """Raised when the API client cannot be initialized."""


# Configuration from environment
HF_TOKEN = os.getenv("HF_TOKEN")
OCR_MODEL_ID = os.getenv("OCR_MODEL_ID", "Qwen/Qwen2.5-VL-7B-Instruct:hyperbolic")
OCR_MAX_TOKENS = int(os.getenv("OCR_MAX_TOKENS", "512"))

# Default extraction instruction used for all pages; can be overridden per call.
BASE_PROMPT = (
    "Extract ALL text from this scanned form page. "
    "Include ALL numbers, handwritten text, typed text, and text inside boxes. "
    "Extract ID numbers, dates, names, scores, and all numeric values. "
    "Do NOT summarize. Do NOT omit anything. "
    'If a field is empty, write "[EMPTY]". '
    "Keep the original formatting and order. "
    "If there is a QR code, a figure (logo, chart, stamp, etc.), or a cachet (stamp), "
    "mention it explicitly in Arabic, in the exact location it appears in the document, "
    "for example: '[رمز QR هنا]', '[شكل هنا]', or '[ختم هنا مع النص بداخله]'. "
    "Do NOT move or reorder anything; maintain the original layout."
)


def _get_client() -> OpenAI:
    """Initialize OpenAI client for HF Router API."""
    if not HF_TOKEN:
        raise ModelLoadError("HF_TOKEN environment variable is not set")

    return OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=HF_TOKEN,
    )


def run_ocr(image_bytes: bytes, prompt_override: str | None = None) -> str:
    """Run OCR on the provided image bytes and return extracted text via HF API."""

    if not image_bytes:
        raise ValueError("Empty image payload")

    # Validate image
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()
    except UnidentifiedImageError as exc:
        raise ValueError("Uploaded file is not a valid image") from exc

    # Encode image to base64
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:image/jpeg;base64,{base64_image}"

    client = _get_client()

    try:
        completion = client.chat.completions.create(
            model=OCR_MODEL_ID,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_override or BASE_PROMPT,
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": data_url},
                        },
                    ],
                }
            ],
            max_tokens=OCR_MAX_TOKENS,
        )
        return completion.choices[0].message.content or ""
    except Exception as exc:
        raise ModelLoadError(f"HF API call failed: {exc}") from exc


if __name__ == "__main__":
    # Smoke test: verify API client initialization
    logging.info("OCR Model: %s", OCR_MODEL_ID)
    logging.info("HF_TOKEN set: %s", bool(HF_TOKEN))

    if not HF_TOKEN:
        logging.error("HF_TOKEN not found in environment. Set it in .env file.")
    else:
        logging.info("API client ready. Upload an image via the /ocr/extract endpoint to test.")
