from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_notekeeper():
    """Root endpoint for AI NoteKeeper microservice."""
    return {"message": "AI NoteKeeper Service"}
