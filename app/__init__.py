import os
from flask import Flask

def create_app(test_config=None):
    # 建立與設定 Flask 應用程式 (App Factory)
    app = Flask(__name__, instance_relative_config=True)
    
    # 預設設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    if test_config is None:
        # 當不測試時，讀取 instance config (如果存在)
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 載入測試設定
        app.config.from_mapping(test_config)

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints
    from app.routes.game import game_bp
    from app.routes.leaderboard import leaderboard_bp
    
    app.register_blueprint(game_bp)
    app.register_blueprint(leaderboard_bp)

    return app
