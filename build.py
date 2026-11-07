#!/usr/bin/env python3
"""將本機遊戲頁輸出為 GitHub Pages 所需的純靜態檔。"""
from pathlib import Path
from game import PAGE

Path(__file__).with_name('index.html').write_text(PAGE, encoding='utf-8')
print('built index.html')
