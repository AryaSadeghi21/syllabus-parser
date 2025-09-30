#!/usr/bin/env python3
"""
Test script for PDF parser
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.pdf_parser import PDFParser

def test_pdf_parser(pdf_path):
    """Test the PDF parser with a given PDF file"""
    try:
        parser = PDFParser()
        print(f"Testing PDF parser with: {pdf_path}")
        print("-" * 50)
        
        # Parse the PDF
        result = parser.parse_pdf(pdf_path)
        
        # Print results
        print("✅ PDF parsed successfully!")
        print("\n📋 Course Info:")
        for key, value in result["course_info"].items():
            print(f"  {key}: {value}")
        
        print(f"\n📚 Assignments found: {len(result['assignments'])}")
        for i, assignment in enumerate(result["assignments"], 1):
            print(f"  {i}. {assignment['title']} (Due: {assignment['due_date']})")
        
        print(f"\n📅 Schedule items found: {len(result['schedule'])}")
        for i, item in enumerate(result["schedule"], 1):
            print(f"  {i}. {item['day']} {item['time']} - {item['description']}")
        
        print(f"\n📆 Important dates found: {len(result['important_dates'])}")
        for i, date_item in enumerate(result["important_dates"], 1):
            print(f"  {i}. {date_item['title']} (Date: {date_item['date']})")
        
        print(f"\n📄 Raw text preview (first 200 chars):")
        print(result["raw_text"][:200] + "...")
        
        return result
        
    except Exception as e:
        print(f"❌ Error parsing PDF: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 test_pdf_parser.py <path_to_pdf>")
        print("Example: python3 test_pdf_parser.py sample_syllabus.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        sys.exit(1)
    
    test_pdf_parser(pdf_path) 