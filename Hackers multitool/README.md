# FSociety Multitool

> The ultimate, modular, and visually advanced hacker's multitool. Inspired by Mr. Robot, built for real-world use.

![FSociety Banner](https://i.imgur.com/1Q9Z1ZB.png)

## 🚀 Features
- **Port Scanner** — Scan a host for open TCP ports
- **Whois Lookup** — Get domain registration info
- **Hash Cracker** — Crack MD5/SHA1 hashes with a wordlist
- **IP Geolocation** — Find info about an IP address
- **Subdomain Finder** — Find subdomains for a domain
- **Password Generator** — Generate strong random passwords
- **Banner Grabbing** — Grab service banners from open ports
- **DNS Lookup** — Resolve domain names to IPs
- **HTTP Header Fetcher** — Fetch HTTP headers from a URL
- **OSINT Username Checker** — Check username presence on popular sites
- **Reverse IP Lookup** — Find all domains hosted on an IP
- **Shodan Search** — Search Shodan for open devices/services
- **Google Dorker** — Automate Google dork queries for OSINT
- **Email Breach Checker** — Check if an email is in a data breach
- **Hash Identifier** — Identify the type of a given hash
- **Exploit Search** — Search Exploit-DB for public exploits
- **Subdomain Brute Forcer** — Aggressive threaded subdomain enumeration
- **Web Crawler** — Crawl a website and list all found links
- **Directory Fuzzer** — Fuzz a web server for common directories/files
- **Nmap Wrapper** — Run Nmap scans from within the tool

## 🛠️ Installation

### Windows
1. Install [Python 3.7+](https://www.python.org/downloads/)
2. (Optional) Install [Nmap](https://nmap.org/download.html) for Nmap Wrapper tool
3. Download or clone this repo
4. Double-click `start.bat` (or run it in cmd)

### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python fsociety_multitool.py
```
- For Nmap Wrapper: `sudo apt install nmap` (or your distro's package manager)

## ⚡ Usage
- Run the tool and select from the menu
- Use the settings menu (`s`) to set defaults (wordlists, timeouts, debug mode)
- Export results from any tool
- View recent activity/history in the lobby

## 📦 Requirements
- Python 3.7+
- `requests`, `colorama`, `termcolor`, `python-whois`, `ipwhois`
- [Nmap](https://nmap.org/) (for Nmap Wrapper)

## 🧠 Credits & Inspiration
- Inspired by Mr. Robot's FSociety and real-world pentesting tools
- Built with ❤️ by hackers, for hackers

## ⚠️ Disclaimer
This tool is for **educational and authorized testing** only. The author is not responsible for misuse.

---

![fsociety](https://i.imgur.com/1Q9Z1ZB.png) 