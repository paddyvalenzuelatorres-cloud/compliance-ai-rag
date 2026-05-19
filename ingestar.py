import os
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Carpeta con PDF
carpeta_docs = "documentos"

# Lista general
all_documents = []

# Leer todos los PDFs
for archivo in os.listdir(carpeta_docs):
    if archivo.endswith(".pdf"):
        ruta_completa = os.path.join(carpeta_docs, archivo)
        print(f"Cargando archivo: {archivo}")

        reader = PdfReader(ruta_completa)

        for page_num, page in enumerate(reader.pages):
            texto = page.extract_text()

            if texto:
                doc = Document(
                    page_content=texto,
                    metadata={
                        "source_file": archivo,
                        "page": page_num + 1
                    }
                )
                all_documents.append(doc)

# Configurar fragmentación
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# Crear chunks
chunks = text_splitter.split_documents(all_documents)

# Resultados
print(f"\nTotal páginas cargadas: {len(all_documents)}")
print(f"Total fragmentos generados: {len(chunks)}")

# Ejemplo
if chunks:
    print("\n--- PRIMER FRAGMENTO ---\n")
    print(chunks[0].page_content)

    print("\n--- METADATA ---\n")
    print(chunks[0].metadata)
else:
    print("No se pudo extraer texto. Revisa si el PDF es escaneado o imagen.")