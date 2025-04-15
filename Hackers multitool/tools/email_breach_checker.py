import requests
from termcolor import colored
import sys
import time

def export_results(email, breaches):
    filename = f"breach_{email.replace('@', '_at_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for b in breaches:
            f.write(f"{b}\n")
    print(colored(f"Results saved to {filename}", "cyan"))

def main():
    print(colored("[Email Breach Checker] Enter an email address:", "cyan"))
    email = input(colored("Email > ", "red")).strip()
    print(colored("Checking haveibeenpwned.com for breaches... (rate limits apply)", "yellow"))
    print(colored("Note: For privacy, use your own API key for heavy use.", "magenta"))
    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {"User-Agent": "FSociety-Multitool", "hibp-api-key": ""}  # User can add their own key here
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            breaches = [b['Name'] for b in resp.json()]
            print(colored(f"\n[Breaches Found]", "green", attrs=["bold"]))
            for b in breaches:
                print(colored(f"- {b}", "yellow"))
            print(colored(f"\nFound in {len(breaches)} breaches.", "magenta"))
            save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
            if save == 'y':
                export_results(email, breaches)
        elif resp.status_code == 404:
            print(colored("No breaches found for this email!", "green"))
        else:
            print(colored(f"API error or rate limit reached: {resp.status_code}", "magenta"))
    except Exception as e:
        print(colored(f"Failed to check breaches: {e}", "red")) 