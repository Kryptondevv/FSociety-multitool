from termcolor import colored
import re

def export_results(hash_input, types):
    filename = f"hashid_{hash_input[:8]}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for t in types:
            f.write(f"{t}\n")
    print(colored(f"Results saved to {filename}", "cyan"))

def identify_hash(hash_input):
    hash_types = []
    l = len(hash_input)
    if re.fullmatch(r"[a-fA-F0-9]{32}", hash_input):
        hash_types.append("MD5")
    if re.fullmatch(r"[a-fA-F0-9]{40}", hash_input):
        hash_types.append("SHA1")
    if re.fullmatch(r"[a-fA-F0-9]{64}", hash_input):
        hash_types.append("SHA256")
    if re.fullmatch(r"[a-fA-F0-9]{128}", hash_input):
        hash_types.append("SHA512")
    if re.fullmatch(r"[a-fA-F0-9]{16}", hash_input):
        hash_types.append("MySQL3")
    if re.fullmatch(r"\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}", hash_input):
        hash_types.append("bcrypt")
    if not hash_types:
        hash_types.append("Unknown or custom hash type")
    return hash_types

def main():
    print(colored("[Hash Identifier] Enter the hash:", "cyan"))
    hash_input = input(colored("Hash > ", "red")).strip()
    types = identify_hash(hash_input)
    print(colored("\n[Possible Hash Types]", "green", attrs=["bold"]))
    for t in types:
        print(colored(f"- {t}", "yellow"))
    save = input(colored("Export results to file? (y/n): ", "cyan")).strip().lower()
    if save == 'y':
        export_results(hash_input, types) 