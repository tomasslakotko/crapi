import re
import pandas as pd
from collections import defaultdict
import sys
import os

def parse_schedule_from_txt(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().strip().splitlines()

    day_pattern = re.compile(r'^[A-Z][a-z]{2}\d{2}')
    daily_blocks = defaultdict(list)

    current_day = None
    for line in lines:
        # Heuristic to handle lines that might belong to the previous day
        if day_pattern.match(line) or not current_day:
            current_day = line.strip()
        
        daily_blocks[current_day].append(line.strip())

    updated_data = []

    for day, lines in daily_blocks.items():
        first_line = lines[0]
        
        # More specific regex for duty types to avoid capturing airline codes
        duty_type_pattern = r'(C/I|C/O|SBY|DAYOFF|OFF|VACATION|[A-Z]{3,})'
        
        match = re.match(r'^([A-Z][a-z]{2})(\d{2})(?:\s+' + duty_type_pattern + r')?(?:\s+([A-Z]{3}))?', first_line)
        
        if match:
            weekday, day_num, duty_type, duty_location = match.groups()
            date_str = f"{weekday}{day_num}"
        else:
            # Fallback for lines like "Thu19" with no duty type on the same line
            day_match = re.match(r'^([A-Z][a-z]{2})(\d{2})', first_line)
            if day_match:
                weekday, day_num = day_match.groups()
                date_str = f"{weekday}{day_num}"
                duty_type, duty_location = None, None
            else:
                # Skip blocks that don't start with a valid day
                continue

        check_in_time = None
        check_out_time = None
        check_in_airport = None
        check_out_airport = None
        hotel = None
        flight_time = duty_time = rest_time = None
        meals = []
        duty_flights = []

        for line in lines:
            # Avoid re-parsing the main duty type from the first line if it's already set
            if "C/I" in line and not duty_type:
                match = re.search(r'C/I\s+([A-Z]{3})\s+(\d{4})', line)
                if match:
                    check_in_airport, check_in_time = match.groups()
                    duty_type = "C/I"
            elif "C/O" in line:
                match = re.search(r'C/O\s+!?(\d{4})\s+([A-Z]{3})', line)
                if match:
                    check_out_time, check_out_airport = match.groups()
            elif re.match(r'^H\d+\s+[A-Z]{3}$', line):
                hotel = line
            elif line.startswith("[FT"):
                match = re.search(r'\[FT\s+([\d:]+)\]', line)
                if match:
                    flight_time = match.group(1)
            elif line.startswith("[DT") or line.startswith("[DP"):
                match = re.search(r'\[D[T|P]\s+([\d:]+)\]', line)
                if match:
                    duty_time = match.group(1)
            elif line.startswith("[RT"):
                match = re.search(r'\[RT\s+([\d:]+)\]', line)
                if match:
                    rest_time = match.group(1)
            elif "meal" in line.lower():
                meals.append(line)
            else:
                # Generic flight pattern matcher for formats like 'OS 453' and 'AZ 1234'
                flight_match = re.match(
                    r'^\s*([A-Z]{2}\s+\d{1,4})(?:\s+R)?\s+([A-Z]{3})\s+(\d{4})\s+(!?\s*\d{4}(?:\+\d)?)\s+([A-Z]{3})\s*([\w\d]*)?',
                    line
                )
                if flight_match:
                    groups = flight_match.groups()
                    flight_number = groups[0].strip()
                    dep_airport = groups[1].strip()
                    dep_time = groups[2].strip()
                    arr_time = groups[3].strip()
                    arr_airport = groups[4].strip()
                    aircraft = groups[5].strip() if len(groups) > 5 and groups[5] else None
                    
                    duty_flights.append({
                        "Flight Number": flight_number,
                        "Departure Airport": dep_airport,
                        "Departure Time": dep_time,
                        "Arrival Time": arr_time,
                        "Arrival Airport": arr_airport,
                        "Aircraft": aircraft,
                        "Requested": "R" in line
                    })

        if not duty_flights:
            # Do not create rows for standalone C/I or C/O entries
            if duty_type not in ['C/I', 'C/O']:
                updated_data.append({
                    "Date": date_str,
                    "Weekday": weekday,
                    "Day Number": day_num,
                    "Duty Type": duty_type,
                    "Duty Location": duty_location,
                    "Check-In Airport": check_in_airport,
                    "Check-In Time": check_in_time,
                    "Check-Out Time": check_out_time,
                    "Hotel": hotel,
                    "Flight Number": None,
                    "Departure Airport": None,
                    "Departure Time": None,
                    "Arrival Time": None,
                    "Arrival Airport": None,
                    "Aircraft": None,
                    "Requested": None,
                    "Flight Time": flight_time,
                    "Duty Time": duty_time,
                    "Rest Time": rest_time,
                    "Meals": ", ".join(meals)
                })
        else:
            for flight in duty_flights:
                updated_data.append({
                    "Date": date_str,
                    "Weekday": weekday,
                    "Day Number": day_num,
                    "Duty Type": 'FLIGHT', # Always mark rows with flights as 'FLIGHT'
                    "Duty Location": duty_location,
                    "Check-In Airport": check_in_airport,
                    "Check-In Time": check_in_time,
                    "Check-Out Time": check_out_time,
                    "Hotel": hotel,
                    "Flight Number": flight["Flight Number"],
                    "Departure Airport": flight["Departure Airport"],
                    "Departure Time": flight["Departure Time"],
                    "Arrival Time": flight["Arrival Time"],
                    "Arrival Airport": flight["Arrival Airport"],
                    "Aircraft": flight["Aircraft"],
                    "Requested": flight["Requested"],
                    "Flight Time": flight_time,
                    "Duty Time": duty_time,
                    "Rest Time": rest_time,
                    "Meals": ", ".join(meals)
                })

    df = pd.DataFrame(updated_data)
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
        print(f"CSV saved to {output_path}")
    except Exception as e:
        print(f"❌ Error converting to CSV: {e}")
        sys.exit(1)
