Week 8 – LLMs, Embeddings, and Retrieval-Augmented Generation (RAG)
Overview

This week marks the transition from traditional software engineering to the AI stack.
The goal was to understand Large Language Models (LLMs), embeddings, and the Retrieval-Augmented Generation (RAG) pattern — and finally, to build an Inventory Chatbot API that allows natural language queries on product data stored in a PostgreSQL database with pgvector.

Project Structure
```
Week_8/
├── api/                      # Flask application
│   ├── app.py                # App entrypoint
│   ├── chat_routes.py        # Chat (RAG) blueprint and endpoint
│   ├── config.py             # App config (loads .env values)
│   ├── db.py                 # SQLAlchemy setup
│   ├── __init__.py           # App factory, blueprint registration
│   ├── models.py             # SQLAlchemy models
│   ├── routes.py             # Product routes (CRUD)
│   ├── schemas/              # Pydantic request/response validation
│   ├── security/             # Auth (JWT, password hashing, decorators)
│   └── seed.py               # DB seeding
├── data/
│   └── products.csv          # Sample product data
├── migrations/               # Alembic migration files
├── requirements.txt          # Python dependencies
└── prompts/                  # Prompts for RAG and embeddings
    ├── system_prompts.py         
└── scripts/                  # Utility scripts for RAG and embeddings
    ├── constants.py          # Constants (models, chunk sizes, etc.)
    ├── data_loader.py        # Load products from DB
    ├── rag_chain.py          # RAG pipeline (retriever → prompt → LLM)
    ├── embedding.py          # Embedding generation
    ├── storage.py            # PGVector integration
    └── query_gpt.py          # Direct LLM query helper

```
### Week 8 Daily Breakdown
## Day 1 – LLMs & Prompt Engineering

- Learned what LLMs are, tokens, and cost calculation.
- Experimented with OpenAI’s API for zero-shot vs few-shot prompting.
- Wrote a script to interact with GPT-3.5-Turbo, log response + cost.

## Day 2 – Embeddings & Vector Stores

- Understood embeddings, cosine similarity, and why vector DBs are needed.
- Installed and enabled pgvector in PostgreSQL.
- Generated embeddings for sample sentences and stored them in DB.

## Day 3 – LangChain Introduction

- Learned LangChain’s core abstractions: Models, Prompts, Output Parsers.
- Refactored Day 1 script using ChatOpenAI, ChatPromptTemplate, and StrOutputParser.
- Practiced LangChain Expression Language (LCEL) chaining.

## Day 4 – Building a RAG Chain

- Understood the Why of RAG → LLMs don’t know private data, so retrieval is required.
- Constructed a RAG chain:
- Load product data from DB
- Split into chunks
- Generate embeddings → store in pgvector
- Create PGVector retriever
- Build chain with LCEL → retriever → prompt → LLM → parser

## Day 5 – Integrating RAG with Flask

- Created a new chat Blueprint.
- Added endpoint POST /chat/inventory → takes user’s question, runs through RAG chain, returns LLM’s answer.
- Secured endpoint with JWT auth.
- Verified routes with flask --app api.app routes.

### End-of-Week Deliverable – Inventory Chatbot API

- PostgreSQL table with vector column (pgvector) for embeddings
- Script to ingest product info → generate embeddings → store in DB
- LangChain RAG chain using PGVector retriever, prompt, and LLM
- Prompt ensures answers are only based on product context
- New chat blueprint added to Flask app
- POST /chat/inventory endpoint accepts {"question": "..."}
- Protected with @jwt_required
- Endpoint runs RAG pipeline and returns JSON answer

###  How to Run

## Install dependencies

```
pip install -r requirements.txt
```

## Set environment variables in .env
```
OPENAI_API_KEY=your_openai_key
DATABASE_URL_WEEK8=postgresql+psycopg2://user:password@localhost:5432/dbname
JWT_SECRET_KEY=your_secret_key
```

## Run database migrations
```
flask --app api.app db upgrade
```

## Generate embeddings
```
python scripts/embedding.py
```

## Start Flask app
```
flask --app api.app run --debug
```

## Test Chat Endpoint (Postman / curl)
```
POST http://127.0.0.1:5000/chat/inventory
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
  "question": "What are the available electronic products?"
}
```