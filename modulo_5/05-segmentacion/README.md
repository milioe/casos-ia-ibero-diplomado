# 05 - Segmentacion de imagenes

Imagenes de prueba en `input/` (`ciclistas.jpg`, `vacas.jpg`). Resultados en `output/`.

## Windows

1. `python -m venv .venv-05-segmentacion`
2. `.venv-05-segmentacion\Scripts\activate`
3. `pip install -r modulo_5/05-segmentacion/requirements.txt`
4. `python modulo_5/05-segmentacion/05_imageGeneration.py`

## Mac

1. `python3 -m venv .venv-05-segmentacion`
2. `source .venv-05-segmentacion/bin/activate`
3. `pip install -r modulo_5/05-segmentacion/requirements.txt`
4. `python modulo_5/05-segmentacion/05_imageGeneration.py`

## Usar el servicio

Dos terminales, desde la raiz del repo.

### Terminal 1 - servidor

1. Activa el ambiente
2. `python modulo_5/05-segmentacion/05_imageGeneration.py`

### Terminal 2 - mandar una imagen

```bash
curl -X POST -F "imagen=@modulo_5/05-segmentacion/input/ciclistas.jpg" -F "tipo=background" http://localhost:8000/segmentar -o modulo_5/05-segmentacion/output/bg.png
```

```bash
curl -X POST -F "imagen=@modulo_5/05-segmentacion/input/ciclistas.jpg" -F "tipo=instance" http://localhost:8000/segmentar -o modulo_5/05-segmentacion/output/inst.png
```

Parar el servidor: `Ctrl+C` en la Terminal 1.
