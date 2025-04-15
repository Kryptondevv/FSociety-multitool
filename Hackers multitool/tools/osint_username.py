import requests
from termcolor import colored
import sys
import time
import re

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

def is_valid_username(username):
    return re.match(r"^[A-Za-z0-9_.-]{3,32}$", username) is not None

def export_results(username, results):
    filename = f"osint_{username}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for site, status in results.items():
            f.write(f"{site}: {status}\n")
    print(colored(f"Results saved to {filename}", "cyan"))

def main():
    print(colored("[OSINT Username Checker] Enter a username:", "cyan"))
    username = input(colored("Username > ", "red")).strip()
    if not is_valid_username(username):
        print(colored("That doesn't look like a valid username. Try again.", "red"))
        return
    sites = {
        "Twitter": f"https://twitter.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "Reddit": f"https://reddit.com/user/{username}",
    }
    spinner(f"Checking for {username} on the interwebs...")
    print(colored("\n[Username Presence]", "green", attrs=["bold"]))
    print(colored("┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓", "cyan"))
    print(colored("┃ Site         ┃ Status                               ┃", "cyan"))
    print(colored("┣━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫", "cyan"))
    results = {}
    for site, url in sites.items():
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                status = "Found"
                color = "green"
            elif resp.status_code == 404:
                status = "Not found"
                color = "red"
            else:
                status = f"HTTP {resp.status_code}"
                color = "yellow"
        except Exception:
            status = "Error"
            color = "red"
        results[site] = status
        print(colored(f"┃ {site.ljust(12)} ┃ {status.ljust(38)} ┃", color))
    print(colored("┗━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛", "cyan"))
    print(colored("OSINT sweep complete. Now go stalk responsibly.", "magenta"))
    save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
    if save == 'y':
        export_results(username, results) 