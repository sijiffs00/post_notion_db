import re
from flask import Flask, request, Response
import requests
import os
import subprocess
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

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
        "Authorization": f"Bearer {os.environ.get('NOTION_API_KEY')}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    today = datetime.now().date().isoformat()
    data = {
        "parent": { "database_id": "22842d112a7880ec8e73f18afb04f27a" },
        "properties": {
            "제목": {
                "title": [
                    {
                        "text": {
                            "content": "영상제목"
                        }
                    }
                ]
            },
            "한줄요약": {
                "rich_text": [
                    {
                        "text": {
                            "content": "이곳에 한줄요약 텍스트"
                        }
                    }
                ]
            },
            "내용": {
                "rich_text": [
                    {
                        "text": {
                            "content": "이곳에 전체 요약 내용"
                        }
                    }
                ]
            },
            "생성일": {
                "date": {
                    "start": today
                }
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code

def request_gemini_summary(transcript_path):
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = f.read()
    api_key = os.environ.get('GEMINI_API_KEY')
    api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-pro:generateContent?key={api_key}"
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
    return response.status_code, response.text

@app.route('/')
def home():
    return 'post_notion_db 프로젝트'

@app.route('/video', methods=['POST'])
def video():
    print("\n✨ post 요청 들어옴.")
    video_url = request.get_data(as_text=True)
    video_id = extract_youtube_id(video_url)
    print(f"1️⃣ 영상ID : {video_id}")

    os.makedirs('yt', exist_ok=True)

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
        gemini_code, _ = request_gemini_summary(transcript_path)
    print(f"4️⃣ Gemini 2.5 Pro 요청결과 : {gemini_code}")

    notion_code = send_notion_request(video_id)
    print(f"5️⃣ 노션 POST 요청 : {notion_code}")

    return Response(f"유튜브영상 ID: {video_id}", status=200, mimetype='text/plain')

if __name__ == '__main__':
    print('서버 ON🔆')
    app.run(host='0.0.0.0', port=5001)
