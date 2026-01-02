from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel
import logging
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from OCR_model import ModelLoadError, run_ocr
from llm.translator import translate_text

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter()


class TranslateRequest(BaseModel):
    """Request body for text translation."""
    text: str


@router.get("/")
def get_translation():
    """Root endpoint for Automatic Translation microservice."""
    logger.info("[API] GET / - Health check")
    return {"message": "Automatic Translation Service"}


@router.post("/ocr/extract")
async def extract_text(file: UploadFile = File(...)):
    """Extract text from an uploaded image using the OCR model."""

    logger.info(f"[API] POST /ocr/extract - Received file: {file.filename}")
    logger.info(f"[API] File size: {file.size} bytes, Content-Type: {file.content_type}")

    try:
        image_bytes = await file.read()
        logger.info(f"[API] Read {len(image_bytes)} bytes from upload")
        
        text = run_ocr(image_bytes)
        
        logger.info(f"[API] OCR completed successfully")
        return {"text": text}
        
    except ValueError as exc:
        logger.error(f"[API] Validation error: {exc}")
        raise HTTPException(status_code=400, detail=str(exc))
    except ModelLoadError as exc:
        logger.error(f"[API] Model/API error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        logger.error(f"[API] Unexpected error: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/translate")
async def translate_arabic_text(request: TranslateRequest):
    """
    Translate extracted Arabic text to French.
    
    Follows the structure of Tunisian marriage contracts (actes de mariage).
    
    Request body:
        {
            "text": "Arabic text extracted from OCR"
        }
    
    Returns:
        {
            "translation": "French translation"
        }
    """
    
    if not request.text or not request.text.strip():
        logger.error("[API] Translation request with empty text")
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    logger.info(f"[API] POST /translate - Received {len(request.text)} characters")
    
    try:
        logger.info("[API] Starting LLM translation")
        translation = translate_text(request.text)
        
        logger.info("[API] Translation completed successfully")
        return {"translation": translation}
        
    except ValueError as exc:
        logger.error(f"[API] Configuration error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        logger.error(f"[API] Translation failed: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail="Translation service error")
