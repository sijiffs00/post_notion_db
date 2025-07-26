from flask import Flask, request, jsonify
from src.extract_youtube_video_id import extract_video_id

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# 단축어 '영상url을 서버에 post요청' 실행시 여기를 탐.
@app.route('/', methods=['POST'])
def handle_youtube_url_request():
    try:
        data = request.get_json(force=True, silent=True)
        url = data.get('url', '') if data else ''
        print(f"받은 url: {url}") 

        if not url:
            return jsonify({'error': 'URL이 제공되지 않았습니다'}), 400

        video_id = extract_video_id(url)
        
        if video_id:
            return jsonify({'video_id': video_id, 'success': True})
        else:
            return jsonify({'error': '유효한 YouTube URL이 아닙니다', 'success': False}), 400

    except Exception as e:
        print(f"서버 에러: {e}")
        return jsonify({'error': '서버 내부 에러가 발생했습니다', 'success': False}), 500

# 서버를 0.0.0.0:5000에서 실행 (외부 접속 허용)
# debug=False로 설정해서 프로덕션 환경처럼 동작하게 함
if __name__ == '__main__':
    # 24시간 동작하게 하려면 이 코드를 백그라운드에서 실행하거나, nohup 등으로 실행하면 돼
    app.run(host='0.0.0.0', port=5001, debug=False)
