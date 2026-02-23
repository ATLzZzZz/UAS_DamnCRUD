# DOKUMENTASI CI/CD PIPELINE

## Automation Testing DamnCRUD dengan GitHub Actions & Pytest Parallel

**Tanggal:** 23 Februari 2026  
**Framework:** Pytest + Selenium WebDriver  
**CI/CD:** GitHub Actions  
**Parallel Execution:** pytest-xdist

---

## RINGKASAN PIPELINE

Pipeline CI/CD ini akan secara otomatis menjalankan 5 test case setiap kali ada:

- Push ke branch `main` atau `master`
- Pull Request ke branch `main` atau `master`
- Manual trigger dari GitHub Actions

---

## ARSITEKTUR CI/CD

```
┌─────────────────────────────────────────────────────────────────┐
│                    GITHUB ACTIONS WORKFLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   TRIGGER    │───▶│    SETUP     │───▶│    TEST      │       │
│  │  (Push/PR)   │    │  (Services)  │    │  (Parallel)  │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                              │                   │                │
│                              ▼                   ▼                │
│                      ┌──────────────┐    ┌──────────────┐       │
│                      │    MySQL     │    │   Pytest     │       │
│                      │   Service    │    │   -n auto    │       │
│                      └──────────────┘    └──────────────┘       │
│                              │                   │                │
│                              ▼                   ▼                │
│                      ┌──────────────┐    ┌──────────────┐       │
│                      │  PHP Server  │    │   Reports    │       │
│                      │  (Built-in)  │    │   (HTML/XML) │       │
│                      └──────────────┘    └──────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## STRUKTUR FILE

```
DamnCRUD/
├── .github/
│   └── workflows/
│       └── test.yml              # GitHub Actions workflow
├── automation/
│   ├── test_pytest.py            # Test cases dengan Pytest
│   ├── conftest.py               # Shared fixtures & hooks
│   ├── pytest.ini                # Pytest configuration
│   ├── requirements.txt          # Python dependencies
│   └── DOKUMENTASI_CI_CD.md      # Dokumentasi ini
├── db/
│   └── damncrud.sql              # Database schema
└── *.php                         # Aplikasi PHP
```

---

## WORKFLOW DETAIL

### File: `.github/workflows/test.yml`

```yaml
name: DamnCRUD Automation Test

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
  workflow_dispatch: # Manual trigger

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: badcrud
        ports:
          - 3306:3306

    steps:
      - Checkout repository
      - Setup PHP 8.1
      - Setup Python 3.11
      - Install dependencies
      - Setup Chrome & ChromeDriver
      - Import database
      - Start PHP server
      - Run Pytest in Parallel (-n auto)
      - Upload test reports
```

---

## 5 TEST CASES YANG DIJALANKAN

| No  | Test Case ID | Test Name                                     | Marker                 |
| --- | ------------ | --------------------------------------------- | ---------------------- |
| 1   | TC-013       | `test_TC013_create_contact_valid_data`        | `@pytest.mark.create`  |
| 2   | TC-018       | `test_TC018_update_contact_valid_data`        | `@pytest.mark.update`  |
| 3   | TC-024       | `test_TC024_delete_contact_with_confirmation` | `@pytest.mark.delete`  |
| 4   | TC-010       | `test_TC010_search_datatables`                | `@pytest.mark.search`  |
| 5   | TC-028       | `test_TC028_view_profile_page`                | `@pytest.mark.profile` |

---

## PARALLEL EXECUTION

### Menggunakan pytest-xdist

```bash
# Auto detect CPU cores dan jalankan parallel
pytest test_pytest.py -n auto -v

# Spesifik 4 workers
pytest test_pytest.py -n 4 -v

