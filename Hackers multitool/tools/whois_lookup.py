import whois
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

def is_valid_domain(domain):
    return re.match(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,6}$", domain) is not None or \
           re.match(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z0-9.-]+$", domain) is not None

def export_results(domain, whois_data):
    filename = f"whois_{domain.replace('.', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for k, v in whois_data.items():
            if v:
                f.write(f"{k}: {v}\n")
    print(colored(f"Results saved to {filename}", "cyan"))

def main():
    print(colored("[Whois Lookup] Enter a domain:", "cyan"))
    domain = input(colored("Domain > ", "red")).strip()
    if not is_valid_domain(domain):
        print(colored("That doesn't look like a valid domain. Try again.", "red"))
        return
    spinner(f"Digging up dirt on {domain}...")
    try:
        w = whois.whois(domain)
        print(colored("\n[Whois Info]", "green", attrs=["bold"]))
        for k, v in w.items():
            if v:
                print(colored(f"{k}: ", "cyan") + colored(str(v), "white"))
        print(colored("\nThat's a lot of info. Use it wisely.", "magenta"))
        if w.get('org') or w.get('registrar'):
            print(colored(f"\nSummary: Registered by {w.get('org') or w.get('registrar', 'unknown')}.", "yellow"))
        save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
        if save == 'y':
            export_results(domain, w)
    except Exception as e:
        print(colored(f"Failed to get whois info: {e}", "red")) 