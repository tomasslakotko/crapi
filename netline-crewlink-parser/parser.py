import pdfplumber
from itertools import groupby
import sys
import os
import re

# === FUNCTION: Simple but effective approach ===
def extract_roster_simple_approach(pdf):
    all_entries = []
    
    for page in pdf.pages:
        # Get all text with positioning
        text_objects = page.extract_words()
        
        # Find all date entries with their positions
        date_objects = []
        for obj in text_objects:
            if re.match(r'^[A-Z][a-z]{2}\d{2}$', obj['text']):
                date_objects.append(obj)
        
        # Process each date
        for date_obj in date_objects:
            date_str = date_obj['text']
            weekday = date_str[:3]
            day_num = date_str[3:]
            
            # Find all text objects near this date (same row, to the right)
            date_y = date_obj['top']
            date_x_end = date_obj['x1']
            
            # Look for objects in the same row (within 5 units vertically)
            row_objects = []
            for obj in text_objects:
                if abs(obj['top'] - date_y) < 5 and obj['x0'] > date_x_end:
                    row_objects.append(obj)
            
            # Sort by X position
            row_objects.sort(key=lambda x: x['x0'])
            
            # Build the text for this date's row
            row_text = ' '.join([obj['text'] for obj in row_objects])
            
            # Parse the row content
            if 'DAYOFF' in row_text:
                location_match = re.search(r'DAYOFF\s+([A-Z]{3})', row_text)
                location = location_match.group(1) if location_match else None
                all_entries.append({
                    'date': date_str,
                    'weekday': weekday,
                    'day_num': day_num,
                    'duty_type': 'DAYOFF',
                    'location': location
                })
            
            elif 'C/I' in row_text:
                ci_match = re.search(r'C/I\s+([A-Z]{3})\s+(\d{4})', row_text)
                if ci_match:
                    airport, time = ci_match.groups()
                    all_entries.append({
                        'date': date_str,
                        'weekday': weekday,
                        'day_num': day_num,
                        'duty_type': 'C/I',
                        'location': airport,
                        'time': time
                    })
            
            # Look for flights in subsequent rows (within reasonable distance)
            for obj in text_objects:
                if (obj['top'] > date_y + 5 and obj['top'] < date_y + 50 and 
                    abs(obj['x0'] - date_obj['x0']) < 100):  # Same column area
                    
                    # Check if this starts a flight line
                    flight_match = re.match(r'^[A-Z]{2}$', obj['text'])
                    if flight_match:
                        # Get the full flight line
                        flight_y = obj['top']
                        flight_objects = []
                        for flight_obj in text_objects:
                            if abs(flight_obj['top'] - flight_y) < 3:
                                flight_objects.append(flight_obj)
                        
                        flight_objects.sort(key=lambda x: x['x0'])
                        flight_text = ' '.join([fo['text'] for fo in flight_objects])
                        
                        # Parse flight information
                        flight_pattern = r'([A-Z]{2}\s+\d{3,4})\s+([A-Z]{3})\s+(\d{4})\s+(\d{4})\s+([A-Z]{3})\s*([A-Z0-9]*)'
                        flight_matches = re.findall(flight_pattern, flight_text)
                        
                        for flight_match in flight_matches:
                            flight_num, dep_airport, dep_time, arr_time, arr_airport, aircraft = flight_match
                            all_entries.append({
                                'date': date_str,
                                'weekday': weekday,
                                'day_num': day_num,
                                'duty_type': 'FLIGHT',
                                'flight_number': flight_num.strip(),
                                'dep_airport': dep_airport,
                                'dep_time': dep_time,
                                'arr_time': arr_time,
                                'arr_airport': arr_airport,
                                'aircraft': aircraft.strip() if aircraft else None
                            })
    
    return all_entries

# === MAIN PROCESS ===
try:
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        print("❌ Error: PDF path not provided.")
        sys.exit(1)

    output_dir = "."
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
        
    with pdfplumber.open(pdf_path) as pdf:
        parsed_data = extract_roster_simple_approach(pdf)

    # Sort by date
    parsed_data.sort(key=lambda x: int(x['day_num']))
    
    # Create clean text output
    clean_lines = []
    for entry in parsed_data:
        if entry['duty_type'] == 'DAYOFF':
            clean_lines.append(f"{entry['date']} DAYOFF {entry.get('location', '')}")
        elif entry['duty_type'] == 'C/I':
            clean_lines.append(f"{entry['date']} C/I {entry.get('location', '')} {entry.get('time', '')}")
        elif entry['duty_type'] == 'FLIGHT':
            clean_lines.append(f"{entry['date']} {entry['flight_number']} {entry['dep_airport']} {entry['dep_time']} {entry['arr_time']} {entry['arr_airport']} {entry.get('aircraft', '')}")

    # Save cleaned output
    combined_path = os.path.join(output_dir, "combined_cleaned_roster.txt")
    with open(combined_path, "w", encoding="utf-8") as f:
        f.write("\n".join(clean_lines))

    print(f"✅ Combined cleaned roster saved to {combined_path}")
    print(f"✅ Parsed {len(parsed_data)} entries")

except Exception as e:
    print(f"❌ Error processing PDF in parser.py: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
