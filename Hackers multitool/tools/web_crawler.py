import requests
from termcolor import colored
import re
import sys
from urllib.parse import urljoin, urlparse

def export_results(url, links):
    filename = f"crawl_{urlparse(url).netloc.replace('.', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for l in links:
            f.write(f"{l}\n")
    print(colored(f"Results saved to {filename}", "cyan"))

def extract_links(url, html):
    return set(re.findall(r'href=["\"](.*?)["\"]', html, re.IGNORECASE))

def main():
    print(colored("[Web Crawler] Enter a URL (with http/https):", "cyan"))
    url = input(colored("URL > ", "red")).strip()
    print(colored(f"Crawling {url} (1 level deep)...", "yellow"))
    try:
        resp = requests.get(url, timeout=10)
        base = urlparse(url).scheme + '://' + urlparse(url).netloc
        links = set()
        for link in extract_links(url, resp.text):
            if link.startswith('http'):
                links.add(link)
            elif link.startswith('/'):
                links.add(urljoin(base, link))
        print(colored(f"\n[Links Found]", "green", attrs=["bold"]))
        for l in links:
            print(colored(f"- {l}", "yellow"))
        print(colored(f"\nFound {len(links)} links.", "magenta"))
        save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
        if save == 'y' and links:
            export_results(url, links)
    except Exception as e:
        print(colored(f"Failed to crawl site: {e}", "red")) 