import hashlib
from termcolor import colored
import sys
import os
import importlib

def print_progress(current, total, bar_length=30):
    percent = float(current) / total if total else 1
    arrow = '█' * int(round(percent * bar_length))
    spaces = '-' * (bar_length - len(arrow))
    sys.stdout.write(f"\rCracking: [{arrow}{spaces}] {int(percent*100)}%")
    sys.stdout.flush()

def get_settings():
    try:
        main = importlib.import_module('fsociety_multitool')
        return getattr(main, 'SETTINGS', {})
    except Exception:
        return {}

def main():
    SETTINGS = get_settings()
    print(colored("[Hash Cracker] Enter the hash:", "cyan"))
    hash_input = input(colored("Hash > ", "red"))
    print(colored("Type (md5/sha1):", "cyan"))
    hash_type = input(colored("Type > ", "red")).lower()
    print(colored("Wordlist file (leave blank for default):", "cyan"))
    wordlist_path = input(colored("Wordlist > ", "red"))
    if not wordlist_path.strip() and SETTINGS.get('default_wordlist'):
        wordlist_path = SETTINGS['default_wordlist']
    if wordlist_path.strip():
        if not os.path.isfile(wordlist_path):
            print(colored("File not found. Using built-in wordlist.", "yellow"))
            wordlist = ["password", "123456", "letmein", "fsociety", "qwerty", "admin", "welcome"]
        else:
            with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
                wordlist = [line.strip() for line in f if line.strip()]
    else:
        wordlist = ["password", "123456", "letmein", "fsociety", "qwerty", "admin", "welcome"]
    print(colored(f"Cracking... ({len(wordlist)} words)", "yellow"))
    found = False
    cracked_word = None
    for idx, word in enumerate(wordlist, 1):
        if hash_type == "md5":
            hashed = hashlib.md5(word.encode()).hexdigest()
        elif hash_type == "sha1":
            hashed = hashlib.sha1(word.encode()).hexdigest()
        else:
            print(colored("Unsupported hash type. Only md5 and sha1 for now.", "red"))
            return
        print_progress(idx, len(wordlist))
        if hashed == hash_input:
            print("\n" + colored(f"Hash cracked!", "green", attrs=["bold"]))
            print(colored(f"{hash_type.upper()}('{word}') = {hash_input}", "green"))
            found = True
            cracked_word = word
            break
    if not found:
        print("\n" + colored("No luck. Try a bigger wordlist or rainbow tables. Or just get creative.", "magenta"))
    save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
    if save == 'y':
        export_results(hash_input, hash_type, cracked_word, found)

def export_results(hash_input, hash_type, word, found):
    filename = f"crack_{hash_type}_{hash_input[:8]}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        if found:
            f.write(f"Hash: {hash_input}\nType: {hash_type}\nCracked: {word}\n")
        else:
            f.write(f"Hash: {hash_input}\nType: {hash_type}\nResult: Not cracked\n")
    print(colored(f"Results saved to {filename}", "cyan")) 