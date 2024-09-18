import streamlit as st
from openai import OpenAI

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["openai_api_key"])

def generate_scripts(expression, grade, topic, participants, num_scripts, script_length):
    # 기존 함수 내용 유지
    ...

st.title("✨인공지능 영어 조교 버틀링🤵")
st.subheader("🎭초등학생을 위한 영어 역할극 대본 생성기📝")

# 확장 설명
with st.expander("❗❗ 글상자를 펼쳐 사용방법을 읽어보세요 👆✅", expanded=False):
    st.markdown(
    """     
    1️⃣ 텍스트에 포함되기 원하는 Key expressions, 또는 단어 등을 자유롭게 입력하세요.<br>
    2️⃣ 학년, 역할 수, 대본 개수, 대본 길이를 설정하세요.<br>
    3️⃣ 이야기의 테마를 입력하세요. (신데렐라, 백설공주 등등...)입력하지 않으면 자유롭게 생성됩니다.<br>
    4️⃣ 생성된 역할극을 확인하고 다운 받으세요.<br>
    <br>
    🙏 생성된 역할극이 적절하지 않을 수 있습니다.<br> 
    🙏 그럴 때에는 다시 [대본 만들기] 버튼을 눌러주세요.
    """
    , unsafe_allow_html=True)

expression = st.text_area("🔸원하는 영어 표현을 입력하세요 (여러 줄 입력 가능):")
grade = st.selectbox("🔸학년을 선택하세요:", ["3학년", "4학년", "5학년", "6학년"])
participants = st.slider("🔸역할극 참여 인원수를 선택하세요:", min_value=2, max_value=6, value=3)
num_scripts = st.slider("🔸생성할 대본 개수를 선택하세요:", min_value=1, max_value=10, value=6)
script_length = st.selectbox("🔸대본의 길이를 선택하세요:", options=["짧게", "보통", "길게"], index=1)
topic = st.text_input("🔸테마를 입력하세요 (선택사항, 예: smurfs, pokemon, etc.):")

if st.button("📝대본 만들기"):
    if expression:
        st.session_state.scripts = generate_scripts(expression, grade, topic, participants, num_scripts, script_length)
        st.session_state.scripts_generated = True
    else:
        st.warning("영어 표현을 입력해주세요.")

if 'scripts_generated' in st.session_state and st.session_state.scripts_generated:
    st.write(st.session_state.scripts)
    
    # 다운로드 버튼 추가
    st.download_button(
        label="📥 텍스트 파일로 다운로드",
        data=st.session_state.scripts,
        file_name="generated_scripts.txt",
        mime="text/plain"
    )
    
    # 생성된 대본을 복사할 수 있는 텍스트 영역 추가
    st.text_area("생성된 대본 (복사하여 사용하세요)", st.session_state.scripts, height=300)
