from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_shadowing():
    """Root endpoint for Shadowing microservice."""
    return {"message": "Shadowing Service"}
