import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama


# ✅ Load PDF
def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()


# ✅ Load Excel
def load_excel(file_path):
    df = pd.read_excel(file_path)

    docs = []
    for i, row in df.iterrows():
        text = " | ".join([f"{col}: {row[col]}" for col in df.columns])
        docs.append(Document(page_content=text))

    return docs


# ✅ Split documents
def split_docs(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(documents)


# ✅ Create vector store
def create_vector_store(chunks):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma.from_documents(chunks, embeddings)
    return db


# ✅ Create RAG chain
def create_rag_chain(db):
    retriever = db.as_retriever()

    llm = Ollama(model="llama3")

    def ask(query):
        docs = retriever.get_relevant_documents(query)
        context = "\n".join([d.page_content for d in docs])

        prompt = f"""
        Answer the question based only on the context below:

        Context:
        {context}

        Question:
        {query}
        """

        return llm.invoke(prompt)

    return ask