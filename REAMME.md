# Windows Prefetch Parser 🕵️‍♂️

![Python](https://img.shields.io/badge/python-3.14.2-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🇬🇧 English / 🇷🇺 Русский

### Description / Описание

**EN:**  
A lightweight Python tool for parsing Windows **Prefetch (.pf) files** and extracting execution artifacts for **digital forensics** and **system analysis**.

The parser automatically decompresses modern Prefetch files, extracts key metadata, and stores the results in a structured **SQLite database** for further investigation.

**RU:**  
Лёгкий инструмент на Python для анализа **Prefetch файлов Windows (.pf)** и извлечения артефактов запуска программ для **цифровой криминалистики** и анализа системы.

Парсер автоматически распаковывает современные Prefetch-файлы, извлекает ключевые метаданные и сохраняет результаты в **базу данных SQLite** для дальнейшего анализа.

---

### Features / Возможности

**EN:**
- 🔍 Parses Windows Prefetch files (`.pf`)
- 🗜 Supports compressed Prefetch formats (Windows 10+)
- ⏱ Extracts **last run timestamps** and execution history
- 💾 Saves results directly to **SQLite database**
- 📂 Collects accessed **files and directories**
- 💿 Extracts **volume serial number and creation time**
- 🧪 Designed for **digital forensics research and education**

**RU:**
- 🔍 Анализирует Prefetch файлы (`.pf`)
- 🗜 Поддерживает сжатые Prefetch (Windows 10+)
- ⏱ Извлекает **время последних запусков**
- 💾 Сохраняет результаты в **SQLite**
- 📂 Собирает **использованные файлы и директории**
- 💿 Извлекает **серийный номер тома и время его создания**
- 🧪 Подходит для **исследований и обучения цифровой криминалистике**

---

### Extracted Artifacts / Извлекаемые артефакты

**EN:**
- Executable name
- Prefetch file name
- File size
- Run count
- Last run timestamps
- Volume serial number
- Volume creation time
- Referenced files
- Referenced directories

**RU:**
- имя исполняемого файла
- имя Prefetch файла
- размер файла
- количество запусков
- время последних запусков
- серийный номер тома
- время создания тома
- использованные файлы
- использованные директории

---

### Use Cases / Применение

**EN:**

- Digital forensics investigations

- Malware execution analysis

- Windows artifact research

- Academic and lab environments

**RU:**

- Расследования цифровой криминалистики

- Анализ запуска вредоносного ПО

- Исследование артефактов Windows

- Учебные и лабораторные работы

---

### Usage / Использование

**EN/RU:**
```bash
# Clone the repository
git clone https://github.com/polovnikovAI/Python-Prefetch-Parser.git
cd Python-Prefetch-Parser

# Run the parser
python prefetch_parser.py <path_to_pf_folder>

# Example:
python prefetch_parser.py C:\Windows\Prefetch
