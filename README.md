# 🌱 習慣化チャレンジアプリ（Flask）

このアプリは、自分の習慣（例：朝ストレッチ、日記を書くなど）を記録し、達成日数・連続記録・達成率を可視化できる **Flask製の習慣化支援アプリ**です。

---

## 🔧 主な機能

- ✅ 習慣を1つ設定して毎日記録
- 💬 メモ機能でその日の感想も保存可能
- 📅 達成カレンダー（月表示）
- 🔥 連続達成記録（Streak）
- 📊 今月の達成率を自動計算
- 🌙 ダーク／ライトテーマ切り替え対応
- 🎉 達成したときの祝福アニメーション表示

---

## 💻 使用技術

- Python 3.x
- Flask
- HTML / CSS / JavaScript
- JSONファイルによるローカルデータ保存

---

## 🚀 セットアップ方法（ローカル実行）

### 1. リポジトリをクローン

```bash
git clone https://github.com/ユーザー名/リポジトリ名.git
cd リポジトリ名

3. 依存ライブラリのインストール
pip install flask
4. アプリを起動
python app.py
（app.py があなたのファイル名の場合）
5. ブラウザでアクセス
http://localhost:5003

## 📁 ファイル構成（例）
habit-tracker-app/
├── app.py
├── data.json
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── README.md

📸 スクリーンショット
<img width="725" height="972" alt="image" src="https://github.com/user-attachments/assets/eb08cebf-7204-4160-877d-43235c44edcb" />



