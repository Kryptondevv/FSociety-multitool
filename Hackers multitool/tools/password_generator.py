import random
import string
from termcolor import colored
import sys
import time

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

def export_results(password):
    filename = "password.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(password + '\n')
    print(colored(f"Password saved to {filename}", "cyan"))

def main():
    print(colored("[Password Generator] How long do you want your password? (8-64):", "cyan"))
    try:
        length = int(input(colored("Length > ", "red")))
        if not 8 <= length <= 64:
            print(colored("Pick a length between 8 and 64. Don't be weird.", "red"))
            return
    except ValueError:
        print(colored("That's not a number. Try again.", "red"))
        return
    print(colored("Include: [1] Letters [2] Digits [3] Symbols (comma separated, e.g. 1,2,3):", "cyan"))
    sets = input(colored("Sets > ", "red")).replace(' ', '').split(',')
    chars = ''
    if '1' in sets:
        chars += string.ascii_letters
    if '2' in sets:
        chars += string.digits
    if '3' in sets:
        chars += string.punctuation
    if not chars:
        print(colored("You need at least one character set. Try again.", "red"))
        return
    spinner("Generating your password...")
    password = ''.join(random.choice(chars) for _ in range(length))
    print(colored("\n[Your new password]", "green", attrs=["bold"]))
    print(colored(password, "yellow", attrs=["bold"]))
    print(colored("Don't use it for your bank. Or do. I'm not your mom.", "magenta"))
    save = input(colored("Export password to file? (y/n): ", "cyan")).strip().lower()
    if save == 'y':
        export_results(password) 