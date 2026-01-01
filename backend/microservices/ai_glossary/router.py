from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_glossary():
    """Root endpoint for AI Glossary microservice."""
    return {"message": "AI Glossary Service"}
