"""
app.py - Gradio Web Interface for ML Books RAG System

A user-friendly web interface to query your ML/AI book collection.
Features:
- Chat interface with conversation history
- Source citations
- Adjustable settings (number of sources, temperature)
"""

import os
from dotenv import load_dotenv
import gradio as gr
from groq import Groq
from sentence_transformers import SentenceTransformer
import chromadb

# Load environment variables
load_dotenv()

# ========================================
# CONFIGURATION
# ========================================

CHROMA_DB_PATH = "data/chroma_db"
COLLECTION_NAME = "ml_books_collection"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ========================================
# INITIALIZE COMPONENTS
# ========================================

print("🚀 Initializing RAG System...")

# Load embedding model
print("📦 Loading embedding model...")
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

# Connect to ChromaDB
print("💾 Connecting to ChromaDB...")
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_collection(name=COLLECTION_NAME)
print(f"✅ Connected! Total chunks: {collection.count()}")

# Initialize Groq
print("🤖 Initializing Groq...")
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in .env file!")
client = Groq(api_key=groq_api_key)
print("✅ System ready!\n")

# ========================================
# RAG FUNCTIONS
# ========================================

def retrieve_context(query, top_k=5):
    """Retrieve relevant chunks from ChromaDB"""
    query_embedding = embedding_model.encode([query])
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )
    return results

def format_context(results):
    """Format retrieved chunks for LLM"""
    context_parts = []
    for idx, (doc, metadata, distance) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    ), 1):
        context_parts.append(
            f"[Source {idx}]\n"
            f"Book: {metadata['book_name']}\n"
            f"Page: {metadata['page_number']}\n"
            f"Relevance: {(1 - distance)*100:.1f}%\n"
            f"Content: {doc}\n"
        )
    return "\n---\n\n".join(context_parts)

def format_sources(results):
    """Format sources for display"""
    sources = []
    for idx, (metadata, distance) in enumerate(zip(
        results['metadatas'][0],
        results['distances'][0]
    ), 1):
        sources.append(
            f"**{idx}. {metadata['book_name']}** (Page {metadata['page_number']}) "
            f"- Relevance: {(1-distance)*100:.1f}%"
        )
    return "\n".join(sources)

def create_prompt(question, context, conversation_history=""):
    """Create prompt for LLM"""
    history_text = ""
    if conversation_history:
        history_text = f"\nPREVIOUS CONVERSATION:\n{conversation_history}\n"
    
    prompt = f"""You are an AI assistant helping students learn about Machine Learning and AI from their textbook collection.

{history_text}
CONTEXT FROM BOOKS:
{context}

CURRENT QUESTION: {question}

INSTRUCTIONS:
1. Answer based ONLY on the context provided
2. If the context lacks information, say "I don't have enough information in your books"
3. ALWAYS cite sources: (Book: [book_name], Page: [page_number])
4. Be clear, educational, and concise
5. Synthesize information from multiple sources when relevant

ANSWER:"""
    return prompt

def generate_answer(question, top_k=5, temperature=0.3, conversation_history=""):
    """Main RAG function"""
    # Retrieve context
    results = retrieve_context(question, top_k=top_k)
    context = format_context(results)
    sources = format_sources(results)
    
    # Create prompt
    prompt = create_prompt(question, context, conversation_history)
    
    # Get answer from Groq
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful AI tutor for Machine Learning and AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=1500
        )
        answer = response.choices[0].message.content
        return answer, sources
    
    except Exception as e:
        return f"❌ Error: {str(e)}", ""

# # ========================================
# # GRADIO INTERFACE
# # ========================================

# def chat_interface(message, history, top_k, temperature):
#     """
#     Gradio chat function
    
#     Args:
#         message: Current user message
#         history: List of [user_msg, bot_msg] pairs
#         top_k: Number of sources to retrieve
#         temperature: LLM temperature
#     """
#     # Format conversation history for context
#     conversation_context = ""
#     if history:
#         recent_history = history[-3:]  # Last 3 exchanges
#         for user_msg, bot_msg in recent_history:
#             conversation_context += f"User: {user_msg}\nAssistant: {bot_msg}\n\n"
    
