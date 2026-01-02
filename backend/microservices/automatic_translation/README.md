# Automatic Translation Microservice

A FastAPI-based microservice for extracting text from document images using OCR and translating Arabic text to French, with specialized support for Tunisian legal documents (marriage contracts).

## Overview

This microservice provides two main capabilities:

1. **OCR (Optical Character Recognition)**: Extract text from document images using Qwen vision-language model via Hugging Face Router API
2. **Translation**: Translate extracted Arabic text to French using GPT-OSS model via Hugging Face Router API

The service is designed to handle Tunisian marriage contracts (actes de mariage) with high accuracy, preserving all legal details, names, dates, and identification numbers.

## Architecture

```
automatic_translation/
├── OCR_model.py          # OCR service using HF Qwen vision model
├── llm/
│   └── translator.py     # Translation service using HF GPT-OSS model
├── router.py             # FastAPI endpoints for OCR and translation
├── main.py               # FastAPI app initialization
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (API keys)
└── Dockerfile            # Docker configuration
```

## Prerequisites

- Docker and Docker Compose
- Hugging Face API access (for OCR and translation models)
- Valid API keys for:
  - `HF_TOKEN`: Hugging Face token for Qwen vision model
  - `gpt_oss_api_key`: API key for GPT-OSS model access

## Setup & Configuration

### 1. Environment Variables

Create or update `.env` file in this directory with your API keys:

```env
HF_TOKEN=your_huggingface_token
gpt_oss_api_key=your_gpt_oss_api_key
```

### 2. Dependencies

All dependencies are defined in `requirements.txt`:

```
fastapi
uvicorn
openai
python-dotenv
pillow
python-multipart
```

Install them locally (optional, for development):

```bash
pip install -r requirements.txt
```

## Running the Service

### Option 1: Docker (Recommended)

From the backend directory:

```bash
# Build and start all services including automatic_translation
docker-compose up --build

# Or rebuild just this service
docker-compose up --build --no-deps automatic_translation
```

The service will be available at `http://localhost:8000` inside the Docker network, and accessible through the gateway at `http://localhost:8000/automatic_translation/` from outside.

### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export HF_TOKEN=your_token
export gpt_oss_api_key=your_key

# Run the service
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### 1. OCR - Extract Text from Image

**Endpoint:** `POST /ocr/extract`

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: Image file (JPEG, PNG, WebP)

**Example:**
```bash
curl -X POST \
  -F "file=@document.jpg" \
  http://localhost:8000/ocr/extract
```

**Response:**
```json
{
  "text": "عقد زواج\n\nالحمد الله وحده، تزوج على بركة الله تعالى..."
}
```

### 2. Translate - Translate Arabic to French

**Endpoint:** `POST /translate`

**Request:**
- Method: POST
- Content-Type: application/json
- Body: JSON with Arabic text

**Example:**
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "عقد زواج..."}' \
  http://localhost:8000/translate
```

**Response:**
```json
{
  "translation": "Louange à Dieu, s'est marié avec la bénédiction et l'aide de Dieu..."
}
```

## Workflow

### Complete OCR + Translation Pipeline

1. **Frontend** (Translation.tsx) uploads a document image
2. **Gateway** routes request to this microservice
3. **OCR Service** extracts Arabic text from the image using Qwen model
4. **Frontend** receives extracted text and automatically triggers translation
5. **Translation Service** translates Arabic text to French
6. **Frontend** displays both extracted and translated text

### Expected Output Format

The translation produces flowing paragraph text formatted like this:

```
Louange à Dieu, s'est marié avec la bénédiction et l'aide de Dieu : le jeune Majdi AZZOUNI, 
de son père Mohamed fils de Taher fils de Belgacem fils de Moubarek AZZOUNI, 
de sa mère Dalila fille de Sahbi fils de Touhami fils de Mohamed AZZOUNI, 
né à Tunis, le 12 juin 1993, tunisien, célibataire selon un extrait de son acte de naissance 
n° 689, émis par la commune de Manouba, le 29 septembre 2025, travailleur à l'étranger, 
demeurant à Tunis, titulaire de la carte d'identité nationale n° 07194119...
```

## Models Used

### OCR Model
- **Model**: `Qwen/Qwen2.5-VL-7B-Instruct:hyperbolic`
- **Provider**: Hugging Face Router API
- **Purpose**: Extract text from document images
- **Input**: Image bytes (base64 encoded)
- **Output**: Extracted Arabic text

### Translation Model
- **Model**: `openai/gpt-oss-120b:cerebras`
- **Provider**: Hugging Face Router API
- **Purpose**: Translate Arabic to French with legal document context
- **Input**: Arabic text
- **Output**: French translation

## Key Features

✅ **Accurate OCR**: Uses state-of-the-art Qwen vision-language model
✅ **Legal Document Support**: Specialized for Tunisian marriage contracts
✅ **Literal Translation**: Word-for-word translation preserving all details
✅ **Name Preservation**: Maintains genealogical chains (père/mère relations)
✅ **Number Accuracy**: Preserves all identification numbers and dates
✅ **Flowing Text**: Natural paragraph format instead of bullet points
✅ **Error Handling**: Comprehensive logging and error messages
✅ **Timeout Support**: 120-second timeout for long API requests

## Logging

The service includes detailed logging at each step:

- `[API]` - HTTP endpoint logs
- `[OCR]` - OCR processing logs
- `[TRANSLATOR]` - Translation service logs

Check Docker logs to debug:
```bash
docker logs backend-automatic_translation-1
```

## Troubleshooting

### API Returns 500 Error
- **Cause**: Missing or invalid API keys in `.env`
- **Solution**: Verify `HF_TOKEN` and `gpt_oss_api_key` are set correctly

### OCR Extraction Returns Empty Text
- **Cause**: Image quality issues or unsupported format
- **Solution**: Use clear JPEG or PNG images (min 300 DPI recommended)

### Translation Service Not Responding
- **Cause**: Service not running or network issues
- **Solution**: Check Docker container is running: `docker ps | grep automatic_translation`

### Timeout Errors
- **Cause**: API requests taking longer than timeout
- **Solution**: Timeout is set to 120 seconds in gateway; increase if needed

## Integration with Frontend

The frontend Translation.tsx component:
1. Uploads image to `/api/automatic_translation/ocr/extract`
2. Receives extracted Arabic text
3. Calls `/api/automatic_translation/translate` with extracted text
4. Displays both versions (Arabic in read-only view, French in editable textarea)
5. Allows downloading both files

## Development Notes

- The OCR model is loaded lazily (first request takes longer)
- Translation uses low temperature (0.3) for consistency
- All responses are logged for debugging
- The service validates image formats before processing

## Future Enhancements

- Support for other document types (invoices, contracts, etc.)
- Batch OCR processing
- Translation to additional languages
- Integration with Qdrant for document embeddings and semantic search
- Rate limiting and API quotas
- Request caching to reduce API calls

## Support

For issues or questions, check the logs and verify:
1. Docker containers are running
2. API keys are correctly set in `.env`
3. Network connectivity to Hugging Face APIs
4. Image file formats are supported (JPEG, PNG, WebP)
