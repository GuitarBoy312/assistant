import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["openai_api_key"])

# 메인 화면 구성
st.title("✨인공지능 영어 조교 버틀링🤵")
st.subheader("✨인공지능 영어 퀴즈 생성기🕵️‍♂️")
st.divider()

# 확장 설명
with st.expander("❗❗ 글상자를 펼쳐 사용방법을 읽어보세요 👆✅", expanded=False):
    st.markdown(
    """     
    1️⃣ 영어 지문을 입력하세요.<br>
    2️⃣ 생성할 문제 수를 선택하세요.<br>
    3️⃣ [문제 만들기] 버튼을 눌러 문제를 생성하세요.<br>
    4️⃣ 생성된 문제를 확인하고 필요하다면 다운로드하세요.<br>
    <br>
    🙏 생성된 문제가 적절하지 않을 수 있습니다.<br> 
    🙏 그럴 때에는 다시 [문제 만들기] 버튼을 눌러주세요.
    """
    , unsafe_allow_html=True)

# 사용자 입력 받기
user_input = st.text_area("영어 지문을 입력하세요:", height=200)
num_questions = st.number_input("생성할 문제 수:", min_value=1, max_value=10, value=3, step=1)

# 학년 선택
grade = st.selectbox("학년을 선택하세요:", ["초등학교 3학년", "초등학교 4학년", "초등학교 5학년", "초등학교 6학년"])

# 영어 수준 선택
level = st.selectbox("영어 수준을 선택하세요:", ["상", "중", "하"])

if st.button("문제 만들기"):
    if user_input:
        st.session_state.questions = []
        
        question_types = [
            "내용 이해",
            "어휘",
            "문법",
            "주제/요지",
            "세부 정보"
        ]
        
        for i in range(num_questions):
            question_type = question_types[i % len(question_types)]
            prompt = f"""다음 영어 지문을 바탕으로 EFL 환경의 {grade}, 영어 수준 {level}에 맞는 간단한 객관식 문제를 만들어주세요:

            {user_input}

            조건:
            1. 문제의 정답은 1개입니다.
            2. 질문과 선택지는 한국어로 제공됩니다.
            3. 4개의 선택지를 제공하세요.
            4. 이 문제는 '{question_type}' 유형의 문제여야 합니다.
            5. 이전에 만든 문제와 중복되지 않도록 해주세요.
            6. {grade}와 영어 수준 {level}에 적합한 난이도로 문제를 만들어주세요.

            형식:
            [문제 유형: {question_type}]
            질문: (한국어로 된 질문)
            A. (선택지)
            B. (선택지)
            C. (선택지)
            D. (선택지)
            정답: (정답 선택지)
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 다양한 유형의 영어 문제를 만드는 전문가입니다."},
                    {"role": "user", "content": prompt}
                ]
            )

            st.session_state.questions.append(response.choices[0].message.content)
        
        st.session_state.questions_generated = True
        st.rerun()
    else:
        st.warning("영어 지문을 입력해주세요.")

if 'questions_generated' in st.session_state and st.session_state.questions_generated:
    st.markdown("### 생성된 문제")
    st.text(user_input)
    
    all_content = f"영어 지문:\n{user_input}\n\n"
    
    for i, question in enumerate(st.session_state.questions, 1):
        st.markdown(f"**문제 {i}**")
        lines = question.split('\n')
        st.markdown(f"*{lines[0]}*")  # 문제 유형 표시
        for line in lines[1:]:
            st.text(line)
        st.divider()
        
        all_content += f"문제 {i}\n"
        all_content += question + "\n\n"

    # 텍스트로 복사할 수 있는 영역 제공
    st.text_area("생성된 모든 문제 (복사하여 사용하세요)", all_content, height=300)

    # 다운로드 버튼 추가
    st.download_button(
        label="텍스트 파일로 다운로드",
        data=all_content,
        file_name="generated_questions.txt",
        mime="text/plain"
    )
