import socket
from termcolor import colored
import sys
import time
import re
import importlib

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

def is_valid_host(host):
    # Accepts IP or domain
    return re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", host) or re.match(r"^[a-zA-Z0-9.-]+$", host)

def export_results(host, port, banner):
    filename = f"banner_{host.replace('.', '_')}_{port}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(banner + '\n')
    print(colored(f"Banner saved to {filename}", "cyan"))

def get_settings():
    try:
        main = importlib.import_module('fsociety_multitool')
        return getattr(main, 'SETTINGS', {})
    except Exception:
        return {}

def main():
    SETTINGS = get_settings()
    timeout = float(SETTINGS.get('default_timeout', 2.0))
    print(colored("[Banner Grabber] Enter host:", "cyan"))
    host = input(colored("Host > ", "red")).strip()
    if not is_valid_host(host):
        print(colored("That doesn't look like a valid host. Try again.", "red"))
        return
    print(colored("Enter port:", "cyan"))
    try:
        port = int(input(colored("Port > ", "red")))
        if not (1 <= port <= 65535):
            raise ValueError
    except ValueError:
        print(colored("That's not a valid port. Try again.", "red"))
        return
    spinner(f"Grabbing banner from {host}:{port}...")
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((host, port))
        banner = sock.recv(1024).decode(errors='ignore')
        print(colored("\n[Banner]", "green", attrs=["bold"]))
        print(colored(banner, "yellow"))
        print(colored("Banner grabbed. Now do something cool with it.", "magenta"))
        sock.close()
        save = input(colored("Export banner to file? (y/n): ", "cyan")).strip().lower()
        if save == 'y':
            export_results(host, port, banner)
    except Exception as e:
        print(colored(f"Failed to grab banner: {e}", "red")) 