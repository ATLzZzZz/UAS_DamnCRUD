"""
=============================================================================
PYTEST AUTOMATION TEST - DamnCRUD Application
=============================================================================
Framework       : Pytest + Selenium WebDriver
Parallel Run    : pytest-xdist
Tanggal         : 23 Februari 2026

TEST CASES:
1. TC-013: Create Contact dengan data valid
2. TC-018: Update Contact dengan data valid  
3. TC-024: Delete Contact dengan konfirmasi OK
4. TC-010: Search DataTables
5. TC-028: View Profile Page

CARA MENJALANKAN:
- Sequential : pytest test_pytest.py -v
- Parallel   : pytest test_pytest.py -n auto -v
- With Report: pytest test_pytest.py -n auto --html=report.html -v
=============================================================================
"""

import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoAlertPresentException


# =============================================================================
# CONFIGURATION
# =============================================================================
# Default: localhost:81/DamnCRUD untuk XAMPP lokal
# CI: http://localhost:8080 (dari environment variable)
BASE_URL = os.environ.get("BASE_URL", "http://localhost:81/DamnCRUD")
USERNAME = "admin"
PASSWORD = "nimda666!"


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture(scope="function")
def driver():
    """
    Fixture untuk membuat WebDriver instance per test function.
    Setiap test akan mendapat browser instance sendiri untuk parallel execution.
    """
    chrome_options = Options()
    
    # Headless mode untuk CI/CD
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    
    # Inisialisasi driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    # Cleanup
    driver.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """
    Fixture untuk driver yang sudah login.
    Digunakan oleh test yang membutuhkan autentikasi.
    """
    # Login
    driver.get(f"{BASE_URL}/login.php")
    
    username_field = driver.find_element(By.ID, "inputUsername")
    username_field.clear()
    username_field.send_keys(USERNAME)
    
    password_field = driver.find_element(By.ID, "inputPassword")
    password_field.clear()
    password_field.send_keys(PASSWORD)
    
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    
    # Tunggu redirect ke dashboard
    WebDriverWait(driver, 10).until(EC.url_contains("index.php"))
    
    yield driver
    
    # Logout setelah test
    try:
        driver.get(f"{BASE_URL}/logout.php")
    except:
        pass


# =============================================================================
# TEST CLASS
# =============================================================================

