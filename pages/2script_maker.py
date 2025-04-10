import streamlit as st
from openai import OpenAI

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["openai_api_key"])

def generate_scripts(expression, grade, topic, participants, num_scripts, script_length):
    length_description = {
        "짧게": "대본은 각각의 등장인물 당 1번의 대사로 구성되어야 합니다.",
        "보통": "대본은 각각의 등장인물 당 2번의 대사로 구성되어야 합니다.",
        "길게": "대본은 각각의 등장인물 당 3번의 대사로 구성되어야 합니다."
    }
    
    prompt = f"""영어를 외국어로 사용하는 한국의 초등학교 {grade} 학생의 수준에 맞는 영어 역할극 대본을 {num_scripts}개 만들어주세요. 
    한국의 초등학생 평균 영어 수준 CEFR - 3학년:pre A1 4학년: pre A1, 5학년: A1, 6학년: A1
    {participants}명이 참여할 수 있는 대본이어야 합니다. {length_description[script_length]} 각 대사는 한 문장으로 이루어집니다.
    다음 표현을 포함해야 합니다: '{expression}'
    각 캐릭터의 대사 앞에 각자 다른 캐릭터의 특성에 맞는(성별, 종, 직업, 코스튬 등) 이모지를 넣어주세요. 같은 캐릭터에는 항상 같은 이모지를 사용하세요.
    예를 들어:
    🦁 simba: Hello, how are you?
    👱🏻‍♀️ elsa: I'm fine, thank you!
    이런 식으로 각 캐릭터마다 다른 이모지를 사용해 주세요.
    각 영어 대사의 오른쪽에 중괄호를 이용하여 한국어 독음을 넣어주세요.
    한국어 독음 오른쪽에 소괄호를 이용하여 해석을 넣어주세요.
    처음에 등장인물, 장소 등을 한국어로 넣어주세요.
    처음 장면에 대한 설명을 한국어 지문으로 넣고 장소나 상황이 바뀌거나 등장인물의 특정한 행동이 필요한 상황 등에 지문을 한국어로 넣어주세요.
    """
    
    if topic:
        prompt += f" 주제는 '{topic}'입니다. {topic}의 스토리를 활용하여 만들어 주세요."
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "당신은 초등학생을 위한 영어 교육 전문가입니다. 재미있고 교육적인 대본을 만들어주세요."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

st.title("✨인공지능 영어 조교 버틀링🤵")
st.subheader("✨인공지능 영어 역할극 대본 생성기🎭")

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
        with st.spinner("대본을 생성 중입니다..."):
            scripts = generate_scripts(expression, grade, topic, participants, num_scripts, script_length)
        st.session_state.scripts = scripts
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
