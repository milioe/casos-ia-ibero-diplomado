import ollama

MODELO = "qwen3.5:4b-mlx"
SYSTEM = "Eres un asistente útil. Respondes en español."
VENTANA = 10  # pares user+assistant (el system siempre va)

def contexto(mensajes):
    return [mensajes[0]] + mensajes[1:][-VENTANA * 2:]

def chat(mensajes, entrada):
    mensajes.append({"role": "user", "content": entrada})
    texto = ""
    for c in ollama.chat(model=MODELO, messages=contexto(mensajes), stream=True, think=False):
        t = c.message.content or ""
        texto += t
        yield t
    mensajes.append({"role": "assistant", "content": texto})

def conversar():
    mensajes = [{"role": "system", "content": SYSTEM}]
    while True:
        entrada = input("Tú: ")
        if entrada.lower() == "salir":
            break
        print("\nQwen: ", end="", flush=True)
        for t in chat(mensajes, entrada):
            print(t, end="", flush=True)
        print("\n")

conversar()
