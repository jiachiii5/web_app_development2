from flask import Blueprint, render_template, request, redirect, url_for, session, flash

game_bp = Blueprint('game', __name__)

@game_bp.route('/', methods=['GET'])
def index():
    """
    遊戲首頁
    - 檢查 Session 中是否有進行中的遊戲。
    - 若無，則初始化隨機數字 (1-100) 與猜測次數。
    - 渲染 templates/game/index.html，顯示遊戲畫面與歷史紀錄。
    """
    pass

@game_bp.route('/guess', methods=['POST'])
def guess():
    """
    提交猜測數字
    - 接收表單傳來的 'guess' 欄位。
    - 驗證輸入合法性 (是否為 1-100 的整數)。
    - 若不合法，flash 提示錯誤。
    - 若合法，比較大小，更新 Session 中的嘗試次數與歷史紀錄。
    - 若猜中，呼叫 Leaderboard model 寫入成績庫，並更改遊戲狀態。
    - 最後重導向回首頁 (/)。
    """
    pass

@game_bp.route('/restart', methods=['POST'])
def restart():
    """
    重新開始遊戲
    - 清除 Session 中的當局遊戲狀態。
    - 重導向回首頁 (/)，讓 index 路由重新初始化遊戲。
    """
    pass
