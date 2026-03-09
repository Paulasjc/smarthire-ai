import fitz  # Esta es la librería PyMuPDF

def extract_text_from_pdf(uploaded_file):
    """
    Toma un archivo subido de Streamlit, lo lee y devuelve el texto plano.
    """
    try:
        # Leemos los bytes del archivo subido
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error al leer el PDF: {e}"
    doc.close()