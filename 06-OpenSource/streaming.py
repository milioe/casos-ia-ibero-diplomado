from ollama import chat

stream = chat(
    model='gemma3:4b',
    messages=[{'role': 'user', 'content': 'por qué el cielo es azul?'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)