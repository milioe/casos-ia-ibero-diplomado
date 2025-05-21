from ollama import chat

messages = [
    {
        'role': 'system',
        'content': '''
        Eres un asistente de soporte técnico experto para una tienda de electrónicos. 
        Tu objetivo es ayudar a los clientes con:
        - Problemas técnicos con sus dispositivos
        - Recomendaciones de productos
        - Información sobre garantías y devoluciones
        - Proceso de compra y envíos

        Debes ser siempre amable, paciente y profesional. Proporciona respuestas claras y detalladas, 
        y asegúrate de obtener toda la información necesaria para ayudar efectivamente al cliente.
'''
    }
]

print("\n=== Soporte Técnico de Electrónicos ===")
print("(Escribe 'salir' para terminar la conversación)")
print("\nAsesor: ¡Hola! ¿En qué puedo ayudarte hoy?\n")

while True:
    user_input = input('\nCliente: ')
    
    if user_input.lower() == 'salir':
        print('\nGracias por contactar con nuestro soporte técnico. ¡Que tengas un excelente día!')
        break
    
    print('\nAsesor:', end=' ', flush=True)
    
    # Realizar la consulta con streaming
    current_response = ''
    for part in chat(
        'llama3.1:8b',
        messages=[*messages, {'role': 'user', 'content': user_input}],
        stream=True
    ):
        chunk = part['message']['content']
        print(chunk, end='', flush=True)
        current_response += chunk
    
    print('\n')
    
    # Agregar la conversación al historial
    messages.extend([
        {'role': 'user', 'content': user_input},
        {'role': 'assistant', 'content': current_response}
    ])
