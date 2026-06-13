#!/usr/bin/env python3
"""案例助手 - 本地AI案例查询服务
同事打开浏览器就能用。
启动：export CASE_HELPER_API_KEY=*** && python3 ~/Desktop/case_helper_server.py
"""

import http.server, json, urllib.request, urllib.error, sys, os, socket

API_KEY=os.env...Y") or ""
API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-v4-flash"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8888

if not API_KEY:
    print("="*50)
    print("  案例助手启动失败 - 未设置API Key")
    print("  查看Key: grep api_key ~/.hermes/config.yaml")
    print("  运行: export CASE_HELPER_API_KEY=***)    print("  重试:", sys.argv[0])
    print("="*50)
    sys.exit(1)

SYSTEM_PROMPT = """你是一名专业的媒体人...（完整规则同前）"""
# (实际运行时使用完整版本)

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(("""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>案例助手</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;background:#f5f5f7;height:100vh;display:flex;flex-direction:column}
.header{background:#1a1a2e;color:#fff;padding:16px 24px;display:flex;align-items:center;gap:12px;flex-shrink:0}
.header h1{font-size:18px;font-weight:600}.header span{font-size:13px;color:#aaa}
.tags{display:flex;gap:8px;flex-wrap:wrap;padding:8px 24px;max-width:800px;margin:0 auto;width:100%;flex-shrink:0}
.tags button{padding:6px 14px;border:1px solid #ddd;border-radius:16px;background:#fff;font-size:13px;cursor:pointer;color:#555}
.tags button:hover{border-color:#1a1a2e;color:#1a1a2e}
.chat{flex:1;overflow-y:auto;padding:20px 24px;display:flex;flex-direction:column;gap:16px;max-width:800px;margin:0 auto;width:100%}
.msg{max-width:85%;padding:12px 16px;border-radius:12px;line-height:1.7;font-size:15px;white-space:pre-wrap;word-break:break-word}
.user{background:#1a1a2e;color:#fff;align-self:flex-end;border-bottom-right-radius:4px}
.bot{background:#fff;color:#1a1a2e;align-self:flex-start;border-bottom-left-radius:4px;box-shadow:0 1px 3px rgba(0,0,0,0.08)}
.waiting{color:#999;font-size:14px;padding:12px 16px;background:#fff;align-self:flex-start;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,0.08)}
@keyframes dots{0%,20%{opacity:0}50%{opacity:1}80%,100%{opacity:0}}
.waiting span{animation:dots 1.4s infinite;font-size:20px;line-height:1}
.waiting span:nth-child(2){animation-delay:.2s}
.waiting span:nth-child(3){animation-delay:.4s}
.input{border-top:1px solid #e0e0e0;padding:16px 24px;background:#fff;display:flex;gap:12px;max-width:800px;margin:0 auto;width:100%;flex-shrink:0}
.input input{flex:1;padding:12px 16px;border:1px solid #ddd;border-radius:8px;font-size:15px;outline:none}
.input input:focus{border-color:#1a1a2e}
.input button{padding:12px 24px;background:#1a1a2e;color:#fff;border:none;border-radius:8px;font-size:15px;cursor:pointer}
.input button:disabled{background:#999;cursor:not-allowed}
</style></head><body>
<div class="header"><h1>📋 案例助手</h1><span>27家企业 · 按需生成</span></div>
<div class="tags">
<button onclick="q('数据治理')">数据治理</button>
<button onclick="q('城市管网')">城市管网</button>
<button onclick="q('化妆品')">化妆品</button>
<button onclick="q('网络安全')">网络安全</button>
<button onclick="q('创新药')">创新药</button>
<button onclick="q('水务')">水务</button>
<button onclick="q('芯片')">芯片</button>
</div>
<div class="chat" id="chat"></div>
<div class="input">
<input id="inp" placeholder="输入需求，如：我在对接一个做数据治理的企业..." onkeydown="if(event.key==='Enter') send()">
<button id="btn" onclick="send()">发送</button>
</div>
<script>
let chat=document.getElementById('chat'),inp=document.getElementById('inp'),btn=document.getElementById('btn');
let busy=false;
function addMsg(t,c){let d=document.createElement('div');d.className='msg '+c;d.textContent=t;chat.appendChild(d);chat.scrollTop=chat.scrollHeight;return d}
function showWaiting(){let d=document.createElement('div');d.className='waiting';d.id='wait';d.innerHTML='思考中<span>.</span><span>.</span><span>.</span>';chat.appendChild(d);chat.scrollTop=chat.scrollHeight}
function hideWaiting(){let e=document.getElementById('wait');if(e)e.remove()}
function q(t){inp.value='我要对接一个做'+t+'的企业，给我一个相关案例';send()}
async function send(){
    let t=inp.value.trim();if(!t||busy)return;
    inp.value='';busy=true;btn.disabled=true;
    addMsg(t,'user');showWaiting();
    try{
        let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({m:t})});
        let d=await r.json();hideWaiting();addMsg(d.reply,'bot');
    }catch(e){hideWaiting();addMsg('请求失败: '+e.message,'bot')}
    busy=false;btn.disabled=false;
}
</script></body></html>""").encode())

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(length))
        user_msg = body.get("m", "")

        payload = json.dumps({"model": MODEL, "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ], "max_tokens": 4096, "temperature": 0.7, "stream": False}).encode()

        req = urllib.request.Request(API_URL, data=payload,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode())
                reply = data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            reply = f"API请求失败: HTTP {e.code}"
        except Exception as e:
            reply = f"出错: {str(e)}"

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"reply": reply}, ensure_ascii=False).encode())

    def log_message(self, *args): pass

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    ip = socket.gethostbyname(socket.gethostname())
    print(f"\n{'='*50}")
    print(f"  ✅ 案例助手已启动")
    print(f"  本机：http://localhost:{PORT}")
    print(f"  同事：http://{ip}:{PORT}")
    print(f"  Ctrl+C 停止")
    print(f"{'='*50}\n")
    try: server.serve_forever()
    except KeyboardInterrupt: print("\n已停止"); server.server_close()
