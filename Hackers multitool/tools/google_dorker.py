import requests
from termcolor import colored
import sys
import time

def export_results(query, results):
    filename = f"dork_{query.replace(' ', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for r in results:
            f.write(f"{r}\n")
    print(colored(f"Results saved to {filename}", "cyan"))

def main():
    print(colored("[Google Dorker] Enter your Google dork query:", "cyan"))
    query = input(colored("Dork > ", "red")).strip()
    print(colored("Enter your SerpAPI key (get one at serpapi.com, free tier available):", "cyan"))
    api_key = input(colored("SerpAPI Key > ", "red")).strip()
    print(colored(f"Searching Google for '{query}'...", "yellow"))
    try:
        url = f"https://serpapi.com/search.json?q={query}&engine=google&api_key={api_key}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        results = []
        if 'organic_results' in data:
            for r in data['organic_results']:
                results.append(r.get('link', ''))
            print(colored(f"\n[Google Dork Results] Showing up to 10 results:", "green", attrs=["bold"]))
            for r in results[:10]:
                print(colored(f"- {r}", "yellow"))
            save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
            if save == 'y':
                export_results(query, results[:10])
        else:
            print(colored("No results found or API limit reached.", "magenta"))
    except Exception as e:
        print(colored(f"Failed to dork Google: {e}", "red"))

if __name__ == "__main__":
    main() 