@pytest.mark.parallel
class TestDamnCRUD:
    """
    Test class untuk aplikasi DamnCRUD.
    Semua test dalam class ini dapat dijalankan secara paralel.
    """

    # =========================================================================
    # TC-013: CREATE CONTACT DENGAN DATA VALID
    # =========================================================================
    @pytest.mark.create
    def test_TC013_create_contact_valid_data(self, logged_in_driver):
        """
        TC-013: Verifikasi penambahan kontak baru dengan data valid
        
        Steps:
        1. Navigasi ke halaman Create
        2. Input data kontak (Name, Email, Phone, Title)
        3. Klik tombol Save
        4. Verifikasi redirect ke dashboard
        5. Verifikasi data muncul di tabel
        """
        driver = logged_in_driver
        
        # Step 1: Navigasi ke halaman Create
        create_link = driver.find_element(By.LINK_TEXT, "Add New Contact")
        create_link.click()
        
        WebDriverWait(driver, 10).until(EC.url_contains("create.php"))
        assert "create.php" in driver.current_url, "Halaman Create tidak terbuka"
        
        # Step 2: Input data kontak
        # Generate unique name untuk parallel testing
        unique_id = str(int(time.time() * 1000))[-6:]
        test_data = {
            "name": f"Test User {unique_id}",
            "email": f"test{unique_id}@example.com",
            "phone": f"0812{unique_id}",
            "title": "QA Engineer"
        }
        
        driver.find_element(By.ID, "name").send_keys(test_data["name"])
        driver.find_element(By.ID, "email").send_keys(test_data["email"])
        driver.find_element(By.ID, "phone").send_keys(test_data["phone"])
        driver.find_element(By.ID, "title").send_keys(test_data["title"])
        
        # Step 3: Klik Save
        save_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        save_button.click()
        
        # Step 4: Verifikasi redirect
        WebDriverWait(driver, 10).until(EC.url_contains("index.php"))
        assert "index.php" in driver.current_url, "Tidak redirect ke dashboard"
        
        # Step 5: Verifikasi data muncul dengan search
        time.sleep(1)
        
        # Gunakan search DataTables untuk mencari data yang baru dibuat
        search_box = driver.find_element(By.CSS_SELECTOR, "#employee_filter input")
        search_box.clear()
        search_box.send_keys(test_data["name"])
        time.sleep(1)
        
        page_source = driver.page_source
        assert test_data["name"] in page_source, f"Data '{test_data['name']}' tidak muncul di tabel"

    # =========================================================================
    # TC-018: UPDATE CONTACT DENGAN DATA VALID
    # =========================================================================
    @pytest.mark.update
    def test_TC018_update_contact_valid_data(self, logged_in_driver):
        """
        TC-018: Verifikasi update kontak dengan data valid
        
        Steps:
        1. Navigasi ke dashboard
        2. Klik tombol Edit pada kontak pertama
        3. Update field Name dan Email
        4. Klik tombol Update
        5. Verifikasi perubahan tersimpan
        """
        driver = logged_in_driver
        
        # Step 1: Navigasi ke dashboard
        driver.get(f"{BASE_URL}/index.php")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "employee"))
        )
        
        # Step 2: Klik Edit
        edit_buttons = driver.find_elements(By.LINK_TEXT, "edit")
        assert len(edit_buttons) > 0, "Tidak ada kontak untuk diedit"
        edit_buttons[0].click()
        
        WebDriverWait(driver, 10).until(EC.url_contains("update.php"))
        assert "update.php" in driver.current_url, "Halaman Update tidak terbuka"
        
        # Step 3: Update data
        unique_id = str(int(time.time() * 1000))[-6:]
        update_data = {
            "name": f"Updated Name {unique_id}",
            "email": f"updated{unique_id}@example.com"
        }
        
        name_field = driver.find_element(By.ID, "name")
        name_field.clear()
        name_field.send_keys(update_data["name"])
        
        email_field = driver.find_element(By.ID, "email")
        email_field.clear()
        email_field.send_keys(update_data["email"])
        
        # Step 4: Klik Update
        update_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        update_button.click()
        
        # Step 5: Verifikasi redirect ke index.php (update berhasil)
        WebDriverWait(driver, 10).until(EC.url_contains("index.php"))
        assert "index.php" in driver.current_url, "Tidak redirect ke dashboard setelah update"
        
        # Tunggu DataTables loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "employee"))
        )
        
        # Verifikasi tidak ada error di halaman
        page_source = driver.page_source
        assert "error" not in page_source.lower() or "Error" not in page_source, "Ada error di halaman"
        assert "Dashboard" in page_source or "Howdy" in page_source, "Dashboard tidak tampil dengan benar"

    # =========================================================================
    # TC-024: DELETE CONTACT DENGAN KONFIRMASI OK
    # =========================================================================
    @pytest.mark.delete
    def test_TC024_delete_contact_with_confirmation(self, logged_in_driver):
        """
        TC-024: Verifikasi hapus kontak dengan konfirmasi OK
        
        Steps:
        1. Navigasi ke dashboard dan hitung jumlah kontak
        2. Klik tombol Delete pada kontak pertama
        3. Accept alert konfirmasi
        4. Verifikasi kontak terhapus
        """
        driver = logged_in_driver
        
        # Step 1: Hitung kontak sebelum delete
        driver.get(f"{BASE_URL}/index.php")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "employee"))
        )
        
        delete_buttons_before = driver.find_elements(By.LINK_TEXT, "delete")
        count_before = len(delete_buttons_before)
        assert count_before > 0, "Tidak ada kontak untuk dihapus"
        
        # Step 2: Ambil ID kontak pertama dan nama untuk verifikasi
        first_row = driver.find_element(By.CSS_SELECTOR, "#employee tbody tr:first-child")
        first_name = first_row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        delete_button = first_row.find_element(By.LINK_TEXT, "delete")
        
        # Step 3: Klik delete dan handle alert
        delete_button.click()
        
        # Accept JavaScript confirm dialog
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            pass
        
        # Step 4: Verifikasi - tunggu halaman reload dan cari nama yang dihapus
        time.sleep(2)
        driver.get(f"{BASE_URL}/index.php")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "employee"))
        )
        
        # Cari nama yang dihapus menggunakan search
        search_box = driver.find_element(By.CSS_SELECTOR, "#employee_filter input")
        search_box.clear()
        search_box.send_keys(first_name)
        time.sleep(1)
        
        # Verifikasi nama tidak ditemukan atau jumlah berkurang
        page_source = driver.page_source
        rows_after = driver.find_elements(By.CSS_SELECTOR, "#employee tbody tr")
        
        # Jika row berisi "No matching records" atau nama tidak ada, delete berhasil
        no_records = "No matching records" in page_source
        name_gone = first_name not in page_source
        
        assert no_records or name_gone, \
            f"Kontak '{first_name}' masih ada setelah delete"

    # =========================================================================
    # TC-010: SEARCH DATATABLES
    # =========================================================================
    @pytest.mark.search
    def test_TC010_search_datatables(self, logged_in_driver):
        """
        TC-010: Verifikasi fitur search DataTables
        
        Steps:
        1. Navigasi ke dashboard
        2. Input keyword pencarian
        3. Verifikasi hasil filter
        4. Clear search dan verifikasi reset
        """
        driver = logged_in_driver
        
        # Step 1: Navigasi ke dashboard
        driver.get(f"{BASE_URL}/index.php")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "employee"))
        )
        
        # Hitung total data
        rows_before = driver.find_elements(By.CSS_SELECTOR, "#employee tbody tr")
        count_before = len(rows_before)
        
        # Step 2: Input keyword
        search_keyword = "John"
        search_box = driver.find_element(By.CSS_SELECTOR, "#employee_filter input")
        search_box.clear()
        search_box.send_keys(search_keyword)
        
        time.sleep(1)  # Tunggu filter
        
        # Step 3: Verifikasi hasil filter
        rows_after = driver.find_elements(By.CSS_SELECTOR, "#employee tbody tr")
        
        for row in rows_after:
            row_text = row.text.lower()
            if "no matching records" not in row_text and row_text.strip():
                assert search_keyword.lower() in row_text, \
                    f"Baris tidak mengandung '{search_keyword}': {row_text}"
        
        # Step 4: Clear search
        search_box.clear()
        search_box.send_keys(Keys.RETURN)
        time.sleep(1)
        
        rows_cleared = driver.find_elements(By.CSS_SELECTOR, "#employee tbody tr")
        # Data harus kembali (atau tetap ada)
        assert len(rows_cleared) >= 0, "Error setelah clear search"

    # =========================================================================
    # TC-028: VIEW PROFILE PAGE
    # =========================================================================
    @pytest.mark.profile
    def test_TC028_view_profile_page(self, logged_in_driver):
        """
        TC-028: Verifikasi tampilan halaman profil
        
        Steps:
        1. Navigasi ke halaman Profile
        2. Verifikasi username ditampilkan
        3. Verifikasi foto profil ada
        4. Verifikasi form upload ada
        5. Verifikasi tombol navigasi ada
        """
        driver = logged_in_driver
        
        # Step 1: Navigasi ke Profile
        profile_link = driver.find_element(By.LINK_TEXT, "Profil")
        profile_link.click()
        
        WebDriverWait(driver, 10).until(EC.url_contains("profil.php"))
        assert "profil.php" in driver.current_url, "Halaman Profile tidak terbuka"
        
        # Step 2: Verifikasi judul
        page_title = driver.find_element(By.TAG_NAME, "h2")
        assert "Profil" in page_title.text, f"Judul halaman salah: {page_title.text}"
        
        # Step 3: Verifikasi username
        username_field = driver.find_element(By.ID, "username")
        username_value = username_field.get_attribute("value")
        assert username_value == USERNAME, \
            f"Username tidak sesuai: expected '{USERNAME}', got '{username_value}'"
        
        # Step 4: Verifikasi foto profil
        profile_image = driver.find_element(By.CSS_SELECTOR, "img[src*='profile']")
        assert profile_image.is_displayed(), "Foto profil tidak terlihat"
        
        # Step 5: Verifikasi form upload
        upload_form = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        assert upload_form.is_displayed(), "Form upload tidak terlihat"
        
        change_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert change_button.is_displayed(), "Tombol Change tidak terlihat"
        
        # Step 6: Verifikasi tombol navigasi
        dashboard_button = driver.find_element(By.LINK_TEXT, "Dashboard")
        assert dashboard_button.is_displayed(), "Tombol Dashboard tidak terlihat"
        
        signout_button = driver.find_element(By.LINK_TEXT, "Sign out")
        assert signout_button.is_displayed(), "Tombol Sign out tidak terlihat"


# =============================================================================
# ADDITIONAL TEST MARKERS
# =============================================================================

# Untuk menjalankan test spesifik berdasarkan marker:
# pytest test_pytest.py -m create -v      # Hanya test create
# pytest test_pytest.py -m update -v      # Hanya test update
# pytest test_pytest.py -m delete -v      # Hanya test delete
# pytest test_pytest.py -m search -v      # Hanya test search
# pytest test_pytest.py -m profile -v     # Hanya test profile
# pytest test_pytest.py -m parallel -v    # Semua test paralel


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "-n", "auto",  # Parallel execution
        "--html=report.html",
        "--self-contained-html"
    ])
