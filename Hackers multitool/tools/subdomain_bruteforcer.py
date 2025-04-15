import socket
from termcolor import colored
import threading
import queue
import sys
import os

def export_results(domain, found):
    filename = f"subbrute_{domain.replace('.', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for sub in found:
            f.write(f"{sub}\n")
    print(colored(f"Results saved to {filename}", "cyan"))

def worker(domain, q, found):
    while not q.empty():
        sub = q.get()
        subdomain = f"{sub}.{domain}"
        try:
            socket.gethostbyname(subdomain)
            found.append(subdomain)
            print(colored(f"[+] {subdomain}", "yellow"))
        except Exception:
            pass
        q.task_done()

def main():
    print(colored("[Subdomain Brute Forcer] Enter a domain:", "cyan"))
    domain = input(colored("Domain > ", "red")).strip()
    print(colored("Wordlist file (leave blank for built-in):", "cyan"))
    wordlist_path = input(colored("Wordlist > ", "red")).strip()
    if wordlist_path and os.path.isfile(wordlist_path):
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            wordlist = [line.strip() for line in f if line.strip()]
    else:
        wordlist = ["www", "mail", "ftp", "test", "dev", "api", "blog", "shop", "admin", "vpn", "staging", "beta", "portal", "m", "secure", "cpanel", "webmail", "ns1", "ns2"]
    q = queue.Queue()
    for sub in wordlist:
        q.put(sub)
    found = []
    threads = []
    print(colored(f"Bruteforcing {len(wordlist)} subdomains...", "yellow"))
    for _ in range(20):
        t = threading.Thread(target=worker, args=(domain, q, found))
        t.daemon = True
        t.start()
        threads.append(t)
    q.join()
    print(colored(f"\n[Discovered Subdomains]", "green", attrs=["bold"]))
    for sub in found:
        print(colored(f"- {sub}", "yellow"))
    print(colored(f"\nFound {len(found)} subdomains.", "magenta"))
    save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
    if save == 'y' and found:
        export_results(domain, found)

if __name__ == "__main__":
    main() 