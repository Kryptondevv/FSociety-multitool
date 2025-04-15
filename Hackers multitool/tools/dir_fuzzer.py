import requests
from termcolor import colored
import sys
import os

def export_results(url, found):
    filename = f"dirfuzz_{url.replace('://', '_').replace('/', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for d in found:
            f.write(f"{d}\n")
    print(colored(f"Results saved to {filename}", "cyan"))

def main():
    print(colored("[Directory Fuzzer] Enter a base URL (with http/https):", "cyan"))
    url = input(colored("URL > ", "red")).strip().rstrip('/')
    print(colored("Wordlist file (leave blank for built-in):", "cyan"))
    wordlist_path = input(colored("Wordlist > ", "red")).strip()
    if wordlist_path and os.path.isfile(wordlist_path):
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            wordlist = [line.strip() for line in f if line.strip()]
    else:
        wordlist = ["admin", "login", "dashboard", "test", "backup", "old", "dev", "uploads", "images", "js", "css", "api", "config", ".git", ".env", "phpinfo.php", "robots.txt"]
    found = []
    print(colored(f"Fuzzing {len(wordlist)} paths on {url}...", "yellow"))
    for w in wordlist:
        target = f"{url}/{w}"
        try:
            resp = requests.get(target, timeout=5)
            if resp.status_code < 400:
                found.append(target)
                print(colored(f"[+] {target} ({resp.status_code})", "yellow"))
        except Exception:
            pass
    print(colored(f"\n[Discovered Paths]", "green", attrs=["bold"]))
    for d in found:
        print(colored(f"- {d}", "yellow"))
    print(colored(f"\nFound {len(found)} valid paths.", "magenta"))
    save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
    if save == 'y' and found:
        export_results(url, found)

if __name__ == "__main__":
    main() 