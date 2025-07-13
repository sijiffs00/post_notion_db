import requests
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

def request_gemini_summary(text: str, api_key: Optional[str] = None, model: str = "gemini-1.5-flash-latest") -> str:
    """
    Gemini 1.5 Flash 모델에 텍스트 요약을 요청하는 함수야.
    
    Args:
        text (str): 요약할 텍스트(스크립트)
        api_key (Optional[str]): Gemini API 키. None이면 환경변수에서 읽어옴.
        model (str): 사용할 Gemini 모델명 (기본값: 'gemini-1.5-flash-latest')
    
    Returns:
        str: Gemini API로부터 받은 요약 결과 텍스트
    """
    # API 키가 없으면 환경변수에서 불러옴
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API 키가 필요해. 인자로 넘기거나 .env 파일에 GEMINI_API_KEY를 설정해줘.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    # Gemini API에 맞는 요청 데이터 포맷
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": text}
                ]
            }
        ]
    }

    # POST 요청 보내기
    response = requests.post(url, headers=headers, json=data)

    # 응답이 성공적이지 않으면 에러 발생
    if response.status_code != 200:
        raise RuntimeError(f"Gemini API 요청 실패: {response.status_code} {response.text}")

    # 결과에서 요약 텍스트 추출
    result = response.json()
    # Gemini 응답 구조에서 요약 텍스트 추출
    try:
        summary = result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Gemini 응답에서 요약 텍스트를 찾을 수 없어: {result}")
    return summary


if __name__ == "__main__":
    print("실행 시작")
    script = (
        "이건 대화 내용을 녹음한 스크립트야. 이 대화의 요지를 파악하고 요약해줘:\n\n"
        "진짜살인적인 더위야 너무 더워서 미칠거같아 이게 말이되나? 너무 더워서 태풍도 한반도를 피해갔다니.. "
        "나도 이나라를 떠나고싶을 정도다. 덥기만한가? 습하기까지.. 어항에 있는 기분이라고 매일매일"
    )
    summary = request_gemini_summary(script)
    print("요약 결과:", summary) 