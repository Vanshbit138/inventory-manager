Week 9 – Production-Ready AI & Advanced Features

Overview
Enhance the RAG application with features required for production use, such as caching and multi-tenancy. Explore the use of open-source models as an alternative to proprietary APIs.

Project Structure
```
Week_9/
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
    ├── llm_cache.py          # Cache generation
    ├── storage.py            # PGVector integration
    └── query_gpt.py          # Direct LLM query helper

```

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