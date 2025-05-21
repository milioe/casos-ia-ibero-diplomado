import gradio as gr
import json
import os
import io
import tempfile
from utils import process_transcript, create_formatted_docx
from datetime import datetime

def read_file(file_path: str) -> str:
    """Extract text from a file based on its extension."""
    file_name = os.path.basename(file_path)
    
    if file_name.lower().endswith('.pdf'):
        from PyPDF2 import PdfReader
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    elif file_name.lower().endswith('.docx'):
        import docx
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    elif file_name.lower().endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    else:
        raise ValueError("Unsupported file format")

def process_document(file_obj):
    """Process uploaded document and extract structured dialogue."""
    try:
        if file_obj is None:
            return "Error: No file uploaded"

        # Get the file path and name
        file_path = file_obj.name
        
        # Read the file content based on its type
        text = read_file(file_path)
        
        # Process the extracted text
        result = process_transcript(text)
        
        # Convert to JSON string with proper formatting
        formatted_json = json.dumps(result.model_dump(), indent=2, ensure_ascii=False)
        
        return formatted_json

    except Exception as e:
        return f"Error processing document: {str(e)}"

def download_as_word(json_data, person_name, file_number, date_time, committee_members):
    """Convert JSON data to Word document and return for download."""
    try:
        if not json_data or json_data.strip() == "":
            return None
        
        # Set default values if fields are empty
        person_name = person_name.strip() if person_name and person_name.strip() else "XXXX"
        file_number = file_number.strip() if file_number and file_number.strip() else "CG/0X/2025"
        date_time = date_time.strip() if date_time and date_time.strip() else "XXXX"
        committee_members = committee_members.strip() if committee_members and committee_members.strip() else "xxxx y xxxx"
        
        # Create the formatted Word document
        docx_bytes = create_formatted_docx(json_data, person_name, file_number, date_time, committee_members)
        
        if docx_bytes is None:
            return None
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        temp_file.write(docx_bytes)
        temp_file.close()
        
        return temp_file.name
        
    except Exception as e:
        print(f"Error downloading Word document: {str(e)}")
        return None

# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as iface:
    gr.Markdown("# Dialogue Structure Extractor")
    gr.Markdown("Upload a document containing dialogue/transcript and get structured output with speaker information.")
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(
                label="Upload Document",
                file_types=[".pdf", ".docx", ".txt"],
                type="filepath"
            )
        
        with gr.Column(scale=2):
            json_output = gr.Textbox(
                label="Structured Dialogue",
                lines=20
            )
    
    with gr.Row():
        process_btn = gr.Button("Process Document")
    
    gr.Markdown("### Document Information")
    with gr.Row():
        with gr.Column(scale=1):
            person_name = gr.Textbox(
                label="Nombre de la persona agraviada",
                placeholder="XXXX",
                info="Dejar en blanco para usar XXXX"
            )
        with gr.Column(scale=1):
            file_number = gr.Textbox(
                label="Número de expediente",
                placeholder="CG/0X/2025",
                info="Dejar en blanco para usar CG/0X/2025"
            )
    
    with gr.Row():
        with gr.Column(scale=1):
            current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            date_time = gr.Textbox(
                label="Fecha y hora (DD/MM/AAAA HH:MM)",
                placeholder=current_date,
                info="Dejar en blanco para usar XXXX"
            )
        with gr.Column(scale=1):
            committee_members = gr.Textbox(
                label="Integrantes de la Unidad del Comité",
                placeholder="xxxx y xxxx",
                info="Nombres de los integrantes separados por 'y' o comas"
            )
    
    with gr.Row():
        download_btn = gr.Button("Download as Word")
    
    word_output = gr.File(label="Download Word Document")
    
    # Set up event handlers
    process_btn.click(
        fn=process_document,
        inputs=file_input,
        outputs=json_output
    )
    
    download_btn.click(
        fn=download_as_word,
        inputs=[json_output, person_name, file_number, date_time, committee_members],
        outputs=word_output
    )

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7071, share=True) 