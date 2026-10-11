from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

def create_vector_store():
    print("Loading data...")

    if not os.path.exists("data"):
        print("❌ 'data' folder not found!")
        return None

    documents = []

    # Load TXT files
    txt_loader = DirectoryLoader(
        "data",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents.extend(txt_loader.load())
    print("✅ TXT files loaded")

    # Load PDF files
    pdf_loader = DirectoryLoader(
        "data",
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    documents.extend(pdf_loader.load())
    print("✅ PDF files loaded")

    print(f"Total documents: {len(documents)}")

    if len(documents) == 0:
        print("❌ No documents found.")
        return None

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    texts = text_splitter.split_documents(documents)
    print(f"✅ Total chunks: {len(texts)}")

    print("Generating embeddings...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local("faiss_index")

    print("✅ Vector store successfully created!")
    return vectorstore

if __name__ == "__main__":
    create_vector_store()