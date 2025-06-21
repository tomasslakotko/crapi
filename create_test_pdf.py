from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
import os

def create_test_pdf():
    # Create PDF document
    doc = SimpleDocTemplate("test_roster.pdf", pagesize=letter)
    story = []
    
    # Add title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=getSampleStyleSheet()['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    title = Paragraph("Lufthansa Netline Crewlink - Individual Duty Plan", title_style)
    story.append(title)
    
    # Add header
    header_data = [['date', 'H', 'duty', 'R', 'dep', 'arr', 'AC', 'info']]
    header_table = Table(header_data, colWidths=[60, 30, 60, 30, 60, 60, 60, 60])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0, 0), (-1, 0), 1, colors.black)
    ]))
    story.append(header_table)
    
    # Add schedule data
    schedule_data = [
        ['Mon01', '', 'C/I', '', 'FRA', '0800', '', ''],
        ['', '', 'AZ 1234', 'R', 'FRA', '0900', '1100', 'MUC A320'],
        ['', '', 'H1 MUC', '', '', '', '', ''],
        ['', '', '[FT 02:00]', '', '[DT 04:00]', '[RT 10:00]', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['Tue02', '', 'AZ 5678', '', 'MUC', '0700', '0900', 'FRA A320'],
        ['', '', 'C/O', '', '1000', 'FRA', '', ''],
        ['', '', '[FT 02:00]', '', '[DT 03:00]', '[RT 11:00]', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['Wed03', '', 'C/I', '', 'FRA', '0600', '', ''],
        ['', '', 'AZ 9012', 'R', 'FRA', '0700', '1300', 'JFK A350'],
        ['', '', 'H2 JFK', '', '', '', '', ''],
        ['', '', 'meal breakfast', '', '', '', '', ''],
        ['', '', '[FT 06:00]', '', '[DT 08:00]', '[RT 16:00]', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['Thu04', '', 'AZ 3456', '', 'JFK', '0800', '2000', 'FRA A350'],
        ['', '', 'C/O', '', '2100', 'FRA', '', ''],
        ['', '', 'meal lunch, dinner', '', '', '', '', ''],
        ['', '', '[FT 12:00]', '', '[DT 14:00]', '[RT 10:00]', '', '']
    ]
    
    schedule_table = Table(schedule_data, colWidths=[60, 30, 120, 30, 60, 60, 60, 80])
    schedule_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightblue),
    ]))
    story.append(schedule_table)
    
    # Add footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=getSampleStyleSheet()['Normal'],
        fontSize=8,
        spaceBefore=30,
        alignment=1
    )
    footer = Paragraph("Individual duty plan for Crew Member - NetLine/Crew", footer_style)
    story.append(footer)
    
    # Build PDF
    doc.build(story)
    print("✅ Test PDF created: test_roster.pdf")

if __name__ == "__main__":
    create_test_pdf() 