from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from pdf2image import convert_from_bytes
from io import BytesIO
import base64
import os
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/convert-pdf-to-images")
async def convert_pdf(
    file: UploadFile = File(...),
    save_to_folder: bool = Form(False)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        pdf_bytes = await file.read()
        images = convert_from_bytes(pdf_bytes)
        result = []
        
        # Create unique folder for this conversion
        conversion_id = str(uuid.uuid4())
        folder_path = f"converted_images/{conversion_id}"
        
        if save_to_folder:
            os.makedirs(folder_path, exist_ok=True)
        
        for i, image in enumerate(images):
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            # Save to file if requested
            if save_to_folder:
                image_path = f"{folder_path}/page_{i+1}.png"
                image.save(image_path, "PNG")
            
            result.append({
                "page": i + 1,
                "data": f"data:image/png;base64,{img_str}",
                "file_path": f"{folder_path}/page_{i+1}.png" if save_to_folder else None
            })

        return JSONResponse(content={
            "conversion_id": conversion_id,
            "folder_path": folder_path if save_to_folder else None,
            "total_pages": len(images),
            "images_folder": {
                "folder_name": f"syllabus_images_{conversion_id}",
                "total_pages": len(images),
                "pages": result
            }
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