# Dengan HTML report
pytest test_pytest.py -n auto --html=report.html -v
```

### Bagaimana Parallel Execution Bekerja:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PYTEST-XDIST PARALLEL                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Master Process                                                  │
│       │                                                          │
│       ├──▶ Worker 1 ──▶ test_TC013_create_contact               │
│       │                                                          │
│       ├──▶ Worker 2 ──▶ test_TC018_update_contact               │
│       │                                                          │
│       ├──▶ Worker 3 ──▶ test_TC024_delete_contact               │
│       │                                                          │
│       ├──▶ Worker 4 ──▶ test_TC010_search_datatables            │
│       │                                                          │
│       └──▶ Worker 5 ──▶ test_TC028_view_profile_page            │
│                                                                  │
│  Setiap worker mendapat browser instance sendiri                │
│  Test dijalankan secara simultan                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## CARA SETUP DI GITHUB

### 1. Push Repository ke GitHub

```bash
cd DamnCRUD
git init
git add .
git commit -m "Initial commit dengan automation testing"
git remote add origin https://github.com/username/DamnCRUD.git
git push -u origin main
```

### 2. Workflow Akan Otomatis Berjalan

Setelah push, GitHub Actions akan:

1. Mendeteksi file `.github/workflows/test.yml`
2. Membuat virtual machine Ubuntu
3. Setup services (MySQL, PHP, Python, Chrome)
4. Menjalankan test secara parallel
5. Generate dan upload reports

### 3. Melihat Hasil di GitHub

1. Buka repository di GitHub
2. Klik tab **Actions**
3. Pilih workflow run yang ingin dilihat
4. Download artifacts (test reports)

---

## MENJALANKAN LOKAL

### 1. Setup Environment

```bash
# Install dependencies
cd DamnCRUD/automation
pip install -r requirements.txt

# Pastikan Chrome terinstall
google-chrome --version
```

### 2. Jalankan Test Parallel

```bash
# Jalankan semua test parallel
pytest test_pytest.py -n auto -v

# Jalankan dengan report
pytest test_pytest.py -n auto --html=report.html --self-contained-html -v

# Jalankan test spesifik
pytest test_pytest.py -m create -v      # Hanya test create
pytest test_pytest.py -m "create or update" -v  # Create dan update
```

### 3. Output yang Diharapkan

```
========================= test session starts =========================
platform linux -- Python 3.11.0, pytest-7.4.0, pluggy-1.3.0
plugins: xdist-3.5.0, html-4.1.1, metadata-3.0.0
4 workers [5 items]

test_pytest.py::TestDamnCRUD::test_TC013_create_contact_valid_data
test_pytest.py::TestDamnCRUD::test_TC018_update_contact_valid_data
test_pytest.py::TestDamnCRUD::test_TC010_search_datatables
test_pytest.py::TestDamnCRUD::test_TC024_delete_contact_with_confirmation
test_pytest.py::TestDamnCRUD::test_TC028_view_profile_page

[gw0] PASSED test_TC013_create_contact_valid_data
[gw1] PASSED test_TC018_update_contact_valid_data
[gw2] PASSED test_TC010_search_datatables
[gw3] PASSED test_TC024_delete_contact_with_confirmation
[gw0] PASSED test_TC028_view_profile_page

========================= 5 passed in 15.23s =========================
```

---

## REPORTS & ARTIFACTS

### HTML Report

- File: `report.html`
- Berisi detail setiap test case
- Screenshot jika test gagal
- Metadata execution

### JUnit XML Report

- File: `test-results.xml`
- Format standar CI/CD
- Digunakan untuk integrasi dengan tools lain
- Ditampilkan di GitHub Actions

---

## TROUBLESHOOTING

### 1. Test Gagal Karena Browser

```bash
# Install Chrome headless dependencies (Linux)
sudo apt-get install -y chromium-browser chromium-chromedriver
```

### 2. Database Connection Error

```bash
# Pastikan MySQL service berjalan
# Cek konfigurasi di functions.php
```

### 3. Port Already in Use

```bash
# Cek port yang digunakan
netstat -tuln | grep 81

# Kill proses jika perlu
kill -9 $(lsof -t -i:81)
```

### 4. Timeout pada CI/CD

```python
# Tambahkan timeout di pytest.ini
timeout = 180  # 3 menit per test
```

---

## BEST PRACTICES

1. **Unique Test Data**: Gunakan timestamp untuk data unik agar test bisa dijalankan parallel tanpa konflik

2. **Independent Tests**: Setiap test harus bisa berjalan sendiri tanpa bergantung pada test lain

3. **Proper Cleanup**: Logout setelah setiap test untuk memastikan state bersih

4. **Headless Mode**: Gunakan headless mode untuk CI/CD agar lebih cepat

5. **Screenshot on Failure**: Simpan screenshot saat test gagal untuk debugging

---

## REFERENSI

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-xdist Documentation](https://pytest-xdist.readthedocs.io/)
- [Selenium Python Documentation](https://selenium-python.readthedocs.io/)
