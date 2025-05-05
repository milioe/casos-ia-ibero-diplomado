import gradio as gr
import requests
import pandas as pd
import json
import logging
import os

def is_valid_image(file_path):
    """Valida si el archivo es una imagen con formato soportado."""
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
    _, ext = os.path.splitext(file_path)
    return ext.lower() in valid_extensions

def process_images(files):
    """
    Envía las imágenes a la Azure Function y procesa la respuesta.
    
    Args:
        files (list): Lista de archivos de imagen
        
    Returns:
        tuple: Un string markdown con información general y un DataFrame con detalles de compras
    """
    try:
        # Validar formatos de archivo
        for file in files:
            if not is_valid_image(file.name):
                return (
                    "### Error\nFormato no soportado. Use PNG, JPEG, GIF o WEBP",
                    pd.DataFrame()
                )

        # Preparar los archivos para la petición
        files_dict = {}
        for i, file in enumerate(files):
            with open(file.name, 'rb') as f:
                files_dict[f'image_{i}'] = (
                    file.name.split('/')[-1],
                    f.read(),
                    'image/jpeg' if file.name.lower().endswith(('.jpg', '.jpeg')) else 'image/png'
                )
        
        response = requests.post(
            'http://localhost:7071/api/extract_info',
            files=files_dict
        )
        
        if response.status_code != 200:
            return (
                f"### Error\n{response.text}",
                pd.DataFrame()
            )
            
        data = response.json()
        
        # Crear markdown con información general
        general_info_md = f"""
### Información de la Compañía

**Compañía:** {data['nombre_compania']}

**RFC:** {data['rfc']}

**Fecha:** {data['fecha']}

**Clave Facturación:** {data['clave_facturacion']}

**Ubicación:** {data['ubicacion']}

**Teléfono:** {data['telefono']}
"""
        
        # Asegurar que todas las listas tengan la misma longitud
        max_length = max(
            len(data['productos']),
            len(data['unidades']),
            len(data['montos'])
        )
        
        # Rellenar las listas más cortas con 'NA'
        productos = data['productos'] + ['NA'] * (max_length - len(data['productos']))
        unidades = data['unidades'] + ['NA'] * (max_length - len(data['unidades']))
        montos = data['montos'] + [0.0] * (max_length - len(data['montos']))
        
        # Crear DataFrame con detalles de compras
        compras_df = pd.DataFrame({
            "Producto": productos,
            "Cantidad": unidades,
            "Monto": [f"${monto:.2f}" if monto != 0.0 else "NA" for monto in montos]
        })
        
        return general_info_md, compras_df
        
    except Exception as e:
        logging.error(f"Error en process_images: {str(e)}")
        return (
            f"### Error\n{str(e)}",
            pd.DataFrame()
        )

# Crear la interfaz
with gr.Blocks(title="Extractor de Tickets", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""# 🧾 Extractor de Tickets""")
    
    with gr.Column():
        files_input = gr.Files(
            label="Arrastra o selecciona tickets",
            file_count="multiple",
            file_types=["image"]
        )
        
        submit_btn = gr.Button("Procesar", variant="primary", size="lg")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Información General")
                general_info_md = gr.Markdown()
            
            with gr.Column():
                gr.Markdown("### Detalles de Compras")
                purchases_table = gr.Dataframe(
                    headers=[
                        "Producto",
                        "Cantidad",
                        "Monto"
                    ],
                    label="Productos y Montos",
                    wrap=True
                )
    
    submit_btn.click(
        fn=process_images,
        inputs=[files_input],
        outputs=[general_info_md, purchases_table]
    )

# Iniciar la aplicación
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True
    ) 