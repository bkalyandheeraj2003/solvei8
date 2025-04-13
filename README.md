🧠 Booking Analytics & Q&A System
This project is a simplified LLM-powered system for answering user queries about hotel bookings using retrieval-based question answering. It uses precomputed analytics stored in SQLite and ChromaDB for fast vector search — no live LLM is required.
***Running the code***:
uvicorn app.api:app --reload
python main.py
The process might take some time as we are using a hugging face LLM model to work on queries
The Project Structure
solvei8_booking_ai/
├── app/
│   ├── api.py                 # API endpoints
│   ├── analytics.py           # Generate and store analytics
│   ├── data_loader.py         # Load and clean dataset
│   ├── embedding_utils.py     # Text summarization + ChromaDB setup
│   ├── rag_qa.py              # Retrieval-based Q&A (no LLM)
│   ├── db.py                  # SQLite setup
├── data/
│   ├── hotel_bookings.csv     # Dataset
│   └── fetchdata.py           # Fetch dataset script
├── main.py                    # One-time setup script
├── requirements.txt
└── README.md
