# Building RAG System That Answers about AI/ML and CSE related 
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