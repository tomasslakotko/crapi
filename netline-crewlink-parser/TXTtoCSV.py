import re
import pandas as pd
from collections import defaultdict
import sys
import os

def parse_schedule_from_txt(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().strip().splitlines()

    parsed_data = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Parse date
        date_match = re.match(r'^([A-Z][a-z]{2})(\d{2})', line)
        if not date_match:
            continue
            
        weekday, day_num = date_match.groups()
        date_str = f"{weekday}{day_num}"
        
        # Remove date from line
        rest_of_line = line[5:].strip()
        
        if 'DAYOFF' in rest_of_line:
            # Parse DAYOFF entry
            location_match = re.search(r'DAYOFF\s+([A-Z]{3})', rest_of_line)
            location = location_match.group(1) if location_match else None
            
            parsed_data.append({
                "Date": date_str,
                "Weekday": weekday,
                "Day Number": day_num,
                "Duty Type": "DAYOFF",
                "Duty Location": location,
                "Check-In Airport": None,
                "Check-In Time": None,
                "Check-Out Time": None,
                "Hotel": None,
                "Flight Number": None,
                "Departure Airport": None,
                "Departure Time": None,
                "Arrival Time": None,
                "Arrival Airport": None,
                "Aircraft": None,
                "Requested": None,
                "Flight Time": None,
                "Duty Time": None,
                "Rest Time": None,
                "Meals": None
            })
            
        elif 'C/I' in rest_of_line:
            # Parse Check-In entry
            ci_match = re.search(r'C/I\s+([A-Z]{3})\s+(\d{4})', rest_of_line)
            if ci_match:
                airport, time = ci_match.groups()
                parsed_data.append({
                    "Date": date_str,
                    "Weekday": weekday,
                    "Day Number": day_num,
                    "Duty Type": "C/I",
                    "Duty Location": airport,
                    "Check-In Airport": airport,
                    "Check-In Time": time,
                    "Check-Out Time": None,
                    "Hotel": None,
                    "Flight Number": None,
                    "Departure Airport": None,
                    "Departure Time": None,
                    "Arrival Time": None,
                    "Arrival Airport": None,
                    "Aircraft": None,
                    "Requested": None,
                    "Flight Time": None,
                    "Duty Time": None,
                    "Rest Time": None,
                    "Meals": None
                })
                
        else:
            # Parse flight entry
            # Format: Tue01 OS 312 ARN 0805 1015 VIE A220
            flight_match = re.match(r'([A-Z]{2}\s+\d{3,4})\s+([A-Z]{3})\s+(\d{4})\s+(\d{4})\s+([A-Z]{3})\s*([A-Z0-9]*)\s*([RS]?)', rest_of_line)
            
            if flight_match:
                flight_num, dep_airport, dep_time, arr_time, arr_airport, aircraft, requested = flight_match.groups()
                
                parsed_data.append({
                    "Date": date_str,
                    "Weekday": weekday,
                    "Day Number": day_num,
                    "Duty Type": "FLIGHT",
                    "Duty Location": None,
                    "Check-In Airport": None,
                    "Check-In Time": None,
                    "Check-Out Time": None,
                    "Hotel": None,
                    "Flight Number": flight_num.strip(),
                    "Departure Airport": dep_airport,
                    "Departure Time": dep_time,
                    "Arrival Time": arr_time,
                    "Arrival Airport": arr_airport,
                    "Aircraft": aircraft.strip() if aircraft else None,
                    "Requested": requested == 'R' if requested else False,
                    "Flight Time": None,
                    "Duty Time": None,
                    "Rest Time": None,
                    "Meals": None
                })

    # Sort by date
    parsed_data.sort(key=lambda x: int(x['Day Number']))
    
    df = pd.DataFrame(parsed_data)
    return df

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        input_path = "combined_cleaned_roster.txt"  # default fallback
    
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    else:
        output_dir = "."
    
    output_path = os.path.join(output_dir, "parsed_schedule.csv")

    try:
        df = parse_schedule_from_txt(input_path)
        df.to_csv(output_path, index=False)
        print(f"✅ CSV saved to {output_path}")
        print(f"✅ Parsed {len(df)} entries")
    except Exception as e:
        print(f"❌ Error converting to CSV: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
