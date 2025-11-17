from ollama import chat
import streamlit as st

st.title("🦙 Ollama Chatbot")

if "ollama_model" not in st.session_state:
    st.session_state["ollama_model"] = "gemma2:2b"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        def generate_response():
            stream = chat(
                model=st.session_state["ollama_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            for chunk in stream:
                if chunk['message']['content']:
                    yield chunk['message']['content']
        
        response = st.write_stream(generate_response())
    st.session_state.messages.append({"role": "assistant", "content": response})
