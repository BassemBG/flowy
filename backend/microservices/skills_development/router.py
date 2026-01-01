from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_skills():
    """Root endpoint for Skills Development microservice."""
    return {"message": "Skills Development Service"}
