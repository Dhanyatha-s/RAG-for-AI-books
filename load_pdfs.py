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

first_page = pdf_reader.pages[0] 

# Extract the text from this page
text = first_page.extract_text()


print("----- TEXT FROM FIRST PAGE -----")
print("\n")
print(text)


# Always close the file when done
pdf_file.close()