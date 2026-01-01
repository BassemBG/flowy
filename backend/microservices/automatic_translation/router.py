from fastapi import APIRouter, File, HTTPException, UploadFile

from OCR_model import ModelLoadError, run_ocr

router = APIRouter()


@router.get("/")
def get_translation():
    """Root endpoint for Automatic Translation microservice."""
    return {"message": "Automatic Translation Service"}


@router.post("/ocr/extract")
async def extract_text(file: UploadFile = File(...)):
    """Extract text from an uploaded image using the OCR model."""

    try:
        image_bytes = await file.read()
        text = run_ocr(image_bytes)
        return {"text": text}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except ModelLoadError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
