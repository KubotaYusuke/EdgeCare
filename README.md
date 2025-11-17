🧠 EdgeCare

「文脈を守って安全に会話できる」エッジ×クラウド型 AI アシスタント

📌 プロジェクト概要

EdgeCare は、
エッジ側で個人情報をマスキング → クラウドLLMに問い合わせ → 再文脈化して返す
という “コンテキストエンジニアリング” 型の対話システムです。

クラウドに送る前に、人物名や家族関係などを自動的に匿名化することで、
安全に・安心して・高品質な対話 を実現します。

現在、Python 実装による PoC 版が動作しています。

🎯 できること

🎙 音声 → テキスト入力（STT）（実装予定）

🔒 名前・家族関係の自動マスキング（エッジ）

☁️ Gemini API によるクラウド生成

🧩 再文脈化（元の人物名に復元）

🔊 音声出力（TTS）（実装予定）

📚 Local RAG（エッジ側知識ベース）（実装予定）

🧱 現在の構成（PoC版）
input → PIIマスキング → Gemini生成 → 再文脈化 → output

🚀 今後実装する機能

Whisper / Gemini Live API を使った音声 I/O

Local RAG（FAISS / Chroma）

CoreML / Neural Engine 最適化（Mac）

UI（Web / Desktop）

ペルソナ制御・会話メモリ管理

👥 チーム参加者募集中

以下の分野に興味のある方を歓迎します：

音声処理（STT/TTS）

CoreML / Neural Engine

Python（API・非同期処理）

RAG・ベクトルDB

UI/UXデザイン

AIプロダクトの企画が好きな方

🛠 セットアップ
git clone https://github.com/KubotaYusuke/EdgeCare
cd EdgeCare
pip install -r requirements.txt
python EdgeCare_PoC.py


※ ハッカソン提供の API キーを使用します。

📄 ライセンス

当面はハッカソン用の限定公開プロジェクトです。

💬 問い合わせ

Discord：KubotaYusuke
DM 歓迎です！
