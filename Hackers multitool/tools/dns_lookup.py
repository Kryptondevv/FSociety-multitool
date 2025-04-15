import socket
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

def export_results(domain, ip_list):
    filename = f"dns_{domain.replace('.', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"A records for {domain}:\n")
        for ip in ip_list:
            f.write(f"{ip}\n")
    print(colored(f"Results saved to {filename}", "cyan"))

def main():
    print(colored("[DNS Lookup] Enter a domain:", "cyan"))
    domain = input(colored("Domain > ", "red")).strip()
    if not is_valid_domain(domain):
        print(colored("That doesn't look like a valid domain. Try again.", "red"))
        return
    spinner(f"Looking up {domain}...")
    try:
        result = socket.gethostbyname_ex(domain)
        print(colored(f"\nA records for {domain}:", "green", attrs=["bold"]))
        for ip in result[2]:
            print(colored(f" - {ip}", "yellow"))
        print(colored("DNS magic complete. Use it for good (or evil).", "magenta"))
        save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
        if save == 'y':
            export_results(domain, result[2])
    except Exception as e:
        print(colored(f"Failed to resolve domain: {e}", "red")) 