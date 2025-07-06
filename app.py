from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

def send_notion_request():
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
                            "content": "https://youtu.be/example123"
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
    while True:
        response = requests.post(url, headers=headers, json=data)
        print(f"Notion API 응답 코드: {response.status_code}")
        print(f"응답 내용: {response.text}")
        time.sleep(5)

@app.route('/')
def home():
    return '서버 잘 돌아가고 있다!'

if __name__ == '__main__':
    print('서버 ON🔆')
    # 백그라운드에서 5초마다 Notion API 요청 보내는 스레드 시작
    t = threading.Thread(target=send_notion_request, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5001)
