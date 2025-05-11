from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    device_id = data.get("device_id", "알 수 없음")
    result = f"받은 ID: {device_id} → 정상 처리 완료"
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(port=5000)
