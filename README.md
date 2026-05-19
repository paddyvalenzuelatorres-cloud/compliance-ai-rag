# Compliance AI Assistant

Sistema RAG (Retrieval-Augmented Generation) desarrollado con Python, LangChain, ChromaDB y Ollama para consulta inteligente de normativa, compliance y protección de datos.

---

## Funcionalidades

- Consulta semántica de documentos PDF
- Recuperación contextual mediante RAG
- Embeddings locales con Sentence Transformers
- Base vectorial utilizando ChromaDB
- Integración LLM local mediante Ollama
- Interfaz web desarrollada con Streamlit
- Trazabilidad documental (fuente y página)

---

## Documentos utilizados

- ISO 27001
- Ley 19.628 - Protección de Datos Personales (Chile)

---

## Tecnologías utilizadas

- Python
- LangChain
- ChromaDB
- Ollama
- Streamlit
- Sentence Transformers
- HuggingFace Embeddings

---

##  Arquitectura

```text
PDFs
→ extracción de texto
→ chunking
→ embeddings
→ ChromaDB
→ búsqueda semántica
→ recuperación contexto
→ LLM (Ollama)
→ respuesta contextual
```

---

##  Estructura del proyecto

```text
compliance-ai-rag/
│
├── app.py
├── rag_chat.py
├── vectorizar.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── screenshots/
│
└── chroma_db/
```

---

## Instalación

### 1. Clonar repositorio

```bash
git clone https://github.com/paddyvalenzuelatorres-cloud/compliance-ai-rag.git
```

---

### 2. Crear entorno virtual

```bash
python -m venv venv
```

---

### 3. Activar entorno virtual

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

---

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 5.  Vectorización documentos

Agregar PDFs dentro de carpeta:

```text
documentos/
```

Luego ejecutar:

```bash
python vectorizar.py
```

---

Ejecutar aplicación

```bash
streamlit run app.py --server.address localhost
```

---

Ejemplos de consultas

- ¿Qué controles recomienda ISO 27001 para proteger información sensible?
- ¿Qué obligaciones establece la Ley 19.628 respecto al tratamiento de datos personales?
- ¿Cómo puede ISO 27001 ayudar al cumplimiento de la Ley 19.628?
- ¿Qué riesgos existen si una organización no protege adecuadamente los datos personales?

---

Screenshots

Agregar capturas de la aplicación aquí.

---

Objetivo del proyecto

Proyecto orientado a IA aplicada, compliance, seguridad de la información y recuperación semántica documental utilizando modelos LLM locales.

---

Mejoras futuras

- Upload dinámico de documentos
- Historial persistente
- Multi-document retrieval
- Citación avanzada de fuentes
- Dashboard métricas
- Soporte multiusuario
- Integración APIs empresariales

---

Autor

Paddy Valenzuela
