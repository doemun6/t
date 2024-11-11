import streamlit as st
import os
from openai import OpenAI

st.title("챗봇")  # 제목 수정

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
    
system_message = '''
    당신의 이름은 챗봇입니다.
    영어로 질문을 받아도 한글로 답해주세요.
    한글이 아닌 답변일 때는 다시 생각해서 꼭 한글로 만들어주세요.
    모든 답변의 끝에는 답변에 맞는 이모티콘도 추가해주세요.
'''

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role" : "system", "content" : system_message}]

# Display chat messages from history on app rerun
for idx, message in enumerate(st.session_state.messages):
    if idx > 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
# Accept user input
if prompt := st.chat_input("대화를 입력해주세요"):  
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})