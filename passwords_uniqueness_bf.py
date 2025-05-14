import hashlib
from typing import List, Dict, Any

class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item: str):
        for i in range(self.num_hashes):
            hash_digest = hashlib.sha256((str(i) + item).encode('utf-8')).hexdigest()
            yield int(hash_digest, 16) % self.size

    def add(self, item: str):
        if not isinstance(item, str) or not item:
            return
        for idx in self._hashes(item):
            self.bit_array[idx] = 1

    def contains(self, item: str) -> bool:
        if not isinstance(item, str) or not item:
            return False
        return all(self.bit_array[idx] for idx in self._hashes(item))


def check_password_uniqueness(bf: BloomFilter, passwords: List[Any]) -> Dict[Any, str]:
    results = {}
    for pw in passwords:
        if not isinstance(pw, str) or not pw:
            results[pw] = "некоректний пароль"
            continue
        if bf.contains(pw):
            results[pw] = "вже використаний"
        else:
            results[pw] = "унікальний"
            bf.add(pw)
    return results

if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
