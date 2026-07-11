"""
09-rag-competencia | Paso 2: agente RAG con tool de busqueda.

  python modulo_5/09-rag-competencia/09_chat.py

Edita system_prompt.md para la competencia.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langgraph.prebuilt import create_react_agent

BASE = Path(__file__).resolve().parent
CHROMA_DIR = BASE / "chroma_db"
PROMPT_FILE = BASE / "system_prompt.md"
MODELO = "gemini-2.0-flash-lite"
K = 3


def cargar_prompt() -> str:
    return PROMPT_FILE.read_text(encoding="utf-8").strip()


def cargar_vector_store():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        collection_name="novalogistica",
    )


def crear_agente(vector_store):
    @tool
    def buscar_politicas(consulta: str) -> str:
        """Busca en los documentos internos de NovaLogistica (PDFs de RH, IT, viaticos)."""
        docs = vector_store.similarity_search(consulta, k=K)
        if not docs:
            return "No se encontro informacion."
        partes = []
        for doc in docs:
            fuente = doc.metadata.get("source", "?")
            pag = doc.metadata.get("page", "?")
            partes.append(f"[{fuente} p.{pag}]\n{doc.page_content}")
        return "\n\n---\n\n".join(partes)

    modelo = ChatGoogleGenerativeAI(model=MODELO, temperature=0.2)
    return create_react_agent(modelo, [buscar_politicas], prompt=cargar_prompt())


def preguntar(agente, texto: str) -> str:
    resultado = agente.invoke({"messages": [HumanMessage(content=texto)]})
    return resultado["messages"][-1].content


def conversar():
    load_dotenv(BASE / ".env")
    if not os.getenv("GOOGLE_API_KEY"):
        raise SystemExit("Falta GOOGLE_API_KEY en modulo_5/09-rag-competencia/.env")
    if not CHROMA_DIR.exists():
        raise SystemExit("Primero ejecuta 09_ingesta.py")

    agente = crear_agente(cargar_vector_store())
    print("Agente NovaLogistica (escribe 'salir')\n")

    while True:
        entrada = input("Tu: ").strip()
        if entrada.lower() == "salir":
            break
        if not entrada:
            continue
        print(f"\nAgente: {preguntar(agente, entrada)}\n")


if __name__ == "__main__":
    conversar()
