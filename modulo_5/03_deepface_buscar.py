"""
Reconocimiento facial 1:N — tu foto vs carpeta banco_rostros/

  pip install deepface opencv-python tf-keras pandas

DeepFace.find compara el rostro de tu foto con cada imagen del banco
y devuelve las más parecidas (distancia baja = más similar).

Teclas:  ESPACIO = capturar y buscar   Q = salir

Agrega más .jpg a banco_rostros/ para ampliar la biblioteca.
"""

from pathlib import Path

import cv2
from deepface import DeepFace

CARPETA = Path(__file__).parent
BANCO = CARPETA / "banco_rostros"
YO = CARPETA / "yo.jpg"
MODELO = "VGG-Face"
DETECTOR = "opencv"
TOP = 5  # coincidencias a mostrar

fotos = [f for f in BANCO.iterdir() if f.suffix.lower() in {".jpg", ".jpeg", ".png"}]
if not fotos:
    raise RuntimeError(f"Agrega fotos con rostros en {BANCO}")

print(f"Banco: {len(fotos)} imágenes en {BANCO.name}/")
print("ESPACIO = capturar y buscar | Q = salir\n")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la cámara")

while True:
    ok, frame = cap.read()
    if not ok:
        break

    cv2.imshow("DeepFace find", frame)
    tecla = cv2.waitKey(1) & 0xFF

    if tecla in (ord("q"), ord("Q")):
        break

    if tecla == ord(" "):
        cv2.imwrite(str(YO), frame)
        print(f"Foto guardada: {YO.name} — buscando en el banco...\n")

        resultados = DeepFace.find(
            img_path=str(YO),
            db_path=str(BANCO),
            model_name=MODELO,
            detector_backend=DETECTOR,
            enforce_detection=False,
            silent=True,
        )

        for i, df in enumerate(resultados, 1):
            print(f"--- Rostro {i} en tu foto ---")
            if df.empty:
                print("  Sin coincidencias bajo el umbral\n")
                continue
            for _, fila in df.head(TOP).iterrows():
                nombre = Path(fila["identity"]).name
                dist, umbral = fila["distance"], fila["threshold"]
                etiqueta = "misma persona" if dist <= umbral else "distinto"
                print(f"  {nombre}: distancia={dist:.3f} (umbral {umbral:.3f}) → {etiqueta}")
            print()

        cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()
