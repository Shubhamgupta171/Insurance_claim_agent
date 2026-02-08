"""
Utility script to convert text FNOL documents to PDF format.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT
from pathlib import Path


def text_to_pdf(text_file: str, pdf_file: str):
    """
    Convert a text file to PDF format.
    
    Args:
        text_file: Path to input text file
        pdf_file: Path to output PDF file
    """
    # Read text content
    with open(text_file, 'r') as f:
        content = f.read()
    
    # Create PDF
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Styles
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=TA_LEFT
    )
    
    # Build content
    story = []
    lines = content.split('\n')
    
    for line in lines:
        if line.strip():
            para = Paragraph(line, normal_style)
            story.append(para)
            story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Spacer(1, 0.15*inch))
    
    # Generate PDF
    doc.build(story)
    print(f"Created: {pdf_file}")


def convert_all_samples():
    """Convert all sample text files to PDFs"""
    sample_dir = Path("tests/sample_fnol")
    
    # Find all .txt files
    txt_files = list(sample_dir.glob("*.txt"))
    
    if not txt_files:
        print("No text files found in tests/sample_fnol/")
        return
    
    print(f"Converting {len(txt_files)} sample files to PDF...\n")
    
    for txt_file in txt_files:
        pdf_file = txt_file.with_suffix('.pdf')
        text_to_pdf(str(txt_file), str(pdf_file))
    
    print(f"\n✓ Converted {len(txt_files)} files successfully!")
    print(f"PDF files are ready in: {sample_dir}")


if __name__ == "__main__":
    convert_all_samples()
