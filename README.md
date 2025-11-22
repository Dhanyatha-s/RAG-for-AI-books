# Building RAG System That Answers about AI/ML and CSE related 
its a RAG system built on AI/ML and Computer Science related books and concepts to query and learn it more efficiently.
<!-- Initialize UV package -->
``` uv init
uv venv ```

<!-- Activate the Virtual Environment -->
```.venv\Scripts\activate```

<!-- Install Core Libraries -->
```
uv add pypdf2 langchain langchain-community chromadb sentence-transformers google-generativeai python-dotenv

```

## What each library does:

- pypdf2: Reads PDF files
- langchain: Framework for building RAG systems (makes our life easier)
- langchain-community: Community integrations (ChromaDB connector)
- chromadb: Vector database (stores embeddings)
- sentence-transformers: Creates embeddings locally
- google-generativeai: Google Gemini API client
- python-dotenv: Manages API keys securely


<!-- Lets Code the Load Files -->
## I've added series of books of AI and ML along with some Computer science concepts that enriches the comprehensiveness in the domain.

<!-- Methods -->
- import Library (PyPDF2)

- open the file with path 

- get the Num of books(filename) and num_page in each filename

- extract text from  it

- Save it into a new folder as json file that contains the extracted text with "FileName", "PageNumber", "Text"

<!-- Chunk the Text  -->
# Now Chunk the text we have extracted from the data folder.

"""
chunk_text.py

Purpose: Load extracted PDF pages and chunk them into smaller pieces for RAG.

Input: data/extracted_pages.json (from load_pdfs.py)
Output: data/chunked_data.json

Chunking Strategy:
- Chunk size: 800 characters (optimal for retrieval)
- Overlap: 200 characters (preserves context at boundaries)
- Uses RecursiveCharacterTextSplitter (splits at natural boundaries)

Why chunking?
1. LLMs have token limits - can't process entire books
2. Smaller chunks = more precise retrieval
3. Better similarity matching in vector search
"""