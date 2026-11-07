#!/usr/bin/env python3
"""コマンド迷宮：單一場景、純本機的互動式終端機怪談。"""
from http.server import BaseHTTPRequestHandler, HTTPServer

PAGE = r'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>コマンド迷宮｜/lost</title><style>
:root{--ink:#d6f5d6;--dim:#79917b;--acid:#a8ff60;--red:#ff6d6d;--panel:#09100b;--line:#27432c}
*{box-sizing:border-box}body{margin:0;background:#030704;color:var(--ink);font:16px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace;min-height:100vh;display:grid;place-items:center}
main{width:min(900px,100%);min-height:100vh;padding:clamp(22px,5vw,56px);background:radial-gradient(circle at 50% 0,#102216,#030704 62%)}
h1{font-size:clamp(1.5rem,4vw,2.8rem);letter-spacing:.12em;margin:0;color:var(--acid);text-shadow:0 0 24px #54b52b}header p{color:var(--dim);margin:.25rem 0 2rem}
#terminal{border:1px solid var(--line);background:var(--panel);box-shadow:0 0 60px #071a09 inset;padding:1.2rem;min-height:52vh;white-space:pre-wrap;overflow-wrap:anywhere}.line{margin:0 0 .75rem}.system{color:var(--dim)}.danger{color:var(--red)}.good{color:var(--acid)}
form{display:flex;gap:.6rem;margin-top:1rem;align-items:center}.prompt{color:var(--acid)}input{flex:1;background:transparent;border:0;border-bottom:1px solid var(--line);color:var(--ink);font:inherit;padding:.65rem 0;outline:0}button{background:#153b1d;border:1px solid #40824a;color:var(--ink);font:inherit;padding:.55rem .9rem;cursor:pointer}button:hover{background:#215b2c}
.chips{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:1rem}.chips button{font-size:.82rem;color:var(--dim);padding:.32rem .55rem}.note{color:var(--dim);font-size:.8rem;margin-top:1.25rem}
</style></head><body><main><header><h1>コマンド迷宮</h1><p>CASE 001：找出誰把 <code>/lost</code> 建在你的系統裡。</p></header>
<section id="terminal" aria-live="polite"></section><form id="form"><span class="prompt">guest@maze:/lost$</span><input id="cmd" autocomplete="off" autofocus aria-label="輸入指令"><button>執行</button></form>
<div class="chips"><button data-c="help">help</button><button data-c="ls">ls</button><button data-c="cat README.txt">cat README.txt</button><button data-c="inspect door">inspect door</button><button data-c="unlock door">unlock door</button><button data-c="exit">exit</button></div>
<p class="note">提示：這裡不會執行真正的 shell 指令。想清楚再輸入；迷宮很喜歡照字面理解。</p></main>
<script>
const out=document.querySelector('#terminal'),form=document.querySelector('#form'),input=document.querySelector('#cmd');
let state={read:false,seenDoor:false,unlocked:false,done:false};
const say=(text,kind='')=>{let p=document.createElement('p');p.className='line '+kind;p.textContent=text;out.append(p);out.scrollTop=out.scrollHeight};
function boot(){say('Booting /lost ...','system');say('沒有帳號、沒有登入紀錄，也沒有建立這個資料夾的人。');say('目錄裡有一扇門。門旁邊貼著一張褪色標籤：請勿使用你記得的指令。','danger');say('輸入 help。','system')}
function run(raw){let c=raw.trim().replace(/\s+/g,' ');if(!c)return; say('guest@maze:/lost$ '+c,'good');if(state.done){say('程序已結束。迷宮仍在執行。','danger');return}
 if(c==='help')say('可用：ls、cat README.txt、inspect door、unlock door、rm README.txt、exit。\n你也可以輸入任何指令；它會記得。');
 else if(c==='ls')say(state.unlocked?'README.txt  door/  you':'README.txt  door/');
 else if(c==='cat README.txt'){state.read=true;say('README.txt\n\n歡迎回來。\n\n規則 1：門只會為「不是你的人」打開。\n規則 2：若你看見自己的名字，別承認。\n規則 3：離開前，請把 README 留給下一個你。');}
 else if(c==='inspect door'){state.seenDoor=true;say(state.read?'門後傳來鍵盤聲。有人正以你的速度打字。鎖孔標示：GUEST ONLY。':'門沒有把手。它像是在等你讀完什麼。','danger')}
 else if(c==='unlock door'){if(!state.read){say('ACCESS DENIED：你不知道自己正在同意什麼。','danger')}else{state.unlocked=true;say('鎖發出一次很輕的喀噠聲。門沒有打開；終端機多了一個游標，正替你閃爍。','danger')}}
 else if(c==='rm README.txt'){state.done=true;say('README.txt 已刪除。\n\n門開了。門外是一張桌子，桌上放著一台正在顯示 /lost 的終端機。\n\nENDING：你把說明留白了。下一個人會以為這是第一次。','danger')}
 else if(c==='exit'){state.done=true;if(state.unlocked&&state.read)say('你沒有碰門。你關掉終端機，卻在黑掉前看見游標替你輸入：guest@maze:/lost$\n\nENDING：你離開了；至少這次是。','good');else say('exit: 你還不知道要從哪裡出去。','danger')}
 else if(/^(sudo|rm -rf|chmod)/.test(c))say('迷宮很高興你把權限交給它，但這裡沒有真正的系統可以救。','danger');
 else say(c+': command not found。\n奇怪的是，錯誤訊息最後多了一行：我知道你本來想打什麼。','danger');}
form.addEventListener('submit',e=>{e.preventDefault();let v=input.value;input.value='';run(v)});document.querySelectorAll('[data-c]').forEach(b=>b.onclick=()=>{input.value=b.dataset.c;input.focus()});boot();
</script></body></html>'''

class GameHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ('/', '/index.html'):
            self.send_error(404)
            return
        body = PAGE.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    print('コマンド迷宮: http://127.0.0.1:8081')
    HTTPServer(('127.0.0.1', 8081), GameHandler).serve_forever()
