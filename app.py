from flask import Flask, request
import requests

app = Flask(__name__)

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
    print(f"Notion API 응답 코드: {response.status_code}")
    print(f"응답 내용: {response.text}")

@app.route('/')
def home():
    return '서버 잘 돌아가고 있다!'

@app.route('/video', methods=['POST'])
def video():
    video_id = request.get_data(as_text=True)
    print(f"받은 영상ID: {video_id}")
    send_notion_request(video_id)
    return f"서버가 받은 영상ID: {video_id}", 200

if __name__ == '__main__':
    print('서버 ON🔆')
    app.run(host='0.0.0.0', port=5001)
