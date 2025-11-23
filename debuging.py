import os 
# with open("data/extracted_pages.json", 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     print(f"Line 2: {lines[2408]}")  # -1 because Python is 0-indexed
#     print(f"Character at column 13: {repr(lines[18094][12])}")  

# import json

# file = r"C:\Users\DHANYATHA\OneDrive\Desktop\rag_book_system\data\extracted_pages.json"

# with open(file, "r", encoding="utf-8") as f:
#     data = f.read()

# print("First 200 characters:\n", data[:200])
# print("\nLast 200 characters:\n", data[-200:])


import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import chromadb

# Initializing Google Gemini ai
load_dotenv()  
# print("\n🧠 Initializing Google Gemini...")
# print("\n Akal larahehai bidu.....")

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: API Key is not found in .env file")
    exit(1)
# After: genai.configure(api_key=api_key)
# Add this:
print("\n🔍 Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"   - {m.name}")


# from dotenv import load_dotenv
# import os

# load_dotenv()  # Reads .env file automatically

# api_key = os.getenv("GOOGLE_API_KEY")

# print("API Key:", api_key)