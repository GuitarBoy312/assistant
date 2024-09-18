import streamlit as st
from openai import OpenAI
import os

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["openai_api_key"])

def generate_scripts(expression, grade, topic, participants, num_scripts, script_length):
    length_description = {
        "짧게": "각 대본은 5-8문장으로 구성되어야 합니다.",
        "보통": "각 대본은 10-15문장으로 구성되어야 합니다.",
        "길게": "각 대본은 20-25문장으로 구성되어야 합니다."
    }
    
    prompt = f"""한국 초등학교 {grade} EFL 학생을 위한 영어 역할극 대본을 {num_scripts}개 만들어주세요. 
    {participants}명이 참여할 수 있는 대본이어야 합니다. {length_description[script_length]} 
    다음 표현을 포함해야 합니다: '{expression}'
    각 캐릭터의 대사 앞에 각자 다른 특징적인 이모지를 넣어주세요. 같은 캐릭터에는 항상 같은 이모지를 사용하세요.
    예를 들어:
    🧑 Tom: Hello, how are you?
    👱🏻‍♀️ Sarah: I'm fine, thank you!
    이런 식으로 각 캐릭터마다 다른 이모지를 사용해 주세요."""
    
    if topic:
        prompt += f" 주제는 '{topic}'입니다."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 요청하신 모델명으로 변경
        messages=[
            {"role": "system", "content": "당신은 초등학생을 위한 영어 교육 전문가입니다. 재미있고 교육적인 대본을 만들어주세요."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

st.title("✨인공지능 영어 조교 버틀링🤵")
st.subheader("🎭초등학생을 위한 영어 역할극 대본 생성기📝")

expression = st.text_area("🔸원하는 영어 표현을 입력하세요 (여러 줄 입력 가능):")
grade = st.selectbox("🔸학년을 선택하세요:", ["3학년", "4학년", "5학년", "6학년"])
participants = st.slider("🔸역할극 참여 인원수를 선택하세요:", min_value=2, max_value=6, value=3)
num_scripts = st.slider("🔸생성할 대본 개수를 선택하세요:", min_value=1, max_value=10, value=6)
script_length = st.selectbox("🔸대본의 길이를 선택하세요:", options=["짧게", "보통", "길게"], index=1)
topic = st.text_input("🔸주제를 입력하세요 (선택사항, 예: smurfs, pokemon, etc.):")

if st.button("📝대본 만들기"):
    if expression:
        scripts = generate_scripts(expression, grade, topic, participants, num_scripts, script_length)
        st.write(scripts)
    else:
        st.warning("영어 표현을 입력해주세요.")
