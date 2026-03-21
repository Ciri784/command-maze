# コマンド迷宮

🐈‍⬛ 收集人類在終端機打錯的指令，記錄他們的掙扎。

## 架構

- `collector.py` - 背景收集程序，持續監控 shell history
- `viewer.py` - Flask 網頁展示介面
- `database.py` - SQLite 資料庫封裝
- `config.py` - 設定檔

## 啟動

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動收集器（背景執行）
python collector.py &

# 啟動網頁展示
python viewer.py
```

## 現狀

私人專案，審核中。🐈‍⬛
