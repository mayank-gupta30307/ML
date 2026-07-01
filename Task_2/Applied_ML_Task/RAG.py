import os
from embedding_fn import embedding
from langchain_community.vectorstores.chroma import Chroma
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.retrievers import BM25Retriever
from Creating_Vectorstore import compiled_data

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
embedding_fn = embedding()
curr_dir = os.path.dirname(__file__)

Vectorstore = Chroma(
    persist_directory = os.path.join(curr_dir , "Vectorstore"),
    embedding_function = embedding_fn
)

data = compiled_data()
bm25_retriever = BM25Retriever.from_documents(data)
bm25_retriever.k = 20

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=api_key,
    temperature=0.1
)

def answer_query(query):
    vec_docs = Vectorstore.similarity_search(query=query , k=20)
    bm25_docs = bm25_retriever.invoke(query)

    unique_docs = {}
    for doc in vec_docs+bm25_docs:
        if doc.page_content not in unique_docs:
            unique_docs[doc.page_content] = doc
    docs = unique_docs.values()
    
    context = "\n\n".join(
        doc.page_content
        + "\n"
        + "\n".join(f"{k}: {v}" for k, v in doc.metadata.items())
        for doc in docs)
    prompt = f"""
You are a healthcare chatbot
Answer ONLY using the provided context.
Try to understand the context and give the answer in a clean format explaining it in detail
also provide possible desease that the person could have and its treatment provide evidence to each thing you say
If evidence is not enough for any claim , say:
"I could not find sufficient information regarding your query"
Do not hallucinate cause if you do i will literally shoot your artificial brain out
Also Do not make things and do not use prior knowledge or anything, if something isnt provided or can't be interpretted say,
don't tell that thing
In case of conflict give priority to WHO source as it is more trusted.
Mention sources and links if given in the context else only provide source provide source at the end in a structured one line per source format.

Context:
{context}

Question:
{query}
"""
    try:
        response = llm.invoke(prompt)
        return response.content[0]["text"]
    except:
        return "Gemimi Limit Reached"
    
if __name__=="__main__":
    query = input("Enter Query : ")
    response = answer_query(query=query)
    print(response)