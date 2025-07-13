import requests
from typing import Optional
import os
from dotenv import load_dotenv  
from src.transcribe_audio_with_whisper import transcribe_audio_with_whisper
from src.request_gemini_summary import request_gemini_summary


load_dotenv()


if __name__ == "__main__":
    print("실행 시작")  
    file_path = "/Users/sojung/Downloads/record_voice.m4a"  # 보낼파일 경로
    text = transcribe_audio_with_whisper(file_path, language="ko")
    print("변환 결과:", text)

    # 변환 성공 시 Gemini에게 요약 요청
    if text:
        summary = request_gemini_summary(text)
        print("요약 결과:", summary)
    else:
        print("음성 인식 결과가 비어있어. 요약을 건너뜀.")
