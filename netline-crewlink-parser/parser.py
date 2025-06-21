import pdfplumber
from itertools import groupby
import sys
import os

# === FUNCTION: Extract lines from one half ===
def extract_column_lines(pdf, column):
    lines = []
    # Adjust split_x to be more robust, in case there's no perfect center split
    split_x = pdf.pages[0].width / 2

    for page in pdf.pages:
        # Use extract_text_lines for better line-by-line accuracy
        all_lines = page.extract_text_lines(layout=True, strip=True)
        
        # Filter lines based on column
        if column == "left":
            page_lines = [line['text'] for line in all_lines if line['x0'] < split_x]
        else:
            page_lines = [line['text'] for line in all_lines if line['x0'] >= split_x]
        
        lines.extend(page_lines)

    return lines

# === FUNCTION: Clean out headers and footers ===
def clean_roster_text(lines):
    cleaned = []
    # Start capturing immediately and filter out unwanted lines
    for line in lines:
        # Stop at common footers or summary sections
        if "Individual duty plan for" in line or \
           "NetLine/Crew" in line or \
           line.strip().lower().startswith("flight time") or \
           line.strip().lower().startswith("hotels"):
            continue

        # Skip the header line if it exists, but don't depend on it
        if line.strip() == "date H duty R dep arr AC info":
            continue
            
        cleaned.append(line)

    return cleaned

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
        left_raw = extract_column_lines(pdf, "left")
        right_raw = extract_column_lines(pdf, "right")

    # Clean both columns
    left_cleaned = clean_roster_text(left_raw)
    right_cleaned = clean_roster_text(right_raw)

    # Combine all lines
    combined_all = left_cleaned + right_cleaned
    
    # Simple filtering for obviously empty or junk lines
    combined_all = [line for line in combined_all if line.strip()]

    # Group by lines that start with a weekday + day number
    import re
    day_start_pattern = re.compile(r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\d{2}")
    blocks = []
    current_block = []
    current_day = None

    # Sort lines based on a rough vertical position heuristic if possible, though it's complex.
    # For now, we assume reasonable order from text extraction.
    
    # Consolidate multi-line entries into blocks
    for line in combined_all:
        if day_start_pattern.match(line):
            if current_block:
                blocks.append(current_block)
            current_block = [line]
        elif current_block:
            current_block.append(line)

    if current_block:
        blocks.append(current_block)

    # Define real calendar order for sorting
    weekday_order = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
    def block_sort_key(block):
        day_str = block[0][:3]
        date_num_match = re.search(r'\d{2}', block[0])
        if not date_num_match: return 99 # Push blocks without a date to the end
        date_num = int(date_num_match.group(0))
        return date_num + weekday_order.get(day_str, 7) / 10

    # Sort blocks
    sorted_blocks = sorted(blocks, key=block_sort_key)

    # Flatten back into lines
    sorted_lines = [line for block in sorted_blocks for line in block]

    # Save
    combined_path = os.path.join(output_dir, "combined_cleaned_roster.txt")
    with open(combined_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted_lines))

    print(f"✅ Combined cleaned roster saved to {combined_path}")

except Exception as e:
    print(f"❌ Error processing PDF in parser.py: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
