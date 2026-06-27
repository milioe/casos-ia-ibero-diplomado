"""
Segmentación de imágenes — API unificada (3 tipos)

  pip install flask 'rembg[cpu]' pillow ultralytics transformers torch
  python 04_imageGeneration.py

Imagen de ejemplo: ciclistas.jpg (varias personas — ideal para instance)

  curl -X POST -F "imagen=@ciclistas.jpg" -F "tipo=background" http://localhost:8000/segmentar -o bg.png
  curl -X POST -F "imagen=@ciclistas.jpg" -F "tipo=semantic"   http://localhost:8000/segmentar -o sem.png
  curl -X POST -F "imagen=@ciclistas.jpg" -F "tipo=instance"  http://localhost:8000/segmentar -o inst.png

Tipos:
  background — quita fondo (rembg / U2Net)
  semantic   — clase por píxel: cielo, persona, coche… (SegFormer)
  instance   — máscara por objeto: persona 1, persona 2… (YOLO-seg)
"""

from io import BytesIO
from pathlib import Path

import numpy as np
import torch
from flask import Flask, request, send_file
from PIL import Image
from rembg import new_session, remove
from transformers import AutoImageProcessor, AutoModelForSemanticSegmentation
from ultralytics import YOLO

TIPOS = ("background", "semantic", "instance")
EJEMPLO = "ciclistas.jpg"  # imagen de prueba incluida en el repo
PUERTO = 8000
CARPETA = Path(__file__).parent
SALIDA = CARPETA / "segmentada.png"

_cache: dict = {}
app = Flask(__name__)


def _color_por_id(i: int) -> tuple[int, int, int]:
    rng = np.random.default_rng(i)
    return tuple(rng.integers(40, 230, 3).astype(int).tolist())


def _superponer(original: Image.Image, capa: Image.Image, alpha: float = 0.55) -> Image.Image:
    base = original.convert("RGB").resize(capa.size)
    return Image.blend(base, capa.convert("RGB"), alpha)


# --- 1. Background (objeto saliente / quitar fondo) ---

def segmentar_background(imagen: Image.Image) -> Image.Image:
    if "rembg" not in _cache:
        _cache["rembg"] = new_session("u2net")
    return remove(imagen.convert("RGB"), session=_cache["rembg"])


# --- 2. Semantic (una etiqueta por píxel, sin instancias) ---

def _modelo_semantic():
    if "semantic" not in _cache:
        nombre = "nvidia/segformer-b0-finetuned-ade-512-512"
        _cache["semantic"] = (
            AutoImageProcessor.from_pretrained(nombre),
            AutoModelForSemanticSegmentation.from_pretrained(nombre),
        )
    return _cache["semantic"]


def segmentar_semantic(imagen: Image.Image) -> Image.Image:
    processor, model = _modelo_semantic()
    rgb = imagen.convert("RGB")
    inputs = processor(images=rgb, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    h, w = rgb.size[1], rgb.size[0]
    upsampled = torch.nn.functional.interpolate(logits, size=(h, w), mode="bilinear", align_corners=False)
    seg = upsampled.argmax(dim=1)[0].cpu().numpy()

    color = np.zeros((h, w, 3), dtype=np.uint8)
    for cid in np.unique(seg):
        color[seg == cid] = _color_por_id(int(cid))
    return _superponer(rgb, Image.fromarray(color))


# --- 3. Instance (máscara por objeto detectado) ---

def _modelo_instance():
    if "instance" not in _cache:
        _cache["instance"] = YOLO("yolov8n-seg.pt")
    return _cache["instance"]


def segmentar_instance(imagen: Image.Image) -> Image.Image:
    rgb = imagen.convert("RGB")
    resultados = _modelo_instance()(np.array(rgb), verbose=False)
    dibujo = resultados[0].plot()[:, :, ::-1]  # BGR → RGB
    return Image.fromarray(dibujo)


# --- Router general ---

_DISPATCH = {
    "background": segmentar_background,
    "semantic": segmentar_semantic,
    "instance": segmentar_instance,
}


def segmentar(imagen: Image.Image, tipo: str) -> Image.Image:
    """Recibe imagen + tipo y devuelve el resultado."""
    tipo = tipo.lower().strip()
    if tipo not in _DISPATCH:
        raise ValueError(f"tipo debe ser uno de: {', '.join(TIPOS)}")
    return _DISPATCH[tipo](imagen)


@app.get("/tipos")
def listar_tipos():
    return {"tipos": list(TIPOS)}


@app.post("/segmentar")
def api_segmentar():
    if "imagen" not in request.files:
        return {"error": "Envía un archivo en el campo 'imagen'"}, 400
    tipo = request.form.get("tipo", "background")
    try:
        entrada = Image.open(request.files["imagen"].stream)
        salida = segmentar(entrada, tipo)
    except ValueError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        return {"error": str(e)}, 500

    salida.save(SALIDA)
    buf = BytesIO()
    salida.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


if __name__ == "__main__":
    print("Tipos:", ", ".join(TIPOS))
    print(f"Ejemplo: {EJEMPLO}")
    print(f"GET  http://localhost:{PUERTO}/tipos")
    print(f'POST http://localhost:{PUERTO}/segmentar  →  curl -F "imagen=@{EJEMPLO}" -F "tipo=instance" ...\n')
    app.run(host="0.0.0.0", port=PUERTO)
