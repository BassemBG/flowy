
# Example Microservice FastAPI App
# To add a new endpoint, define it here or in a router and include it.

from fastapi import FastAPI
from router import router

app = FastAPI()
app.include_router(router)

# Example endpoint (remove if not needed)
@app.get("/health")
def health_check():
	"""Health check endpoint for monitoring."""
	return {"status": "ok"}
