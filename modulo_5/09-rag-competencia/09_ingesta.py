"""
09-rag-competencia | Paso 1: indexar PDFs en Chroma.

  python modulo_5/09-rag-competencia/09_ingesta.py

Requiere: GOOGLE_API_KEY en .env y PDFs en documentos/pdf/
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE = Path(__file__).resolve().parent
PDF_DIR = BASE / "documentos" / "pdf"
CHROMA_DIR = BASE / "chroma_db"

CHUNK_SIZE = 900
CHUNK_OVERLAP = 150


def cargar_pdfs():
    docs = []
    for pdf in sorted(PDF_DIR.glob("*.pdf")):
        cargados = PyPDFLoader(str(pdf)).load()
        for doc in cargados:
            doc.metadata["source"] = pdf.name
        docs.extend(cargados)
        print(f"  {pdf.name}: {len(cargados)} paginas")
    return docs


def main():
    load_dotenv(BASE / ".env")
    if not os.getenv("GOOGLE_API_KEY"):
        raise SystemExit("Falta GOOGLE_API_KEY en modulo_5/09-rag-competencia/.env")

    if not list(PDF_DIR.glob("*.pdf")):
        raise SystemExit(
            "No hay PDFs. Ejecuta primero:\n"
            "  python modulo_5/09-rag-competencia/scripts/generar_pdfs.py"
        )

    print("Cargando PDFs...")
    docs = cargar_pdfs()
    print(f"Total paginas: {len(docs)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
    )
    chunks = splitter.split_documents(docs)
    print(f"Chunks: {len(chunks)}")

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name="novalogistica",
    )
    print(f"Indice guardado en {CHROMA_DIR}")


if __name__ == "__main__":
    main()
