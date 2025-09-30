# Syllabus Parser Backend

A FastAPI backend for parsing syllabus PDFs and exporting to Google Calendar and Notion.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the backend directory:

```env
# Google Calendar API
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Notion API
NOTION_TOKEN=your_notion_integration_token_here

# App Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### 3. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Upload & Parse

- `POST /api/upload-syllabus` - Upload and parse a PDF syllabus
- `GET /api/session/{session_id}` - Get parsed data for a session

### Export

- `POST /api/export/google-calendar` - Export to Google Calendar
- `POST /api/export/notion` - Export to Notion
- `GET /api/download/{session_id}` - Download parsed data as JSON

## API Documentation

Once the server is running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   └── routes/
│   │       ├── upload.py    # File upload endpoints
│   │       └── export.py    # Export endpoints
│   ├── services/
│   │   ├── pdf_parser.py    # PDF parsing logic
│   │   ├── google_calendar.py
│   │   └── notion_service.py
│   └── models/
│       └── syllabus.py      # Data models
├── requirements.txt
└── README.md
```

## Development

### Current Status

- ✅ Basic FastAPI structure
- ✅ PDF upload and parsing
- ✅ Export endpoints (simulated)
- ⏳ Google Calendar integration
- ⏳ Notion integration
- ⏳ Error handling and validation

### Next Steps

1. Implement actual Google Calendar OAuth flow
2. Implement actual Notion API integration
3. Add proper error handling and validation
4. Add database storage for sessions
5. Add authentication and rate limiting
