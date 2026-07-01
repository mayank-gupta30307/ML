import streamlit as st
with st.spinner("Rebooting The Program..."):
    from RAG import answer_query

st.title("Medical Chatbot Assistant")

query = st.chat_input("Enter Query")

if query:
    with st.chat_message("user"):
        st.write(query)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = answer_query(query)
            st.write(response)