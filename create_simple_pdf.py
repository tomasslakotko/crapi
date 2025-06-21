from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def create_simple_pdf():
    # Create PDF with simple text layout
    c = canvas.Canvas("simple_roster.pdf", pagesize=letter)
    width, height = letter
    
    # Set font and size
    c.setFont("Helvetica", 10)
    
    # Add title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Lufthansa Netline Crewlink - Individual Duty Plan")
    
    # Add header
    c.setFont("Helvetica", 10)
    y_position = height - 100
    
    header_text = "date H duty R dep arr AC info"
    c.drawString(50, y_position, header_text)
    y_position -= 20
    
    # Add schedule data
    schedule_lines = [
        "Mon01",
        "C/I FRA 0800",
        "AZ 1234 FRA 0900 1100 MUC A320",
        "H1 MUC",
        "[FT 02:00] [DT 04:00] [RT 10:00]",
        "",
        "Tue02",
        "AZ 5678 MUC 0700 0900 FRA A320",
        "C/O 1000 FRA",
        "[FT 02:00] [DT 03:00] [RT 11:00]",
        "",
        "Wed03",
        "C/I FRA 0600",
        "AZ 9012 FRA 0700 1300 JFK A350",
        "H2 JFK",
        "meal breakfast",
        "[FT 06:00] [DT 08:00] [RT 16:00]",
        "",
        "Thu04",
        "AZ 3456 JFK 0800 2000 FRA A350",
        "C/O 2100 FRA",
        "meal lunch, dinner",
        "[FT 12:00] [DT 14:00] [RT 10:00]"
    ]
    
    for line in schedule_lines:
        c.drawString(50, y_position, line)
        y_position -= 15
    
    # Add footer
    c.drawString(50, y_position - 20, "Individual duty plan for Crew Member - NetLine/Crew")
    
    c.save()
    print("✅ Simple PDF created: simple_roster.pdf")

if __name__ == "__main__":
    create_simple_pdf() 