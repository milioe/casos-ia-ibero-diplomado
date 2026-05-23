# Word2Vec a escala — Notebook

Material del Módulo 4 NLP para entrenar y explorar Word2Vec en español.

## Notebooks

**`09_Word2Vec.ipynb`**
- Word2Vec a mano con Keras (Skip-gram con ventana)
- Corpus pequeño fintech
- CBOW vs Skip-gram y negative sampling (conceptual)

**`10_Word2Vec_scaling.ipynb`**
- Parte 1: Borges (*Funes el memorioso*) → PDF, tokens, Word2Vec, PCA 3D
- Parte 2: **Corpus completo Kaggle** (todos los `.zip` de la carpeta de Drive)
  - Listado y descarga automática con `gdown` (sin lista fija en código)
  - Carga de todos los ZIP, CBOW + Skip-gram con `gensim`
  - Vecinos, analogías, suma/resta de vectores, PCA 3D
  - Guardado opcional de modelos `.pkl`

## Instalación

```bash
pip install numpy matplotlib pandas scikit-learn gensim pypdf plotly gdown
```

## Corpus en Google Drive

https://drive.google.com/drive/folders/1U9V2Wp-ccTAz7JP__FxU1uAF79by-9uf?usp=sharing

Todos los `.zip` publicados en esa carpeta (fragmentos del [corpus Kaggle de 120M palabras](https://www.kaggle.com/datasets/rtatman/120-million-word-spanish-corpus/data)).

Colócalos en `corpus_descargado/` o deja que el notebook liste y descargue desde Drive (`DESCARGAR_FALTANTES = True`).

## Uso en clase

1. Ejecuta el notebook `10_Word2Vec_scaling.ipynb` de arriba hacia abajo.
2. Parte 1: solo necesitas `borges_funes.pdf`.
3. Parte 2: para demo rápida usa `N_ARCHIVOS = 3`; para corpus completo `N_ARCHIVOS = None` (puede tardar horas y requiere RAM).
4. Tras entrenar, ejecuta la celda **Guardar modelos** (`GUARDAR_MODELOS = True`) → `modelo_word2vec_sg.pkl` en esta carpeta.

## Probar el modelo guardado (CLI)

```bash
cd "Modulo 4: NLP"
python 10_word2vec_cli.py rey reina
python 10_word2vec_cli.py rey - hombre + mujer
```

## Parámetros clave (Parte 2)

| Variable | Valor por defecto | Significado |
|----------|-------------------|-------------|
| `N_ARCHIVOS` | `None` (todos en Drive) | Cuántos ZIP descargar/procesar |
| `MAX_LINEAS_POR_ARCHIVO` | `None` (archivo completo) | Límite por zip para pruebas rápidas |
| `VECTOR_SIZE` | 100 | Dimensión del embedding |
| `WINDOW` | 5 | Ventana Skip-gram / CBOW |
| `MIN_COUNT` | 10 | Mínimo de apariciones en el corpus |
| `EPOCHS` | 5 | Pasadas sobre el corpus |

## The Bitter Lesson

- **1 zip / poco texto** → vecinos ruidosos (`rey` ≈ `ii`, `san`).
- **10+ zips** → sinónimos y ciudades empiezan a tener sentido.
- **Muchos zips** → analogías tipo `rey - hombre + mujer ≈ reina` funcionan mejor.

## Referencias

- [Paper Word2Vec (Mikolov 2013)](https://arxiv.org/abs/1301.3781)
- [The Bitter Lesson (Sutton)](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)
