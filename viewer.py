#!/usr/bin/env python3
"""
コマンド迷宮 展示頁面
用 Flask 簡單展示收集到的錯誤指令
"""
from flask import Flask, render_template_string, jsonify
from database import get_recent, get_top, get_stats

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>コマンド迷宮 - 人類的掙扎</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: 'SF Mono', 'Fira Code', monospace; 
            background: #1a1a2e; 
            color: #eee; 
            min-height: 100vh;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 20px; }
        h1 { 
            text-align: center; 
            padding: 30px;
            color: #00d4ff;
            text-shadow: 0 0 10px rgba(0,212,255,0.5);
        }
        h2 { color: #ff6b6b; margin: 30px 0 15px; border-bottom: 1px solid #333; padding-bottom: 5px; }
        .stats { 
            display: flex; 
            justify-content: center; 
            gap: 40px; 
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .stat { text-align: center; }
        .stat-value { font-size: 2em; color: #00d4ff; }
        .stat-label { color: #888; font-size: 0.9em; }
        .command-list { list-style: none; }
        .command-item { 
            background: #16213e; 
            margin: 8px 0; 
            padding: 12px 15px; 
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-left: 3px solid #e94560;
        }
        .command-text { 
            font-family: 'Courier New', monospace;
            color: #ff6b6b;
        }
        .command-meta { 
            color: #666; 
            font-size: 0.85em;
            display: flex;
            gap: 15px;
        }
        .count { 
            background: #e94560; 
            color: white; 
            padding: 2px 8px; 
            border-radius: 10px;
            font-size: 0.8em;
        }
        .shell-badge {
            background: #333;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.75em;
        }
        .footer {
            text-align: center;
            padding: 30px;
            color: #444;
            font-size: 0.8em;
        }
        .cat { font-size: 2em; text-align: center; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="cat">🐈‍⬛</div>
        <h1>コマンド迷宮</h1>
        <p style="text-align:center;color:#666">記錄人類在終端機的掙扎與錯誤</p>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{{ stats.total_entries }}</div>
                <div class="stat-label">總記錄數</div>
            </div>
            <div class="stat">
                <div class="stat-value">{{ stats.unique_commands }}</div>
                <div class="stat-label">不同指令</div>
            </div>
            <div class="stat">
                <div class="stat-value">{{ stats.error_commands }}</div>
                <div class="stat-label">錯誤指令</div>
            </div>
        </div>

        <h2>最近捕獲 🔥</h2>
        <ul class="command-list">
            {% for cmd in recent %}
            <li class="command-item">
                <span class="command-text">{{ cmd.command }}</span>
                <div class="command-meta">
                    <span class="count">{{ cmd.count }}x</span>
                    <span class="shell-badge">{{ cmd.shell or '?' }}</span>
                </div>
            </li>
            {% endfor %}
        </ul>

        <h2>常見錯誤排行榜 👑</h2>
        <ul class="command-list">
            {% for cmd in top %}
            <li class="command-item">
                <span class="command-text">{{ cmd.command }}</span>
                <div class="command-meta">
                    <span class="count">{{ cmd.count }}x</span>
                </div>
            </li>
            {% endfor %}
        </ul>

        <div class="footer">
            コマンド迷宮 v0.1 | 收集來自 terminal 的悲鳴
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    stats = get_stats()
    recent = get_recent(limit=20, error_only=False)
    top = get_top(limit=10, error_only=True)
    return render_template_string(HTML_TEMPLATE, stats=stats, recent=recent, top=top)

@app.route('/api/stats')
def api_stats():
    return jsonify(get_stats())

@app.route('/api/recent')
def api_recent():
    return jsonify([dict(row) for row in get_recent(50)])

@app.route('/api/top')
def api_top():
    return jsonify([dict(row) for row in get_top(20, error_only=True)])


if __name__ == '__main__':
    from config import WEB_HOST, WEB_PORT
    print(f"コマンド迷宮 展示頁面啟動: http://{WEB_HOST}:{WEB_PORT}")
    app.run(host=WEB_HOST, port=WEB_PORT, debug=False)
