from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_translation():
    """Root endpoint for Automatic Translation microservice."""
    return {"message": "Automatic Translation Service"}
