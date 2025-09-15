from flask import Blueprint, request, jsonify
from .security.decorators import jwt_required, roles_required, get_current_user_id
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.pgvector import PGVector
from scripts.constants import (
    HF_EMBEDDINGS,
    DATABASE_URL_WEEK8,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


documents_bp = Blueprint("documents", __name__, url_prefix="/documents")


@documents_bp.route("/upload", methods=["POST"])
@jwt_required
@roles_required("admin", "manager", "user")
def upload_document() -> tuple:
    """Upload a text file, chunk, embed, and store vectors with user_id metadata."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided under 'file'"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        user_id = get_current_user_id()
    except Exception as e:
        return jsonify({"error": "Unauthorized: invalid token", "details": str(e)}), 401

    try:
        # Read and decode file
        content = file.read().decode("utf-8", errors="ignore")
        if not content.strip():
            return jsonify({"error": "File is empty"}), 400

        # Chunk content
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
        )
        chunks = splitter.split_text(content)

        # Prepare vector store
        if not DATABASE_URL_WEEK8:
            return jsonify({"error": "DATABASE_URL_WEEK8 not configured"}), 500

        vector_store = PGVector(
            collection_name="product_embedding_hf",
            connection_string=DATABASE_URL_WEEK8,
            embedding_function=HF_EMBEDDINGS,
        )

        # Build documents with metadata
        from langchain_core.documents import Document

        docs = []
        for idx, chunk in enumerate(chunks):
            docs.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "user_id": str(user_id),
                        "chunk_index": idx,
                        "source": file.filename,
                        "scope": "private",
                    },
                )
            )

        # Store
        if docs:
            vector_store.add_documents(docs)

        return (
            jsonify(
                {
                    "message": "Upload successful",
                    "chunks": len(docs),
                    "user_id": user_id,
                    "filename": file.filename,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
