"""
Script untuk menjalankan Automation Test DamnCRUD
Jalankan dengan: python run_tests.py
"""

import subprocess
import sys
import os

def install_requirements():
    """Install dependencies dari requirements.txt"""
    print("="*60)
    print("INSTALLING REQUIREMENTS...")
    print("="*60)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("\n")

def run_all_tests():
    """Jalankan semua test cases"""
    print("="*60)
    print("RUNNING ALL TEST CASES")
    print("="*60)
    subprocess.call([sys.executable, "test_damncrud.py"])

def run_single_test(test_name):
    """Jalankan test case tertentu"""
    print(f"="*60)
    print(f"RUNNING TEST: {test_name}")
    print(f"="*60)
    subprocess.call([
        sys.executable, "-m", "pytest", 
        f"test_damncrud.py::DamnCRUDTest::{test_name}", 
        "-v"
    ])

def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     AUTOMATION TEST RUNNER - DamnCRUD Application        ║
    ╠══════════════════════════════════════════════════════════╣
    ║  1. Install Requirements                                  ║
    ║  2. Run All Tests                                        ║
    ║  3. Run TC-013: Create Contact                           ║
    ║  4. Run TC-018: Update Contact                           ║
    ║  5. Run TC-024: Delete Contact                           ║
    ║  6. Run TC-010: Search DataTables                        ║
    ║  7. Run TC-028: View Profile                             ║
    ║  0. Exit                                                 ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    choice = input("Pilih opsi (0-7): ")
    
    if choice == "1":
        install_requirements()
    elif choice == "2":
        run_all_tests()
    elif choice == "3":
        run_single_test("test_TC013_create_contact_valid_data")
    elif choice == "4":
        run_single_test("test_TC018_update_contact_valid_data")
    elif choice == "5":
        run_single_test("test_TC024_delete_contact_with_confirmation")
    elif choice == "6":
        run_single_test("test_TC010_search_datatables")
    elif choice == "7":
        run_single_test("test_TC028_view_profile_page")
    elif choice == "0":
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Pilihan tidak valid!")

if __name__ == "__main__":
    # Pindah ke direktori script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
