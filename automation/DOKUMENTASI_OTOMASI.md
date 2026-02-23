# DOKUMENTASI LANGKAH-LANGKAH OTOMASI

## Functional Testing - DamnCRUD Application

**Tanggal:** 23 Februari 2026  
**Framework:** Python + Selenium WebDriver  
**Browser:** Google Chrome

---

## DAFTAR TEST CASE YANG DIAUTOMASI

| No  | Test Case ID | Test Case Objective                 |
| --- | ------------ | ----------------------------------- |
| 1   | TC-013       | Create Contact dengan data valid    |
| 2   | TC-018       | Update Contact dengan data valid    |
| 3   | TC-024       | Delete Contact dengan konfirmasi OK |
| 4   | TC-010       | Search DataTables                   |
| 5   | TC-028       | View Profile Page                   |

---

## PRASYARAT (PREREQUISITES)

### 1. Software yang Dibutuhkan

- Python 3.8 atau lebih baru
- Google Chrome Browser (versi terbaru)
- ChromeDriver (sesuai versi Chrome)
- XAMPP dengan Apache & MySQL running

### 2. Instalasi Dependencies

```bash
cd DamnCRUD/automation
pip install -r requirements.txt
```

### 3. Konfigurasi

- Pastikan aplikasi DamnCRUD berjalan di `http://localhost:81/DamnCRUD`
- Sesuaikan `BASE_URL` di script jika port berbeda
- Import database `damncrud.sql` ke MySQL

---

## LANGKAH-LANGKAH OTOMASI DETAIL

---

### TEST CASE 1: TC-013 - CREATE CONTACT DENGAN DATA VALID

**Objective:** Verifikasi penambahan kontak baru dengan data valid

**Pre-condition:** User sudah login ke sistem

#### Langkah-langkah Otomasi:

| Step | Action              | Locator/Method                                                         | Input/Data             | Expected                  |
| ---- | ------------------- | ---------------------------------------------------------------------- | ---------------------- | ------------------------- |
| 1    | Buka halaman Create | `find_element(By.LINK_TEXT, "Create")` lalu `click()`                  | -                      | URL berubah ke create.php |
| 2    | Verifikasi halaman  | `wait.until(EC.url_contains("create.php"))`                            | -                      | Halaman create terbuka    |
| 3    | Input Name          | `find_element(By.ID, "name")` lalu `send_keys()`                       | "Automation Test User" | Field terisi              |
| 4    | Input Email         | `find_element(By.ID, "email")` lalu `send_keys()`                      | "autotest@example.com" | Field terisi              |
| 5    | Input Phone         | `find_element(By.ID, "phone")` lalu `send_keys()`                      | "081234567890"         | Field terisi              |
| 6    | Input Title         | `find_element(By.ID, "title")` lalu `send_keys()`                      | "QA Engineer"          | Field terisi              |
| 7    | Klik Save           | `find_element(By.CSS_SELECTOR, "input[type='submit']")` lalu `click()` | -                      | Form tersubmit            |
| 8    | Verifikasi redirect | `wait.until(EC.url_contains("index.php"))`                             | -                      | Redirect ke dashboard     |
| 9    | Verifikasi data     | `assertIn(test_data["name"], page_source)`                             | -                      | Data muncul di tabel      |

**Kode Selenium:**

```python
# Input data kontak
name_field = driver.find_element(By.ID, "name")
name_field.send_keys("Automation Test User")

email_field = driver.find_element(By.ID, "email")
email_field.send_keys("autotest@example.com")

phone_field = driver.find_element(By.ID, "phone")
phone_field.send_keys("081234567890")

title_field = driver.find_element(By.ID, "title")
title_field.send_keys("QA Engineer")

# Submit
save_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
save_button.click()
```

---

### TEST CASE 2: TC-018 - UPDATE CONTACT DENGAN DATA VALID

**Objective:** Verifikasi update kontak dengan data valid

**Pre-condition:** User sudah login, ada data kontak di database

#### Langkah-langkah Otomasi:

| Step | Action               | Locator/Method                                                         | Input/Data             | Expected                |
| ---- | -------------------- | ---------------------------------------------------------------------- | ---------------------- | ----------------------- |
| 1    | Buka dashboard       | `driver.get(BASE_URL + "/index.php")`                                  | -                      | Dashboard terbuka       |
| 2    | Verifikasi tabel     | `wait.until(EC.presence_of_element_located((By.ID, "employee")))`      | -                      | Tabel terload           |
| 3    | Klik Edit            | `find_elements(By.LINK_TEXT, "edit")[0]` lalu `click()`                | -                      | Halaman update terbuka  |
| 4    | Verifikasi URL       | `wait.until(EC.url_contains("update.php"))`                            | -                      | URL berisi update.php   |
| 5    | Clear & Update Name  | `find_element(By.ID, "name")` lalu `clear()` dan `send_keys()`         | "Updated Contact Name" | Field terupdate         |
| 6    | Clear & Update Email | `find_element(By.ID, "email")` lalu `clear()` dan `send_keys()`        | "updated@example.com"  | Field terupdate         |
| 7    | Klik Update          | `find_element(By.CSS_SELECTOR, "input[type='submit']")` lalu `click()` | -                      | Form tersubmit          |
| 8    | Verifikasi redirect  | `wait.until(EC.url_contains("index.php"))`                             | -                      | Redirect ke dashboard   |
| 9    | Verifikasi perubahan | `assertIn(update_data["name"], page_source)`                           | -                      | Data terupdate di tabel |

