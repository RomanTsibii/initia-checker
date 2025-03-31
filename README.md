# initia-checker

Скрипт для перевірки eligibility адрес у Initia Airdrop через API.  
Підтримує роботу через проксі (1 адреса = 1 проксі), виводить дані в табличному форматі.

---

## 📦 Залежності

- Python 3.7+
- `requests`

---

## ⚙️ Встановлення

```bash
# Клонувати репозиторій
git clone https://github.com/RomanTsibii/initia-checker.git
cd initia-checker

# Створити та активувати віртуальне середовище
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Встановити залежності
pip install requests
