import requests
import json

# ==========================================
# 1. 設定 (APIキーなどを入れてください)
# ==========================================
API_KEY = "4b02b7aa-bfd7-4af8-9dca-e829c99ffddf"
AGENT_ID = "0f83d193-32de-41b1-b2d8-2ede89bf4242"
PROJECT_ID = "7ed3a47b-c0c2-47c8-a9a8-ee57bffce47e" # STUDIOのURLから取得して書き換え

BASE_URL = "https://api.japan-ai.co.jp"
ENDPOINT = "/chat/v2"

# ==========================================
# 2. マスキング辞書定義 (要件通り)
# ==========================================
# キー: 元の言葉, 値: {relation: 置換後, category: 分類}
MASKING_DICT = {
    "喜多　育三": {"relation": "わたし", "category": "本人"},
    "喜多育三":   {"relation": "わたし", "category": "本人"}, # 表記揺れ対応
    "大地":       {"relation": "孫", "category": "家族"},
    "母":         {"relation": "娘", "category": "家族"},
    "78歳":       {"relation": "後期高齢者", "category": "年齢"},
    "神奈川県　横浜市": {"relation": "神奈川県", "category": "住所"},
    "横浜市":     {"relation": "神奈川県内の市", "category": "住所"},
}

# 逆引き辞書 (自動生成) relation -> original
REVERSE_DICT = {v["relation"]: k for k, v in MASKING_DICT.items()}

# ==========================================
# 3. 処理関数 (Pythonロジック)
# ==========================================

def mask_text(text):
    """ユーザー入力をマスキングする"""
    masked_text = text
    log = []
    
    # 文字列が長い順にソートして置換 (部分一致防止)
    sorted_keys = sorted(MASKING_DICT.keys(), key=len, reverse=True)
    
    for name in sorted_keys:
        if name in masked_text:
            relation = MASKING_DICT[name]["relation"]
            masked_text = masked_text.replace(name, relation)
            log.append(f"{name} -> {relation}")
            
    return masked_text, log

def demask_text(text):
    """AIの回答を元に戻す"""
    final_text = text
    log = []
    
    # 文字列が長い順にソート
    sorted_relations = sorted(REVERSE_DICT.keys(), key=len, reverse=True)
    
    for relation in sorted_relations:
        original_name = REVERSE_DICT[relation]
        
        # パターン1: 「孫さん」のような敬称付きを優先的に戻す
        target_san = f"{relation}さん"
        if target_san in final_text:
            replacement = f"{original_name}さん"
            final_text = final_text.replace(target_san, replacement)
            log.append(f"{target_san} -> {replacement}")
            
        # パターン2: 敬称なしの単語を戻す
        if relation in final_text:
            final_text = final_text.replace(relation, original_name)
            log.append(f"{relation} -> {original_name}")
            
    return final_text, log

def call_japan_ai(masked_prompt):
    """JAPAN AI APIを呼び出す"""
    url = BASE_URL + ENDPOINT
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # LLMには「マスキングされた状態」を正として認識させるコンテキストを付与
    system_context = """
あなたは高齢者に寄り添う介護支援エージェントです。
以下のユーザー情報を前提に会話してください。
- ユーザー: 「わたし」(後期高齢者)
- 居住地: 「神奈川県」
- 家族: 「孫」、「娘」
"""
    
    payload = {
        "model": "gpt-4o", # または gpt-4o
        "prompt": f"{system_context}\n\nユーザーの発言:\n{masked_prompt}",
        "stream": False,
        "agentName": AGENT_ID,
        "projectId": PROJECT_ID
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        print(f"DEBUG: Raw Response = {json.dumps(data, ensure_ascii=False)}")
        if data.get("status") == "succeeded":
            return data.get("chatMessage", "")
        else:
            return f"Error: {data}"
    except Exception as e:
        return f"API Error: {e}"

# ==========================================
# 4. メイン実行フロー
# ==========================================
if __name__ == "__main__":
    # --- 入力 (テスト用) ---

    user_input = "私は喜多育三、78歳です。神奈川県　横浜市に住んでいますが、孫の大地が最近来なくて寂しい。"
    while True:
        user_input = input("ユーザー入力をどうぞ (終了するには 'exit' と入力): ")
        if user_input == "":
            print("入力が空です。もう一度入力してください。")
            continue

        if user_input.lower() == 'exit':
            exit()

    

        print(f"1. 入力:\n{user_input}\n")

        # --- Step 1: Pythonでマスキング ---
        masked_input, mask_log = mask_text(user_input)
        print(f"2. マスキング結果 (Python処理):\n{masked_input}")
        print(f"   変換ログ: {mask_log}\n")

        # --- Step 2: API呼び出し (個人情報は送信されません) ---
        print("3. AI思考中(API送信)...")
        raw_response = call_japan_ai(masked_input)
        print(f"   AI生回答 (関係性表現):\n{raw_response}\n")

        # --- Step 3: Pythonで復号 (デマスキング) ---
        final_response, demask_log = demask_text(raw_response)
        
        print("-" * 40)
        print(f"4. 最終回答:\n{final_response}")
        print("-" * 40)
        print(f"   復元ログ: {demask_log}")