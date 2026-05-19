from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import ollama

# Modelo embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Cargar base vectorial
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

print("Sistema RAG iniciado.")

while True:
    pregunta = input("\nPregunta: ")

    if pregunta.lower() == "salir":
        break

    # Buscar chunks relevantes
    resultados = vectorstore.similarity_search(
        pregunta,
        k=3
    )

    # Construir contexto
    contexto = "\n\n".join([
        f"""
        Fuente: {doc.metadata['source_file']}
        Página: {doc.metadata['page']}

        Contenido:
        {doc.page_content}
        """
        for doc in resultados
    ])

    # Prompt
    prompt = f"""
    Responde usando SOLO la información entregada.

    Contexto:
    {contexto}

    Pregunta:
    {pregunta}
    """

    # LLM
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\nRespuesta:\n")
    print(response["message"]["content"])

    print("\n--- FUENTES ---")
    for doc in resultados:
        print(
            f"{doc.metadata['source_file']} | página {doc.metadata['page']}"
        )