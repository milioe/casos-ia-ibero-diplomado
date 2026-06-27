# Guía rápida — Ollama

**Terminal:** Mac → `Cmd+Espacio`, escribe *Terminal*. Windows → tecla Windows, escribe *PowerShell*.

Instala en [ollama.com](https://ollama.com/download). Mismos comandos en Mac y Windows.

```bash
ollama --version
ollama list
ollama pull nomic-embed-text
ollama run qwen3.5:4b          # /bye para salir
ollama rm qwen3.5:4b           # sin :latest (aunque list lo muestre así)
```

**Windows / Linux:**

```bash
ollama pull qwen3.5:4b
```

**Mac con chip M** — baja la variante `-mlx`. **MLX** es el framework de Apple para correr modelos en el GPU del chip M (Metal); Ollama empaqueta una versión optimizada para eso. Suele ir más rápido que `qwen3.5:4b` estándar en Mac.

No necesitas borrar nada *antes* del pull; si ya bajaste `qwen3.5:4b`, puedes eliminarlo después para liberar ~3.4 GB:

```bash
ollama pull qwen3.5:4b-mlx
ollama rm qwen3.5:4b           # opcional, solo si ya lo tenías
```

Pesos de [qwen3.5](https://ollama.com/library/qwen3.5) (entra al modelo → **Tags** para verlos en la web):

| `ollama pull …` | Peso |
|-----------------|------|
| `qwen3.5:0.8b` | 1.0 GB |
| `qwen3.5:2b` | 2.7 GB |
| `qwen3.5:4b` | 3.4 GB |
| `qwen3.5:4b-mlx` | 4.0 GB (Mac M) |
| `qwen3.5:9b` | 6.6 GB |
| `nomic-embed-text` | 274 MB |

`ollama list` confirma lo instalado. Durante `pull` también ves el tamaño.
