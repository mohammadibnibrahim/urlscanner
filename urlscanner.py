#!/usr/local/python3.13/bin/python3.13

# Importing required libraries
import requests
import argparse
import re

# Parsing arguments
parser = argparse.ArgumentParser(description="Automating usage of urlscanner.io")
parser.add_argument('-m', '--mode', type=str, help="Specify the mode. (subdomains|directories)")
parser.add_argument('-d', '--domains', type=str, help="Specify the file that contains the domains you want to enumerate.")
parser.add_argument('-o', '--output_file', type=str, help='Specify the file to append the results to. Default: urlscanner_output.txt', default='urlscanner_output.txt')
args = parser.parse_args()

# Usage check
if args.mode == None or args.domains == None:
    print("Usage: python3 urlscanner.py -m <subdomains|directories> -o <domains_file>")
    exit()

# Banner
def print_banner():
    print(r'''
      ___           ___           ___       ___           ___           ___           ___           ___           ___           ___     
     /\__\         /\  \         /\__\     /\  \         /\  \         /\  \         /\__\         /\__\         /\  \         /\  \    
    /:/  /        /::\  \       /:/  /    /::\  \       /::\  \       /::\  \       /::|  |       /::|  |       /::\  \       /::\  \   
   /:/  /        /:/\:\  \     /:/  /    /:/\ \  \     /:/\:\  \     /:/\:\  \     /:|:|  |      /:|:|  |      /:/\:\  \     /:/\:\  \  
  /:/  /  ___   /::\~\:\  \   /:/  /    _\:\~\ \  \   /:/  \:\  \   /::\~\:\  \   /:/|:|  |__   /:/|:|  |__   /::\~\:\  \   /::\~\:\  \ 
 /:/__/  /\__\ /:/\:\ \:\__\ /:/__/    /\ \:\ \ \__\ /:/__/ \:\__\ /:/\:\ \:\__\ /:/ |:| /\__\ /:/ |:| /\__\ /:/\:\ \:\__\ /:/\:\ \:\__\
 \:\  \ /:/  / \/_|::\/:/  / \:\  \    \:\ \:\ \/__/ \:\  \  \/__/ \/__\:\/:/  / \/__|:|/:/  / \/__|:|/:/  / \:\~\:\ \/__/ \/_|::\/:/  /
  \:\  /:/  /     |:|::/  /   \:\  \    \:\ \:\__\    \:\  \            \::/  /      |:/:/  /      |:/:/  /   \:\ \:\__\      |:|::/  / 
   \:\/:/  /      |:|\/__/     \:\  \    \:\/:/  /     \:\  \           /:/  /       |::/  /       |::/  /     \:\ \/__/      |:|\/__/  
    \::/  /       |:|  |        \:\__\    \::/  /       \:\__\         /:/  /        /:/  /        /:/  /       \:\__\        |:|  |    
     \/__/         \|__|         \/__/     \/__/         \/__/         \/__/         \/__/         \/__/         \/__/         \|__|    
                                                                                                    
                                                                                                    Created by: Mohammad Ibn Ibrahim
    ''')

# Functions for better performance and elminiating false-positives
# Remove comments
def sanitize_domain(domain):
    return domain.strip().lower() if domain.strip() and not domain.strip().startswith("#") else None

# Handle errors
def safe_request(url, headers):
    try:
        return requests.get(url, headers=headers)
    except requests.RequestException:
        return None

# Remove duplicates
def dedup_and_sort(items):
    return sorted(set(items))

# Initialize constants
MODE=args.mode
DOMAINS_FILE=args.domains
API_KEY="" # Change this to your own API Key

if len(API_KEY) == 0:
	print("You must supply your own API Key in the code in the line 57.")
	exit()

OUTPUT_FILE=args.output_file

# Check the mode
if MODE != "subdomains" and MODE != "directories":
    print(f"Invalid mode: {MODE}. Use 'subdomains' or 'directories'.")
    exit()

print_banner()

with open(DOMAINS_FILE) as file:
    for line in file:
        domain = sanitize_domain(line)
        if not domain:
            continue
        print(f"Processing {domain}")

        url = f"https://urlscan.io/api/v1/search/?q=page.domain:{domain}&size=100"
        header = {"API-Key": f"{API_KEY}"}
        response = safe_request(url, headers=header)
        if not response:
            continue

        if MODE == "subdomains":
            matched = re.findall(rf"https?://((?:[a-zA-Z0-9_-]+\.)+{re.escape(domain)})", response.text)
            stripped = [re.sub(r"^https?://", "", url) for url in matched]
            filtered = [url for url in stripped if url != domain]
            cleaned = [url.split("/")[0] for url in filtered]
            unique = dedup_and_sort(cleaned)

            with open(OUTPUT_FILE, "a") as f:
                for sub in unique:
                    f.write(sub + "\n")
                print(f"[Finished and the results are saved at {OUTPUT_FILE}]")

        elif MODE == "directories":
            matched = re.findall(rf"https?://(?:[a-zA-Z0-9_-]+\.)+{re.escape(domain)}/[^\s\"'>]+", response.text)
            unique = dedup_and_sort(matched)

            with open(OUTPUT_FILE, "a") as f:
                for url in unique:
                    f.write(url + "\n")
                print(f"[Finished and the results are saved at {OUTPUT_FILE}]")
