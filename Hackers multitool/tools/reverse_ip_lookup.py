import requests
from termcolor import colored
import sys
import time

def export_results(ip, domains):
    filename = f"reverseip_{ip.replace('.', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for d in domains:
            f.write(f"{d}\n")
    print(colored(f"Results saved to {filename}", "cyan"))

def main():
    print(colored("[Reverse IP Lookup] Enter an IP address:", "cyan"))
    ip = input(colored("IP > ", "red")).strip()
    print(colored(f"Looking up domains hosted on {ip}...", "yellow"))
    try:
        url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200 and resp.text.strip():
            domains = resp.text.strip().split('\n')
            print(colored("\n[Domains Found]", "green", attrs=["bold"]))
            for d in domains:
                print(colored(f"- {d}", "yellow"))
            print(colored(f"\nFound {len(domains)} domains.", "magenta"))
            save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
            if save == 'y':
                export_results(ip, domains)
        else:
            print(colored("No domains found or API limit reached.", "magenta"))
    except Exception as e:
        print(colored(f"Failed to perform reverse IP lookup: {e}", "red"))

if __name__ == "__main__":
    main() 