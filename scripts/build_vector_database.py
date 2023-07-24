import os
import openai
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.schema import Document
from langchain.document_loaders import PyPDFLoader
from tqdm import tqdm
import chromadb
assert chromadb.__version__ == "0.4.2"


SCIKIT_IMAGE_VERSION = os.environ.get("SCIKIT_IMAGE_VERSION")
assert SCIKIT_IMAGE_VERSION is not None, "Please set SCIKIT_IMAGE_VERSION environment variable"

def create_embeddings_from_pdf(pdf_path, collection_name):
    # convert pdf to texts
    loader = PyPDFLoader(pdf_path)
    # split texts into chunks
    doc = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(doc)
    # create embeddings
    embeddings = OpenAIEmbeddings()
    print(f"Creating embeddings (#documents={len(documents)}))")
    vectordb = Chroma.from_documents(documents, embeddings, persist_directory="docs/vectordb", collection_name=collection_name)
    return vectordb

if __name__ == "__main__":
    vectordb = create_embeddings_from_pdf(f"docs/scikit-image-{SCIKIT_IMAGE_VERSION}.pdf", collection_name="scikit-image")
    vectordb.persist()
    print("Embeddings created")


    vectordb = Chroma(collection_name="scikit-image", persist_directory="docs/vectordb", embedding_function=OpenAIEmbeddings())
    retriever = vectordb.as_retriever(score_threshold=0.4)
    items = retriever.get_relevant_documents("scikit-image release", verbose=True)
    print(items)
    
