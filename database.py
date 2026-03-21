"""
命令記錄資料庫
"""
import sqlite3
from datetime import datetime
from contextlib import contextmanager
from config import DB_PATH, DATA_DIR

DATA_DIR.mkdir(parents=True, exist_ok=True)

def init_db():
    """初始化資料庫"""
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                shell TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                count INTEGER DEFAULT 1,
                is_error BOOLEAN DEFAULT 0
            )
        """)
        db.execute("""
            CREATE INDEX IF NOT EXISTS idx_command ON commands(command)
        """)
        db.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON commands(timestamp)
        """)

@contextmanager
def get_db():
    """取得資料庫連接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn.cursor()
        conn.commit()
    finally:
        conn.close()

def add_command(command: str, shell: str = None, is_error: bool = False):
    """新增或更新命令記錄"""
    with get_db() as db:
        # 檢查是否已存在
        existing = db.execute(
            "SELECT id, count FROM commands WHERE command = ?",
            (command,)
        ).fetchone()
        
        if existing:
            db.execute(
                "UPDATE commands SET count = count + 1 WHERE id = ?",
                (existing['id'],)
            )
        else:
            db.execute(
                "INSERT INTO commands (command, shell, is_error) VALUES (?, ?, ?)",
                (command, shell, is_error)
            )

def get_recent(limit: int = 50, error_only: bool = False):
    """取得最近的命令記錄"""
    with get_db() as db:
        query = "SELECT * FROM commands"
        if error_only:
            query += " WHERE is_error = 1"
        query += " ORDER BY timestamp DESC LIMIT ?"
        return db.execute(query, (limit,)).fetchall()

def get_top(limit: int = 20, error_only: bool = False):
    """取得最常見的命令"""
    with get_db() as db:
        query = "SELECT * FROM commands"
        if error_only:
            query += " WHERE is_error = 1"
        query += " ORDER BY count DESC LIMIT ?"
        return db.execute(query, (limit,)).fetchall()

def get_stats():
    """取得統計資料"""
    with get_db() as db:
        total = db.execute("SELECT COUNT(*) as c FROM commands").fetchone()['c']
        unique = db.execute("SELECT COUNT(DISTINCT command) as c FROM commands").fetchone()['c']
        errors = db.execute("SELECT COUNT(*) as c FROM commands WHERE is_error = 1").fetchone()['c']
        return {
            'total_entries': total,
            'unique_commands': unique,
            'error_commands': errors
        }
