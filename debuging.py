import os 
with open("data/extracted_pages.json", 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"Line 2: {lines[2408]}")  # -1 because Python is 0-indexed
    print(f"Character at column 13: {repr(lines[18094][12])}")  