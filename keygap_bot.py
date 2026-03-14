import http.server, socketserver, sqlite3, json, threading, time, subprocess, os
from urllib.parse import parse_qs, quote
from datetime import datetime

# --- CONFIGURAZIONE ---
TARGET_ID = "keygap-21"
DB_FILE = 'keygap_newsletter.db'
PORT = 8100

def init_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS subscribers (id INTEGER PRIMARY KEY, email TEXT, data TEXT)')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"\033[1;33m⚠️ ERRORE DB: {e}\033[0m")

class FinalHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Header fondamentale per permettere la comunicazione da GitHub
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Bypass-Tunnel-Reminder')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def security_shield(self):
        banned = ['/.env', '/.git', '/wp-admin', '/info.php', 'robots.txt']
        if any(path in self.path for path in banned):
            print(f"\033[1;31m🛡️  ATTACCO BLOCCATO: {self.path}\033[0m")
            self.send_response(403); self.end_headers()
            return True
        return False

    def do_GET(self):
        if self.security_shield(): return
        
        if self.path.startswith('/filter'):
            f = self.path.split('=')[-1]
            urls = {
                'warehouse': f"https://www.amazon.it/warehouse?tag={TARGET_ID}",
                'lightning': f"https://www.amazon.it/gp/goldbox?tag={TARGET_ID}",
                'low20': f"https://www.amazon.it/s?k=offerte&tag={TARGET_ID}&low-price=&high-price=20",
                'tech': f"https://www.amazon.it/s?k=informatica&tag={TARGET_ID}&pct-off=20-99",
                'home': f"https://www.amazon.it/s?k=casa+e+cucina&tag={TARGET_ID}&pct-off=20-99",
                'hardware': f"https://www.amazon.it/s?k=hardware+pc&tag={TARGET_ID}",
                'gaming': f"https://www.amazon.it/s?k=gaming+accessori&tag={TARGET_ID}",
                'smarthome': f"https://www.amazon.it/s?k=domotica&tag={TARGET_ID}",
                'smartphone': f"https://www.amazon.it/s?k=smartphone&tag={TARGET_ID}",
                'bestsellers': f"https://www.amazon.it/gp/bestsellers?tag={TARGET_ID}",
                'novita': f"https://www.amazon.it/gp/new-releases?tag={TARGET_ID}",
                'offerte': f"https://www.amazon.it/gp/goldbox?tag={TARGET_ID}"
            }
            target_url = urls.get(f, f"https://www.amazon.it/?tag={TARGET_ID}")
            print(f"\033[1;32m🔗 FILTRO ATTIVATO: {f} -> Reindirizzamento inviato\033[0m")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"url": target_url}).encode())
        else:
            self.send_response(200); self.send_header('Content-type', 'text/plain'); self.end_headers()
            self.wfile.write(b"K-SOVEREIGN NODE OPERATIONAL")

    def do_POST(self):
        if self.security_shield(): return
        cl = int(self.headers['Content-Length'])
        pd = parse_qs(self.rfile.read(cl).decode('utf-8'))
        
        if self.path in ['/node-search', '/search']:
            q = pd.get('q', [''])[0]
            if q:
                amazon_url = f"https://www.amazon.it/s?k={quote(q)}&tag={TARGET_ID}&pct-off=20-99"
                print(f"\033[1;36m🚀 RICERCA INTERCETTATA: {q}\033[0m")
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"url": amazon_url}).encode())

if __name__ == "__main__":
    init_db()
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), FinalHandler) as httpd:
        print(f"\033[1;32m[OK] K-SOVEREIGN v14.6 ATTIVO - PORTA {PORT}\033[0m")
        httpd.serve_forever()