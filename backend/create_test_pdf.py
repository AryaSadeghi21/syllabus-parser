#!/usr/bin/env python3
"""
Create a test PDF for testing the syllabus parser
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def create_test_pdf():
    """Create a test syllabus PDF"""
    filename = "test_syllabus.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, 10*inch, "CS 101: Introduction to Computer Science")
    
    # Course Info
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, 9.5*inch, "Course Information:")
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 9.2*inch, "Course Code: CS 101")
    c.drawString(1*inch, 9.0*inch, "Instructor: Dr. Smith")
    c.drawString(1*inch, 8.8*inch, "Semester: Fall 2024")
    
    # Schedule
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, 8.2*inch, "Class Schedule:")
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 7.9*inch, "Monday 9:00 AM - 10:30 AM Room 101")
    c.drawString(1*inch, 7.7*inch, "Wednesday 2:00 PM - 3:30 PM Lab A")
    
    # Assignments
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, 7.1*inch, "Assignments:")
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 6.8*inch, "Assignment 1 due: 01/15/2024")
    c.drawString(1*inch, 6.6*inch, "Assignment 2 due: 01/22/2024")
    c.drawString(1*inch, 6.4*inch, "Project 1 due: 02/01/2024")
    
    # Important Dates
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, 5.8*inch, "Important Dates:")
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 5.5*inch, "Midterm Exam: 02/15/2024")
    c.drawString(1*inch, 5.3*inch, "Final Exam: 05/10/2024")
    c.drawString(1*inch, 5.1*inch, "Spring Break: 03/15/2024")
    
    c.save()
    print(f"✅ Test PDF created: {filename}")

if __name__ == "__main__":
    create_test_pdf() 