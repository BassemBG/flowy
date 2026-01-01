from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_whatsapp_agent():
    """Root endpoint for WhatsApp Agent microservice."""
    return {"message": "WhatsApp Agent Module"}
