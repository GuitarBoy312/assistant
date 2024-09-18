import streamlit as st
from openai import OpenAI
import io

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Streamlit 앱 제목 설정
st.title("✨인공지능 영어 조교 버틀링🤵")
st.subheader("✨ 인공지능 외국어 노래 학습 도우미🎵")

# 확장 설명
with st.expander("❗❗ 글상자를 펼쳐 사용방법을 읽어보세요 👆✅", expanded=False):
    st.markdown(
    """     
    1️⃣ 노래 가사나 제목을 입력란에 붙여넣으세요.제목을 입력하면 주요 가사만 번역됩니다.<br>
    2️⃣ '번역하기' 버튼을 클릭하세요.<br>
    3️⃣ 전체 가사 번역, 발음 가이드, 주요 단어, 노래 메시지를 확인하세요. 다운로드 가능합니다.<br>
    4️⃣ 원어 발음 듣기를 활용해서 수업에 활용하세요. 다운로드도 가능합니다.<br>
    <br>
    🙏 생성된 번역이 적절하지 않을 수 있습니다.<br> 
    🙏 그럴 때에는 다시 [번역하기] 버튼을 눌러주세요.
    """
    , unsafe_allow_html=True)
    
# 사용자 입력 받기
song_input = st.text_area("🎼노래 가사를 입력하세요:")

if st.button("📝번역하기"):
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
        
        st.session_state.analysis = response.choices[0].message.content

        # 결과 표시
        st.subheader("가사 분석")
        
        # 가사 분석과 추가 정보를 분리
        parts = st.session_state.analysis.split("2. 초등학생이 배우면 좋을 단어", 1)
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
            st.session_state.audio_bytes = io.BytesIO(audio_response.content)
            
            # Streamlit audio 위젯으로 재생
            st.audio(st.session_state.audio_bytes, format="audio/mp3")
            
        except Exception as e:
            st.error(f"TTS API 호출 중 오류 발생: {str(e)}")

# 분석 결과가 있을 때만 다운로드 버튼 표시
if 'analysis' in st.session_state:
    st.download_button(
        label="📥 분석 결과 텍스트 파일로 다운로드",
        data=st.session_state.analysis,
        file_name="song_analysis.txt",
        mime="text/plain"
    )

# 음성 파일이 있을 때만 다운로드 버튼 표시
if 'audio_bytes' in st.session_state:
    st.download_button(
        label="📥 음성 파일 다운로드",
        data=st.session_state.audio_bytes.getvalue(),
        file_name="song_audio.mp3",
        mime="audio/mp3"
    )
