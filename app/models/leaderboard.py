import sqlite3
import os
import logging

# 確保 instance 目錄存在
DB_DIR = os.path.join(os.path.dirname(__file__), '../../instance')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'database.db')

def get_db_connection():
    """建立與 SQLite 資料庫的連線"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # 讓回傳的資料可以用字典的方式存取欄位
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        raise

class Leaderboard:
    """處理排行榜資料表的 CRUD 邏輯"""

    @staticmethod
    def create(player_name, attempts):
        """
        新增一筆成績紀錄
        :param player_name: 玩家名稱 (字串)
        :param attempts: 猜測次數 (整數)
        :return: 新增的紀錄 ID，若失敗則回傳 None
        """
        try:
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
        except sqlite3.Error as e:
            logging.error(f"Error creating leaderboard record: {e}")
            return None

    @staticmethod
    def get_top_scores(limit=10):
        """
        取得前 N 名最佳成績（依猜測次數從小到大排序，同次數依時間排序）
        :param limit: 取回的資料筆數 (預設 10)
        :return: 成績清單 (字典陣列)
        """
        try:
            conn = get_db_connection()
            scores = conn.execute(
                'SELECT * FROM leaderboard ORDER BY attempts ASC, created_at ASC LIMIT ?',
                (limit,)
            ).fetchall()
            conn.close()
            return [dict(row) for row in scores]
        except sqlite3.Error as e:
            logging.error(f"Error fetching top scores: {e}")
            return []

    @staticmethod
    def get_all():
        """
        取得所有成績（依建立時間排序）
        :return: 成績清單 (字典陣列)
        """
        try:
            conn = get_db_connection()
            scores = conn.execute('SELECT * FROM leaderboard ORDER BY created_at DESC').fetchall()
            conn.close()
            return [dict(row) for row in scores]
        except sqlite3.Error as e:
            logging.error(f"Error fetching all scores: {e}")
            return []

    @staticmethod
    def get_by_id(record_id):
        """
        依 ID 取得特定的成績紀錄
        :param record_id: 紀錄的 ID (整數)
        :return: 成績紀錄 (字典)，若無則回傳 None
        """
        try:
            conn = get_db_connection()
            score = conn.execute('SELECT * FROM leaderboard WHERE id = ?', (record_id,)).fetchone()
            conn.close()
            return dict(score) if score else None
        except sqlite3.Error as e:
            logging.error(f"Error fetching score by id: {e}")
            return None

    @staticmethod
    def update(record_id, player_name=None, attempts=None):
        """
        更新特定的成績紀錄（保留供未來可能使用）
        :param record_id: 紀錄的 ID (整數)
        :param player_name: 更新的玩家名稱 (選填)
        :param attempts: 更新的猜測次數 (選填)
        :return: 布林值 (是否更新成功)
        """
        try:
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
            return True
        except sqlite3.Error as e:
            logging.error(f"Error updating score: {e}")
            return False

    @staticmethod
    def delete(record_id):
        """
        刪除特定的成績紀錄
        :param record_id: 紀錄的 ID (整數)
        :return: 布林值 (是否刪除成功)
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM leaderboard WHERE id = ?', (record_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            logging.error(f"Error deleting score: {e}")
            return False
