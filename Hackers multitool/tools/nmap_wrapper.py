import subprocess
from termcolor import colored
import sys
import shutil

def export_results(target, args, output):
    filename = f"nmap_{target.replace('.', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(output)
    print(colored(f"Results saved to {filename}", "cyan"))

def main():
    if not shutil.which('nmap'):
        print(colored("Nmap is not installed or not in PATH!", "red"))
        return
    print(colored("[Nmap Wrapper] Enter a target (IP or domain):", "cyan"))
    target = input(colored("Target > ", "red")).strip()
    print(colored("Enter scan arguments (e.g. -sS, -sV, -A):", "cyan"))
    args = input(colored("Args > ", "red")).strip()
    print(colored(f"Running: nmap {args} {target}", "yellow"))
    try:
        result = subprocess.run(['nmap'] + args.split() + [target], capture_output=True, text=True, timeout=120)
        print(colored("\n[Nmap Output]", "green", attrs=["bold"]))
        print(colored(result.stdout, "yellow"))
        save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
        if save == 'y':
            export_results(target, args, result.stdout)
    except Exception as e:
        print(colored(f"Failed to run nmap: {e}", "red"))

if __name__ == "__main__":
    main() 