#     # Generate answer
#     answer, sources = generate_answer(
#         message, 
#         top_k=int(top_k), 
#         temperature=temperature,
#         conversation_history=conversation_context
#     )
    
#     # Format response with sources
#     full_response = f"{answer}\n\n---\n\n**📚 Sources:**\n{sources}"
    
#     return full_response

# # ========================================
# # BUILD GRADIO APP
# # ========================================

# # Custom CSS for better styling
# custom_css = """
# #main-container {
#     max-width: 1200px;
#     margin: auto;
# }
# .source-box {
#     background-color: #f0f0f0;
#     padding: 10px;
#     border-radius: 5px;
#     margin-top: 10px;
# }
# """

# # Create the interface
# with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    
#     # Header
#     gr.Markdown(
#         """
#         # 📚 ML/AI Books RAG System
        
#         Ask questions about Machine Learning and AI, and get answers from your textbook collection!
        
#         **Features:**
#         - 🔍 Semantic search across 17,000+ text chunks
#         - 📖 Answers from 10+ ML/AI textbooks
#         - 🎯 Source citations with page numbers
#         - 💬 Conversation history support
#         """
#     )
    
#     # Main chat interface
#     with gr.Row():
#         with gr.Column(scale=3):
#             chatbot = gr.Chatbot(
#                 height=500,
#                 label="Chat",
#                 show_label=False,
#                 avatar_images=(None, "🤖")
#             )
            
#             with gr.Row():
#                 msg = gr.Textbox(
#                     label="Ask a question",
#                     placeholder="e.g., What is gradient descent?",
#                     scale=4
#                 )
#                 submit = gr.Button("Send", variant="primary", scale=1)
            
#             gr.Examples(
#                 examples=[
#                     "What is gradient descent?",
#                     "Explain the difference between supervised and unsupervised learning",
#                     "What is backpropagation and how does it work?",
#                     "What are the key components of a transformer architecture?",
#                     "How do convolutional neural networks work?",
#                     "What is overfitting and how can I prevent it?",
#                 ],
#                 inputs=msg,
#                 label="Example Questions"
#             )
        
#         # Settings sidebar
#         with gr.Column(scale=1):
#             gr.Markdown("### ⚙️ Settings")
            
#             top_k = gr.Slider(
#                 minimum=1,
#                 maximum=10,
#                 value=5,
#                 step=1,
#                 label="Number of Sources",
#                 info="How many relevant chunks to retrieve"
#             )
            
#             temperature = gr.Slider(
#                 minimum=0.0,
#                 maximum=1.0,
#                 value=0.3,
#                 step=0.1,
#                 label="Temperature",
#                 info="Higher = more creative, Lower = more focused"
#             )
            
#             clear = gr.Button("🗑️ Clear Chat")
            
#             gr.Markdown(
#                 """
#                 ### 📊 System Info
                
#                 - **Total Chunks:** 17,283
#                 - **Books Indexed:** 10+
#                 - **Model:** Llama 3.1 70B
#                 - **Embedding:** all-MiniLM-L6-v2
#                 """
#             )
    
#     # Footer
#     gr.Markdown(
#         """
#         ---
#         💡 **Tips:**
#         - Ask specific questions for better results
#         - Check the source citations to verify information
#         - Adjust settings to experiment with results
        
#         Built with ❤️ using Gradio, ChromaDB, and Groq
#         """
#     )
    
#     # Event handlers
#     msg.submit(
#         chat_interface,
#         inputs=[msg, chatbot, top_k, temperature],
#         outputs=chatbot
#     ).then(
#         lambda: "",
#         outputs=msg
#     )
    
#     submit.click(
#         chat_interface,
#         inputs=[msg, chatbot, top_k, temperature],
#         outputs=chatbot
#     ).then(
#         lambda: "",
#         outputs=msg
#     )
    
