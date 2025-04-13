***🧠 Booking Analytics & Q&A System***
This project is a simplified LLM-powered system for answering user queries about hotel bookings using retrieval-based question answering. It uses precomputed analytics stored in SQLite and ChromaDB for fast vector search — no live LLM is required.
***Running the code***:
uvicorn app.api:app --reload, 
python main.py
The process might take some time as we are using a hugging face LLM model to work on queries
