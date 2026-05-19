import streamlit as st
import ollama
from datetime import datetime

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# ------------------------------------------------
# CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="Compliance AI",
    page_icon="🔐",
    layout="wide"
)

# ------------------------------------------------
# ESTILOS
# ------------------------------------------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

with st.sidebar:

    st.title("⚙️ Configuración")

    top_k = st.slider(
        "Cantidad de fragmentos",
        min_value=1,
        max_value=10,
        value=5
    )

    st.markdown("---")

    st.markdown("""
    ### 📚 Documentos cargados
    - ISO 27001
    - Ley 19.628
    """)

    st.markdown("---")

    if st.button("🧹 Limpiar chat"):
        st.session_state.messages = []

# ------------------------------------------------
# TÍTULO
# ------------------------------------------------

st.title("🔐 Compliance AI Assistant")

st.markdown("""
Asistente RAG para consulta de normativa, compliance y protección de datos.
""")

# ------------------------------------------------
# EMBEDDINGS
# ------------------------------------------------

@st.cache_resource
def load_vectorstore():

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model
    )

    return vectorstore

vectorstore = load_vectorstore()

# ------------------------------------------------
# CHAT HISTORY
# ------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ------------------------------------------------
# INPUT
# ------------------------------------------------

prompt = st.chat_input(
    "Haz una pregunta sobre compliance..."
)

if prompt:

    # Guardar usuario
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Buscar respuesta
    with st.chat_message("assistant"):

        with st.spinner("Analizando documentos..."):

            resultados = vectorstore.similarity_search(
                prompt,
                k=top_k
            )

            contexto = "\n\n".join([
                f"""
                Fuente: {doc.metadata['source_file']}
                Página: {doc.metadata['page']}

                Contenido:
                {doc.page_content}
                """
                for doc in resultados
            ])

            prompt_llm = f"""
            Responde SOLO usando el contexto entregado.

            Si la información no existe,
            indica claramente que no fue encontrada.

            CONTEXTO:
            {contexto}

            PREGUNTA:
            {prompt}
            """

            response = ollama.chat(
                model="llama3",
                messages=[
                    {
                        "role": "user",
                        "content": prompt_llm
                    }
                ]
            )

            respuesta = response["message"]["content"]

            st.markdown(respuesta)

            # Fuentes
            with st.expander("📖 Ver fuentes utilizadas"):

                for doc in resultados:

                    st.markdown(f"""
                    **Documento:** {doc.metadata['source_file']}

                    **Página:** {doc.metadata['page']}
                    """)

                    st.caption(doc.page_content[:300] + "...")

    # Guardar respuesta
    st.session_state.messages.append({
        "role": "assistant",
        "content": respuesta
    })

# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.markdown("---")

st.caption(
    f"Compliance AI | RAG + Ollama + ChromaDB | {datetime.now().year}"
)