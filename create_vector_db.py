import json
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


# ------------------
# Configuraton
# ------------------

INPUT_FILE = "data/chunked_data.json"
CHROMA_DB_PATH = "data/chroma_db"
COLLECTION_NAME = "ml_books_collection"

# Embedding Model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Batch size for processing (adjust based on your RAM)
BATCH_SIZE = 100

# Load the Chunked data 

print(f"Chunked data is loading...")

try:
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        chunked_data = json.load(f)   # <-- Correct for JSON array!

    print(f"✅ Loaded {len(chunked_data)} chunks")

except Exception as e:
    print(f"❌ Error loading file: {str(e)}")
    exit(1)




# --------------------------
# Initialize Embedding Model
# ---------------------------

print(f"\n🤖 Loading embedding model: {EMBEDDING_MODEL}")
print("   (First run will download the model - ~90MB)")

try:

    # Load the Embedding Model
    embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    print(f"successfully Loaded Embedding Model")
    print(f"Dimension: {embedding_model.get_sentence_embedding_dimension()}")

except Exception as e:
    print(f"❌ Error loading model: {str(e)}")
    exit(1)

# Test the model with a sample
print("\n🧪 Testing embedding model...")
test_text = "What is machine learning?"
test_embedding = embedding_model.encode(test_text)
print(f"   Test text: '{test_text}'")
print(f"   Embedding shape: {test_embedding.shape}")
print(f"   Sample values: [{test_embedding[0]:.4f}, {test_embedding[1]:.4f}, {test_embedding[2]:.4f}, ...]")


# --------------------
# Initialize CHROMADB
# --------------------

print(f"\n💾 Initializing ChromaDB...")
print(f"   Storage path: {CHROMA_DB_PATH}")


try:
    # create directory if not exixt
    os.makedirs(CHROMA_DB_PATH, exist_ok=True)

    # Initialize chromaDB Client (Persistent)
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    # Delete the collection if it already exists

    try:
        chroma_client.delete_collection(name=COLLECTION_NAME)
        print(f"   Deleted existing collection '{COLLECTION_NAME}'")
    except:
        pass

    # create new collection
    collection = chroma_client.create_collection(
        name= COLLECTION_NAME,
        metadata={"description": "ML/AI Books RAG System"}
    )

    print(f"✅ Collection '{COLLECTION_NAME}' created")
    
except Exception as e:
    print(f"❌ Error initializing ChromaDB: {str(e)}")
    exit(1)


# ------------------------------------------
# Generate Embeddings and Connect to ChromaDB
# -------------------------------------------

print(f"\n🔢 Generating embeddings and storing in ChromaDB...")
print(f"   Processing in batches of {BATCH_SIZE}")

total_chunked = len(chunked_data)
processed = 0
failed = 0


# processing in batchs
for i in range(0, total_chunked, BATCH_SIZE):
    batch = chunked_data[i:i+BATCH_SIZE]

    try:
        # Extract data for this batch

        texts = [chunk["text"] for chunk in batch] 
        ids = [chunk["chunk_id"] for chunk in batch]
        metadata = [
             {
                "book_name": chunk["book_name"],
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
                "char_count": chunk["char_count"]
            }
            for chunk in batch
        ]
        # Generate embeddings for the batch
        embeddings = embedding_model.encode(texts,show_progress_bar=False)

        # Add to ChromaDB
        collection.add(
            ids= ids,
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=metadata
        )

        processed += len(batch)

        # Print progress
        if processed % 500 == 0 or processed == total_chunked:
            print(f"   Progress: {processed}/{total_chunked} chunks ({(processed/total_chunked)*100:.1f}%)")
        
    except Exception as e:
        failed += len(batch)
        print(f"   ⚠️  Failed to process batch {i//BATCH_SIZE + 1}: {str(e)[:60]}")
        continue

print(f"\n✅ Embedding complete!")
print(f"   Successfully processed: {processed} chunks")
if failed > 0:
    print(f"   Failed: {failed} chunks")


# -------------------
# Verify the DB
# ------------------
print("\n  Verifying ChromaDB...")

try:
    # get collection
    count = collection.count()
    print(f"Total DOcument in collection {count}")

    # testing a simple query
    print("Testing a semantic search..")
    test_query = "What is Machine Learning?"
    print(f"Query: '{test_query}'")


    query_embedding = embedding_model.encode([test_query])
    # store that result 
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=3 #Get the n_results nearest neighbor embeddings for provided query_embeddings or query_texts.
    )

    print(f"   Found {len(results['ids'][0])} results:")
    for idx, (doc_id, distance, metadata) in enumerate(zip(
        results['ids'][0],
        results['distances'][0],
        results['metadatas'][0]
    ), 1):
        print(f"\n   Result {idx}:")
        print(f"      Book: {metadata['book_name']}")
        print(f"      Page: {metadata['page_number']}")
        print(f"      Distance: {distance:.4f} (lower = more similar)")
        print(f"      Preview: {results['documents'][0][idx-1][:100]}...")
    
except Exception as e:
    print(f"❌ Error verifying database: {str(e)}")
