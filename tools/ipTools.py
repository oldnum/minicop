import sys
import socket
import ipaddress
import requests
from urllib.parse import urlparse
from time import sleep
from colorama import Fore

def __isCloudFlare(link):
    parsed_uri = urlparse(link)
    domain = "{uri.netloc}".format(uri=parsed_uri)
    try:
        origin = socket.gethostbyname(domain)
        iprange = requests.get("https://www.cloudflare.com/ips-v4").text
        ipv4 = [row.rstrip() for row in iprange.splitlines()]
        for i in range(len(ipv4)):
            if ipaddress.ip_address(origin) in ipaddress.ip_network(ipv4[i]):
                print(
                    f"{Fore.RED}[!] {Fore.CYAN}Este site é protegido pela CloudFlare, este ataque pode não produzir os resultados desejados.{Fore.RESET}"
                )
                sleep(1)
    except socket.gaierror:
        return False

def __GetAddressInfo(target):
    try:
        ip = target.split(":")[0]
        port = int(target.split(":")[1])
    except IndexError:
        print(f"{Fore.RED}[!] {Fore.MAGENTA}Deves inserir um ip e port{Fore.RESET}")
        sys.exit(1)
    else:
        return ip, port

def __GetURLInfo(target):
    if not target.startswith("http"):
        target = f"http://{target}"
    return target


def __GetEmailMessage():
    server, username = ReadSenderEmail()
    subject = input(f"{Fore.BLUE}[?] {Fore.MAGENTA}Enter the Subject (leave blank for random value): ")
    body = input(f"{Fore.BLUE}[?] {Fore.MAGENTA}Enter Your Message (leave blank for random value): ")
    return [server, username, subject, body]

def GetTargetAddress(target, method):
    if method == "HTTP":
        url = __GetURLInfo(target)
        __isCloudFlare(url)
        return url
    else:
        return target


""" Is connected to internet """
def InternetConnectionCheck():
    try:
        requests.get("https://google.com", timeout=2)
    except:
        print(
            f"{Fore.RED}[!] {Fore.MAGENTA}Your device is not connected to the Internet{Fore.RESET}"
        )
        sys.exit(1)
