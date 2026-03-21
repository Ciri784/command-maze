"""
コマンド迷宮 - 收集人類在終端機打錯的指令
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "commands.db"

# 追蹤的 history 檔案
HISTORY_FILES = [
    os.path.expanduser("~/.bash_history"),
    os.path.expanduser("~/.zsh_history"),
    os.path.expanduser("~/.history"),
    os.path.expanduser("~/.python_history"),
]

# 網頁展示設定
WEB_HOST = "0.0.0.0"
WEB_PORT = 8080
