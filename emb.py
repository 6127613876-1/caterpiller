from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Load and split PDF documents
def load_and_split_pdfs(pdf_dir):
    all_chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(pdf_dir, filename))
            pages = loader.load()
            chunks = splitter.split_documents(pages)
            all_chunks.extend(chunks)
    
    return all_chunks

# Load PDF files
docs = load_and_split_pdfs("pdfs")  # Folder with PDF files

# Create and persist vector DB
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectordb = Chroma.from_documents(documents=docs, embedding=embedding, persist_directory="db")
vectordb.persist()
print("✅ PDFs embedded and saved to vector DB")
