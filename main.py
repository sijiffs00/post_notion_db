import requests
from typing import Optional
import os
from dotenv import load_dotenv  
from transcribe_audio_with_whisper import transcribe_audio_with_whisper


load_dotenv()


if __name__ == "__main__":
    print("실행 시작")  
    file_path = "/Users/sojung/Downloads/record_voice.m4a"  # 보낼파일 경로
    text = transcribe_audio_with_whisper(file_path, language="ko")
    print("변환 결과:", text)
