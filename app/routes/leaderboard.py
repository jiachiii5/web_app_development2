from flask import Blueprint, render_template
# from app.models.leaderboard import Leaderboard

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/leaderboard', methods=['GET'])
def index():
    """
    排行榜頁面
    - 從 SQLite 資料庫呼叫 Model 取得前 10 名最佳成績。
    - 渲染 templates/leaderboard/index.html 並顯示表格。
    """
    pass
