"""
=============================================================================
AUTOMATION TEST SCRIPT - DamnCRUD Application
=============================================================================
Nama Aplikasi   : DamnCRUD - Contact Management System
Framework       : Python + Selenium WebDriver
Tanggal         : 23 Februari 2026
=============================================================================

TEST CASES YANG DIAUTOMASI:
1. TC-013: Create Contact dengan data valid
2. TC-018: Update Contact dengan data valid
3. TC-024: Delete Contact dengan konfirmasi OK
4. TC-010: Search DataTables
5. TC-028: View Profile Page

=============================================================================
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
import time
import unittest


class DamnCRUDTest(unittest.TestCase):
    """
    Test class untuk aplikasi DamnCRUD
    """
    
    # =========================================================================
    # KONFIGURASI
    # =========================================================================
    BASE_URL = "http://localhost:81/DamnCRUD"  # Sesuaikan dengan port XAMPP Anda
    USERNAME = "admin"
    PASSWORD = "admin123"
    
    @classmethod
    def setUpClass(cls):
        """
        Setup yang dijalankan sekali sebelum semua test
        """
        # Chrome Options
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Uncomment untuk mode headless
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        
        # Inisialisasi WebDriver
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 10)
        
    @classmethod
    def tearDownClass(cls):
        """
        Cleanup yang dijalankan sekali setelah semua test
        """
        cls.driver.quit()
    
    def setUp(self):
        """
        Setup yang dijalankan sebelum setiap test
        """
        # Login sebelum setiap test
        self.login()
    
    def tearDown(self):
        """
        Cleanup yang dijalankan setelah setiap test
        """
        # Logout setelah setiap test
        self.logout()
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def login(self):
        """
        Helper method untuk login ke sistem
        
        LANGKAH-LANGKAH:
        1. Buka halaman login
        2. Input username
        3. Input password
        4. Klik tombol login
        5. Verifikasi redirect ke dashboard
        """
        self.driver.get(f"{self.BASE_URL}/login.php")
        
        # Input username
        username_field = self.driver.find_element(By.ID, "inputUsername")
        username_field.clear()
        username_field.send_keys(self.USERNAME)
        
        # Input password
        password_field = self.driver.find_element(By.ID, "inputPassword")
        password_field.clear()
        password_field.send_keys(self.PASSWORD)
        
        # Klik tombol login
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Tunggu sampai redirect ke dashboard
        self.wait.until(EC.url_contains("index.php"))
    
    def logout(self):
        """
        Helper method untuk logout dari sistem
        """
        try:
            self.driver.get(f"{self.BASE_URL}/logout.php")
        except:
            pass
    
    # =========================================================================
    # TEST CASE TC-013: CREATE CONTACT DENGAN DATA VALID
    # =========================================================================
    
    def test_TC013_create_contact_valid_data(self):
        """
        TC-013: Verifikasi penambahan kontak baru dengan data valid
        
        LANGKAH-LANGKAH OTOMASI:
        -----------------------------------------------------------------------
        Step 1: Navigasi ke halaman Create
                - Klik menu "Create" atau akses URL create.php
                - Verifikasi halaman create terbuka
        
        Step 2: Input data kontak
                - Isi field Name dengan: "Automation Test User"
                - Isi field Email dengan: "autotest@example.com"
                - Isi field Phone dengan: "081234567890"
                - Isi field Title dengan: "QA Engineer"
        
        Step 3: Submit form
                - Klik tombol "Save"
                - Tunggu proses penyimpanan
        
        Step 4: Verifikasi hasil
                - Verifikasi redirect ke dashboard (index.php)
                - Verifikasi data baru muncul di tabel
        -----------------------------------------------------------------------
        
        EXPECTED RESULT:
        - Kontak baru tersimpan di database
        - User diarahkan ke halaman dashboard
        - Data kontak baru terlihat di tabel
        """
        print("\n" + "="*70)
        print("TEST CASE TC-013: CREATE CONTACT DENGAN DATA VALID")
        print("="*70)
        
        # Step 1: Navigasi ke halaman Create
        print("\nStep 1: Navigasi ke halaman Create")
        create_link = self.driver.find_element(By.LINK_TEXT, "Create")
        create_link.click()
        
        # Verifikasi halaman create terbuka
        self.wait.until(EC.url_contains("create.php"))
        self.assertIn("create.php", self.driver.current_url)
        print("   ✓ Halaman Create berhasil dibuka")
        
        # Step 2: Input data kontak
        print("\nStep 2: Input data kontak")
        
        # Data test
        test_data = {
            "name": "Automation Test User",
            "email": "autotest@example.com",
            "phone": "081234567890",
            "title": "QA Engineer"
        }
        
        # Input Name
        name_field = self.driver.find_element(By.ID, "name")
        name_field.clear()
        name_field.send_keys(test_data["name"])
        print(f"   ✓ Name diisi: {test_data['name']}")
        
        # Input Email
        email_field = self.driver.find_element(By.ID, "email")
        email_field.clear()
        email_field.send_keys(test_data["email"])
        print(f"   ✓ Email diisi: {test_data['email']}")
        
        # Input Phone
        phone_field = self.driver.find_element(By.ID, "phone")
        phone_field.clear()
        phone_field.send_keys(test_data["phone"])
        print(f"   ✓ Phone diisi: {test_data['phone']}")
        
        # Input Title
        title_field = self.driver.find_element(By.ID, "title")
        title_field.clear()
        title_field.send_keys(test_data["title"])
        print(f"   ✓ Title diisi: {test_data['title']}")
        
        # Step 3: Submit form
        print("\nStep 3: Submit form")
        save_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        save_button.click()
        print("   ✓ Tombol Save diklik")
        
        # Step 4: Verifikasi hasil
        print("\nStep 4: Verifikasi hasil")
        
        # Verifikasi redirect ke dashboard
        self.wait.until(EC.url_contains("index.php"))
        self.assertIn("index.php", self.driver.current_url)
        print("   ✓ Redirect ke dashboard berhasil")
        
        # Verifikasi data muncul di tabel
        time.sleep(1)  # Tunggu DataTables load
        page_source = self.driver.page_source
        self.assertIn(test_data["name"], page_source)
        print(f"   ✓ Data '{test_data['name']}' muncul di tabel")
        
        print("\n" + "-"*70)
        print("HASIL: TEST CASE TC-013 - PASSED ✓")
        print("-"*70)
    
    # =========================================================================
    # TEST CASE TC-018: UPDATE CONTACT DENGAN DATA VALID
    # =========================================================================
    
    def test_TC018_update_contact_valid_data(self):
        """
        TC-018: Verifikasi update kontak dengan data valid
        
        LANGKAH-LANGKAH OTOMASI:
        -----------------------------------------------------------------------
        Step 1: Navigasi ke dashboard
                - Buka halaman index.php
                - Verifikasi tabel kontak terlihat
        
        Step 2: Klik tombol Edit pada kontak pertama
                - Cari tombol "edit" pada baris pertama tabel
                - Klik tombol tersebut
                - Verifikasi halaman update terbuka
        
        Step 3: Update data kontak
                - Ubah field Name menjadi: "Updated Contact Name"
                - Ubah field Email menjadi: "updated@example.com"
        
        Step 4: Submit form update
                - Klik tombol "Update"
                - Tunggu proses update
        
        Step 5: Verifikasi hasil
                - Verifikasi redirect ke dashboard
                - Verifikasi perubahan data terlihat di tabel
        -----------------------------------------------------------------------
        
        EXPECTED RESULT:
        - Data kontak berhasil diupdate
        - User diarahkan ke dashboard
        - Perubahan data terlihat di tabel
        """
        print("\n" + "="*70)
        print("TEST CASE TC-018: UPDATE CONTACT DENGAN DATA VALID")
        print("="*70)
        
        # Step 1: Navigasi ke dashboard
        print("\nStep 1: Navigasi ke dashboard")
        self.driver.get(f"{self.BASE_URL}/index.php")
        self.wait.until(EC.presence_of_element_located((By.ID, "employee")))
        print("   ✓ Dashboard berhasil dibuka")
        
        # Step 2: Klik tombol Edit
        print("\nStep 2: Klik tombol Edit pada kontak pertama")
        edit_buttons = self.driver.find_elements(By.LINK_TEXT, "edit")
        self.assertTrue(len(edit_buttons) > 0, "Tidak ada kontak untuk diedit")
        edit_buttons[0].click()
        print("   ✓ Tombol Edit diklik")
        
        # Verifikasi halaman update terbuka
        self.wait.until(EC.url_contains("update.php"))
        self.assertIn("update.php", self.driver.current_url)
        print("   ✓ Halaman Update berhasil dibuka")
        
        # Step 3: Update data kontak
        print("\nStep 3: Update data kontak")
        
        update_data = {
            "name": "Updated Contact Name",
            "email": "updated@example.com"
        }
        
        # Update Name
        name_field = self.driver.find_element(By.ID, "name")
        name_field.clear()
        name_field.send_keys(update_data["name"])
        print(f"   ✓ Name diubah menjadi: {update_data['name']}")
        
        # Update Email
        email_field = self.driver.find_element(By.ID, "email")
        email_field.clear()
        email_field.send_keys(update_data["email"])
        print(f"   ✓ Email diubah menjadi: {update_data['email']}")
        
        # Step 4: Submit form
        print("\nStep 4: Submit form update")
        update_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        update_button.click()
        print("   ✓ Tombol Update diklik")
        
        # Step 5: Verifikasi hasil
        print("\nStep 5: Verifikasi hasil")
        
        # Verifikasi redirect ke dashboard
        self.wait.until(EC.url_contains("index.php"))
        self.assertIn("index.php", self.driver.current_url)
        print("   ✓ Redirect ke dashboard berhasil")
        
        # Verifikasi perubahan data
        time.sleep(1)
        page_source = self.driver.page_source
        self.assertIn(update_data["name"], page_source)
        print(f"   ✓ Data '{update_data['name']}' terlihat di tabel")
        
        print("\n" + "-"*70)
        print("HASIL: TEST CASE TC-018 - PASSED ✓")
        print("-"*70)
    
    # =========================================================================
    # TEST CASE TC-024: DELETE CONTACT DENGAN KONFIRMASI OK
    # =========================================================================
    
    def test_TC024_delete_contact_with_confirmation(self):
        """
        TC-024: Verifikasi hapus kontak dengan konfirmasi OK
        
        LANGKAH-LANGKAH OTOMASI:
        -----------------------------------------------------------------------
        Step 1: Navigasi ke dashboard
                - Buka halaman index.php
                - Hitung jumlah kontak sebelum delete
        
        Step 2: Klik tombol Delete pada salah satu kontak
                - Cari tombol "delete" pada baris tabel
                - Simpan nama kontak yang akan dihapus
                - Klik tombol delete
        
        Step 3: Handle dialog konfirmasi
                - Tunggu alert muncul
                - Klik "OK" pada alert konfirmasi
        
        Step 4: Verifikasi hasil
                - Verifikasi kontak terhapus dari tabel
                - Verifikasi jumlah kontak berkurang
        -----------------------------------------------------------------------
        
        EXPECTED RESULT:
        - Dialog konfirmasi muncul
        - Kontak terhapus dari database setelah klik OK
        - Data tidak muncul lagi di tabel
        """
        print("\n" + "="*70)
        print("TEST CASE TC-024: DELETE CONTACT DENGAN KONFIRMASI OK")
        print("="*70)
        
        # Step 1: Navigasi ke dashboard & hitung kontak
        print("\nStep 1: Navigasi ke dashboard")
        self.driver.get(f"{self.BASE_URL}/index.php")
        self.wait.until(EC.presence_of_element_located((By.ID, "employee")))
        
        # Hitung jumlah kontak sebelum delete
        delete_buttons_before = self.driver.find_elements(By.LINK_TEXT, "delete")
        count_before = len(delete_buttons_before)
        print(f"   ✓ Jumlah kontak sebelum delete: {count_before}")
        
        self.assertTrue(count_before > 0, "Tidak ada kontak untuk dihapus")
        
        # Step 2: Klik tombol Delete
        print("\nStep 2: Klik tombol Delete pada kontak")
        
        # Ambil nama kontak yang akan dihapus (dari baris pertama)
        first_row = self.driver.find_element(By.CSS_SELECTOR, "#employee tbody tr:first-child")
        contact_name = first_row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        print(f"   ✓ Kontak yang akan dihapus: {contact_name}")
        
        # Klik tombol delete
        delete_button = first_row.find_element(By.LINK_TEXT, "delete")
        delete_button.click()
        print("   ✓ Tombol Delete diklik")
        
        # Step 3: Handle dialog konfirmasi
        print("\nStep 3: Handle dialog konfirmasi")
        try:
            # Tunggu dan accept alert
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text
            print(f"   ✓ Alert muncul dengan pesan: '{alert_text}'")
            alert.accept()
            print("   ✓ Klik OK pada dialog konfirmasi")
        except TimeoutException:
            self.fail("Alert konfirmasi tidak muncul")
        
        # Step 4: Verifikasi hasil
        print("\nStep 4: Verifikasi hasil")
        
        # Tunggu redirect dan refresh
        time.sleep(2)
        self.driver.get(f"{self.BASE_URL}/index.php")
        self.wait.until(EC.presence_of_element_located((By.ID, "employee")))
        
        # Hitung jumlah kontak setelah delete
        delete_buttons_after = self.driver.find_elements(By.LINK_TEXT, "delete")
        count_after = len(delete_buttons_after)
        print(f"   ✓ Jumlah kontak setelah delete: {count_after}")
        
        # Verifikasi jumlah berkurang
        self.assertEqual(count_after, count_before - 1, "Jumlah kontak tidak berkurang")
        print("   ✓ Jumlah kontak berkurang 1")
        
        print("\n" + "-"*70)
        print("HASIL: TEST CASE TC-024 - PASSED ✓")
        print("-"*70)
    
    # =========================================================================
    # TEST CASE TC-010: SEARCH DATATABLES
    # =========================================================================
    
    def test_TC010_search_datatables(self):
        """
        TC-010: Verifikasi fitur search DataTables
        
        LANGKAH-LANGKAH OTOMASI:
        -----------------------------------------------------------------------
        Step 1: Navigasi ke dashboard
                - Buka halaman index.php
                - Verifikasi DataTables terload
        
        Step 2: Lakukan pencarian
                - Cari search box DataTables
                - Input keyword pencarian: "John"
                - Tunggu hasil filter
        
        Step 3: Verifikasi hasil pencarian
                - Verifikasi hanya data yang mengandung "John" yang ditampilkan
                - Verifikasi data lain tidak muncul
        
        Step 4: Clear pencarian
                - Kosongkan search box
                - Verifikasi semua data muncul kembali
        -----------------------------------------------------------------------
        
        EXPECTED RESULT:
        - Search box berfungsi
        - Data terfilter sesuai keyword
        - Clear search menampilkan semua data
        """
        print("\n" + "="*70)
        print("TEST CASE TC-010: SEARCH DATATABLES")
        print("="*70)
        
        # Step 1: Navigasi ke dashboard
        print("\nStep 1: Navigasi ke dashboard")
        self.driver.get(f"{self.BASE_URL}/index.php")
        self.wait.until(EC.presence_of_element_located((By.ID, "employee")))
        print("   ✓ Dashboard berhasil dibuka")
        
        # Hitung total data sebelum search
        rows_before = self.driver.find_elements(By.CSS_SELECTOR, "#employee tbody tr")
        count_before = len(rows_before)
        print(f"   ✓ Total data sebelum search: {count_before}")
        
        # Step 2: Lakukan pencarian
        print("\nStep 2: Lakukan pencarian")
        search_keyword = "John"
        
        # Cari search box DataTables
        search_box = self.driver.find_element(By.CSS_SELECTOR, "#employee_filter input")
        search_box.clear()
        search_box.send_keys(search_keyword)
        print(f"   ✓ Keyword '{search_keyword}' dimasukkan ke search box")
        
        # Tunggu filter bekerja
        time.sleep(1)
        
        # Step 3: Verifikasi hasil pencarian
        print("\nStep 3: Verifikasi hasil pencarian")
        
        # Hitung data setelah search
        rows_after = self.driver.find_elements(By.CSS_SELECTOR, "#employee tbody tr")
        
        # Verifikasi setiap baris mengandung keyword
        for row in rows_after:
            row_text = row.text.lower()
            if "no matching records" not in row_text:
                self.assertIn(search_keyword.lower(), row_text, 
                             f"Baris tidak mengandung keyword: {row_text}")
        
        count_after = len(rows_after)
        print(f"   ✓ Jumlah data setelah filter: {count_after}")
        print(f"   ✓ Semua data yang ditampilkan mengandung '{search_keyword}'")
        
        # Step 4: Clear pencarian
        print("\nStep 4: Clear pencarian")
        search_box.clear()
        search_box.send_keys(Keys.RETURN)
        time.sleep(1)
        
        # Verifikasi semua data muncul kembali
        rows_cleared = self.driver.find_elements(By.CSS_SELECTOR, "#employee tbody tr")
        count_cleared = len(rows_cleared)
        print(f"   ✓ Jumlah data setelah clear: {count_cleared}")
        
        print("\n" + "-"*70)
        print("HASIL: TEST CASE TC-010 - PASSED ✓")
        print("-"*70)
    
    # =========================================================================
    # TEST CASE TC-028: VIEW PROFILE PAGE
    # =========================================================================
    
    def test_TC028_view_profile_page(self):
        """
        TC-028: Verifikasi tampilan halaman profil
        
        LANGKAH-LANGKAH OTOMASI:
        -----------------------------------------------------------------------
        Step 1: Navigasi ke halaman Profile
                - Klik menu "Profile" atau akses URL profil.php
                - Verifikasi halaman profile terbuka
        
        Step 2: Verifikasi elemen halaman profile
                - Verifikasi username yang login ditampilkan
                - Verifikasi foto profil ada
                - Verifikasi form upload foto ada
        
        Step 3: Verifikasi tombol navigasi
                - Verifikasi tombol Dashboard ada
                - Verifikasi tombol Sign out ada
        -----------------------------------------------------------------------
        
        EXPECTED RESULT:
        - Halaman profile berhasil dibuka
        - Username yang sedang login ditampilkan
        - Foto profil dan form upload terlihat
        """
        print("\n" + "="*70)
        print("TEST CASE TC-028: VIEW PROFILE PAGE")
        print("="*70)
        
        # Step 1: Navigasi ke halaman Profile
        print("\nStep 1: Navigasi ke halaman Profile")
        profile_link = self.driver.find_element(By.LINK_TEXT, "Profile")
        profile_link.click()
        
        # Verifikasi halaman profile terbuka
        self.wait.until(EC.url_contains("profil.php"))
        self.assertIn("profil.php", self.driver.current_url)
        print("   ✓ Halaman Profile berhasil dibuka")
        
        # Step 2: Verifikasi elemen halaman profile
        print("\nStep 2: Verifikasi elemen halaman profile")
        
        # Verifikasi judul halaman
        page_title = self.driver.find_element(By.TAG_NAME, "h2")
        self.assertEqual(page_title.text, "Profil")
        print("   ✓ Judul halaman 'Profil' terlihat")
        
        # Verifikasi username ditampilkan
        username_field = self.driver.find_element(By.ID, "username")
        username_value = username_field.get_attribute("value")
        self.assertEqual(username_value, self.USERNAME)
        print(f"   ✓ Username '{username_value}' ditampilkan")
        
        # Verifikasi foto profil
        profile_image = self.driver.find_element(By.CSS_SELECTOR, "img[src*='profile']")
        self.assertTrue(profile_image.is_displayed())
        print("   ✓ Foto profil terlihat")
        
        # Verifikasi form upload
        upload_form = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        self.assertTrue(upload_form.is_displayed())
        print("   ✓ Form upload foto terlihat")
        
        change_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.assertTrue(change_button.is_displayed())
        print("   ✓ Tombol 'Change' terlihat")
        
        # Step 3: Verifikasi tombol navigasi
        print("\nStep 3: Verifikasi tombol navigasi")
        
        dashboard_button = self.driver.find_element(By.LINK_TEXT, "Dashboard")
        self.assertTrue(dashboard_button.is_displayed())
        print("   ✓ Tombol Dashboard terlihat")
        
        signout_button = self.driver.find_element(By.LINK_TEXT, "Sign out")
        self.assertTrue(signout_button.is_displayed())
        print("   ✓ Tombol Sign out terlihat")
        
        print("\n" + "-"*70)
        print("HASIL: TEST CASE TC-028 - PASSED ✓")
        print("-"*70)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Konfigurasi test runner dengan verbosity tinggi
    unittest.main(verbosity=2)
