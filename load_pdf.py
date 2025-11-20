import PyPDF2
import os
import json


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


# -------------------------------
#  SAVE EXTRACTED DATA
# --------------------------------

print("\n" + "-" * 60)
print("SAVEING EXTRACTED DATA")
print("-" * 60)

data_folder = "data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
    print(f"   Created '{data_folder}' folder")

# Save to JSON file
output_file = os.path.join(data_folder, "extracted_pages.json")

try:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_books, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(all_books_data)} pages to '{output_file}'")

    # Show file size
    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"   File size: {file_size_mb:.2f} MB")

except Exception as e:
    print(f"❌ Error saving file: {str(e)}")

print("\n" + "="*60)
print("✅ LOAD_PDFS.PY COMPLETE!")
print("="*60)
print("Next step: Run 'python chunk_text.py' to chunk the extracted text")