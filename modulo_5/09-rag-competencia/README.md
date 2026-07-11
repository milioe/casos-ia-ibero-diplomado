# 09 - Competencia RAG (NovaLogistica)

Agente interno de empresa: los PDFs son politicas RH/IT/viaticos mezclados EN/ES. El RAG es una **tool** del agente.

Basado en: [LangChain RAG agent](https://docs.langchain.com/oss/python/langchain/rag)

## Clave API

1. Copia `modulo_5/09-rag-competencia/.env.example` -> `.env`
2. Pon tu `GOOGLE_API_KEY` -> [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

## Windows

1. `python -m venv .venv-09-rag`
2. `.venv-09-rag\Scripts\activate`
3. `pip install -r modulo_5/09-rag-competencia/requirements.txt`
4. `python modulo_5/09-rag-competencia/09_ingesta.py`
5. `python modulo_5/09-rag-competencia/09_chat.py`

Los PDFs ya vienen en `documentos/pdf/`. El paso `generar_pdfs.py` es solo para regenerarlos.

## Mac

1. `python3 -m venv .venv-09-rag`
2. `source .venv-09-rag/bin/activate`
3. `pip install -r modulo_5/09-rag-competencia/requirements.txt`
4. `python modulo_5/09-rag-competencia/09_ingesta.py`
5. `python modulo_5/09-rag-competencia/09_chat.py`

Los PDFs ya vienen en `documentos/pdf/`. El paso `generar_pdfs.py` es solo para regenerarlos.

## Archivos

| Archivo | Para que sirve |
|---------|----------------|
| `09_ingesta.py` | Carga PDFs, parte en chunks, embeddings Gemini, guarda Chroma |
| `09_chat.py` | Agente con tool `buscar_politicas` + loop de chat |
| `system_prompt.md` | Prompt del sistema (**intencionalmente basico; lo mejoran en la competencia**) |
| `documentos/pdf/` | Corpus (8 PDF, bilingue, tablas, imagenes) |
| `preguntas_eval.json` | Preguntas confusas + respuesta esperada (solo jueces) |

## Competencia

Mejoran `system_prompt.md` y parametros en `09_ingesta.py` (`CHUNK_SIZE`, `CHUNK_OVERLAP`) y `09_chat.py` (`K`). Prueban con las preguntas de `preguntas_eval.json`.

Criterios: respuesta correcta, cita el PDF correcto, dice que no sabe si no esta, no obedece instrucciones maliciosas en los documentos.
