from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CourseInfo(BaseModel):
    course_name: str = ""
    course_code: str = ""
    instructor: str = ""
    semester: str = ""
    year: str = ""

class Assignment(BaseModel):
    title: str
    due_date: Optional[str] = None
    description: str = ""

class ScheduleItem(BaseModel):
    day: str = ""
    time: str = ""
    location: str = ""
    description: str = ""

class ImportantDate(BaseModel):
    title: str
    date: Optional[str] = None
    description: str = ""

class SyllabusData(BaseModel):
    course_info: CourseInfo
    assignments: List[Assignment] = []
    schedule: List[ScheduleItem] = []
    important_dates: List[ImportantDate] = []
    raw_text: str = ""

class ExportRequest(BaseModel):
    session_id: str
    calendar_id: Optional[str] = "primary"
    database_id: Optional[str] = None

class UploadResponse(BaseModel):
    success: bool
    session_id: str
    message: str
    data: SyllabusData

class ExportResponse(BaseModel):
    success: bool
    message: str
    events_created: Optional[int] = None
    pages_created: Optional[int] = None 