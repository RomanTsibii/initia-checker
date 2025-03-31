# initia-checker

Скрипт для перевірки eligibility адрес у Initia Airdrop через API.  
Підтримує роботу через проксі (1 адреса = 1 проксі), виводить дані в табличному форматі.

Приклад виводу
![image](https://github.com/user-attachments/assets/8645b62f-e623-408a-b604-06df203b4baf)

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
```

## ⚙️ Редагування address.txt і proxy.txt 

### Впишіть всі адреси EVM де кожна з нового рядка
 
### Впишіть всі проексі у форматі ip:port:user:password де кожна з нового рядка 

### Всі акаунти будуть перевірятись 1 адреса = 1 ІР, якщо ІР нема - то буде помилка 

## ⚙️ Запуск 
```bash
python3 checker.py
```
