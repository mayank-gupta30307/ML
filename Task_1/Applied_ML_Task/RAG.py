import os
from embedding_fn import embedding
from langchain_community.vectorstores.chroma import Chroma
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
embedding_fn = embedding()

Vectorstore = Chroma(
    persist_directory=os.path.join(os.path.dirname(__file__),"Vectorstore"),
    embedding_function=embedding_fn
)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=api_key,
    temperature=0.5
)

def answer_query(query):
    docs = Vectorstore.similarity_search(
        query=query,
        k=25
    )
    context = "\n\n".join(doc.page_content+"\nSource : "+doc.metadata["Source"] for doc in docs)
    prompt = f"""
Answer ONLY using the provided context.
Try to understand the context and give the answer in a clean format explaining it in detail
if answer is not in any of the contexts provided, say:
"I could not find sufficient information in the papers."
Do not hallucinate cause if you do i will literally shoot your artificial brain out
Mention all the paper names used to understnad it.

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