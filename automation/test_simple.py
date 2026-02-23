"""
=============================================================================
AUTOMATION TEST SCRIPT - DamnCRUD Application (Auto Driver Version)
=============================================================================
Versi ini menggunakan webdriver-manager untuk otomatis download ChromeDriver
Install: pip install selenium webdriver-manager
=============================================================================
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# =============================================================================
# KONFIGURASI
# =============================================================================
BASE_URL = "http://localhost:81/DamnCRUD"  # Sesuaikan port jika berbeda
USERNAME = "admin"
PASSWORD = "admin123"

# =============================================================================
# SETUP DRIVER
# =============================================================================
def setup_driver():
    """Setup Chrome driver dengan webdriver-manager"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--headless")  # Uncomment untuk mode headless
    
    # Auto download & setup ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def login(driver):
    """Login ke sistem"""
    driver.get(f"{BASE_URL}/login.php")
    driver.find_element(By.ID, "inputUsername").send_keys(USERNAME)
    driver.find_element(By.ID, "inputPassword").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.url_contains("index.php"))
    print("✓ Login berhasil")

def logout(driver):
    """Logout dari sistem"""
    driver.get(f"{BASE_URL}/logout.php")
    print("✓ Logout berhasil")

# =============================================================================
# TEST CASE TC-013: CREATE CONTACT
# =============================================================================
def test_create_contact(driver):
    """
    TC-013: Create Contact dengan data valid
    """
    print("\n" + "="*60)
    print("TC-013: CREATE CONTACT DENGAN DATA VALID")
    print("="*60)
    
    # Step 1: Klik menu Create
    driver.find_element(By.LINK_TEXT, "Create").click()
    WebDriverWait(driver, 10).until(EC.url_contains("create.php"))
    print("Step 1: ✓ Halaman Create dibuka")
    
    # Step 2: Input data
    test_data = {
        "name": "Selenium Test User",
        "email": "selenium@test.com",
        "phone": "081234567890",
        "title": "Automation Tester"
    }
    
    driver.find_element(By.ID, "name").send_keys(test_data["name"])
    driver.find_element(By.ID, "email").send_keys(test_data["email"])
    driver.find_element(By.ID, "phone").send_keys(test_data["phone"])
    driver.find_element(By.ID, "title").send_keys(test_data["title"])
    print(f"Step 2: ✓ Data diinput: {test_data['name']}")
    
    # Step 3: Klik Save
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    print("Step 3: ✓ Tombol Save diklik")
    
    # Step 4: Verifikasi
    WebDriverWait(driver, 10).until(EC.url_contains("index.php"))
    assert test_data["name"] in driver.page_source
    print(f"Step 4: ✓ Data '{test_data['name']}' muncul di tabel")
    
    print("\n>>> HASIL: TC-013 PASSED ✓")
    return True

# =============================================================================
# TEST CASE TC-018: UPDATE CONTACT
# =============================================================================
def test_update_contact(driver):
    """
    TC-018: Update Contact dengan data valid
    """
    print("\n" + "="*60)
    print("TC-018: UPDATE CONTACT DENGAN DATA VALID")
    print("="*60)
    
    # Step 1: Buka dashboard
    driver.get(f"{BASE_URL}/index.php")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "employee")))
    print("Step 1: ✓ Dashboard dibuka")
    
    # Step 2: Klik Edit
    edit_buttons = driver.find_elements(By.LINK_TEXT, "edit")
    if len(edit_buttons) > 0:
        edit_buttons[0].click()
        WebDriverWait(driver, 10).until(EC.url_contains("update.php"))
        print("Step 2: ✓ Halaman Update dibuka")
    else:
        print("Step 2: ✗ Tidak ada data untuk diupdate")
        return False
    
    # Step 3: Update data
    name_field = driver.find_element(By.ID, "name")
    name_field.clear()
    new_name = "Updated By Selenium"
    name_field.send_keys(new_name)
    print(f"Step 3: ✓ Name diubah: {new_name}")
    
    # Step 4: Klik Update
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    print("Step 4: ✓ Tombol Update diklik")
    
    # Step 5: Verifikasi
    WebDriverWait(driver, 10).until(EC.url_contains("index.php"))
    assert new_name in driver.page_source
    print(f"Step 5: ✓ Data '{new_name}' terlihat di tabel")
    
    print("\n>>> HASIL: TC-018 PASSED ✓")
    return True

