# コマンド迷宮

🐈‍⬛ 終端機規則怪談與互動短篇。

目前可玩的是 `game.py` 的第一案：`/lost`。它是純本機、純前端狀態的假終端機，**不會執行玩家輸入的 shell 指令**。

## 遊玩

```bash
python3 game.py
```

開啟 <http://127.0.0.1:8081>，輸入 `help` 開始。

## GitHub Pages

遊戲不需要後端。要輸出可部署的靜態頁：

```bash
python3 build.py
```

將產生的 `index.html` 部署到 GitHub Pages 即可。

## 舊原型

- `collector.py` - 背景收集程序，持續監控 shell history
- `viewer.py` - Flask 網頁展示介面
- `database.py` - SQLite 資料庫封裝
- `config.py` - 設定檔

以下是早期的「錯誤指令展示」原型；它不是目前遊戲流程的一部分。

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動收集器（背景執行）
python collector.py &

# 啟動網頁展示
python viewer.py
```

## 現狀

私人專案，`/lost` 垂直切片製作中。🐈‍⬛
