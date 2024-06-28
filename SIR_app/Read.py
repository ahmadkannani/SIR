import pythoncom
from docx import Document
import win32com.client
import os 
def read_doc_file(doc_path):
    pythoncom.CoInitialize()  # Initialize the COM library
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    doc_path = os.path.join(BASE_DIR, 'SIR_app/Data/{0}'.format(doc_path))

    try:
        if doc_path.endswith('.docx'):
            # For .docx files, use the python-docx library
            doc = Document(doc_path)
            paragraphs = [paragraph.text for paragraph in doc.paragraphs]
            return '\n'.join(paragraphs)
        elif doc_path.endswith('.doc'):
            # For .doc files, use the pywin32 library
            word_app = win32com.client.Dispatch('Word.Application')
            doc = word_app.Documents.Open(doc_path)
            content = doc.Content.Text
            doc.Close()
            return content
        else:
            print(f"Unsupported file format: {doc_path}")
            return None
    finally:
        pythoncom.CoUninitialize()  # Uninitialize the COM library

