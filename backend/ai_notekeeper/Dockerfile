# Dockerfile for AI NoteKeeper
FROM python:3.9-slim

WORKDIR /app

COPY . /app

# Install dependencies from requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "ai_notekeeper.router:app", "--host", "0.0.0.0", "--port", "8005"]