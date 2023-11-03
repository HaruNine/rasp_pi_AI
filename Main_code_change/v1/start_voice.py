import os
import subprocess
import speech_recognition as sr
from google.cloud import texttospeech
import wave
import pyaudio

keyfile_path = "구글.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = keyfile_path

# 키워드
KEYWORD = "라니"

# 음성 인식 객체 생성
recognizer = sr.Recognizer()

# Google Cloud Text-to-Speech 클라이언트 초기화
client = texttospeech.TextToSpeechClient()

def record_and_recognize():
    with sr.Microphone() as source:
        print("말씀해주세요...")

        while True:
            try:
                # ambient noise를 측정하여 adjust
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=3)

                # 음성을 텍스트로 변환
                text = recognizer.recognize_google(audio, language="ko-KR")
                print(f"인식된 텍스트: {text}")

                # 특정 키워드 감지
                if KEYWORD in text:
                    print(f"키워드 '{KEYWORD}' 감지됨!")
                    execute_voice_chat()
                    break  # 키워드를 찾았으므로 반복 중단
                else:
                    print("키워드가 감지되지 않았습니다.")

            except sr.UnknownValueError:
                print("음성을 인식할 수 없습니다.")
            except sr.RequestError as e:
                print(f"Google 음성 API 요청 오류: {e}")

def execute_voice_chat():
    try:
        speak_response("네 라니입니다")  # "네" 음성 출력
        # voice_chat.py 실행
        subprocess.run(["python3", "/home/pi1/weeb1/voice_chat.py"])
    except Exception as e:
        print(f"voice_chat.py 실행 중 오류 발생: {e}")

def speak_response(response_text):
    # Google Cloud Text-to-Speech API를 사용하여 음성 생성
    synthesis_input = texttospeech.SynthesisInput(text=response_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-Wavenet-A",
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # 음성을 WAV 파일로 저장
    with open("response.wav", "wb") as out:
        out.write(response.audio_content)

    # WAV 파일을 스피커로 출력
    play_audio("response.wav")

def play_audio(file_path):
    chunk = 1024
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True
    )

    data = wf.readframes(chunk)

    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.close()
    p.terminate()

if __name__ == "__main__":
    record_and_recognize()
