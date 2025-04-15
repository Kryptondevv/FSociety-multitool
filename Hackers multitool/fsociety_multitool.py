import sys
import time
import random
import traceback
from colorama import init, Fore, Style
from termcolor import colored

init(autoreset=True)

TOOLS = [
    ("Port Scanner", "port_scanner", "Scan a host for open TCP ports."),
    ("Whois Lookup", "whois_lookup", "Get domain registration info."),
    ("Hash Cracker", "hash_cracker", "Crack MD5/SHA1 hashes with a wordlist."),
    ("IP Geolocation", "ip_geolocation", "Find info about an IP address."),
    ("Subdomain Finder", "subdomain_finder", "Find subdomains for a domain (coming soon)."),
    ("Password Generator", "password_generator", "Generate strong random passwords."),
    ("Banner Grabbing", "banner_grabber", "Grab service banners from open ports."),
    ("DNS Lookup", "dns_lookup", "Resolve domain names to IPs."),
    ("HTTP Header Fetcher", "http_headers", "Fetch HTTP headers from a URL."),
    ("OSINT Username Checker", "osint_username", "Check username presence on popular sites."),
    # Advanced tools:
    ("Reverse IP Lookup", "reverse_ip_lookup", "Find all domains hosted on an IP."),
    ("Shodan Search", "shodan_search", "Search Shodan for open devices/services."),
    ("Google Dorker", "google_dorker", "Automate Google dork queries for OSINT."),
    ("Email Breach Checker", "email_breach_checker", "Check if an email is in a data breach."),
    ("Hash Identifier", "hash_identifier", "Identify the type of a given hash."),
    ("Exploit Search", "exploit_search", "Search Exploit-DB for public exploits."),
    ("Subdomain Brute Forcer", "subdomain_bruteforcer", "Aggressive threaded subdomain enumeration."),
    ("Web Crawler", "web_crawler", "Crawl a website and list all found links."),
    ("Directory Fuzzer", "dir_fuzzer", "Fuzz a web server for common directories/files."),
    ("Nmap Wrapper", "nmap_wrapper", "Run Nmap scans from within the tool."),
]

FUN_QUOTES = [
    "Hack the planet!",
    "The quieter you become, the more you are able to hear.",
    "Every lock has a key.",
    "There is no patch for human stupidity.",
    "If you can't hack it, you don't own it.",
    "We are FSociety. We are everyone. We are no one.",
    "The best way to predict the future is to invent it.",
    "You are only as secure as your weakest password.",
    "Welcome to the dark side. We have root access.",
]

BOX_TOP = "┏" + "━"*58 + "┓"
BOX_BOTTOM = "┗" + "━"*58 + "┛"

# Store up to 5 recent activities: (timestamp, tool name, main input)
HISTORY = []
HISTORY_LIMIT = 5

# Settings (in-memory for now)
SETTINGS = {
    "default_wordlist": "",
    "default_timeout": 2.0,
    "debug_mode": "off",
}

SETTINGS_INFO = {
    "default_wordlist": "Default wordlist file for hash/subdomain tools (blank = built-in)",
    "default_timeout": "Default timeout (seconds) for network tools",
    "debug_mode": "Show full error tracebacks (on/off)",
}

