import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import chromadb

# load environment variable
load_dotenv()

# --------------------------
# Configuarton
# --------------------------
 
CHROMA_DB_PATH = "data/chroma_db"
COLLECTION_NAME = "ml_books_collection"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# How many chunks to retrieve
TOP_K = 5

# --------------------------
# Initialize components
# --------------------------
print("🤖 RAG SYSTEM - QUERY INTERFACE")

print("Loading Embedding model")
embedding_model = SentenceTransformer(EMBEDDING_MODEL)
print("✅ Embedding model loaded")

# Connecting to ChromaDB

chroma_client  = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_collection(name=COLLECTION_NAME)

print(f"✅ Connected to collection: {COLLECTION_NAME}")
print(f"   Total chunks: {collection.count()}")

# Initializing Google Gemini ai

# print("\n🧠 Initializing Google Gemini...")
# print("\n Akal larahehai bidu.....")

# api_key = os.getenv("GOOGLE_API_KEY")

# if not api_key:
#     print("Error: API Key is not found in .env file")
#     exit(1)

# genai.configure(api_key=api_key)
# model = genai.GenerativeModel('models/gemini-1.5-flash-8b')
# print("✅ Gemini initialized")

# -----------------------------------
# Initialize Groq
# ---------------------------------------

print("\n🧠 Initializing Groq (Llama)...")
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ Error: GROQ_API_KEY not found in .env file!")
    exit(1)

client = Groq(api_key=api_key)
print("✅ Groq initialized (using llama-3.1-70b-versatile)")

# -----------------------
# Rag system
# -------------------------

def retrieve_context(query, top_k=TOP_K):
    """
    Retrieve relevant chunks from ChromaDB
    """
    # convert query to embedding
    query_embedding  =  embedding_model.encode([query])

    # search inside chromaDB
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )

    return results

def format_context(results):
    """
    Format retrieved chunks into context for LLM
    """
    context_parts = []
    for idx,(doc, metadata, distance) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    ),1):
        context_parts.append(f"[Source {idx}]\n"
            f"Book: {metadata['book_name']}\n"
            f"Page: {metadata['page_number']}\n"
            f"Relevance Score: {1 - distance:.2f}\n"
            f"Content: {doc}\n")
        
    return "\n---\n\n".join(context_parts)

def create_prompt(question, context):
    """
    Create the prompt for Gemini
    """
    prompt = f"""You are an AI assistant helping a student learn about Machine Learning and AI from their textbook collection.

Use ONLY the following context from the student's books to answer the question.

CONTEXT FROM BOOKS:
{context}

STUDENT'S QUESTION: {question}

INSTRUCTIONS:
1. Answer based ONLY on the context provided above
2. If the context doesn't contain enough information, say "I don't have enough information in your books to answer this fully"
3. ALWAYS cite your sources using the format: (Book: [book_name], Page: [page_number])
4. Be clear, educational, and concise
5. If multiple sources provide information, synthesize them and cite all relevant sources

ANSWER:"""
    
    return prompt

def ask_question(question):
    """
    Main RAG function: retrieve context + generate answer
    """

    print(f"\n{'='*60}")
    print(f"❓ QUESTION: {question}")
    print(f"{'='*60}\n")
    
    # Step 1: Retrieve relevant chunks
    print("🔍 Searching your books...")
    results = retrieve_context(question)
    
    print(f"✅ Found {len(results['ids'][0])} relevant chunks\n")

    # Show what was retrieved
    print("📚 Retrieved sources:")
    for idx, metadata in enumerate(results['metadatas'][0], 1):
        print(f"   {idx}. {metadata['book_name']} (Page {metadata['page_number']})")
    
    # Step 2: Format context
    context = format_context(results)
    
    # Step 3: Create prompt
    prompt = create_prompt(question, context)
    
    # Step 4: Get answer from Gemini
    print("\n🧠 Generating answer with Gemini...\n")
    
    # try:
    #     response = model.generate_content(prompt)
    #     answer = response.text
        
    #     print("="*60)
    #     print("💡 ANSWER:")
    #     print("="*60)
    #     print(answer)
    #     print("\n" + "="*60)
        
    #     return answer
        
    # except Exception as e:
    #     print(f"❌ Error generating answer: {str(e)}")
    #     return None

    try:
        # Groq API call
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Free, fast, powerful
            messages=[
                {"role": "system", "content": "You are a helpful AI tutor for Machine Learning and AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        answer = response.choices[0].message.content
        
        print("="*60)
        print("💡 ANSWER:")
        print("="*60)
        print(answer)
        print("\n" + "="*60)
        
        return answer
        
    except Exception as e:
        print(f"❌ Error generating answer: {str(e)}")
        return None

# ========================================
# INTERACTIVE MODE
# ========================================

def interactive_mode():
    """
    Interactive Q&A loop
    """
    print("\n" + "="*60)
    print("🎓 INTERACTIVE MODE")
    print("="*60)
    print("Ask questions about ML/AI from your books!")
    print("Type 'quit' or 'exit' to stop\n")
    
    while True:
        try:
            question = input("\n❓ Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not question:
                print("⚠️  Please enter a question")
                continue
            
            ask_question(question)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

# ========================================
# MAIN
# ========================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("✅ SYSTEM READY!")
    print("="*60)
    
    # Test with a sample question
    print("\n🧪 Testing with sample question...\n")
    ask_question("What is gradient descent?")
    
    # Start interactive mode
    interactive_mode()