#     clear.click(lambda: None, outputs=chatbot)

# # ========================================
# # LAUNCH
# # ========================================

# if __name__ == "__main__":
#     demo.launch(
#         share=False,
#         server_name="127.0.0.1",  # Changed!
#         server_port=7860
#     )


# ========================================
# BUILD GRADIO APP
# ========================================

def respond(message, history, top_k, temperature):
    """
    Chat response function for Gradio ChatInterface
    
    Args:
        message: Current user message
        history: List of [user_msg, bot_msg] pairs
        top_k: Number of sources to retrieve
        temperature: LLM temperature
    """
    # Format conversation history for context
    conversation_context = ""
    if history:
        recent_history = history[-3:]  # Last 3 exchanges
        for user_msg, bot_msg in recent_history:
            conversation_context += f"User: {user_msg}\nAssistant: {bot_msg}\n\n"
    
    # Generate answer
    answer, sources = generate_answer(
        message, 
        top_k=int(top_k), 
        temperature=temperature,
        conversation_history=conversation_context
    )
    
    # Format response with sources
    full_response = f"{answer}\n\n---\n\n**📚 Sources:**\n{sources}"
    
    return full_response

# Create the interface with custom layout
with gr.Blocks(title="ML Books RAG System") as demo:
    
    # Header
    gr.Markdown(
        """
        # 📚 ML/AI Books RAG System
        
        Ask questions about Machine Learning and AI, and get answers from your textbook collection!
    
        """
    )
    
    with gr.Row():
        with gr.Column(scale=3):
            # Chat interface
            chatbot = gr.Chatbot(
                height=500,
                label="Chat",
                show_copy_button=True
            )
            
            msg = gr.Textbox(
                label="Your Question",
                placeholder="e.g., What is gradient descent?",
                lines=2
            )
            
            with gr.Row():
                submit = gr.Button("Send 🚀", variant="primary")
                clear = gr.Button("Clear 🗑️")
            
            gr.Examples(
                examples=[
                    "What is gradient descent?",
                    "Explain the difference between supervised and unsupervised learning",
                    "What is backpropagation and how does it work?",
                    "What are the key components of a transformer architecture?",
                    "How do convolutional neural networks work?",
                    "What is overfitting and how can I prevent it?",
                ],
                inputs=msg
            )
        
        # Settings sidebar
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ Settings")
            
            top_k = gr.Slider(
                minimum=1,
                maximum=10,
                value=5,
                step=1,
                label="Number of Sources",
                info="How many relevant chunks to retrieve"
            )
            
            temperature = gr.Slider(
                minimum=0.0,
                maximum=1.0,
                value=0.3,
                step=0.1,
                label="Temperature",
                info="Higher = more creative, Lower = more focused"
            )
            
            gr.Markdown(
                """
                ### 📊 System Info
                
                - **Total Chunks:** 17,283
                - **Books Indexed:** 10+
                - **Model:** Llama 3.1 70B
                - **Embedding:** all-MiniLM-L6-v2
                """
            )
    
    # Footer
    gr.Markdown(
        """
        ---
        💡 **Tips:**
        - Ask specific questions for better results
        - Check the source citations to verify information
        - Adjust settings to experiment with results
        
        Built with ❤️ using Gradio, ChromaDB, and Groq
        """
    )
    
    # Event handlers
    def user_submit(message, history, top_k, temperature):
        """Handle user message submission"""
        if not message.strip():
            return "", history
        
        # Get bot response
        bot_message = respond(message, history, top_k, temperature)
        
        # Update history
        history = history + [[message, bot_message]]
        
        return "", history
    
    msg.submit(
        user_submit,
        inputs=[msg, chatbot, top_k, temperature],
        outputs=[msg, chatbot]
    )
    
    submit.click(
        user_submit,
        inputs=[msg, chatbot, top_k, temperature],
        outputs=[msg, chatbot]
    )
    
    clear.click(
        lambda: [],
        outputs=chatbot
    )

# ========================================
# LAUNCH
# ========================================

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860
    )