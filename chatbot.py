from groq import Groq
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()
api_token = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_token)

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your research assistant. How can I help you today? You can ask me to explain research papers or anything else you're curious about!"}
    ]

st.header("Research Chatbot-V2")
st.subheader("~ Powered by GROQ")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant. Provide clear, concise explanations about research topics and papers when asked."},
                    *st.session_state.messages  
                ],
                model="deepseek-r1-distill-qwen-32b",
                stream=False,
            )
            response = chat_completion.choices[0].message.content
            st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

if st.button("Clear Conversation"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Conversation cleared! How can I assist you now?"}
    ]
    st.experimental_rerun()