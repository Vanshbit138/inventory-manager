# Week 9 – Production-Ready AI & Advanced Features

## Overview
This project enhances the RAG (Retrieval-Augmented Generation) application with production-ready features, including:
- LLM caching to reduce latency and costs.
- Multi-tenancy to ensure secure, user-specific document access.
- Support for open-source models as alternatives to proprietary APIs.
- Improved scalability and security for real-world deployment.

---

## Project Structure
```
Week_9/
├── alembic.ini
├── api/                      
│   ├── app.py                # App entrypoint
│   ├── chat_routes.py        # Chat (RAG) blueprint and endpoint
│   ├── config.py             # App config (loads .env values)
│   ├── db.py                 # SQLAlchemy setup
│   ├── documents.py          # Document ingestion and management
│   ├── __init__.py           # App factory, blueprint registration
│   ├── models.py             # SQLAlchemy models
│   ├── routes.py             # Product routes (CRUD)
│   ├── schemas/              # Pydantic request/response validation
│   │   ├── request.py
│   │   └── response.py
│   ├── security/             # Auth (JWT, password hashing, decorators)
│   │   ├── auth.py
│   │   ├── decorators.py
│   │   ├── jwt_utils.py
│   │   └── password.py
│   └── seed.py               # DB seeding
├── data/
│   └── products.csv          # Sample product data
├── migrations/               # Alembic migration files
│   ├── env.py
│   └── versions/
├── prompts/
│   └── system_prompt.py      # System prompts for RAG and embeddings
├── report.txt                # End-of-week report
├── requirements.txt          # Python dependencies
├── scripts/                  # Utility scripts for RAG and embeddings
│   ├── cli.py
│   ├── constants.py
│   ├── data_loader.py
│   ├── embedded_sentences.py
│   ├── embedding.py
│   ├── llm_cache.py
│   ├── query_gpt.py
│   ├── rag_chain.py
│   ├── rag_cli.py
│   ├── storage.py
│   └── text_splitter.py
└── README.md
```

---

## Features
- **LLM Caching**: Reduces redundant API calls and improves performance.
- **Open-Source Model Integration**: Uses Hugging Face embeddings and local LLMs via Ollama.
- **Multi-Tenancy**: Secure user isolation using metadata filtering with `user_id`.
- **Model Toggling**: Easily switch between OpenAI API and local open-source models.
- **Scalability & Security**: Built with SQLAlchemy, JWT authentication, and Alembic migrations.

---

## Setup Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set environment variables in `.env`
```env
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/dbname
JWT_SECRET_KEY=your_secret_key
```

### 3. Run database migrations
```bash
flask --app api.app db upgrade
```

### 4. Generate embeddings
```bash
python scripts/embedding.py
```

### 5. Start Flask app
```bash
flask --app api.app run --debug
```

---

## Usage

### Chat Endpoint
**POST** `/chat/inventory`
```http
POST http://127.0.0.1:5000/chat/inventory
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
  "question": "What are the available electronic products?"
}
```

### Document Upload Endpoint
**POST** `/documents/upload`
- Upload a text file, which will be chunked, embedded, and stored with your `user_id`.

---

## End-of-Week Deliverables
- Multi-tenant, model-agnostic chat API.
- Secure document upload with embeddings linked to users.
- LLM caching layer integrated.
- Ability to toggle between OpenAI and open-source models.
- Final report comparing OpenAI vs. open-source models (cost, speed, quality).


