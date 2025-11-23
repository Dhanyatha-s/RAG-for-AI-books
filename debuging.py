import os 
# with open("data/extracted_pages.json", 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     print(f"Line 2: {lines[2408]}")  # -1 because Python is 0-indexed
#     print(f"Character at column 13: {repr(lines[18094][12])}")  

import json

file = r"C:\Users\DHANYATHA\OneDrive\Desktop\rag_book_system\data\extracted_pages.json"

with open(file, "r", encoding="utf-8") as f:
    data = f.read()

print("First 200 characters:\n", data[:200])
print("\nLast 200 characters:\n", data[-200:])
