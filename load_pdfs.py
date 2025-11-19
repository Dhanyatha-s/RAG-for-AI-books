import PyPDF2
import os

# Path to your PDF
pdf_path = r"C:\Users\DHANYATHA\OneDrive\Desktop\rag_book_system\Books\AI Engineering.pdf"

# read the file
# with open("AI Engineering.pdf", "rb") as file:
#     content = file.read() # general way


pdf_file = open(pdf_path, "rb")
# Create PDF Reader
pdf_reader = PyPDF2.PdfReader(pdf_file)

# get the Total Number of pages we have in this book
num_pages = len(pdf_reader.pages)

"""
pages: List[PageObject] (property)
Read-only property that emulates a list of Page<PyPDF2._page.Page> objects.
"""

print(f"Total pages in the book: {num_pages}")

# -------------------------------
# Extract the text from page 1
# -------------------------------

# Select first page

# first_page = pdf_reader.pages[0] 

# # Extract the text from this page
# text = first_page.extract_text()


# print("----- TEXT FROM FIRST PAGE -----")
# print("\n")
# print(text)


# Always close the file when done
# pdf_file.close()


# -----------------------------------
# Extract ALL THE PAGES from the pdf
# -----------------------------------

# all_pages = []

# for page_num in range(num_pages):
#     # Get the page
#     page = pdf_reader.pages[page_num]

#     # extract the text
#     text = page.extract_text()

#     # Store it with page info
#     pages = {
#         "page_number":page_num + 1,
#         "text" : text
#     }

#     all_pages.append(pages)

#     print(f"Extracted Page {num_pages + 1}/{num_pages}")

# print(f"Successfully extracted  {len(all_pages)} pages")

# print("\n--- SAMPLE FROM PAGE 3 ---") #first 500 characters from selected page
# print(all_pages[2]["text"][:500])


# Create a list to store all pages
all_pages = []

# Loop through each page
for page_num in range(num_pages):
    # Get the page
    page = pdf_reader.pages[page_num]
    
    # Extract text
    text = page.extract_text()
    
    # Store it with page info
    page_data = {
        "page_number": page_num + 1,  # +1 because humans count from 1, not 0
        "text": text
    }
    
    all_pages.append(page_data)
    
    # Print progress (so you know it's working)
    print(f"Extracted page {page_num + 1}/{num_pages}")

# Print summary
print(f"\n✅ Successfully extracted {len(all_pages)} pages!")

# Print a sample - first 500 characters from page 1
print("\n--- SAMPLE FROM PAGE 1 ---")
print(all_pages[0]["text"][:500])