import streamlit as st
from openai import OpenAI
import os

st.title("✨인공지능 영어 조교: 잉글링👱🏾‍♂️")
st.header("📝영어 텍스트 생성기")

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["openai_api_key"])

# 사용자 입력 받기
grade = st.selectbox("학년 선택", ["3학년", "4학년", "5학년", "6학년"])
level = st.selectbox("영어 수준", ["상", "중", "하"])
text_length = st.selectbox("텍스트 길이", ["짧게", "보통", "길게"])
english_expression = st.text_area("원하는 영어 표현을 입력하세요")

if st.button("텍스트 생성"):
    if english_expression:
        # OpenAI API를 사용하여 텍스트 생성
        prompt = f"""
        다음 조건에 맞는 영어 텍스트를 생성해주세요:
        - 학년: {grade}
        - 영어 수준: {level}
        - 텍스트 길이: {text_length}, 짧게: 50자 이하, 보통: 50자 이상 100자 이하, 길게: 100자 이상
        - 포함할 영어 표현: {english_expression}

        생성된 텍스트는 EFL 환경의 초등학교 영어 수업에서 사용하기에 적합해야 합니다.
        다음과 같은 형식의 간단하고 명확한 문장을 사용해주세요:

        예시 2:
        Tony's Missing Cake
        Tony's cake is missing.
        Tony called Mr. Holmes for help.
        Mr. Holmes went to Tony's house.
        "What did you do yesterday, Mike?"
        "I made a car."
        "Judy, what did you do yesterday?"
        "I played baseball."
        "Tony, your cat ate the cake. Look at the cream on her foot."
        "Oh, no!"

        예시 3:
        We Should Save the Earth
        The earth is sick.
        The weather is getting warmer.
        The water is getting worse.
        We should save energy and water.
        We should recycle things, too.

        예시 4:
        Gyeongbokgung
        Q: May I borrow a wheelchair?
        A: Yes, you may. Please come to the office.
        Q: May I ride a bike?
        A: No, you may not. You can't ride a bike at Gyeongbokgung.

        이 예시들을 참고하여 요청한 조건에 맞는 새로운 텍스트를 생성해주세요. 
        짧은 역할극 형식으로 만들어 주세요. 역할마다 알맞은 이모지를 앞에 붙여주세요. 초등학생이 알아보기 쉽게 한문장이 끝날때마다 줄바꿈을 꼭 하세요.
        한국어 해석을 아래에 달아주세요."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content
        st.write(result)
    else:
        st.warning("영어 표현을 입력해주세요.")
