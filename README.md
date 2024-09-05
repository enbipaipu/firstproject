# 献立アプリ
## ダウンロード

### 手順
1. レポジトリのクローン
```bash
git clone git@github.com:enbipaipu/firstproject.git
```

2. プロジェクトのディレクトリに移動
```bash
cd firstproject
```

5. djangoのインストール
```bash
pip install openai langchain_openai python-dotenv bs4
```

7. マイグレーションをする
```bash
python manage.py migrate
```

8. サーバー起動
```bash
python manage.py runserver 8080
```

9. http://127.0.0.1:8080
にアクセス
