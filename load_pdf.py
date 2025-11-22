import PyPDF2
import os
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter


books_folder = r'C:\Users\DHANYATHA\OneDrive\Desktop\rag_book_system\Books'

# Finding All PDFs
pdf_files = [f for f in os.listdir(books_folder) if f.endswith(".pdf") ]

print(f"Found {len(pdf_files)}s Files in the folder ")
for i, pdf in enumerate(pdf_files,1):
    print(f"{i}.{pdf}")


# Store all the books
all_books = []
# Process each pdfs

for pdf_filename in pdf_files:
    print(f"\nProcessing: {pdf_filename}")
    print("- " * 60)

    # get full path of each pdfs
    pdf_path = os.path.join(books_folder, pdf_filename)
    try:

        # open pdf
        pdf_file = open(pdf_path, "rb")

        # reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # get Num of pages
        num_pages = len(pdf_reader.pages)

        print(f"Total Pages: {num_pages}")

        extracted_count = 0
        failed_count =0

        # Extract Pages
        for page_num in range(num_pages):
            try:
                page = pdf_reader.pages[page_num]
                text = page.extract_text()

                if text and len(text.strip()) > 10:
                    page_data = {
                        "book_name": pdf_filename,
                        "page_number": page_num,
                        "text":text
                    }
                    all_books.append(page_data)
                    extracted_count += 1

                    if extracted_count % 50 == 0:
                        print(f"   ✅ Extracted {extracted_count} pages...")
                else:
                    failed_count += 1
                
            

            except Exception as e:
                failed_count += 1
                # Only print error for first few failures
                if failed_count <= 3:
                    print(f"   ❌ Error on page {page_num + 1}: {str(e)[:40]}...")
        
        # Close the file
        pdf_file.close()

        print(f"   ✅ Done: {extracted_count} pages extracted, {failed_count} skipped")
        
    except Exception as e:
        print(f"   ❌ Failed to process {pdf_filename}: {str(e)}")
        continue
    

# Final summary
# print("\n" + "="*60)
# print("🎉 EXTRACTION COMPLETE!")
# print("="*60)
# print(f"Total books processed: {len(pdf_files)}")
# print(f"Total pages extracted: {len(all_books)}")

# Show breakdown by book
# print("\n📊 Breakdown by book:")
# from collections import Counter
# book_page_counts = Counter([item["book_name"] for item in all_books])
# for book, count in book_page_counts.items():
#     print(f"   {book}: {count} pages")

# Show a sample from the first book
# if all_books:
#     print("\n--- SAMPLE FROM FIRST PAGE ---")
#     print(f"Book: {all_books[0]['book_name']}")
#     print(f"Page: {all_books[0]['page_number']}")
#     print(f"Text preview: {all_books[0]['text'][:300]}...")


# # ========================================
# # SAVE EXTRACTED DATA TO FILE (JSONL)
# # ========================================

# print("\n" + "="*60)
# print("💾 SAVING EXTRACTED DATA...")
# print("="*60)

# # Create data folder if it doesn't exist
# data_folder = "data"
# if not os.path.exists(data_folder):
#     os.makedirs(data_folder)
#     print(f"   Created '{data_folder}' folder")

# print("   Cleaning text data...")

# def clean_text(text):
#     """Remove problematic characters that break JSON encoding"""
#     if not text:
#         return ""
    
#     import re
    
#     # Step 1: Remove null bytes
#     text = text.replace('\x00', '')
    
#     # Step 2: Remove surrogate pairs (U+D800 to U+DFFF)
#     # These cause the 'surrogates not allowed' error
#     text = re.sub(r'[\ud800-\udfff]', '', text)
    
#     # Step 3: Remove other problematic Unicode
#     # Encode to UTF-8 with error handling, then decode back
#     text = text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
    
#     # Step 4: Remove control characters (keep newlines and tabs)
#     cleaned = ''.join(char for char in text 
#                      if char in '\n\t' or ord(char) >= 32)
    
#     return cleaned

# # Clean all text data
# cleaned_count = 0
# for page in all_books:
#     original_len = len(page["text"])
#     page["text"] = clean_text(page["text"])
#     if len(page["text"]) < original_len:
#         cleaned_count += 1

# print(f"   Cleaned {cleaned_count} pages with problematic characters")

# # Save as JSONL (one JSON object per line)
# output_file = os.path.join(data_folder, "extracted_pages.json")

# try:
#     saved_count = 0
#     failed_count = 0
    
#     with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
#         for idx, page in enumerate(all_books):
#             try:
#                 # Convert to JSON string
#                 json_str = json.dumps(page, ensure_ascii=False)
                
#                 # Double-check it's valid by parsing it back
#                 json.loads(json_str)
                
#                 # Write to file
#                 f.write(json_str + '\n')
#                 saved_count += 1
                
#             except Exception as e:
#                 failed_count += 1
#                 if failed_count <= 5:  # Only show first 5 errors
#                     print(f"   ⚠️  Failed to save page {page.get('page_number', '?')} from {page.get('book_name', '?')}: {str(e)[:60]}")
    
#     print(f"✅ Saved {saved_count} pages to '{output_file}'")
#     if failed_count > 0:
#         print(f"⚠️  {failed_count} pages failed to save")
    
#     # Show file size
#     file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
#     print(f"   File size: {file_size_mb:.2f} MB")
    
# except Exception as e:
#     print(f"❌ Error saving file: {str(e)}")
#     import traceback
#     traceback.print_exc()

# print("\n" + "="*60)
# print("✅ LOAD_PDFS.PY COMPLETE!")
# print("="*60)
# print("Next step: Run 'python chunk_text.py' to chunk the extracted text")

# ========================================
# STEP 2.4: CHUNK THE TEXT
# ========================================

print("\n" + "="*60)
print("✂️  CHUNKING TEXT...")
print("="*60)

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,        # Target size for each chunk
    chunk_overlap=200,     # Overlap between chunks
    length_function=len,   # How to measure length (character count)
    separators=["\n\n", "\n", " ", ""]  # Split priorities
)

# Store chunked data
chunked_data = []

# Process each page
for idx, page_data in enumerate(all_books):
    # Split the page text into chunks
    chunks = text_splitter.split_text(page_data["text"])
    
    # Store each chunk with metadata
    for chunk_idx, chunk_text in enumerate(chunks):
        chunk_data = {
            "book_name": page_data["book_name"],
            "page_number": page_data["page_number"],
            "chunk_id": f"{page_data['book_name']}_p{page_data['page_number']}_c{chunk_idx}",
            "chunk_index": chunk_idx,  # Which chunk from this page (0, 1, 2, ...)
            "text": chunk_text
        }
        chunked_data.append(chunk_data)
    
    # Print progress every 100 pages
    if (idx + 1) % 100 == 0:
        print(f"   Chunked {idx + 1}/{len(all_books)} pages...")

print(f"\n✅ Chunking complete!")
print(f"   Original pages: {len(all_books)}")
print(f"   Total chunks created: {len(chunked_data)}")
print(f"   Average chunks per page: {len(chunked_data) / len(all_books):.2f}")