**Kode Selenium:**

```python
# Klik tombol edit pertama
edit_buttons = driver.find_elements(By.LINK_TEXT, "edit")
edit_buttons[0].click()

# Update data
name_field = driver.find_element(By.ID, "name")
name_field.clear()
name_field.send_keys("Updated Contact Name")

email_field = driver.find_element(By.ID, "email")
email_field.clear()
email_field.send_keys("updated@example.com")

# Submit
update_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
update_button.click()
```

---

### TEST CASE 3: TC-024 - DELETE CONTACT DENGAN KONFIRMASI OK

**Objective:** Verifikasi hapus kontak dengan konfirmasi OK

**Pre-condition:** User sudah login, ada data kontak di database

#### Langkah-langkah Otomasi:

| Step | Action            | Locator/Method                                                                    | Input/Data | Expected                       |
| ---- | ----------------- | --------------------------------------------------------------------------------- | ---------- | ------------------------------ |
| 1    | Buka dashboard    | `driver.get(BASE_URL + "/index.php")`                                             | -          | Dashboard terbuka              |
| 2    | Hitung kontak     | `len(find_elements(By.LINK_TEXT, "delete"))`                                      | -          | Mendapat jumlah kontak         |
| 3    | Ambil nama kontak | `find_element(By.CSS_SELECTOR, "#employee tbody tr:first-child td:nth-child(2)")` | -          | Mendapat nama kontak           |
| 4    | Klik Delete       | `find_element(By.LINK_TEXT, "delete")` lalu `click()`                             | -          | Alert muncul                   |
| 5    | Tunggu Alert      | `wait.until(EC.alert_is_present())`                                               | -          | Alert terdeteksi               |
| 6    | Accept Alert      | `alert.accept()`                                                                  | -          | Alert ditutup, delete diproses |
| 7    | Refresh page      | `driver.get(BASE_URL + "/index.php")`                                             | -          | Halaman refresh                |
| 8    | Hitung ulang      | `len(find_elements(By.LINK_TEXT, "delete"))`                                      | -          | Jumlah berkurang 1             |
| 9    | Verifikasi        | `assertEqual(count_after, count_before - 1)`                                      | -          | Kontak terhapus                |

**Kode Selenium:**

```python
# Hitung kontak sebelum delete
delete_buttons_before = driver.find_elements(By.LINK_TEXT, "delete")
count_before = len(delete_buttons_before)

# Klik delete pada kontak pertama
first_row = driver.find_element(By.CSS_SELECTOR, "#employee tbody tr:first-child")
delete_button = first_row.find_element(By.LINK_TEXT, "delete")
delete_button.click()

# Handle alert konfirmasi
alert = wait.until(EC.alert_is_present())
alert.accept()

# Verifikasi delete berhasil
driver.get(BASE_URL + "/index.php")
delete_buttons_after = driver.find_elements(By.LINK_TEXT, "delete")
count_after = len(delete_buttons_after)
assert count_after == count_before - 1
```

---

### TEST CASE 4: TC-010 - SEARCH DATATABLES

**Objective:** Verifikasi fitur search DataTables berfungsi

**Pre-condition:** User sudah login, ada data kontak di database

#### Langkah-langkah Otomasi:

| Step | Action           | Locator/Method                                              | Input/Data | Expected                     |
| ---- | ---------------- | ----------------------------------------------------------- | ---------- | ---------------------------- |
| 1    | Buka dashboard   | `driver.get(BASE_URL + "/index.php")`                       | -          | Dashboard terbuka            |
| 2    | Hitung data awal | `len(find_elements(By.CSS_SELECTOR, "#employee tbody tr"))` | -          | Mendapat total data          |
| 3    | Cari search box  | `find_element(By.CSS_SELECTOR, "#employee_filter input")`   | -          | Search box ditemukan         |
| 4    | Input keyword    | `send_keys("John")`                                         | "John"     | Keyword diinput              |
| 5    | Tunggu filter    | `time.sleep(1)`                                             | -          | DataTables memfilter         |
| 6    | Ambil hasil      | `find_elements(By.CSS_SELECTOR, "#employee tbody tr")`      | -          | Data terfilter               |
| 7    | Verifikasi hasil | Loop setiap row, `assertIn("john", row_text.lower())`       | -          | Semua row mengandung keyword |
| 8    | Clear search     | `search_box.clear()`                                        | -          | Search box kosong            |
| 9    | Verifikasi reset | Hitung ulang data                                           | -          | Semua data muncul kembali    |

**Kode Selenium:**

