import re
from flask import Flask, request, Response
import requests
import os
import subprocess
import json

app = Flask(__name__)

def extract_youtube_id(url):
    # 여러 유튜브 URL 포맷에서 ID 추출
    patterns = [
        r"youtu\.be/([\w-]+)",
        r"youtube\.com/watch\?v=([\w-]+)",
        r"youtube\.com/embed/([\w-]+)",
        r"youtube\.com/v/([\w-]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def send_notion_request(video_id):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": "Bearer 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",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    data = {
        "parent": { "database_id": "22842d112a7880ec8e73f18afb04f27a" },
        "properties": {
            "제목": {
                "title": [
                    {
                        "text": {
                            "content": "7월 6일 영상 요약"
                        }
                    }
                ]
            },
            "영상URL": {
                "rich_text": [
                    {
                        "text": {
                            "content": video_id
                        }
                    }
                ]
            },
            "내용": {
                "rich_text": [
                    {
                        "text": {
                            "content": "이 영상은 Claude가 자동으로 요약한 결과입니다."
                        }
                    }
                ]
            },
            "생성일": {
                "date": {
                    "start": "2025-07-06"
                }
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    # Notion 응답은 로그로 남기지 않음

def request_gemini_summary(transcript_path):
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = f.read()
    api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-pro:generateContent?key=AIzaSyB6R2m7pr9jATCoY7-BoY67aOkmqZVGE5U"
    headers = {"Content-Type": "application/json"}
    prompt = f"다음은 유튜브 영상의 자막이야. 3줄요약과 서론,본론,결말 을 작성해. 마지막에는 핵심내용을 서술해.:\n{transcript}"
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    return response.status_code

@app.route('/')
def home():
    return '서버 잘 돌아가고 있다!'

@app.route('/video', methods=['POST'])
def video():
    print("\n✨ post 요청 들어옴.")
    video_url = request.get_data(as_text=True)
    video_id = extract_youtube_id(video_url)
    print(f"1️⃣ 영상ID : {video_id}")

    send_notion_request(video_id)

    # 1. yt 폴더가 없으면 생성
    os.makedirs('yt', exist_ok=True)

    # 2. yt-dlp 명령어 실행 (yt 폴더 경로를 명시적으로 지정)
    youtube_url = f"https://youtu.be/{video_id}"
    vtt_path = os.path.join('yt', 'download_script.ko.vtt')
    transcript_path = os.path.join('yt', 'transcript.txt')
    cmd = [
        "yt-dlp",
        "-o", vtt_path.replace('.ko.vtt', '.%(ext)s'),
        "--write-auto-sub",
        "--sub-lang", "ko",
        "--skip-download",
        youtube_url
    ]
    vtt_result = "실패"
    try:
        subprocess.run(cmd, check=True)
        if os.path.exists(vtt_path):
            vtt_result = "성공"
    except subprocess.CalledProcessError:
        vtt_result = "실패"
    print(f"2️⃣ yt/download_script.ko.vtt 파일 생성 : {vtt_result}")

    # 3. iconv/sed/awk 명령어로 transcript.txt 생성
    transcript_result = "실패"
    if vtt_result == "성공":
        filter_cmd = f"iconv -f utf-8 -t utf-8 '{vtt_path}' | " \
                     f"LC_CTYPE=UTF-8 sed -e '/^[0-9]/d' -e '/^$/d' -e 's/<[^>]*>//g' | " \
                     f"awk '!seen[$0]++' > '{transcript_path}'"
        try:
            subprocess.run(filter_cmd, shell=True, check=True)
            if os.path.exists(transcript_path):
                transcript_result = "성공"
        except subprocess.CalledProcessError:
            transcript_result = "실패"
    print(f"3️⃣ yt/transcript.txt 파일 생성 : {transcript_result}")

    gemini_code = "-"
    if transcript_result == "성공":
        gemini_code = request_gemini_summary(transcript_path)
    print(f"4️⃣ Gemini 2.5 Pro 요청결과 : {gemini_code}")

    return Response(f"유튜브영상 ID: {video_id}", status=200, mimetype='text/plain')

if __name__ == '__main__':
    print('서버 ON🔆')
    app.run(host='0.0.0.0', port=5001)
