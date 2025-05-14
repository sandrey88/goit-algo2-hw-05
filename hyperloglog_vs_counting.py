import time
from hyperloglog import HyperLogLog
import re

LOG_FILE = "lms-stage-access.log"
IP_REGEX = re.compile(r"(\d{1,3}\.){3}\d{1,3}")

import json

def load_ips_from_log(filename):
    """Завантаження IP-адрес з JSON-лог-файлу, ігноруючи некоректні рядки."""
    ips = []
    with open(filename, encoding="utf-8", errors="ignore") as f:
        for line in f:
            try:
                data = json.loads(line)
                ip = data.get("remote_addr")
                if ip:
                    ips.append(ip)
                    for ip_x in xff.split(','):
                        ip_x = ip_x.strip()
                        if ip_x:
                            ips.append(ip_x)
            except Exception:
                continue  # ігнорувати некоректні рядки
    return ips

def exact_count(ips):
    """Точний підрахунок унікальних IP через set."""
    start = time.time()
    unique = set(ips)
    duration = time.time() - start
    return len(unique), duration

def hll_count(ips, p=14):
    """Підрахунок унікальних IP через HyperLogLog."""
    hll = HyperLogLog(p=p)
    start = time.time()
    for ip in ips:
        hll.add(ip)
    count = hll.count()
    duration = time.time() - start
    return count, duration

def print_table(exact, hll):
    print("Результати порівняння:")
    print(f"{'':25s}{'Точний підрахунок':>20s}{'HyperLogLog':>15s}")
    print(f"{'Унікальні елементи':25s}{exact[0]:>20.1f}{hll[0]:>15.1f}")
    print(f"{'Час виконання (сек.)':25s}{exact[1]:>20.2f}{hll[1]:>15.2f}")

if __name__ == "__main__":
    ips = load_ips_from_log(LOG_FILE)
    print(f"Завантажено {len(ips)} IP-адрес.")
    exact = exact_count(ips)
    hll = hll_count(ips)

    print_table(exact, hll)