```python
# Cari search box DataTables
search_box = driver.find_element(By.CSS_SELECTOR, "#employee_filter input")
search_box.send_keys("John")
time.sleep(1)

# Verifikasi hasil filter
rows = driver.find_elements(By.CSS_SELECTOR, "#employee tbody tr")
for row in rows:
    assert "john" in row.text.lower()

# Clear search
search_box.clear()
```

---

### TEST CASE 5: TC-028 - VIEW PROFILE PAGE

**Objective:** Verifikasi tampilan halaman profil

**Pre-condition:** User sudah login

#### Langkah-langkah Otomasi:

| Step | Action                   | Locator/Method                                                  | Input/Data | Expected                    |
| ---- | ------------------------ | --------------------------------------------------------------- | ---------- | --------------------------- |
| 1    | Klik menu Profile        | `find_element(By.LINK_TEXT, "Profile")` lalu `click()`          | -          | Navigasi ke profil          |
| 2    | Verifikasi URL           | `wait.until(EC.url_contains("profil.php"))`                     | -          | URL berisi profil.php       |
| 3    | Verifikasi judul         | `find_element(By.TAG_NAME, "h2")`                               | -          | Text = "Profil"             |
| 4    | Verifikasi username      | `find_element(By.ID, "username")` lalu `get_attribute("value")` | -          | Value = username yang login |
| 5    | Verifikasi foto          | `find_element(By.CSS_SELECTOR, "img[src*='profile']")`          | -          | Gambar terlihat             |
| 6    | Verifikasi upload form   | `find_element(By.CSS_SELECTOR, "input[type='file']")`           | -          | Input file ada              |
| 7    | Verifikasi tombol Change | `find_element(By.CSS_SELECTOR, "button[type='submit']")`        | -          | Tombol terlihat             |
| 8    | Verifikasi Dashboard btn | `find_element(By.LINK_TEXT, "Dashboard")`                       | -          | Link ada                    |
| 9    | Verifikasi Sign out btn  | `find_element(By.LINK_TEXT, "Sign out")`                        | -          | Link ada                    |

**Kode Selenium:**

```python
# Navigasi ke Profile
profile_link = driver.find_element(By.LINK_TEXT, "Profile")
profile_link.click()

# Verifikasi elemen
page_title = driver.find_element(By.TAG_NAME, "h2")
assert page_title.text == "Profil"

username_field = driver.find_element(By.ID, "username")
assert username_field.get_attribute("value") == "admin"

profile_image = driver.find_element(By.CSS_SELECTOR, "img[src*='profile']")
assert profile_image.is_displayed()

upload_form = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
assert upload_form.is_displayed()
```

---

## CARA MENJALANKAN TEST

### 1. Persiapan

```bash
# Masuk ke folder automation
cd DamnCRUD/automation

# Install dependencies
pip install -r requirements.txt
```

### 2. Jalankan Semua Test

```bash
python test_damncrud.py
```

### 3. Jalankan Test Spesifik

```bash
# Jalankan test create saja
python -m pytest test_damncrud.py::DamnCRUDTest::test_TC013_create_contact_valid_data -v

# Jalankan test update saja
python -m pytest test_damncrud.py::DamnCRUDTest::test_TC018_update_contact_valid_data -v
```

### 4. Generate Report HTML

```bash
python -m pytest test_damncrud.py --html=report.html
```

---

## STRUKTUR LOCATOR YANG DIGUNAKAN

| Elemen                 | Locator Type    | Locator Value            |
| ---------------------- | --------------- | ------------------------ |
| Username field (login) | By.ID           | `inputUsername`          |
| Password field (login) | By.ID           | `inputPassword`          |
| Login button           | By.CSS_SELECTOR | `button[type='submit']`  |
| Name field             | By.ID           | `name`                   |
| Email field            | By.ID           | `email`                  |
| Phone field            | By.ID           | `phone`                  |
| Title field            | By.ID           | `title`                  |
| Save/Update button     | By.CSS_SELECTOR | `input[type='submit']`   |
| Edit link              | By.LINK_TEXT    | `edit`                   |
| Delete link            | By.LINK_TEXT    | `delete`                 |
| DataTables search      | By.CSS_SELECTOR | `#employee_filter input` |
| Table rows             | By.CSS_SELECTOR | `#employee tbody tr`     |
| Profile link           | By.LINK_TEXT    | `Profile`                |
| Profile image          | By.CSS_SELECTOR | `img[src*='profile']`    |

---

## CATATAN PENTING

1. **Urutan Eksekusi:** Test dijalankan secara alfabetis. Jika ada ketergantungan, gunakan naming yang tepat.

2. **Data Test:** Setiap test menggunakan data yang berbeda untuk menghindari konflik.

3. **Cleanup:** Method `tearDown()` melakukan logout setelah setiap test untuk memastikan state yang bersih.

4. **Wait Strategy:** Menggunakan kombinasi implicit wait dan explicit wait untuk stabilitas.

5. **Alert Handling:** Test delete menggunakan `EC.alert_is_present()` untuk menangani JavaScript confirm dialog.
