import socket
from termcolor import colored
import sys
import time
import re
import importlib
import os

def spinner(msg):
    spinner_chars = '|/-\\'
    sys.stdout.write(colored(msg + ' ', 'yellow'))
    for _ in range(10):
        for c in spinner_chars:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.05)
            sys.stdout.write('\b')
    sys.stdout.write(' ')
    sys.stdout.flush()

def is_valid_domain(domain):
    return re.match(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,6}$", domain) is not None or \
           re.match(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z0-9.-]+$", domain) is not None

def get_settings():
    try:
        main = importlib.import_module('fsociety_multitool')
        return getattr(main, 'SETTINGS', {})
    except Exception:
        return {}

def export_results(domain, found):
    filename = f"subdomains_{domain.replace('.', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for sub in found:
            f.write(f"{sub}\n")
    print(colored(f"Results saved to {filename}", "cyan"))

def main():
    SETTINGS = get_settings()
    print(colored("[Subdomain Finder] Enter a domain:", "cyan"))
    domain = input(colored("Domain > ", "red")).strip()
    if not is_valid_domain(domain):
        print(colored("That doesn't look like a valid domain. Try again.", "red"))
        return
    print(colored("Wordlist file (leave blank for default):", "cyan"))
    wordlist_path = input(colored("Wordlist > ", "red")).strip()
    if not wordlist_path and SETTINGS.get('default_wordlist'):
        wordlist_path = SETTINGS['default_wordlist']
    if wordlist_path:
        if not os.path.isfile(wordlist_path):
            print(colored("File not found. Using built-in wordlist.", "yellow"))
            wordlist = ["www", "mail", "ftp", "test", "dev", "api", "blog", "shop", "admin", "vpn"]
        else:
            with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
                wordlist = [line.strip() for line in f if line.strip()]
    else:
        wordlist = ["www", "mail", "ftp", "test", "dev", "api", "blog", "shop", "admin", "vpn"]
    found = []
    spinner(f"Checking subdomains for {domain}...")
    print(colored("\n[Discovered Subdomains]", "green", attrs=["bold"]))
    print(colored("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓", "cyan"))
    for sub in wordlist:
        subdomain = f"{sub}.{domain}"
        try:
            socket.gethostbyname(subdomain)
            found.append(subdomain)
            print(colored(f"┃ {subdomain.ljust(36)} ┃", "yellow"))
        except Exception:
            pass
    print(colored("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛", "cyan"))
    if found:
        print(colored(f"\nFound {len(found)} subdomains. Time to dig deeper!", "magenta"))
    else:
        print(colored("No subdomains found with this tiny wordlist. Try a bigger one!", "magenta"))
    save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
    if save == 'y' and found:
        export_results(domain, found)

if __name__ == "__main__":
    main() 