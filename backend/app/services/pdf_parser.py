import pdfplumber
import re
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

class PDFParser:
    def __init__(self):
        self.text_content = ""
        self.tables = []
        self.parsed_data = {}
        
    def parse_pdf(self, file_path: str, semester_start_date: str | None = None) -> Dict[str, Any]:
        """
        Parse a PDF file and extract structured syllabus data using pdfplumber
        """
        try:
            # Extract text and tables
            self.text_content, self.tables = self._extract_text_and_tables(file_path)
            
            # Store semester start date for reference
            self.semester_start_date = semester_start_date
            
            # Parse different sections with improved algorithms
            self.parsed_data = {
                "course_info": self._extract_course_info_improved(),
                "assignments": self._extract_assignments_improved(),
                "schedule": self._extract_schedule_improved(),
                "important_dates": self._extract_important_dates_improved(),
                "raw_text": self.text_content[:1000] + "..." if len(self.text_content) > 1000 else self.text_content
            }
            
            return self.parsed_data
            
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def _extract_text_and_tables(self, file_path: str) -> tuple[str, List]:
        """
        Extract text content and tables from PDF file
        """
        text = ""
        tables = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # Extract text
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    
                    # Extract tables
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)
            
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
        
        return text, tables
    
    def _extract_course_info_improved(self) -> Dict[str, str]:
        """
        Extract basic course information with improved pattern matching
        """
        course_info = {
            "course_name": "",
            "course_code": "",
            "instructor": "",
            "semester": "",
            "year": ""
        }
        
        # Look for course info in text
        lines = self.text_content.split('\n')
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Course name patterns (more comprehensive)
            if any(keyword in line_lower for keyword in ['course:', 'class:', 'subject:', 'course title:', 'course name:']):
                # Extract the part after the colon
                match = re.search(r'(?:course|class|subject|course title|course name):\s*([^\n]+)', line, re.IGNORECASE)
                if match:
                    course_info["course_name"] = match.group(1).strip()
            
            # Course code patterns (more flexible)
            code_match = re.search(r'([A-Z]{2,4}\s*\d{3,4}[A-Z]?)', line, re.IGNORECASE)
            if code_match and not course_info["course_code"]:
                course_info["course_code"] = code_match.group(1).upper()
            
            # Instructor patterns
            if any(keyword in line_lower for keyword in ['instructor:', 'professor:', 'teacher:', 'faculty:', 'lecturer:']):
                match = re.search(r'(?:instructor|professor|teacher|faculty|lecturer):\s*([^\n]+)', line, re.IGNORECASE)
                if match:
                    course_info["instructor"] = match.group(1).strip()
            
            # Semester/Year patterns
            semester_match = re.search(r'(spring|summer|fall|winter)\s*(\d{4})', line_lower)
            if semester_match:
                course_info["semester"] = semester_match.group(1).capitalize()
                course_info["year"] = semester_match.group(2)
        
        return course_info
    
    def _extract_assignments_improved(self) -> List[Dict[str, str]]:
        """
        Extract assignment information with improved pattern matching
        """
        assignments = []
        
        # Look for assignment sections in text
        assignment_keywords = ['assignment', 'homework', 'project', 'essay', 'paper', 'lab', 'quiz', 'exam']
        
        lines = self.text_content.split('\n')
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line contains assignment-related content
            if any(keyword in line_lower for keyword in assignment_keywords):
                # Extract assignment number/title
                assignment_match = re.search(r'(assignment|homework|project|essay|paper|lab|quiz|exam)\s*#?\s*(\d+|[IVX]+)', line_lower)
                
                if assignment_match:
                    assignment_type = assignment_match.group(1)
                    assignment_num = assignment_match.group(2)
                    
                    # Extract due date (multiple formats)
                    date_patterns = [
                        r'due\s*:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                        r'due\s*date\s*:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                        r'(\d{4}-\d{2}-\d{2})'
                    ]
                    
                    due_date = ""
                    for pattern in date_patterns:
                        date_match = re.search(pattern, line, re.IGNORECASE)
                        if date_match:
                            due_date = date_match.group(1)
                            break
                    
                    assignment = {
                        "title": f"{assignment_type.capitalize()} {assignment_num}",
                        "due_date": due_date,
                        "description": line[:200] + "..." if len(line) > 200 else line
                    }
                    assignments.append(assignment)
        
        # Also check tables for assignments
        for table in self.tables:
            for row in table:
                if row and any(cell and any(keyword in str(cell).lower() for keyword in assignment_keywords) for cell in row):
                    # Process table row as assignment
                    row_text = " ".join([str(cell) for cell in row if cell])
                    if any(keyword in row_text.lower() for keyword in assignment_keywords):
                        assignment_match = re.search(r'(assignment|homework|project|essay|paper|lab|quiz|exam)\s*#?\s*(\d+|[IVX]+)', row_text.lower())
                        if assignment_match:
                            assignment_type = assignment_match.group(1)
                            assignment_num = assignment_match.group(2)
                            
                            # Extract due date
                            date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', row_text)
                            due_date = date_match.group(1) if date_match else ""
                            
                            assignment = {
                                "title": f"{assignment_type.capitalize()} {assignment_num}",
                                "due_date": due_date,
                                "description": row_text
                            }
                            assignments.append(assignment)
        
        return assignments
    
    def _extract_schedule_improved(self) -> List[Dict[str, str]]:
        """
        Extract class schedule information with improved pattern matching
        """
        schedule = []
        
        # Look for schedule patterns in text
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        
        lines = self.text_content.split('\n')
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line contains schedule information
            if any(day in line_lower for day in days):
                # Extract day
                day_found = ""
                for day in days:
                    if day in line_lower:
                        day_found = day.capitalize()
                        break
                
                # Extract time (multiple formats)
                time_patterns = [
                    r'(\d{1,2}:\d{2}\s*[AP]M)',
                    r'(\d{1,2}:\d{2})',
                    r'(\d{1,2}[AP]M)'
                ]
                
                time_found = ""
                for pattern in time_patterns:
                    time_match = re.search(pattern, line, re.IGNORECASE)
                    if time_match:
                        time_found = time_match.group(1)
                        break
                
                # Extract location (room/building)
                location_patterns = [
                    r'room\s*(\d+)',
                    r'building\s*([A-Z]+)',
                    r'([A-Z]+\s*\d+)',  # Common room format like "HSS 101"
                ]
                
                location_found = ""
                for pattern in location_patterns:
                    location_match = re.search(pattern, line, re.IGNORECASE)
                    if location_match:
                        location_found = location_match.group(1)
                        break
                
                schedule_item = {
                    "day": day_found,
                    "time": time_found,
                    "location": location_found,
                    "description": line
                }
                schedule.append(schedule_item)
        
        # Also check tables for schedule
        for table in self.tables:
            for row in table:
                if row and any(cell and any(day in str(cell).lower() for day in days) for cell in row):
                    row_text = " ".join([str(cell) for cell in row if cell])
                    if any(day in row_text.lower() for day in days):
                        # Extract schedule info from table row
                        day_found = ""
                        for day in days:
                            if day in row_text.lower():
                                day_found = day.capitalize()
                                break
                        
                        time_match = re.search(r'(\d{1,2}:\d{2}\s*[AP]M)', row_text, re.IGNORECASE)
                        time_found = time_match.group(1) if time_match else ""
                        
                        location_match = re.search(r'([A-Z]+\s*\d+)', row_text)
                        location_found = location_match.group(1) if location_match else ""
                        
                        schedule_item = {
                            "day": day_found,
                            "time": time_found,
                            "location": location_found,
                            "description": row_text
                        }
                        schedule.append(schedule_item)
        
        return schedule
    
    def _extract_important_dates_improved(self) -> List[Dict[str, str]]:
        """
        Extract important dates and deadlines with improved pattern matching
        """
        important_dates = []
        
        # Keywords for important dates
        date_keywords = ['deadline', 'due', 'exam', 'test', 'final', 'midterm', 'holiday', 'break', 'deadline']
        
        lines = self.text_content.split('\n')
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line contains important date information
            if any(keyword in line_lower for keyword in date_keywords):
                # Extract the event title
                event_title = line.strip()
                
                # Extract date (multiple formats)
                date_patterns = [
                    r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                    r'(\d{4}-\d{2}-\d{2})',
                    r'(\w+\s+\d{1,2},?\s+\d{4})',  # "January 15, 2024"
                ]
                
                date_found = ""
                for pattern in date_patterns:
                    date_match = re.search(pattern, line, re.IGNORECASE)
                    if date_match:
                        date_found = date_match.group(1)
                        break
                
                date_item = {
                    "title": event_title,
                    "date": date_found,
                    "description": line
                }
                important_dates.append(date_item)
        
        return important_dates 