
# Example Gateway FastAPI App
# This service proxies requests to backend microservices.
# To add a new microservice, add its name and URL to MICROSERVICE_URLS.

from fastapi import FastAPI, Request
import httpx

app = FastAPI()

MICROSERVICE_URLS = {
    "whatsapp_agent": "http://whatsapp_agent:8000",
    "ai_glossary": "http://ai_glossary:8000",
    "ai_notekeeper": "http://ai_notekeeper:8000",
    "automatic_translation": "http://automatic_translation:8000",
    "skills_development": "http://skills_development:8000",
    "shadowing": "http://shadowing:8000",
}

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(service: str, path: str, request: Request):
    """
    Proxies requests to the appropriate microservice.
    Example: /ai_glossary/some-endpoint -> http://ai_glossary:8000/some-endpoint
    """
    if service not in MICROSERVICE_URLS:
        return {"error": "Unknown service"}
    url = f"{MICROSERVICE_URLS[service]}/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method, url,
            headers=request.headers.raw,
            content=await request.body()
        )
    # Forward the response from the microservice
    return response.json()

# To add a new microservice:
# 1. Add its name and URL to MICROSERVICE_URLS above.
# 2. Make sure it is included in docker-compose.yml and running.
