from flask import Flask, request, jsonify

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# POST 요청을 처리하는 엔드포인트 생성
@app.route('/', methods=['POST'])
def hello_world():
    # 요청 body에서 url 값만 추출해서 로그로 출력
    body = request.data.decode('utf-8')
    url = ''
    # body가 예를 들어 '{"url":"https://youtube.com/xxx"}' 형태라고 가정
    if '"url"' in body:
        try:
            url = body.split('"url"')[1].split(':')[1].strip().strip('"{} ')
        except Exception:
            url = ''
    print(f"받은url: {url}")
    return 'Hello World'

    

# 서버를 0.0.0.0:5000에서 실행 (외부 접속 허용)
# debug=False로 설정해서 프로덕션 환경처럼 동작하게 함
if __name__ == '__main__':
    # 24시간 동작하게 하려면 이 코드를 백그라운드에서 실행하거나, nohup 등으로 실행하면 돼
    app.run(host='0.0.0.0', port=5001, debug=False)
