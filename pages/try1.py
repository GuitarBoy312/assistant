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
    1️⃣ 노래 가사나 제목을 입력란에 붙여넣으세요. 제목을 입력하면 주요 가사만 번역됩니다.<br>
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
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "당신은 초등학생을 위한 외국어 노래 학습 도우미입니다."},
                {"role": "user", "content": f"""다음 노래 가사를 분석해주세요: {song_input}

1. 노래 제목을 제공해주세요.

2. 전체 가사를 다음 형식으로 제공해주세요:
   [원어 가사]|||[발음 가이드]|||[한국어 번역]
   각 줄을 이 형식으로 제공하고, 줄 바꿈으로 구분해주세요.

3. 초등학생이 배우면 좋을 단어 5개 선정 및 설명

4. 노래의 주제나 메시지 요약"""}
            ]
        )
        
        st.session_state.analysis = response.choices[0].message.content

        # 결과 파싱
        parts = st.session_state.analysis.split("\n\n")
        title = parts[0].replace("1. ", "").strip()
        lyrics = [line.split("|||") for line in parts[1].split("\n") if "|||" in line]
        
        # 체크박스 생성
        col1, col2, col3 = st.columns(3)
        with col1:
            show_original = st.checkbox("원어 가사", value=True)
        with col2:
            show_pronunciation = st.checkbox("발음 가이드", value=True)
        with col3:
            show_translation = st.checkbox("한국어 번역", value=True)

        # 가사 표시
        st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
        for i, (original, pronunciation, translation) in enumerate(lyrics):
            html = f"<div id='line-{i}'>"
            if show_original:
                html += f"<b><font color='blue'>{original}</font></b><br>"
            if show_pronunciation:
                html += f"<font color='gray'>{pronunciation}</font><br>"
            if show_translation:
                html += f"<font color='black'>{translation}</font><br>"
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

            # TTS 버튼 추가
            if st.button(f"🔊 {i+1}번 줄 듣기"):
                try:
                    audio_response = client.audio.speech.create(
                        model="tts-1",
                        voice="alloy",
                        input=original
                    )
                    st.audio(audio_response.content, format="audio/mp3")
                except Exception as e:
                    st.error(f"TTS API 호출 중 오류 발생: {str(e)}")

        # 추가 정보 표시
        st.subheader("주요 단어")
        st.write(parts[2])
        st.subheader("노래 메시지")
        st.write(parts[3])

        # 전체 가사 TTS
        st.subheader("전체 가사 듣기")
        try:
            full_lyrics = " ".join([line[0] for line in lyrics])
            audio_response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=full_lyrics
            )
            st.session_state.audio_bytes = io.BytesIO(audio_response.content)
            st.audio(st.session_state.audio_bytes, format="audio/mp3")
        except Exception as e:
            st.error(f"전체 가사 TTS API 호출 중 오류 발생: {str(e)}")

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