# =============================================================================
# TEST CASE TC-024: DELETE CONTACT
# =============================================================================
def test_delete_contact(driver):
    """
    TC-024: Delete Contact dengan konfirmasi OK
    """
    print("\n" + "="*60)
    print("TC-024: DELETE CONTACT DENGAN KONFIRMASI OK")
    print("="*60)
    
    # Step 1: Buka dashboard & hitung data
    driver.get(f"{BASE_URL}/index.php")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "employee")))
    
    delete_buttons = driver.find_elements(By.LINK_TEXT, "delete")
    count_before = len(delete_buttons)
    print(f"Step 1: ✓ Jumlah kontak sebelum: {count_before}")
    
    if count_before == 0:
        print("Step 1: ✗ Tidak ada data untuk dihapus")
        return False
    
    # Step 2: Klik Delete
    delete_buttons[0].click()
    print("Step 2: ✓ Tombol Delete diklik")
    
    # Step 3: Handle alert
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert.accept()
    print("Step 3: ✓ Alert konfirmasi di-accept")
    
    # Step 4: Verifikasi
    time.sleep(1)
    driver.get(f"{BASE_URL}/index.php")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "employee")))
    
    delete_buttons_after = driver.find_elements(By.LINK_TEXT, "delete")
    count_after = len(delete_buttons_after)
    print(f"Step 4: ✓ Jumlah kontak setelah: {count_after}")
    
    assert count_after == count_before - 1
    print("Step 4: ✓ Kontak berhasil dihapus")
    
    print("\n>>> HASIL: TC-024 PASSED ✓")
    return True

# =============================================================================
# TEST CASE TC-010: SEARCH DATATABLES
# =============================================================================
def test_search_datatables(driver):
    """
    TC-010: Search DataTables
    """
    print("\n" + "="*60)
    print("TC-010: SEARCH DATATABLES")
    print("="*60)
    
    # Step 1: Buka dashboard
    driver.get(f"{BASE_URL}/index.php")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "employee")))
    print("Step 1: ✓ Dashboard dibuka")
    
    # Step 2: Input keyword pencarian
    search_keyword = "John"
    search_box = driver.find_element(By.CSS_SELECTOR, "#employee_filter input")
    search_box.send_keys(search_keyword)
    print(f"Step 2: ✓ Keyword '{search_keyword}' diinputkan")
    
    time.sleep(1)  # Tunggu filter
    
    # Step 3: Verifikasi hasil
    rows = driver.find_elements(By.CSS_SELECTOR, "#employee tbody tr")
    print(f"Step 3: ✓ Ditemukan {len(rows)} baris hasil")
    
    for row in rows:
        row_text = row.text.lower()
        if "no matching records" not in row_text:
            assert search_keyword.lower() in row_text
    print(f"Step 3: ✓ Semua hasil mengandung '{search_keyword}'")
    
    # Step 4: Clear search
    search_box.clear()
    time.sleep(1)
    print("Step 4: ✓ Search box dikosongkan")
    
    print("\n>>> HASIL: TC-010 PASSED ✓")
    return True

# =============================================================================
# TEST CASE TC-028: VIEW PROFILE
# =============================================================================
def test_view_profile(driver):
    """
    TC-028: View Profile Page
    """
    print("\n" + "="*60)
    print("TC-028: VIEW PROFILE PAGE")
    print("="*60)
    
    # Step 1: Klik menu Profile
    driver.find_element(By.LINK_TEXT, "Profile").click()
    WebDriverWait(driver, 10).until(EC.url_contains("profil.php"))
    print("Step 1: ✓ Halaman Profile dibuka")
    
    # Step 2: Verifikasi judul
    title = driver.find_element(By.TAG_NAME, "h2")
    assert title.text == "Profil"
    print("Step 2: ✓ Judul 'Profil' terlihat")
    
    # Step 3: Verifikasi username
    username_field = driver.find_element(By.ID, "username")
    assert username_field.get_attribute("value") == USERNAME
    print(f"Step 3: ✓ Username '{USERNAME}' ditampilkan")
    
    # Step 4: Verifikasi elemen lain
    profile_img = driver.find_element(By.CSS_SELECTOR, "img[src*='profile']")
    assert profile_img.is_displayed()
    print("Step 4: ✓ Foto profil terlihat")
    
    upload_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    assert upload_input.is_displayed()
    print("Step 4: ✓ Form upload terlihat")
    
    print("\n>>> HASIL: TC-028 PASSED ✓")
    return True

# =============================================================================
# MAIN EXECUTION
# =============================================================================
def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║        AUTOMATION TEST - DamnCRUD Application            ║
    ║        Framework: Python + Selenium WebDriver            ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    driver = setup_driver()
    results = {}
    
    try:
        # Login
        login(driver)
        
        # Jalankan test cases
        results["TC-013 Create Contact"] = test_create_contact(driver)
        results["TC-018 Update Contact"] = test_update_contact(driver)
        results["TC-024 Delete Contact"] = test_delete_contact(driver)
        results["TC-010 Search DataTables"] = test_search_datatables(driver)
        results["TC-028 View Profile"] = test_view_profile(driver)
        
        # Logout
        logout(driver)
        
    except Exception as e:
        print(f"\n!!! ERROR: {str(e)}")
    finally:
        driver.quit()
    
    # Print summary
    print("\n" + "="*60)
    print("RINGKASAN HASIL TEST")
    print("="*60)
    for test_name, result in results.items():
        status = "PASSED ✓" if result else "FAILED ✗"
        print(f"  {test_name}: {status}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    print(f"\nTotal: {passed}/{total} test cases passed")
    print("="*60)

if __name__ == "__main__":
    main()
