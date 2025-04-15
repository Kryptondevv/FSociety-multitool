from ipwhois import IPWhois
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

def is_valid_ip(ip):
    return re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip) is not None

def export_results(ip, geo_data):
    filename = f"geo_{ip.replace('.', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for k in ["network", "asn", "asn_description", "asn_country_code", "asn_registry", "entities"]:
            if k in geo_data and geo_data[k]:
                f.write(f"{k}: {geo_data[k]}\n")
    print(colored(f"Results saved to {filename}", "cyan"))

def main():
    print(colored("[IP Geolocation] Enter an IP address:", "cyan"))
    ip = input(colored("IP > ", "red")).strip()
    if not is_valid_ip(ip):
        print(colored("That doesn't look like a valid IPv4 address. Try again.", "red"))
        return
    spinner(f"Tracking {ip}... (not creepy at all)")
    try:
        obj = IPWhois(ip)
        res = obj.lookup_rdap()
        print(colored("\n[IP Geolocation Info]", "green", attrs=["bold"]))
        for k in ["network", "asn", "asn_description", "asn_country_code", "asn_registry", "entities"]:
            if k in res and res[k]:
                print(colored(f"{k}: ", "cyan") + colored(str(res[k]), "white"))
        print(colored("\nNow you know where they live. Sort of.", "magenta"))
        if res.get('asn_country_code'):
            print(colored(f"\nSummary: ASN country code is {res['asn_country_code']}.", "yellow"))
        save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
        if save == 'y':
            export_results(ip, res)
    except Exception as e:
        print(colored(f"Failed to get geolocation info: {e}", "red")) 