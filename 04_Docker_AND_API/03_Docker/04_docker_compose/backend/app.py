import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

# ──────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────
API_KEY    = os.environ.get("GEMINI_API_KEY", "ัYour GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash"

client = genai.Client(api_key=API_KEY)
app    = Flask(__name__)
CORS(app)   # อนุญาตให้ Frontend เรียกหา Backend ได้

# ──────────────────────────────────────────
# Core helper — เรียก Gemini API
# ──────────────────────────────────────────
def call_gemini(
    prompt: str,
    history: list[dict] | None = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> str:
    """
    เรียก Gemini API และคืนค่าเป็น string

    Args:
        prompt      : ข้อความจากผู้ใช้ (turn ปัจจุบัน)
        history     : ประวัติการสนทนา รูปแบบ [{"role": "user"|"model", "parts": "..."}]
        temperature : ความสร้างสรรค์ของคำตอบ (0.0 = แม่นยำ, 1.0 = สร้างสรรค์)
        max_tokens  : จำนวน token สูงสุดที่ให้สร้าง
    """
    # สร้าง contents จาก history + prompt ปัจจุบัน
    contents = []
    if history:
        for turn in history:
            contents.append(
                types.Content(role=turn["role"], parts=[types.Part(text=turn["parts"])])
            )
    contents.append(
        types.Content(role="user", parts=[types.Part(text=prompt)])
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        ),
    )
    return response.text


# ──────────────────────────────────────────
# API Endpoints
# ──────────────────────────────────────────
@app.route("/chat", methods=["POST"])
def chat():
    """
    รับ JSON: { "message": "...", "history": [...] }
    คืน JSON: { "reply": "..." }
    """
    data    = request.get_json()
    message = data.get("message", "").strip()
    history = data.get("history", [])

    if not message:
        return jsonify({"error": "message ว่างเปล่า"}), 400

    try:
        reply = call_gemini(prompt=message, history=history)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """ตรวจสอบว่า server ทำงานอยู่"""
    return jsonify({"status": "ok", "model": MODEL_NAME})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