def print_history():
    if not HISTORY:
        return
    print(Fore.YELLOW + Style.BRIGHT + "┏━━ Recent Activity ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    for ts, tool, main_input in HISTORY[-HISTORY_LIMIT:][::-1]:
        print(Fore.YELLOW + Style.BRIGHT + f"┃ [{ts}] {tool}: {main_input}")
    print(Fore.YELLOW + Style.BRIGHT + "┗" + "━"*56 + "┛")
    print()

def print_lobby():
    print(Fore.CYAN + Style.BRIGHT + BOX_TOP)
    print(Fore.CYAN + Style.BRIGHT + "┃" + " FSociety Multitool v2.0 - Welcome, Operator!".ljust(58) + "┃")
    print(Fore.CYAN + Style.BRIGHT + "┃" + " "*58 + "┃")
    print(Fore.CYAN + Style.BRIGHT + "┃" + f" {random.choice(FUN_QUOTES)}".ljust(58) + "┃")
    print(Fore.CYAN + Style.BRIGHT + "┃" + " "*58 + "┃")
    print(Fore.CYAN + Style.BRIGHT + BOX_BOTTOM)
    print()
    print_history()
    print(colored("Available Tools:", "yellow", attrs=["bold"]))
    for idx, (name, _, desc) in enumerate(TOOLS, 1):
        print(colored(f" {idx:2d}. {name.ljust(25)} ", "green") + colored(f"- {desc}", "white"))
    print(colored("  0. Exit", "red"))
    print(colored("  h. Help/About", "cyan"))
    print(colored("  s. Settings", "magenta"))
    print()

def print_help():
    print(Fore.MAGENTA + Style.BRIGHT + BOX_TOP)
    print(Fore.MAGENTA + Style.BRIGHT + "┃" + " FSociety Multitool - About & Help".ljust(58) + "┃")
    print(Fore.MAGENTA + Style.BRIGHT + BOX_BOTTOM)
    print(colored("This is your all-in-one hacking multitool. Each tool is modular, ", "magenta"))
    print(colored("and you can add your own in the 'tools' directory. Use wisely!", "magenta"))
    print(colored("Navigate with numbers. Type 'h' for help, 's' for settings, '0' to exit.", "magenta"))
    print(colored("If you break it, you buy it. If you get caught, we don't know you.", "magenta"))
    print()

def print_settings():
    print(Fore.MAGENTA + Style.BRIGHT + BOX_TOP)
    print(Fore.MAGENTA + Style.BRIGHT + "┃" + " FSociety Multitool - Settings".ljust(58) + "┃")
    print(Fore.MAGENTA + Style.BRIGHT + BOX_BOTTOM)
    for k, v in SETTINGS.items():
        print(colored(f"{k}: ", "yellow") + colored(f"{v}", "white") + colored(f"  # {SETTINGS_INFO[k]}", "cyan"))
    print()
    print(colored("Type the setting name to change it, or press Enter to return.", "magenta"))
    choice = input(colored("Setting > ", "magenta")).strip()
    if choice in SETTINGS:
        new_val = input(colored(f"New value for {choice} (current: {SETTINGS[choice]}): ", "magenta")).strip()
        if choice == "default_timeout":
            try:
                SETTINGS[choice] = float(new_val)
            except Exception:
                print(colored("Invalid value. Timeout must be a number.", "red"))
        elif choice == "debug_mode":
            if new_val.lower() in ["on", "off"]:
                SETTINGS[choice] = new_val.lower()
            else:
                print(colored("Invalid value. Use 'on' or 'off' only.", "red"))
        else:
            SETTINGS[choice] = new_val
        print(colored(f"{choice} updated!", "green"))
        time.sleep(1)

def run_tool(tool_module, tool_name):
    # Ask for main input for history (if possible)
    main_input = ""
    try:
        if tool_module in ["port_scanner", "whois_lookup", "ip_geolocation", "subdomain_finder", "dns_lookup", "http_headers", "osint_username"]:
            prompt = {
                "port_scanner": "Target host/IP",
                "whois_lookup": "Domain",
                "ip_geolocation": "IP address",
                "subdomain_finder": "Domain",
                "dns_lookup": "Domain",
                "http_headers": "URL",
                "osint_username": "Username"
            }[tool_module]
            main_input = input(colored(f"[History] {prompt}: ", "cyan")).strip()
        elif tool_module == "hash_cracker":
            main_input = input(colored("[History] Hash: ", "cyan")).strip()
        elif tool_module == "password_generator":
            main_input = input(colored("[History] Password length: ", "cyan")).strip()
        elif tool_module == "banner_grabber":
            main_input = input(colored("[History] Host:Port (e.g. 127.0.0.1:80): ", "cyan")).strip()
    except Exception:
        main_input = "(input error)"
    # Record history
    HISTORY.append((time.strftime("%H:%M:%S"), tool_name, main_input))
    if len(HISTORY) > HISTORY_LIMIT:
        HISTORY.pop(0)
    # Actually run the tool
    try:
        mod = __import__(f"tools.{tool_module}", fromlist=["main"])
        mod.main()
    except Exception as e:
        if SETTINGS.get("debug_mode", "off") == "on":
            print(colored(f"Error running {tool_module}:\n", "red"))
            traceback.print_exc()
        else:
            print(colored(f"Error running {tool_module}: {e}", "red"))

def main():
    while True:
        print_lobby()
        choice = input(colored("FSociety > ", "red", attrs=["bold"]))
        if choice == "0":
            print(colored("Exiting. Stay paranoid.", "magenta"))
            sys.exit(0)
        elif choice.lower() == "h":
            print_help()
            input(colored("Press Enter to return to the lobby...", "cyan"))
        elif choice.lower() == "s":
            print_settings()
        elif choice.isdigit() and 1 <= int(choice) <= len(TOOLS):
            tool_name, tool_module, _ = TOOLS[int(choice)-1]
            run_tool(tool_module, tool_name)
            input(colored("\nPress Enter to return to the lobby...", "cyan"))
        else:
            print(colored("Invalid choice. Try again, 1337 h4x0r.", "red"))
            time.sleep(1)

if __name__ == "__main__":
    main() 