# Backend

This is the backend for the project, built with FastAPI. It contains modular services for:

- WhatsApp Agent
- AI Glossary Management
- Automatic Translation
- Skills Development
- AI NoteKeeper
- Shadowing

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

3. Use Docker Compose to run all services:
   ```bash
   docker-compose up
   ```

## Environment Variables

Set the following variables in the `.env` file:
- `APP_ENV`: Application environment (e.g., `development`, `production`)
- `DEBUG`: Enable or disable debug mode.