from flask import Flask, request, Response, jsonify
import json
import os
from dotenv import load_dotenv
from waitress import serve

app = Flask(__name__)

# 🔥 환경 변수 로드
load_dotenv()
API_KEY = os.getenv("API_KEY")

@app.route('/')
def home():
    return "API Key 인증이 적용된 웹툰 요약 서버입니다!"

@app.route('/summarize', methods=['POST'])
def summarize_text():
    # 🔥 API Key 확인
    provided_key = request.headers.get("X-API-KEY")
    if provided_key != API_KEY:
        return jsonify({"error": "Invalid API Key"}), 403

    data = request.get_json(force=True)
    text = data.get("text", "")

    if not text or len(text.split()) < 5:
        return jsonify({"summary": "입력된 웹툰 내용이 너무 짧습니다. 최소 5단어 이상 입력해 주세요."})

    try:
        summary = f"요약: {text[:50]}..."  # 임시 요약 기능
    except Exception as e:
        summary = f"요약 생성 중 오류 발생: {str(e)}"

    return jsonify({"summary": summary})

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
