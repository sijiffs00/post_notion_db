import requests
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

def transcribe_audio_with_whisper(file_path: str, language: str = "ko", model: str = "whisper-1", api_key: Optional[str] = None) -> str:
    """
    m4a 음성파일을 Whisper API에 post 요청 보내서 텍스트로 변환하는 함수
        성공 시 -> 텍스트 반환
        실패 시 -> 예외 발생
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API 키가 필요해. 인자로 넘기거나 .env 파일에 OPENAI_API_KEY를 설정해줘.")

    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    files = {
        "file": open(file_path, "rb")
    }
    data = {
        "model": model,
        "language": language
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    files["file"].close()  # 파일 핸들 닫기

    if response.status_code != 200:
        raise RuntimeError(f"Whisper API 요청 실패: {response.status_code} {response.text}")

    result = response.json()
    return result.get("text", "") 