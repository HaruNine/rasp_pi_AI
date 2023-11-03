from google.cloud import texttospeech
import os

keyfile_path = "구글 api.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = keyfile_path

def text_to_speech(text, output_file="output.wav"):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

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

    with open(output_file, "wb") as out:
        out.write(response.audio_content)

def play_audio(file_path):
    os.system(f"aplay {file_path}")  # aplay 명령어는 라즈베리파이에서 WAV 파일을 재생하는 명령어입니다.

if __name__ == "__main__":
    text_input = input("텍스트를 입력하세요: ")
    output_file_path = "output.wav"

    text_to_speech(text_input, output_file_path)
    play_audio(output_file_path)
