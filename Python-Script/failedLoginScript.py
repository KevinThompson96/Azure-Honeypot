import csv
import requests
from collections import defaultdict

# === CONFIG ===
API_KEY = "YOUR_API_KEY_HERE"
INPUT_FILE = "Failed_Logins.csv" # change if needed
OUTPUT_FILE = "output.txt"
IP_COLUMN_NAME = "sourcehost"  # change if needed

# === STORAGE ===
country_counts = defaultdict(int)
ip_cache = {}  # avoid duplicate API calls

# === FUNCTION TO GET COUNTRY ===
def get_country(ip):
    if ip in ip_cache:
        return ip_cache[ip]

    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        country = data.get("country_name", "Unknown")
        ip_cache[ip] = country
        return country

    except Exception as e:
        print(f"Error with IP {ip}: {e}")
        return "Unknown"

# === READ CSV ===
with open(INPUT_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        ip = row.get(IP_COLUMN_NAME)

        if not ip:
            continue

        country = get_country(ip)
        country_counts[country] += 1

# === SORT RESULTS ===
sorted_results = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)

# === WRITE OUTPUT ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("Failed Login Attempts by Country\n")
    f.write("--------------------------------\n")

    for country, count in sorted_results:
        f.write(f"{country}: {count}\n")

print(f"Done! Results saved to {OUTPUT_FILE}")