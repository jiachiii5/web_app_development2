import random
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.leaderboard import Leaderboard

game_bp = Blueprint('game', __name__)

@game_bp.route('/', methods=['GET'])
def index():
    """
    遊戲首頁
    - 檢查 Session 中是否有進行中的遊戲。
    - 若無，則初始化隨機數字 (1-100) 與猜測次數。
    - 渲染 templates/game/index.html，顯示遊戲畫面與歷史紀錄。
    """
    # 檢查是否需要初始化新遊戲
    if 'target_number' not in session or session.get('game_over'):
        session['target_number'] = random.randint(1, 100)
        session['attempts'] = 0
        session['history'] = []
        session['game_over'] = False
        
    return render_template('game/index.html', 
                           attempts=session.get('attempts', 0),
                           history=session.get('history', []),
                           game_over=session.get('game_over', False))

@game_bp.route('/guess', methods=['POST'])
def guess():
    """
    提交猜測數字
    - 接收表單傳來的 'guess' 欄位。
    - 驗證輸入合法性 (是否為 1-100 的整數)。
    - 若合法，比較大小，更新 Session 中的嘗試次數與歷史紀錄。
    - 若猜中，呼叫 Leaderboard model 寫入成績庫，並更改遊戲狀態。
    """
    if 'target_number' not in session or session.get('game_over'):
        flash("請先開始新遊戲！", "warning")
        return redirect(url_for('game.index'))

    guess_str = request.form.get('guess', '').strip()
    
    # 驗證輸入合法性
    if not guess_str:
        flash("請輸入數字！", "danger")
        return redirect(url_for('game.index'))
        
    if not guess_str.isdigit():
        flash("請輸入有效的整數！", "danger")
        return redirect(url_for('game.index'))
        
    guess_num = int(guess_str)
    if guess_num < 1 or guess_num > 100:
        flash("請輸入 1 到 100 之間的數字！", "danger")
        return redirect(url_for('game.index'))

    # 更新猜測狀態
    target = session['target_number']
    session['attempts'] += 1
    
    # 判斷大小
    if guess_num > target:
        result = "太大"
        flash(f"您的猜測 {guess_num}：太大！", "info")
    elif guess_num < target:
        result = "太小"
        flash(f"您的猜測 {guess_num}：太小！", "info")
    else:
        result = "正確"
        session['game_over'] = True
        flash(f"恭喜猜中！答案是 {target}，您總共猜了 {session['attempts']} 次！", "success")
        
        # 將成績寫入排行榜資料庫
        # 若表單有提供玩家名稱則使用，否則使用預設值
        player_name = request.form.get('player_name', '匿名玩家').strip()
        if not player_name:
            player_name = "匿名玩家"
            
        Leaderboard.create(player_name, session['attempts'])

    # 更新歷史紀錄
    history = session.get('history', [])
    # 把最新的猜測加到清單最前面
    history.insert(0, {'guess': guess_num, 'result': result})
    session['history'] = history
    
    # 標記 Session 被修改過，確保 Flask 儲存
    session.modified = True

    return redirect(url_for('game.index'))

@game_bp.route('/restart', methods=['POST'])
def restart():
    """
    重新開始遊戲
    - 清除 Session 中的當局遊戲狀態。
    - 重導向回首頁 (/)。
    """
    session.pop('target_number', None)
    session.pop('attempts', None)
    session.pop('history', None)
    session.pop('game_over', None)
    
    flash("已為您重新開始一局新遊戲！", "success")
    return redirect(url_for('game.index'))
