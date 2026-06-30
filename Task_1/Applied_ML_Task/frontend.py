import streamlit as st
with st.spinner("Loading Database Records..."):
    from RAG import answer_query

st.title("Retrieval-Augmented Generation(RAG) Chatbot")

query = st.text_input("Enter Query")

if query:
    with st.spinner("Searching answer for your query..."):
        response = answer_query(query)
    st.write(response)