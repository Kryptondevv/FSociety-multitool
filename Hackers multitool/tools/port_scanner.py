import socket
from termcolor import colored
import sys
import time
import importlib

def print_progress(current, total, bar_length=30):
    percent = float(current) / total
    arrow = '█' * int(round(percent * bar_length))
    spaces = '-' * (bar_length - len(arrow))
    sys.stdout.write(f"\rScanning: [{arrow}{spaces}] {int(percent*100)}%")
    sys.stdout.flush()

def get_settings():
    try:
        main = importlib.import_module('fsociety_multitool')
        return getattr(main, 'SETTINGS', {})
    except Exception:
        return {}

def export_results(target, open_ports):
    filename = f"scan_{target.replace('.', '_')}.txt"
    with open(filename, 'w') as f:
        f.write(f"Open ports for {target}:\n")
        for port in open_ports:
            f.write(f"{port}\n")
    print(colored(f"Results saved to {filename}", "cyan"))

def main():
    SETTINGS = get_settings()
    timeout = float(SETTINGS.get('default_timeout', 0.3))
    print(colored("[Port Scanner] Enter your target (IP or domain):", "cyan"))
    target = input(colored("Target > ", "red"))
    print(colored("Enter port range (e.g. 1-1000):", "cyan"))
    port_range = input(colored("Range > ", "red"))
    try:
        start_port, end_port = map(int, port_range.split('-'))
        if not (1 <= start_port <= end_port <= 65535):
            raise ValueError
    except Exception:
        print(colored("Invalid port range. Using default 1-1000.", "yellow"))
        start_port, end_port = 1, 1000
    total_ports = end_port - start_port + 1
    open_ports = []
    print(colored(f"Scanning {target} for open ports ({start_port}-{end_port})...", "yellow"))
    for idx, port in enumerate(range(start_port, end_port+1), 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except Exception:
            pass
        print_progress(idx, total_ports)
    print()  # Newline after progress bar
    if open_ports:
        print(colored(f"\nOpen ports on {target}:", "green", attrs=["bold"]))
        print(colored("┏━━━━━━┓", "cyan"))
        print(colored("┃ Port ┃", "cyan"))
        print(colored("┡━━━━━━┩", "cyan"))
        for port in open_ports:
            print(colored(f"┃ {str(port).ljust(4)} ┃", "green"))
        print(colored("└──────┘", "cyan"))
        print(colored(f"\nDone. {len(open_ports)} open ports found. Time to get creative!", "magenta"))
        save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
        if save == 'y':
            export_results(target, open_ports)
    else:
        print(colored("\nNo open ports found. Either you're unlucky, or they're just that good.", "magenta")) 