# 04 - DeepFace

Dos scripts, un solo ambiente.

## Windows

1. `python -m venv .venv-04-deepface`
2. `.venv-04-deepface\Scripts\activate`
3. `pip install -r modulo_5/04-deepface/requirements.txt`
4. `python modulo_5/04-deepface/04_deepface_detectar.py`
5. `python modulo_5/04-deepface/04_deepface_buscar.py`

## Mac

1. `python3 -m venv .venv-04-deepface`
2. `source .venv-04-deepface/bin/activate`
3. `pip install -r modulo_5/04-deepface/requirements.txt`
4. `python modulo_5/04-deepface/04_deepface_detectar.py`
5. `python modulo_5/04-deepface/04_deepface_buscar.py`

## Limpiar (liberar espacio)

1. `deactivate`
2. `rm -rf .venv-04-deepface`
3. `rm -rf ~/.deepface`
4. `rm -rf ~/.keras` (opcional)
