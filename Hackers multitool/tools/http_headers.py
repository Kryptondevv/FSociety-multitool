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

def is_valid_url(url):
    return re.match(r"^https?://[\w.-]+", url) is not None

def export_results(url, headers):
    filename = f"headers_{url.replace('://', '_').replace('/', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for k, v in headers.items():
            f.write(f"{k}: {v}\n")
    print(colored(f"Headers saved to {filename}", "cyan"))

def main():
    print(colored("[HTTP Header Fetcher] Enter a URL (with http/https):", "cyan"))
    url = input(colored("URL > ", "red")).strip()
    if not is_valid_url(url):
        print(colored("That doesn't look like a valid URL. Try again.", "red"))
        return
    spinner(f"Fetching headers from {url}...")
    try:
        resp = requests.head(url, timeout=5)
        print(colored("\n[HTTP Headers]", "green", attrs=["bold"]))
        print(colored("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓", "cyan"))
        for k, v in resp.headers.items():
            print(colored(f"┃ {k.ljust(20)} : {v}", "yellow"))
        print(colored("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛", "cyan"))
        print(colored("Headers fetched. Now analyze like a pro.", "magenta"))
        save = input(colored("Export headers to file? (y/n): ", "cyan")).strip().lower()
        if save == 'y':
            export_results(url, resp.headers)
    except Exception as e:
        print(colored(f"Failed to fetch headers: {e}", "red")) 