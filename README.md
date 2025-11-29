# 🧠 Conversational AI Chatbot using FastAPI

This project is a high-speed, stateful chatbot backend built using **FastAPI** and the **Groq API**. It provides a simple API endpoint to handle conversations, maintains chat history in memory for different users, and leverages Groq's LLaMA 3.1 model for near-instant, streamed responses.

## ✨ Features

* **High-Speed Responses:** Utilizes the Groq API (running LLaMA 3.1 8b-Instant) for extremely fast text generation.
* **Stateful Conversation Management:** Manages multiple, distinct conversations simultaneously using a unique `conversation_id`. Each session's history is stored in memory.
* **Real-time Streaming:** Streams responses from the Groq API chunk-by-chunk for a real-time, "typing" effect on the frontend.
* **Modern API Backend:** Built on the high-performance, asynchronous **FastAPI** framework.
* **Data Validation:** Uses **Pydantic** models to validate incoming request data, ensuring type safety and error handling.
* **CORS Enabled:** Pre-configured with CORS middleware to allow requests from any frontend origin, making development easy.
* **Secure API Key Handling:** Safely loads the `GROQ_API_KEY` from a `.env` file.

---

## 🛠️ Technologies Used

* **Backend:** FastAPI
* **AI Model:** Groq (LLaMA 3.1 8b-Instant)
* **API Client:** `groq` Python SDK
* **Server:** Uvicorn
* **Data Validation:** Pydantic
* **Environment Variables:** `python-dotenv`

---
