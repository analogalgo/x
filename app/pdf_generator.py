from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

def build_pdf(output_path, month_year, first_name, letter_content):
    doc = SimpleDocTemplate(output_path, pagesize=letter,
        topMargin=1.0*inch, bottomMargin=0.75*inch,
        leftMargin=1.0*inch, rightMargin=1.0*inch)
        
    # Styles
    H = ParagraphStyle('H', fontName='Courier-Bold', fontSize=14, leading=18, alignment=TA_CENTER)
    D = ParagraphStyle('D', fontName='Courier', fontSize=8, leading=12, alignment=TA_CENTER, spaceAfter=20)
    B = ParagraphStyle('B', fontName='Times-Roman', fontSize=11, leading=16, alignment=TA_LEFT, spaceAfter=10)
    
    # Story
    story = [
        Paragraph("&#9824; &nbsp; &#9829; &nbsp; &#9827; &nbsp; &#9830;", H),
        Paragraph(month_year.upper(), D),
        Spacer(1, 12),
        Paragraph(f"Dear {first_name},", B),
        Spacer(1, 6)
    ]
    
    for para in letter_content.split('\n\n'):
        if para.strip():
            story.append(Paragraph(para.strip(), B))
            
    # Footer
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Courier', 6)
        canvas.drawCentredString(letter[0]/2, 0.4*inch, "THE ANALOG ALGORITHM")
        canvas.restoreState()
        
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return output_path
