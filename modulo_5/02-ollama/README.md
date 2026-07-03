# 02 - Chat Ollama

## Ollama (antes del script)

1. Instala desde [ollama.com/download](https://ollama.com/download)
2. Mac M: `ollama pull qwen3.5:4b-mlx` | otro: `ollama pull qwen3.5:4b`
3. `ollama list`

## Windows

1. `python -m venv .venv-02-ollama`
2. `.venv-02-ollama\Scripts\activate`
3. `pip install -r modulo_5/02-ollama/requirements.txt`
4. `python modulo_5/02-ollama/02_ollama_chat.py`

## Mac

1. `python3 -m venv .venv-02-ollama`
2. `source .venv-02-ollama/bin/activate`
3. `pip install -r modulo_5/02-ollama/requirements.txt`
4. `python modulo_5/02-ollama/02_ollama_chat.py`


## Eliminar un modelo

Libera espacio en disco si ya no lo usas (el nombre es el de la columna `NAME` en `ollama list`):

1. `ollama rm qwen3.5:4b-mlx`
2. `ollama list` (debe desaparecer de la lista)

Varios a la vez: `ollama rm modelo1 modelo2`