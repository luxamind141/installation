import requests
import random
import time
import threading
from colorama import Fore, Style, init
import uuid

init(autoreset=True)

# User Agents pour variation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (Linux; Android 11)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
]

DEFAULT_MESSAGES = [
    "Wsh y’avait genre personne en cours d’anglais, contrôle surprise ou fuite collective ? 😭",
    "Le mec a laissé son sac dans le couloir toute la journée… vol ou oubli intentionnel ? 👀",
    "Y’a encore eu une baston à la récré, mais cette fois c’était pour une place à la prise 😭🔌",
    "Le micro du prof de musique a buggé, ça a crié comme dans un film d’horreur 😭💀",
    "Y’a un mec qui a ramené une pizza en plein cours… et il a partagé avec personne 😤",
    "Les chiottes du 2e étage sont encore bouchées… qui met du PQ comme ça sérieux 😭",
    "Un prof a dit 'ouvrez Pronote' et 3 élèves ont littéralement disparu 😭📉",
    "Une alarme a sonné en plein DS… et tout le monde s’est regardé genre ‘c’est un signe ?’ 🔥",
    "La machine à café marche plus… j’vous jure c’est la fin du monde pour les terminales ☕💔",
    "Quelqu’un a écrit 'vive les vacances' sur le TNI… en avril. Motivation à -200.",
    "Y’avait un pigeon en salle de SVT… il assistait au cours ou il notait les absents ? 🐦",
    "Un élève a mis une sono dans son sac, on avait ambiance boîte à la cantine 🔊😂",
    "Le CPE a dit 'vous êtes fatigués ? Moi aussi'. Instant respect ✊",
    "Quelqu’un a ramené un oreiller en cours… respect au roi de la sieste 👑💤",
    "La sonnerie a pas marché ce matin, toute la classe en mode 'on vient ou pas ?' ⏰❓",
    "Y’avait un ballon coincé dans les lumières du gymnase… il date de 2018 je crois 😭",
    "Un gars s’est endormi avec son stylo dans la bouche… il s’est réveillé genre ‘j’ai loupé quoi ?’ 💤✍️",
    "Le tableau affichait 'journée portes ouvertes'… sauf qu’on était déjà enfermés 😭🚪",
    "Le prof a sorti 'j’ai eu pire que vous cette année'… ambiance 💀",
    "Un mec a crié 'j’ai eu 4' après avoir vu sa note, la classe a applaudi comme s’il avait 18 😂👏"
]

NGL_API_URL = "https://ngl.link/api/submit"


def display_intro():
    print(Fore.CYAN + "Script By")
    time.sleep(0.5)
    print(Fore.LIGHTYELLOW_EX + r"""
 ▄█       ███    █▄   ▄████████  ▄██████▄     ▄████████    ▄████████ 
███       ███    ███ ███    ███ ███    ███   ███    ███   ███    ███ 
███       ███    ███ ███    █▀  ███    ███   ███    ███   ███    ███ 
███       ███    ███ ███        ███    ███  ▄███▄▄▄▄██▀   ███    ███ 
███       ███    ███ ███        ███    ███ ▀▀███▀▀▀▀▀   ▀███████████ 
███       ███    ███ ███    █▄  ███    ███ ▀███████████   ███    ███ 
███▌    ▄ ███    ███ ███    ███ ███    ███   ███    ███   ███    ███ 
█████▄▄██ ████████▀  ████████▀   ▀██████▀    ███    ███   ███    █▀  
▀                                            ███    ███              
""")
    time.sleep(1)
    print(Fore.LIGHTGREEN_EX + "\n\n\n")
    print(Fore.GREEN + """
   ,d8888b                 d8b                                d8b 
   88P'                    ?88                                88P 
d888888P                    88b                              d88  
  ?88'    ?88   d8P d8888b  888  d88'      88bd88b  d888b8b  888  
  88P     d88   88 d8P' P  888bd8P'       88P' ?8bd8P' ?88  ?88  
 d88      ?8(  d88 88b     d88888b        d88   88P88b  ,88b  88b 
d88'      ?88P'?8b?888P'd88' ?88b,    d88'   88b?88P'88b  88b
                                                          )88     
                                                         ,88P     
                                                     ?8888P      
""")


