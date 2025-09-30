from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
import uuid
import tempfile
import os
from datetime import datetime
from app.services.pdf_parser import PDFParser
from app.models.syllabus import SyllabusData

router = APIRouter()

# In-memory storage for demo (use database in production)
sessions = {}

@router.post("/upload-syllabus")
async def upload_syllabus(
    file: UploadFile = File(...),
    semester_start_date: str = Form(None)
):
    """
    Upload and parse a syllabus PDF file with semester start date
    """
    try:
        # Validate file type
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Validate file size (max 10MB)
        if file.size and file.size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size too large. Maximum 10MB allowed")
        
        # Validate semester start date
        if semester_start_date:
            try:
                datetime.strptime(semester_start_date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Create session ID
        session_id = str(uuid.uuid4())
        
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Parse PDF with semester start date context
            parser = PDFParser()
            parsed_data = parser.parse_pdf(temp_file_path, semester_start_date)
            
            # Store session data including raw PDF path
            sessions[session_id] = {
                "file_path": temp_file_path,
                "parsed_data": parsed_data,
                "filename": file.filename,
                "semester_start_date": semester_start_date,
                "raw_pdf_path": temp_file_path  # Keep reference to raw PDF
            }
            
            return JSONResponse(content={
                "success": True,
                "session_id": session_id,
                "message": "Syllabus parsed successfully",
                "data": parsed_data,
                "semester_start_date": semester_start_date
            })
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise HTTPException(status_code=500, detail=f"Error parsing PDF: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    """
    Extract text from a PDF file
    """
    try:
        # Validate file type
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Validate file size (max 10MB)
        if file.size and file.size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size too large. Maximum 10MB allowed")
        
        # Create session ID
        session_id = str(uuid.uuid4())
        
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Extract text using the PDF parser
            parser = PDFParser()
            parsed_data = parser.parse_pdf(temp_file_path)
            
            # Get the raw text content
            extracted_text = parser.text_content
            
            return JSONResponse(content={
                "success": True,
                "session_id": session_id,
                "total_pages": len(parsed_data.get("raw_text", "").split("...")),
                "extracted_text": extracted_text,
                "file_name": file.filename
            })
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/export-pdf/{session_id}")
async def export_raw_pdf(session_id: str):
    """
    Export the raw PDF file for n8n automation
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[session_id]
    pdf_path = session_data.get("raw_pdf_path")
    filename = session_data.get("filename", "syllabus.pdf")
    
    if not pdf_path or not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    return FileResponse(
        path=pdf_path,
        filename=filename,
        media_type="application/pdf"
    )

@router.get("/session/{session_id}")
async def get_session_data(session_id: str):
    """
    Get parsed data for a session
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "success": True,
        "session_id": session_id,
        "data": sessions[session_id]["parsed_data"],
        "semester_start_date": sessions[session_id].get("semester_start_date")
    } 