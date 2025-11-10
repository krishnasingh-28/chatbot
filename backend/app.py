# =============================
# 🧠 FASTAPI + GROQ CHATBOT APP
# =============================
# This application uses FastAPI to create a backend chatbot API.
# It integrates Groq’s LLM (LLaMA 3 model) to generate AI responses.
# The app supports multiple conversations using unique IDs and handles
# user messages dynamically.

# -----------------------------
# 1️⃣ Import Required Libraries
# -----------------------------

import os                         # Used to access environment variables (like API keys)
from typing import List, Dict     # For type hinting lists and dictionaries
from dotenv import load_dotenv    # For loading environment variables from a .env file
from fastapi import FastAPI, HTTPException  # FastAPI for building APIs, HTTPException for error handling
from pydantic import BaseModel    # Used for validating incoming request data
from groq import Groq             # Groq Python SDK to interact with Groq’s AI models
from fastapi.middleware.cors import CORSMiddleware  # To allow frontend apps to access the backend (CORS setup)

# -----------------------------
# 2️⃣ Load Environment Variables
# -----------------------------

# Load variables from the .env file (like GROQ_API_KEY)
load_dotenv()

# Fetch the Groq API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# If the API key is missing, stop the program and show an error
if not GROQ_API_KEY:
    raise ValueError("❌ API key for Groq is missing. Please set GROQ_API_KEY in the .env file.")

# -----------------------------
# 3️⃣ Initialize FastAPI App
# -----------------------------

# Create the FastAPI app instance
app = FastAPI()

# -----------------------------
# 4️⃣ Add CORS Middleware
# -----------------------------
# CORS (Cross-Origin Resource Sharing) allows frontend (like React)
# to make API requests to this backend.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins (for development)
    allow_credentials=True,       # Allow cookies and credentials
    allow_methods=["*"],          # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # Allow all headers
)

# -----------------------------
# 5️⃣ Initialize Groq Client
# -----------------------------
# Create a Groq API client using the key loaded above

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# 6️⃣ Define Request Model
# -----------------------------
# This model validates the structure of data that comes in POST requests.

class UserInput(BaseModel):
    message: str          # The message sent by the user
    role: str = "user"    # Default role is "user"
    conversation_id: str  # Unique ID to track different chat sessions

# -----------------------------
# 7️⃣ Define Conversation Class
# -----------------------------
# Each conversation stores a list of messages (chat history) and an active flag.

class Conversation:
    def __init__(self):
        # Initialize the conversation with a system prompt (context)
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": "You are a useful AI assistant."}
        ]
        self.active: bool = True  # Indicates whether the session is still active

# -----------------------------
# 8️⃣ Store All Conversations
# -----------------------------
# We'll store all active chat sessions in memory (dictionary)
# Key = conversation_id, Value = Conversation object

conversations: Dict[str, Conversation] = {}

# -----------------------------
# 9️⃣ Function to Query Groq API
# -----------------------------
# This function sends the conversation to the Groq API and
# returns the AI model’s generated response.

def query_groq_api(conversation: Conversation) -> str:
    try:
        # Send all messages (history) to the LLaMA model
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # Model name
            messages=conversation.messages, # Entire conversation context
            temperature=1,                  # Controls randomness (1 = balanced)
            max_tokens=1024,                # Maximum number of tokens to generate
            top_p=1,                        # Nucleus sampling parameter
            stream=True,                    # Stream response chunks
            stop=None,                      # No specific stop sequence
        )
        
        # We'll combine streamed chunks into one final response string
        response = ""
        for chunk in completion:
            # Each chunk may contain partial text; combine all
            response += chunk.choices[0].delta.content or ""
        
        # Return the complete AI-generated message
        return response
    
    except Exception as e:
        # Handle any Groq API or network errors gracefully
        raise HTTPException(status_code=500, detail=f"Error with Groq API: {str(e)}")

# -----------------------------
# 🔟 Helper Function: Manage Conversations
# -----------------------------
# This function retrieves an existing conversation or creates a new one.

def get_or_create_conversation(conversation_id: str) -> Conversation:
    # If the given conversation ID doesn’t exist, create a new session
    if conversation_id not in conversations:
        conversations[conversation_id] = Conversation()
    # Return the conversation object
    return conversations[conversation_id]

# -----------------------------
# 1️⃣1️⃣ Main Chat Endpoint
# -----------------------------
# This endpoint receives a message, sends it to the AI, and returns a response.

@app.post("/chat/")
async def chat(input: UserInput):
    # Retrieve or create a conversation for the provided ID
    conversation = get_or_create_conversation(input.conversation_id)

    # If the conversation is marked as inactive, block further messages
    if not conversation.active:
        raise HTTPException(
            status_code=400,
            detail="The chat session has ended. Please start a new session."
        )
        
    try:
        # 1. Append user's message to conversation history
        conversation.messages.append({
            "role": input.role,
            "content": input.message
        })
        
        # 2. Send the conversation to Groq and get AI response
        response = query_groq_api(conversation)
        
        # 3. Add AI's response to the conversation history
        conversation.messages.append({
            "role": "assistant",
            "content": response
        })
        
        # 4. Send back AI’s response to the frontend
        return {
            "response": response,
            "conversation_id": input.conversation_id
        }
        
    except Exception as e:
        # Catch and return any unexpected error
        raise HTTPException(status_code=500, detail=str(e))
    
# -----------------------------
# 1️⃣2️⃣ Run the FastAPI Server
# -----------------------------
# This section starts the app when you run the file directly.
# You can visit http://127.0.0.1:8000/docs to test your API interactively.

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app on all available network interfaces, port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
