from flask import Flask, request, jsonify

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# POST 요청을 처리하는 엔드포인트 생성
@app.route('/', methods=['POST'])
def hello_world():
    # 요청 body에서 JSON 데이터 추출
    data = request.get_json(force=True, silent=True)
    # data가 None이거나 'url' 키가 없을 경우를 대비해서 기본값 '' 사용
    url = data.get('url', '') if data else ''
    # url 값을 로그로 출력
    print(f"받은 url: {url}")
    return 'Hello World'

    

# 서버를 0.0.0.0:5000에서 실행 (외부 접속 허용)
# debug=False로 설정해서 프로덕션 환경처럼 동작하게 함
if __name__ == '__main__':
    # 24시간 동작하게 하려면 이 코드를 백그라운드에서 실행하거나, nohup 등으로 실행하면 돼
    app.run(host='0.0.0.0', port=5001, debug=False)
