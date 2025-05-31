import requests
import time
import base64
from datetime import datetime

# === CONFIG ===
GITHUB_USERNAME = "luxamind141"
CENTRALOG_REPO = "centralog"
LOG_FILE_PATH = "log.txt"
TASK_FILE_PATH = "task.txt"

# Token GitHub (privilégier stockage sécurisé)
GITHUB_TOKEN = "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"

def get_github_file_sha(repo, path):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()["sha"]
    return None

def update_github_file(repo, path, content, commit_msg):
    print(f"[INFO] Mise à jour du fichier {path} dans {repo}...")
    sha = get_github_file_sha(repo, path)
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    content_b64 = base64.b64encode(content.encode()).decode()
    data = {
        "message": commit_msg,
        "content": content_b64,
        "branch": "main"
    }
    if sha:
        data["sha"] = sha
    r = requests.put(url, json=data, headers=headers)
    if r.status_code in [200, 201]:
        print(f"[INFO] Fichier {path} mis à jour avec succès.")
        return True
    else:
        print(f"[ERROR] Échec mise à jour {path} : HTTP {r.status_code} - {r.text}")
        return False

def get_task_url():
    print("[INFO] Récupération du contenu de task.txt via API GitHub avec headers anti-cache...")
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/executionscript/contents/{TASK_FILE_PATH}"
    headers = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.raw"
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        url_task = r.text.strip()
        if url_task == "":
            print("[INFO] Aucune tâche à faire (task.txt vide).")
            return None
        print(f"[INFO] Tâche détectée : {url_task}")
        return url_task
    else:
        print(f"[ERROR] Impossible de récupérer task.txt via API : HTTP {r.status_code}")
        return None

def run_remote_script(url):
    try:
        print(f"[INFO] Téléchargement du script : {url}")
        r = requests.get(url)
        if r.status_code != 200:
            print(f"[ERROR] Échec téléchargement script : HTTP {r.status_code}")
            return False
        code = r.text
        print("[INFO] Exécution du script...")
        exec(code, {})  # exécution dans namespace vide
        print("[INFO] Script exécuté avec succès.")
        return True
    except Exception as e:
        print(f"[ERROR] Exception pendant l'exécution du script : {e}")
        return False

def main():
    while True:
        now = datetime.now().strftime("%d/%m/%y %H:%M")
        log_msg = f"launch : {now}\nexescript : none"
        update_github_file(CENTRALOG_REPO, LOG_FILE_PATH, log_msg, "Mise à jour log lancement")

        task_url = get_task_url()
        if task_url:
            success = run_remote_script(task_url)
            if success:
                update_github_file("executionscript", "task.txt", "", "Effacer task.txt après exécution")
                update_github_file(CENTRALOG_REPO, LOG_FILE_PATH, "TaskOK", "Mise à jour log task OK")

        time.sleep(60)

if __name__ == "__main__":
    main()
