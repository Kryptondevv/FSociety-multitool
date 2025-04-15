import requests
from termcolor import colored
import sys
import time

def export_results(query, results):
    filename = f"shodan_{query.replace(' ', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for r in results:
            f.write(f"IP: {r['ip_str']} | Port: {r.get('port', 'N/A')} | Org: {r.get('org', 'N/A')}\n")
    print(colored(f"Results saved to {filename}", "cyan"))

def main():
    print(colored("[Shodan Search] Enter your Shodan API key:", "cyan"))
    api_key = input(colored("API Key > ", "red")).strip()
    print(colored("Enter your Shodan search query (e.g. apache, port:22):", "cyan"))
    query = input(colored("Query > ", "red")).strip()
    print(colored(f"Searching Shodan for '{query}'...", "yellow"))
    try:
        url = f"https://api.shodan.io/shodan/host/search?key={api_key}&query={query}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        if 'matches' in data and data['matches']:
            print(colored(f"\n[Shodan Results] Showing up to 10 results:", "green", attrs=["bold"]))
            results = data['matches'][:10]
            for r in results:
                print(colored(f"IP: {r['ip_str']} | Port: {r.get('port', 'N/A')} | Org: {r.get('org', 'N/A')}", "yellow"))
            save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
            if save == 'y':
                export_results(query, results)
        else:
            print(colored("No results found or API limit reached.", "magenta"))
    except Exception as e:
        print(colored(f"Failed to search Shodan: {e}", "red"))

if __name__ == "__main__":
    main() 