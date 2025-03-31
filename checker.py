import requests
import time
import random
import warnings
import json
from itertools import zip_longest

warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

ADDRESS_FILE = 'address.txt'
PROXY_FILE = 'proxy.txt'
OUTPUT_FILE = 'eligible.txt'
URL_TEMPLATE = 'https://airdrop-api.initia.xyz/info/initia/{}'

HEADERS = {
    'User-Agent': 'curl/8.5.0',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Referer': 'https://airdrop.initia.xyz/',
    'Accept-Language': 'en-US,en;q=0.9'
}

def load_addresses(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def load_proxies(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def format_proxy(proxy_line):
    ip, port, user, password = proxy_line.split(':')
    return {
        'http': f'http://{user}:{password}@{ip}:{port}',
        'https': f'http://{user}:{password}@{ip}:{port}'
    }

def check_address(address, proxy):
    try:
        url = URL_TEMPLATE.format(address.lower())
        time.sleep(random.uniform(0.6, 1.2))
        response = requests.get(url, headers=HEADERS, proxies=proxy, timeout=10, verify=False)

        if response.status_code == 200:
            try:
                data = response.json()
            except json.JSONDecodeError:
                return {'address': address, 'error': "Invalid JSON"}

            return {
                'address': address,
                'amount': data.get('amount', 'N/A'),
                'xp_rank': data.get('xp_rank', 'N/A'),
                'jennie_level': data.get('jennie_level', 'N/A'),
                'frame_level': data.get('frame_level', 'N/A'),
                'filet_mignon': data.get('filet_mignon', 'N/A'),
                'status': '✅ ELIGIBLE'
            }
        elif response.status_code == 403:
            return {'address': address, 'status': '❌ Not eligible'}
        else:
            return {'address': address, 'status': f"❌ Error {response.status_code}"}
    except Exception as e:
        return {'address': address, 'status': f"❌ {str(e)}"}

def main():
    addresses = load_addresses(ADDRESS_FILE)
    raw_proxies = load_proxies(PROXY_FILE)
    proxies = [format_proxy(p) for p in raw_proxies]
    proxy_texts = [p.split(':')[0] for p in raw_proxies]  # лише IP
    address_proxy_pairs = list(zip_longest(addresses, proxies, proxy_texts))

    eligible_results = []
    amount_list = []

    print(f"{'#':<4} | {'Address':<42} | {'Proxy':<21} | {'Amount':>10} | {'XP Rank':>8} | {'Jennie':>6} | {'Frame':>5} | {'Filet':>5} | {'Status':<15}")
    print("-" * 128)

    for idx, (address, proxy, proxy_str) in enumerate(address_proxy_pairs, start=1):
        if not address:
            continue

        result = check_address(address, proxy)
        status = result.get('status', '❌ Unknown')

        amount_raw = result.get('amount', 'N/A')
        amount_value = round(int(amount_raw) / 1_000_000, 2) if amount_raw != 'N/A' else 0
        amount_list.append(amount_value)
        amount_formatted = f"{amount_value:>10.2f}".replace('.', ',')

        print(f"{idx:<4} | {address:<42} | {proxy_str:<21} | {amount_formatted} | "
              f"{result.get('xp_rank','N/A'):>8} | {result.get('jennie_level','N/A'):>6} | "
              f"{result.get('frame_level','N/A'):>5} | {result.get('filet_mignon','N/A'):>5} | {status:<15}")

        if status.startswith("✅"):
            eligible_results.append({
                'address': address,
                'amount': amount_raw
            })

    print("-" * 128)
    print(f"✅ Eligible: {len(eligible_results)} / {len(addresses)}")

    # Додатковий вивід списку Amount
    print("\nВивід токенів для кожного акаунта:")
    for amt in amount_list:
        print(str(amt).replace('.', ','))

    print(f"\nСума всіх токенів: {str(round(sum(amount_list), 2)).replace('.', ',')}")

    # Запис eligible у файл
    if eligible_results:
        with open(OUTPUT_FILE, 'w') as f:
            for entry in eligible_results:
                f.write(entry['address'] + '\n')

if __name__ == "__main__":
    main()
