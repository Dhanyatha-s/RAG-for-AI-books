
import json
import os
# from langchain_text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter



# ------------------------
# Configure
# -------------------------

INPUT_FILE = "data/extracted_pages.json"
OUTPUT_FILE = "data/chunked_data.json"

CHUNK_SIZE = 800       # Target characters per chunk
CHUNK_OVERLAP = 200    # Overlap between adjacent chunks

# Load the data from the data/extracted.json

print(f"Loading the input file {INPUT_FILE}")

try:

    with open(INPUT_FILE, "r", encoding='utf-8') as f:
        all_books = json.load(f)

        print(f"✅ Loaded {len(all_books)} pages")
except Exception as e:
    print(f"❌ Error loading file: {str(e)}")
    exit(1)


# Initializing Text Splitter
print(f"\n⚙️  Initializing text splitter...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = CHUNK_SIZE,
    chunk_overlap = CHUNK_OVERLAP,
    length_function = len,
    separators=["\n\n", "\n", ". ", " ", ""]
)

# Chunk the Text
print(f"\n  Chunking the text...")
chunked_data = []
total_chars_before = 0
total_chars_after = 0

for idx, page_data in enumerate(all_books):
    # track chars counts
    total_chars_before += len(page_data["text"])

    # Split the page text into chunks
    chunks = text_splitter.split_text(page_data["text"])

    # Store each chunk with metadata
    for chunk_idx, chunk_text in enumerate(chunks):
        chunk_data = {
            "chunk_id": f"{page_data['book_name']}_p{page_data['page_number']}_c{chunk_idx}",
            "book_name": page_data["book_name"],
            "page_number": page_data["page_number"],
            "chunk_index": chunk_idx,
            "total_chunks_in_page": len(chunks),
            "text": chunk_text,
            "char_count": len(chunk_text)
        }
        chunked_data.append(chunk_data)
        total_chars_after += len(chunk_text)

    # Print progress every 100 pages
    if (idx + 1) % 100 == 0:
        print(f"   Progress: {idx + 1}/{len(all_books)} pages chunked...")

print(f"\n✅ Chunking complete!")