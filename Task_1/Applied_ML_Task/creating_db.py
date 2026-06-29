import os
from pypdf import PdfReader
from langchain_classic.schema.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from embedding_fn import embedding
from langchain_community.vectorstores.chroma import Chroma


data_path = os.path.dirname(__file__) + "\\PDFs"

def load_files(path):
    documents = []
    for pdf in os.listdir(path):
        reader = PdfReader(path+"\\"+pdf)
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text = full_text + text + "\n"
        documents.append({
            "Text":full_text,
            "Source":pdf
        })
    return documents

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000 , chunk_overlap=250)
    chunks = []
    for document in documents:
        chunked_text = text_splitter.split_text(document["Text"])
        for chunk in chunked_text:
            chunks.append(Document(
                page_content=chunk,
                metadata={"Source":document["Source"]}
            ))
    return chunks

def build_vectorstore(chunks , path):
    embedding_fn = embedding()
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_fn,
        persist_directory=os.path.join(path,"Vectorstore")
    )

if __name__=="__main__":
    documents = load_files(data_path)
    chunks = split_text(documents)
    build_vectorstore(chunks , os.path.dirname(__file__)) 