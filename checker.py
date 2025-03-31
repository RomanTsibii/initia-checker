import requests
import json
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import zip_longest

warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

ADDRESS_FILE = 'address.txt'
PROXY_FILE = 'proxy.txt'
OUTPUT_FILE = 'eligible.txt'
URL_TEMPLATE = 'https://airdrop-api.initia.xyz/info/initia/{}'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
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

def check_address(address, proxy, proxy_str):
    try:
        url = URL_TEMPLATE.format(address.lower())
        response = requests.get(url, headers=HEADERS, proxies=proxy, timeout=10, verify=False)

        if response.status_code == 200:
            try:
                data = response.json()
            except json.JSONDecodeError:
                return None

            amount_raw = data.get('amount', 'N/A')
            amount_value = round(int(amount_raw) / 1_000_000, 2) if amount_raw != 'N/A' else 0
            result_line = (f"{address:<42} | {proxy_str:<21} | {amount_value:>10.2f} | "
                           f"{data.get('xp_rank','N/A'):>8} | {data.get('jennie_level','N/A'):>6} | "
                           f"{data.get('frame_level','N/A'):>5} | {data.get('filet_mignon','N/A'):>5} | ✅ ELIGIBLE")

            # Сохраняем сразу
            with open(OUTPUT_FILE, 'a') as f:
                f.write(address + '\n')

            return result_line

        elif response.status_code == 403:
            return f"{address:<42} | {proxy_str:<21} | {'-':>10} | {'-':>8} | {'-':>6} | {'-':>5} | {'-':>5} | ❌ Not eligible"
        else:
            return f"{address:<42} | {proxy_str:<21} | {'-':>10} | {'-':>8} | {'-':>6} | {'-':>5} | {'-':>5} | ❌ Error {response.status_code}"

    except Exception as e:
        return f"{address:<42} | {proxy_str:<21} | {'-':>10} | {'-':>8} | {'-':>6} | {'-':>5} | {'-':>5} | ❌ {str(e)}"

def main():
    addresses = load_addresses(ADDRESS_FILE)
    raw_proxies = load_proxies(PROXY_FILE)
    proxies = [format_proxy(p) for p in raw_proxies]
    proxy_texts = [p.split(':')[0] for p in raw_proxies]
    address_proxy_pairs = list(zip_longest(addresses, proxies, proxy_texts))

    print(f"{'#':<4} | {'Address':<42} | {'Proxy':<21} | {'Amount':>10} | {'XP Rank':>8} | {'Jennie':>6} | {'Frame':>5} | {'Filet':>5} | {'Status':<15}")
    print("-" * 128)

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_data = {
            executor.submit(check_address, addr, prox, prox_str): (i, addr)
            for i, (addr, prox, prox_str) in enumerate(address_proxy_pairs, 1) if addr
        }

        for future in as_completed(future_to_data):
            idx, addr = future_to_data[future]
            try:
                result_line = future.result()
                if result_line:
                    print(f"{idx:<4} | {result_line}")
            except Exception as exc:
                print(f"{idx:<4} | {addr:<42} | ERROR: {exc}")

if __name__ == "__main__":
    main()
