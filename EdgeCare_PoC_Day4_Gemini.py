# EdgeCare_PoC_Day4_Gemini_HTTP.py
import os
import requests
import json

RAG = {
    "大地": {"relation": "孫"},
    "母": {"relation": "娘"}
}

def semantic_mask(text):
    for name, info in RAG.items():
        if name in text:
            text = text.replace(name, info["relation"])
    return text

def recontextualize(text):
    for name, info in RAG.items():
        if info["relation"] in text:
            text = text.replace(info["relation"], name)
    return text

def cloud_send_gemini_http(text):
    api_key = os.getenv("GOOGLE_API_KEY")
    api_key = "AIzaSyCbOZMMGvgd6_yaYWFtXF6_9BsuJPOH6K4" #APIキーをテストのために生で入力。のちに修正予定。
    if not api_key:
        raise ValueError("環境変数 GOOGLE_API_KEY が設定されていません")

    # ✅ 最新安定版モデルを指定
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-pro:generateContent?key={api_key}"

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": f"以下の発話に対して自然で温かい返答を日本語で生成してください。\nユーザー発話: {text}"}]}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise RuntimeError(f"Gemini API Error: {response.status_code} {response.text}")

    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise RuntimeError(f"Gemini API Error: {response.status_code} {response.text}")

    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

if __name__ == "__main__":
    while True:
        print("送信するテキストを入力してください（終了するには 'exit' と入力）:")
        input_text = input()
        if input_text.lower() == 'exit':
            print("終了します。")
            break
        print("🎙 入力:", input_text)

        masked = semantic_mask(input_text)
        print("🔒 クラウド送信用:", masked)

        reply = cloud_send_gemini_http(masked)
        print("☁️ Gemini応答:", reply)

        final_output = recontextualize(reply)
        print("💬 再文脈化後:", final_output)