def generate_device_id():
    return str(uuid.uuid4())

def send_ngl_message(username, message, proxy, user_agent):
    headers = {
        "User-Agent": user_agent,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "username": username,
        "question": message,
        "deviceId": generate_device_id()
    }
    try:
        response = requests.post(
            NGL_API_URL,
            headers=headers,
            data=data,
            proxies={"http": proxy, "https": proxy},
            timeout=10
        )
        return response.status_code == 200
    except Exception:
        return False


def spam_worker(username, messages, proxies, message_limit, delay, ua_change_interval, proxy_change_interval):
    proxy_idx = 0
    message_count = 0
    ua_idx = 0
    user_agent = user_agents[ua_idx % len(user_agents)]
    proxy = f"http://{proxies[proxy_idx]}"

    while True:
        message = random.choice(messages)

        if message_count > 0 and message_count % ua_change_interval == 0:
            ua_idx += 1
            user_agent = user_agents[ua_idx % len(user_agents)]

        if message_count > 0 and message_count % proxy_change_interval == 0:
            proxy_idx = (proxy_idx + 1) % len(proxies)
            proxy = f"http://{proxies[proxy_idx]}"
            print(Fore.CYAN + f"[INFO] Thread {threading.current_thread().name} → Changement de proxy : {proxy}")

        success = send_ngl_message(username, message, proxy, user_agent)
        status = Fore.GREEN + "[SUCCÈS]" if success else Fore.RED + "[ÉCHEC]"
        print(f"{status} Thread {threading.current_thread().name} → Message: {message[:30]}... via {proxy}")

        if not success:
            proxy_idx = (proxy_idx + 1) % len(proxies)
            proxy = f"http://{proxies[proxy_idx]}"
            print(Fore.YELLOW + f"[WARN] Thread {threading.current_thread().name} → Proxy changé suite à erreur : {proxy}")

        message_count += 1
        if message_limit and message_count >= message_limit:
            print(Fore.LIGHTMAGENTA_EX + f"[INFO] Thread {threading.current_thread().name} → Limite atteinte ({message_limit} messages), arrêt.")
            break

        time.sleep(delay)


def main():
    display_intro()

    username = input("🔤 Entrez le pseudo NGL (destinataire) : ").strip()

    use_proxy = input("🌐 Utiliser un proxy ? (y/n) : ").strip().lower() == 'y'
    proxy_list = []
    if use_proxy:
        with open("proxy_list.txt", "r") as f:
            proxy_list = [line.strip() for line in f if line.strip()]
        if not proxy_list:
            print(Fore.RED + "[ERREUR] Aucun proxy valide trouvé.")
            return

    mode = input("🚀 Mode (slow / normal / fast) : ").strip().lower()
    delay = {"slow": 5, "normal": 1, "fast": 0.25}.get(mode, 1)

    ua_change_interval = int(input("🔁 Changer de User Agent tous les combien de messages ? : "))
    proxy_change_interval = int(input("🔁 Changer de Proxy tous les combien de messages ? : ")) if use_proxy else 1000

    use_default_msg = input("💬 Utiliser les messages par défaut ? (y/n) : ").strip().lower() == 'y'
    messages = DEFAULT_MESSAGES if use_default_msg else [input("Entrez votre message personnalisé : ")]

    num_threads = int(input("🔢 Nombre de threads à utiliser : "))

    limit_mode = input("⏱️ Limite par (messages / temps / infini) ? : ").strip().lower()
    message_limit = None
    if limit_mode == "messages":
        message_limit = int(input("🔢 Nombre total de messages par thread : "))
    elif limit_mode == "temps":
        time_limit = int(input("⏱️ Temps en minutes : ")) * 60
        message_limit = int(time_limit / delay)

    input(Fore.LIGHTBLUE_EX + "\n✅ Tout est prêt. Appuyez sur Entrée pour démarrer.\n")

    for i in range(num_threads):
        thread = threading.Thread(
            target=spam_worker,
            name=f"T{i+1}",
            args=(username, messages, proxy_list if use_proxy else [""], message_limit, delay, ua_change_interval, proxy_change_interval),
            daemon=True
        )
        thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.LIGHTRED_EX + "\n[INTERRUPT] Arrêt demandé. Fin du script.")


if __name__ == "__main__":
    main()
