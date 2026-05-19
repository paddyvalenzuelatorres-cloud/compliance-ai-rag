import os
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Carpeta de documentos
carpeta_docs = "documentos"

# Lista documentos
all_documents = []

# Leer PDFs
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

# Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(all_documents)

print(f"Total fragmentos generados: {len(chunks)}")

# Modelo embeddings gratuito
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Crear base vectorial
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="chroma_db"
)

# Guardar
vectorstore.persist()

print("Base vectorial creada y guardada en /chroma_db")