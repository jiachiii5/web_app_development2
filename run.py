from dotenv import load_dotenv
import os
from app import create_app

# 載入 .env 檔案（如果存在）
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # 啟動伺服器
    app.run(debug=True)
