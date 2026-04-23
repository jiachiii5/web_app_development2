import sqlite3
import os

# 確保 instance 目錄存在
DB_DIR = os.path.join(os.path.dirname(__file__), '../../instance')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'database.db')

def get_db_connection():
    """建立與 SQLite 資料庫的連線"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓回傳的資料可以用字典的方式存取欄位
    return conn

class Leaderboard:
    """處理排行榜資料表的 CRUD 邏輯"""

    @staticmethod
    def create(player_name, attempts):
        """新增一筆成績紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO leaderboard (player_name, attempts) VALUES (?, ?)',
            (player_name, attempts)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_top_scores(limit=10):
        """取得前 N 名最佳成績（依猜測次數從小到大排序，同次數依時間排序）"""
        conn = get_db_connection()
        scores = conn.execute(
            'SELECT * FROM leaderboard ORDER BY attempts ASC, created_at ASC LIMIT ?',
            (limit,)
        ).fetchall()
        conn.close()
        return [dict(row) for row in scores]

    @staticmethod
    def get_all():
        """取得所有成績（依建立時間排序）"""
        conn = get_db_connection()
        scores = conn.execute('SELECT * FROM leaderboard ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(row) for row in scores]

    @staticmethod
    def get_by_id(record_id):
        """依 ID 取得特定的成績紀錄"""
        conn = get_db_connection()
        score = conn.execute('SELECT * FROM leaderboard WHERE id = ?', (record_id,)).fetchone()
        conn.close()
        return dict(score) if score else None

    @staticmethod
    def update(record_id, player_name=None, attempts=None):
        """更新特定的成績紀錄（保留供未來可能使用）"""
        conn = get_db_connection()
        if player_name is not None and attempts is not None:
            conn.execute('UPDATE leaderboard SET player_name = ?, attempts = ? WHERE id = ?', 
                         (player_name, attempts, record_id))
        elif player_name is not None:
            conn.execute('UPDATE leaderboard SET player_name = ? WHERE id = ?', 
                         (player_name, record_id))
        elif attempts is not None:
            conn.execute('UPDATE leaderboard SET attempts = ? WHERE id = ?', 
                         (attempts, record_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(record_id):
        """刪除特定的成績紀錄"""
        conn = get_db_connection()
        conn.execute('DELETE FROM leaderboard WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()
