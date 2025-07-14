# Meet urlscanner: A Better Way to Use urlscan.io from Your Terminal
## The Problem

While diving into a bug bounty hunting session, I found myself needing quick insights from urlscan.io. The platform is powerful, but let’s be honest; it’s not the most automation-friendly tool out there for terminal-first hunters like us.

I quickly hit two major roadblocks:

    The API only accepted one URL per request, making batch analysis a headache.

    The API response was bloated with excessive details I didn’t care about.

So I thought:

    “Why not write a script that trims the fat and brings only what I need, fast and clean all from the terminal?”

## Introducing: urlscanner.py

A lightweight Python script designed for bug bounty hunters, OSINT investigators, and developers who want to enumerate subdomains or directory structure data from urlscan.io without the noise.
### Features:
- Accepts a file of domains, processes them all in one go
- Supports two focused modes: subdomains and directories
- Clean output with minimal overhead
- Easy to automate and integrate with other tools

## Installation

**Clone the repo:**

`git clone https://github.com/mohammadibnibrahim/urlscanner`

**Make it global so you can run it from anywhere:**

`cd urlscanner; sudo mv urlscanner.py /usr/local/bin/urlscanner.py`

## Usage

`python3 urlscanner.py -m <subdomains|directories> -d domains.txt -o output.txt`

### Arguments:

    -m / --mode – Choose between subdomains or directories

    -d / --domains – A file containing the domains you want to scan

    -o / --output_file – (Optional) Where to save the results. Default: urlscanner_output.txt

# Why This Exists
- Because using the web interface and the API aren't scalable for hunters.
- This tool helps you stay in the terminal, automate your scans, and get just the data that matters.

# Follow me on social media

[Linkedin](https://www.linkedin.com/in/mohammadibnibrahim)
[Twitter](https://x.com/mhmdibnibrahim)
[Medium](https://mohammadibnibrahim.medium.com/)

$H4ppy H4ck1ng!$

