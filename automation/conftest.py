"""
=============================================================================
PYTEST CONFTEST - Shared Fixtures & Hooks
=============================================================================
File: conftest.py
Berisi fixtures dan hooks yang digunakan bersama oleh semua test
=============================================================================
"""

import pytest
import os
from datetime import datetime


# =============================================================================
# PYTEST HOOKS
# =============================================================================

def pytest_configure(config):
    """
    Hook yang dijalankan saat pytest dikonfigurasi.
    Menambahkan metadata ke report.
    """
    # Hanya set metadata jika pytest-html tersedia
    if hasattr(config, '_metadata'):
        config._metadata['Project Name'] = 'DamnCRUD Automation Test'
        config._metadata['Test Framework'] = 'Pytest + Selenium'
        config._metadata['Executed By'] = os.environ.get('USER', 'CI/CD Pipeline')
        config._metadata['Execution Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        config._metadata['Base URL'] = os.environ.get('BASE_URL', 'http://localhost:81/DamnCRUD')
        config._metadata['Parallel Workers'] = 'Auto (pytest-xdist)'


def pytest_collection_modifyitems(config, items):
    """
    Hook untuk modifikasi test items setelah collection.
    Menandai semua test dengan marker 'parallel'.
    """
    for item in items:
        if "TestDamnCRUD" in str(item.cls):
            item.add_marker(pytest.mark.parallel)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook untuk menambahkan informasi tambahan ke report.
    """
    outcome = yield
    report = outcome.get_result()
    
    # Tambahkan docstring sebagai description
    if report.when == "call":
        report.description = str(item.function.__doc__ or "")


# =============================================================================
# SESSION FIXTURES
# =============================================================================

@pytest.fixture(scope="session", autouse=True)
def test_session_info():
    """
    Fixture session yang menampilkan info saat test dimulai dan selesai.
    """
    print("\n" + "="*70)
    print("STARTING TEST SESSION")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {os.environ.get('BASE_URL', 'http://localhost:81/DamnCRUD')}")
    print("="*70 + "\n")
    
    yield
    
    print("\n" + "="*70)
    print("TEST SESSION COMPLETED")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")


# =============================================================================
# UTILITY FIXTURES
# =============================================================================

@pytest.fixture
def base_url():
    """
    Fixture untuk mendapatkan base URL dari environment variable.
    """
    return os.environ.get('BASE_URL', 'http://localhost:81/DamnCRUD')


@pytest.fixture
def credentials():
    """
    Fixture untuk mendapatkan kredensial login.
    """
    return {
        'username': os.environ.get('TEST_USERNAME', 'admin'),
        'password': os.environ.get('TEST_PASSWORD', 'admin123')
    }


# =============================================================================
# SCREENSHOT ON FAILURE (untuk debugging)
# =============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Hook untuk mengambil screenshot saat test gagal.
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == 'call' and rep.failed:
        # Cek apakah ada driver fixture
        if 'driver' in item.funcargs or 'logged_in_driver' in item.funcargs:
            driver = item.funcargs.get('driver') or item.funcargs.get('logged_in_driver')
            if driver:
                try:
                    # Buat folder screenshots jika belum ada
                    screenshot_dir = 'screenshots'
                    if not os.path.exists(screenshot_dir):
                        os.makedirs(screenshot_dir)
                    
                    # Simpan screenshot
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    screenshot_path = f"{screenshot_dir}/{item.name}_{timestamp}.png"
                    driver.save_screenshot(screenshot_path)
                    print(f"\n📸 Screenshot saved: {screenshot_path}")
                except Exception as e:
                    print(f"\n⚠️ Failed to save screenshot: {str(e)}")
