# PDF Question Answering System using RAG, LangChain, OpenAI & ChromaDB

A Python-based **Retrieval-Augmented Generation (RAG)** application that allows users to ask questions about PDF documents and receive context-aware answers using OpenAI's GPT-4o model.

The application extracts text from PDF files, splits it into smaller chunks, generates embeddings, stores them in a ChromaDB vector database, and retrieves relevant information to answer user queries.

## 🚀 Features

- **PDF Document Loading:** Extracts text and metadata from PDF files using `PyPDFLoader`.
- **Text Splitting:** Splits documents into manageable chunks using `RecursiveCharacterTextSplitter`.
- **Text Embeddings:** Generates vector embeddings using OpenAI Embeddings.
- **Vector Database:** Stores and retrieves document embeddings using ChromaDB.
- **RAG Pipeline:** Uses LangChain's `RetrievalQA` chain to generate context-aware answers.
- **Semantic Search:** Retrieves the top 3 most relevant document chunks for each query.
- **Source References:** Displays the source PDF and page numbers used to generate answers.
- **Token Usage Tracking:** Tracks prompt tokens, completion tokens, total tokens, and estimated API cost.
- **Persistent Storage:** Saves embeddings locally so the vector database can be reused.
- **Interactive CLI:** Allows users to continuously ask questions until they type `exit`.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| LangChain | RAG application framework |
| OpenAI GPT-4o | Large Language Model |
| OpenAI Embeddings | Text embedding generation |
| ChromaDB | Vector database |
| PyPDF | PDF document processing |

## 📂 Project Structure

```text
PDF-RAG-Application/
│
├── main.py                  # Main application code
├── yourdocument.pdf         # Input PDF document
├── chroma_vector_store/     # Persistent ChromaDB storage
├── README.md                # Project documentation
└── requirements.txt         # Project dependencies
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Navigate to the project directory:

```bash
cd PDF-RAG-Application
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install langchain langchain-community langchain-openai chromadb pypdf
```

> Note: The supplied code uses older LangChain import paths. Depending on your installed LangChain version, you may need to update the imports and use compatible package versions.

### 4. Configure OpenAI API Key

Generate an API key from the [OpenAI Platform](https://platform.openai.com/api-keys).

Set the API key as an environment variable.

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your-api-key"
```

**Linux / macOS:**
```bash
export OPENAI_API_KEY="your-api-key"
```

Alternatively, use a `.env` file with `python-dotenv`.

**Important:** Never commit your actual API key to GitHub.

### 5. Add Your PDF Document

Place your PDF file in the project directory and update the PDF path in `main.py`:

```python
pdf_path = "yourdocument.pdf"
```

Replace `yourdocument.pdf` with your actual PDF filename.

## ▶️ Usage

Run the application:

```bash
python main.py
```

The application will:

1. Load the PDF document.
2. Extract its text.
3. Split the text into chunks of 1000 characters with 200 characters of overlap.
4. Generate embeddings for each chunk.
5. Store embeddings in ChromaDB.
6. Initialize the RAG pipeline.
7. Wait for user questions.

## 🧠 How RAG Works

The application follows a Retrieval-Augmented Generation workflow.

```text
             PDF Document
                  |
                  ▼
           PDF Text Extraction
                  |
                  ▼
             Text Splitting
                  |
                  ▼
          Generate Embeddings
                  |
                  ▼
          ChromaDB Vector Store
                  |
                  ▼
             User Query
                  |
                  ▼
          Semantic Retrieval
             (Top 3 Chunks)
                  |
                  ▼
          GPT-4o + Retrieved Context
                  |
                  ▼
             Generated Answer
                  |
                  ▼
        Answer + Source References
```

## ⚙️ Configuration

You can customize the RAG pipeline using the following parameters:

| Parameter | Default Value | Description |
|---|---|---|
| `chunk_size` | 1000 | Maximum chunk size |
| `chunk_overlap` | 200 | Overlapping characters between chunks |
| `search_type` | similarity | Retrieval search method |
| `k` | 3 | Number of relevant chunks retrieved |
| `model` | gpt-4o | OpenAI chat model |
| `temperature` | 0 | Controls response randomness |

## 📊 Token Usage and Cost Tracking

The application uses LangChain's `get_openai_callback()` to monitor API usage.

It displays:

- Prompt token count
- Completion token count
- Total token count
- Estimated API cost

This helps monitor OpenAI API consumption and manage application costs.

## ⚠️ Important Notes

- An active OpenAI API key is required.
- OpenAI API usage may incur charges.
- PDF files should contain extractable text. Scanned PDFs may require OCR processing.
- The ChromaDB directory stores embeddings persistently.
- The current implementation does not automatically detect changes in an existing PDF.
- If you change the source PDF, consider rebuilding the vector database to avoid retrieving outdated information.
- The configured vector store directory is `chroma_vector_store`.

## 🔮 Future Improvements

Potential enhancements include:

- Support for multiple PDF documents.
- OCR support for scanned PDFs.
- Streamlit or FastAPI-based user interface.
- Chat history and conversational memory.
- Improved retrieval using MMR or hybrid search.
- Metadata filtering.
- Document upload functionality.
- Support for additional LLM providers.
- Automatic document update detection.



