from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import upload, image_conversion

app = FastAPI(
    title="Syllabus Parser API",
    description="API for parsing syllabus PDFs and exporting to various platforms",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8080",
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(image_conversion.router, prefix="/api", tags=["image_conversion"])

@app.get("/")
async def root():
    return {"message": "Syllabus Parser API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 