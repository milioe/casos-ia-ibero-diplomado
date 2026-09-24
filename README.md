# Módulo 4 — Procesamiento de lenguaje natural (NLP)

Material del módulo en la carpeta [`modulo_4`](modulo_4/). Cada notebook incluye un enlace para abrirlo en **Google Colab** desde la primera celda.

## Contenido

| Notebook | Descripción breve |
|----------|-------------------|
| [`01_Texto_y_maquina.ipynb`](modulo_4/01_Texto_y_maquina.ipynb) | Cómo "ve" la máquina el texto: caracteres, Unicode, palabras, vocabulario y límites de representaciones clásicas. |
| [`02-PDF_reporte.ipynb`](modulo_4/02-PDF_reporte.ipynb) | **Parsing** de un PDF con texto digital (`pypdf`) y **Split** por página. Cierra mostrando que el parsing falla cuando el documento es en realidad una imagen. |
| [`03-OCRfacturas.ipynb`](modulo_4/03-OCRfacturas.ipynb) | **Parsing** (Tesseract, EasyOCR) y **Extraction** (regex, Falcon-OCR, LlamaExtract) sobre la misma factura — 4 métodos, comparados a simple vista, más una guía de "¿cuál me conviene?". |
| [`04_TF-IDF.ipynb`](modulo_4/04_TF-IDF.ipynb) | TF-IDF desde cero (TF, IDF, y el vector final) sobre tickets de soporte, y comparación contra `TfidfVectorizer` de scikit-learn. |
| [`05_Jaccard_Coseno.ipynb`](modulo_4/05_Jaccard_Coseno.ipynb) | Similitud de Jaccard y coseno para medir qué tan parecidos son dos textos, sobre el mismo corpus de tickets de soporte. |
| [`06_Intro_redes_neuronales.ipynb`](modulo_4/06_Intro_redes_neuronales.ipynb) | Redes neuronales desde lo más chico posible (un perceptrón) hasta un caso real: predecir lluvia con el dataset *Rain in Australia*. |
| [`07_Word2Vec.ipynb`](modulo_4/07_Word2Vec.ipynb) | Word2Vec a mano con Keras (Skip-gram, ventana 1) sobre "el usuario no puede transferir en la app", CBOW vs Skip-gram y negative sampling. |
| [`08_Word2Vec_scaling.ipynb`](modulo_4/08_Word2Vec_scaling.ipynb) | Word2Vec con `gensim` sobre un corpus grande en español: vecinos, analogías, PCA 3D y export a Embedding Projector. |

## Contacto

- Email: emilio@milioe.com
