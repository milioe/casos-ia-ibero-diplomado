import pickle
from pathlib import Path

# --- Pon aquí tus palabras ---
SUMAR = ["rey", "mujer"]      # vectores que sumas
RESTAR = ["hombre"]           # vectores que restas (deja [] si no quieres restar)

m = pickle.load(open(Path(__file__).parent / "modelo_word2vec_sg.pkl", "rb"))
sims = m.wv.most_similar(positive=SUMAR, negative=RESTAR, topn=8)
for p, s in sims:
    print(f"{p}\t{s:.4f}")
