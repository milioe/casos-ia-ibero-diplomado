"""
Detección facial con webcam + DeepFace (open source).

  pip install deepface opencv-python tf-keras

Teclas:  ESPACIO = analizar   Q = salir

Qué puede hacer DeepFace (además de edad / género / emoción):
  - analyze → también "race" (impreciso; descomentar en ACCIONES si lo quieres)
  - analyze + anti_spoofing → ¿rostro real o foto/pantalla?
  - verify(img1, img2) → ¿es la misma persona?
  - represent(img) → vector embedding del rostro (búsqueda / comparación)
  - find(img, db_path) → buscar ese rostro en una carpeta de fotos
"""

import cv2
from deepface import DeepFace

DETECTOR = "opencv"
ACCIONES = ["age", "gender", "emotion"]  # opcional: agrega "race"
ANTI_SPOOFING = True  # detecta si es persona real o spoof (foto de foto)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la cámara")

print("Cámara lista — ESPACIO = analizar | Q = salir\n")

while True:
    ok, frame = cap.read()
    if not ok:
        break

    cv2.imshow("DeepFace", frame)
    tecla = cv2.waitKey(1) & 0xFF

    if tecla in (ord("q"), ord("Q")):
        break

    if tecla == ord(" "):
        print("Analizando...")
        resultados = DeepFace.analyze(
            img_path=frame,
            actions=ACCIONES,
            detector_backend=DETECTOR,
            enforce_detection=False,
            anti_spoofing=ANTI_SPOOFING,
        )
        if isinstance(resultados, dict):
            resultados = [resultados]

        for i, r in enumerate(resultados, 1):
            x, y, w, h = r["region"]["x"], r["region"]["y"], r["region"]["w"], r["region"]["h"]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            real = r.get("is_real", True)
            etiqueta_real = "REAL" if real else "SPOOF"
            texto = f"{r['dominant_emotion']} | {r['age']}a | {r['dominant_gender']} | {etiqueta_real}"
            cv2.putText(frame, texto, (x, max(y - 8, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            print(f"  Rostro {i}: edad={r['age']}, género={r['dominant_gender']}, emoción={r['dominant_emotion']}")
            if ANTI_SPOOFING:
                print(f"    Anti-spoof: {etiqueta_real} (score={r.get('antispoof_score', 0):.2f})")
            if "dominant_race" in r:
                print(f"    Etnia estimada: {r['dominant_race']}")
            emociones = sorted(r["emotion"].items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"    Top emociones: {', '.join(f'{e} {v:.0f}%' for e, v in emociones)}")
        print()

        cv2.imshow("DeepFace", frame)
        cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()
