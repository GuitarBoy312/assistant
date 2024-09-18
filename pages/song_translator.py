import streamlit as st
from openai import OpenAI
import os
import base64
import io

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Streamlit 앱 제목 설정
st.title("✨인공지능 영어 조교 버틀링🤵")
st.subheader("🎶외국어 노래 학습 도우미🎵")

# 사용자 입력 받기
song_input = st.text_area("🎼노래 가사를 입력하세요:")

if st.button("번역하기"):
    if song_input:
        # OpenAI API를 사용하여 가사 분석 및 번역
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 초등학생을 위한 외국어 노래 학습 도우미입니다."},
                {"role": "user", "content": f"""다음 노래 가사를 분석해주세요: {song_input}

1. 전체 가사를 원어 가사 한 줄, 한국어로 된 발음 가이드 한 줄, 한국어 번역 한 줄, 한 줄 띄우고 다음 줄도 같은 형식으로 반복...으 로 제공해주세요: [원어 가사], [발음 가이드], [한국어 번역] 이라는 정보들이나 각 줄의 번호는 표시하지 않음.
   
2. 초등학생이 배우면 좋을 단어 5개 선정 및 설명

3. 노래의 주제나 메시지 요약"""}
            ]
        )
        
        analysis = response.choices[0].message.content

        # 결과 표시
        st.subheader("가사 분석")
        
        # 가사 분석과 추가 정보를 분리
        parts = analysis.split("2. 초등학생이 배우면 좋을 단어", 1)
        lyrics_analysis = parts[0].strip()
        st.write(lyrics_analysis)

        # 원어 발음 듣기 기능 (OpenAI TTS 사용)
        st.subheader("원어 발음 듣기")
        try:
            # OpenAI TTS API를 사용하여 음성 생성
            audio_response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=song_input
            )
            
            # 오디오 데이터를 바이트 스트림으로 변환
            audio_bytes = io.BytesIO(audio_response.content)
            
            # Streamlit audio 위젯으로 재생
            st.audio(audio_bytes, format="audio/mp3")
            
        except Exception as e:
            st.error(f"TTS API 호출 중 오류 발생: {str(e)}")

# 앱 사용 가이드
st.sidebar.title("사용 가이드")
st.sidebar.write("1. 노래 제목이나 가사를 입력란에 붙여넣으세요.")
st.sidebar.write("2. '분석하기' 버튼을 클릭하세요.")
st.sidebar.write("3. 전체 가사 번역, 발음 가이드, 주요 단어, 노래 메시지를 확인하세요.")
st.sidebar.write("4. 원어 발음을 들어보세요.")

