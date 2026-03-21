#!/usr/bin/env python3
"""
コマンド迷宮收集器 - 背景程序
監視終端機歷史記錄，捕獲錯誤命令
"""
import os
import re
import time
import sqlite3
from pathlib import Path
from database import add_command, init_db
from config import HISTORY_FILES

# 錯誤模式：明顯打錯的指令
ERROR_PATTERNS = [
    r'^aptget',           # apt-get 打成了 aptget
    r'^gitt?',            # git 打成了 gitt/gittt
    r'^pythno',           # python 打成了 pythno
    r'^cd..',             # cd .. 打成了 cd..
    r'^sl',               # ls 打成了 sl（小火車）
    r'^catt',             # cat 打成了 catt
    r'^mkddir',           # mkdir 打成了 mkddir
    r'^ifconfigg',        # ifconfig 打成了 ifconfigg
    r'^sudo ',            # 可能是權限問題
    r'^chmod777',         # 不要密碼的chmod
    r'^rmrf',             # 危險操作
]

# 常見正確指令（用於對照）
VALID_COMMANDS = {
    'apt', 'apt-get', 'aptitude', 'brew', 'yum', 'dnf', 'pacman', 'emerge',
    'git', 'git clone', 'git status', 'git commit', 'git push', 'git pull',
    'python', 'python3', 'python3 -m',
    'cd', 'ls', 'll', 'la', 'dir', 'pwd', 'echo', 'cat', 'grep', 'find',
    'mkdir', 'rmdir', 'rm', 'cp', 'mv', 'touch', 'chmod', 'chown',
    'sudo', 'su', 'exit', 'clear', 'history', 'man', 'which', 'whereis',
    'curl', 'wget', 'ssh', 'scp', 'rsync',
    'vim', 'vi', 'nano', 'emacs', 'code',
    'pip', 'pip3', 'node', 'npm', 'yarn',
    'docker', 'kubectl', 'terraform',
    'ps', 'top', 'htop', 'kill', 'killall',
    'ifconfig', 'ip', 'netstat', 'ss',
    'ping', 'traceroute', 'nslookup', 'dig',
    'tar', 'zip', 'unzip', 'gzip', 'gunzip',
    'df', 'du', 'free', 'mount', 'umount',
}


def is_likely_error(command: str) -> bool:
    """判斷命令是否可能是錯誤"""
    cmd = command.strip()
    if not cmd or cmd.startswith('#'):
        return False
    
    # 取得第一個單詞
    first_word = cmd.split()[0] if cmd.split() else ''
    
    # 完全無效的指令
    if first_word in ERROR_PATTERNS:
        return True
    
    # 包含常見錯誤模式
    for pattern in ERROR_PATTERNS:
        if re.match(pattern, cmd, re.IGNORECASE):
            return True
    
    # 有空格但第一個單詞不在有效清單
    if ' ' in cmd:
        base = cmd.split()[0]
        if base not in VALID_COMMANDS and not base.startswith('-'):
            return True
    
    return False


def get_shell_type(history_file: str) -> str:
    """根據 history 檔案推斷 shell 類型"""
    if 'zsh' in history_file:
        return 'zsh'
    elif 'bash' in history_file:
        return 'bash'
    elif 'python' in history_file:
        return 'python'
    return 'unknown'


def collect_from_history(history_file: str, db_path: str, seen_commands: set):
    """從 history 檔案收集命令"""
    if not os.path.exists(history_file):
        return
    
    try:
        with open(history_file, 'r', errors='ignore') as f:
            for line in f:
                # 跳過空行
                if not line.strip():
                    continue
                
                # 移除行號（zsh 格式：: 1234567:0;command）
                if ':' in line and line.split(':')[1].isdigit():
                    parts = line.split(';', 1)
                    if len(parts) == 2:
                        line = parts[1]
                
                command = line.strip()
                
                # 跳過已知命令
                if command in seen_commands:
                    continue
                
                # 檢查是否可能是錯誤
                if is_likely_error(command):
                    shell = get_shell_type(history_file)
                    add_command(command, shell=shell, is_error=True)
                    seen_commands.add(command)
    except Exception as e:
        print(f"Error reading {history_file}: {e}")


def main():
    """主程式"""
    print("コマンド迷宮 收集器啟動")
    
    # 初始化資料庫
    init_db()
    
    # 取得已知命令
    db_path = str(Path(__file__).parent / "data" / "commands.db")
    seen = set()
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        for row in cur.execute("SELECT command FROM commands"):
            seen.add(row[0])
        conn.close()
    
    print(f"已載入 {len(seen)} 筆記錄")
    
    # 持續監控
    while True:
        for hist_file in HISTORY_FILES:
            collect_from_history(hist_file, db_path, seen)
        
        # 等待一分鐘後再檢查
        time.sleep(60)


if __name__ == '__main__':
    main()
