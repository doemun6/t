import streamlit as st
import os
from openai import OpenAI
from PIL import Image

# 페이지 설정
st.set_page_config(page_title="🗨️ 파이썬 챗봇", page_icon="💬")  

# 제목 수정 및 이모티콘 추가
st.title("🗨️ 파이썬 챗봇")  

# 배경 그라데이션 설정
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #FFDDC1, #FBBF24);  /* 그라데이션 색상 */
        background-size: cover;
    }
    /* 사용자 메시지 스타일 */
    .user-message {
        background-color: #e2f0cb;  /* 연한 녹색 */
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        text-align: right;
    }
    /* 어시스턴트 메시지 스타일 */
    .assistant-message {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        text-align: left;
    }
    /* 전체 채팅 영역 스타일 */
    .chat-container {
        max-width: 600px;
        margin: auto;
        padding: 10px;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 챗봇 이미지 표시
try:
    image = Image.open('bot.png')  # 카카오톡 스타일의 챗봇 이미지 사용
    st.image(image, caption='안녕하세요, 파이썬 챗봇입니다. 무슨 말이든 건네주세요!', use_column_width=True)
except FileNotFoundError:
    st.warning("챗봇 이미지를 찾을 수 없습니다. 'bot.png' 파일을 추가해주세요.")

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 기본 모델 설정
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
    
# 시스템 메시지 설정
system_message = '''
    당신의 이름은 파이썬 챗봇입니다.
    영어로 질문을 받아도 한글로 답해주세요.
    한글이 아닌 답변일 때는 다시 생각해서 꼭 한글로 만들어주세요.
    모든 답변의 끝에는 답변에 맞는 이모티콘도 추가해주세요.
'''

# 채팅 내역 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role" : "system", "content" : system_message}]

# 채팅 메시지 컨테이너
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# 채팅 내역 표시
for idx, message in enumerate(st.session_state.messages):
    if idx == 0:
        continue  # 시스템 메시지는 표시하지 않음
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

# 채팅 메시지 컨테이너 닫기
st.markdown('</div>', unsafe_allow_html=True)

# 사용자 입력 받기
if prompt := st.chat_input("대화를 입력해주세요"):  
    # 사용자 메시지를 채팅 내역에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 어시스턴트의 응답 생성
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=st.session_state.messages
    )
    assistant_message = response.choices[0].message.content
    # 어시스턴트 메시지를 채팅 내역에 추가
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    # 전체 채팅 컨테이너 다시 표시
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for idx, message in enumerate(st.session_state.messages):
        if idx == 0:
            continue  # 시스템 메시지는 표시하지 않음
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
