"""
Create custom distribution packages for customers
Each package contains ONLY that customer's license key
"""
import json
import shutil
from pathlib import Path
from datetime import datetime

def create_customer_package(customer_name, license_key):
    """
    Create a distribution package with ONLY that customer's license
    """
    print(f"\n{'='*70}")
    print(f"Creating package for: {customer_name}")
    print(f"{'='*70}")
    
    # Load master database
    try:
        with open('licenses_db.json', 'r') as f:
            all_licenses = json.load(f)
    except FileNotFoundError:
        print("ERROR: licenses_db.json not found!")
        return False
    
    # Find this customer's license
    customer_license = None
    for lic in all_licenses:
        if lic['key'] == license_key:
            customer_license = lic
            break
    
    if not customer_license:
        print(f"ERROR: License key {license_key} not found in database!")
        return False
    
    # Create distributions folder
    dist_folder = Path("distributions")
    dist_folder.mkdir(exist_ok=True)
    
    # Create customer folder name (no spaces)
    safe_name = customer_name.replace(' ', '_').replace('/', '_')
    customer_folder = dist_folder / safe_name
    
    # Remove old package if exists
    if customer_folder.exists():
        print(f"WARNING: Removing old package...")
        shutil.rmtree(customer_folder)
    
    # Create folder structure
    customer_folder.mkdir(parents=True)
    
    print(f"Copying application files...")
    
    # Copy entire TasteParadise folder from dist
    source = Path("dist") / "TasteParadise"
    dest = customer_folder / "TasteParadise"
    
    if not source.exists():
        print(f"ERROR: dist/TasteParadise folder not found!")
        print(f"   Run: pyinstaller TasteParadise.spec --clean")
        return False
    
    shutil.copytree(source, dest)
    
    # Create custom licenses_db.json with ONLY this customer's key
    print(f"Creating custom license database...")
    custom_db = [customer_license]
    
    db_file = dest / "licenses_db.json"
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(custom_db, f, indent=2)
    
    # Create SETUP.bat
    print(f"Creating SETUP.bat...")
    setup_file = customer_folder / "SETUP.bat"
    with open(setup_file, 'w', encoding='utf-8') as f:
        f.write(f"""@echo off
title TasteParadise Restaurant Management - Setup
color 0A

echo ======================================================================
echo                    TASTE PARADISE
echo            Restaurant Management System v1.0
echo ======================================================================
echo.
echo Licensed to: {customer_license['customer']}
echo Plan: {customer_license['plan'].upper()}
echo Valid Until: {customer_license['expiry_date'][:10]}
echo.
echo Starting TasteParadise...
echo.

cd TasteParadise
TasteParadise.exe --mode both

pause
""")
    
    # Create README.txt (NO SPECIAL CHARACTERS)
    print(f"Creating README.txt...")
    readme_file = customer_folder / "README.txt"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(f"""======================================================================
                    TASTE PARADISE
          Restaurant Management System - Version 1.0
======================================================================

LICENSED TO: {customer_license['customer']}
EMAIL: {customer_license.get('email', 'N/A')}
PLAN: {customer_license['plan'].upper()}
VALID UNTIL: {customer_license['expiry_date'][:10]}

======================================================================

QUICK START GUIDE
-----------------

1. INSTALLATION:
   - Extract this folder to any location
   - Recommended: C:\\TasteParadise
   - Do NOT move files inside the TasteParadise folder

2. FIRST TIME SETUP:
   - Double-click SETUP.bat
   - Enter your license key when prompted:
   
   LICENSE KEY: {license_key}
   
   - Wait for activation (5-10 seconds)
   - Application will open automatically

3. DAILY USE:
   - Run SETUP.bat to start the application
   - Or go to TasteParadise folder and run TasteParadise.exe

4. NETWORK ACCESS (OPTIONAL):
   - After starting, note the "Network URL" displayed
   - Example: http://192.168.1.105:8002
   - Open this URL on other devices (tablets/phones/PCs)
   - All devices must be on the same WiFi network

SYSTEM REQUIREMENTS
-------------------
[OK] Windows 10 or Windows 11 (64-bit)
[OK] Minimum 4GB RAM
[OK] 500MB free disk space
[OK] Internet connection (for first-time activation)

IMPORTANT NOTES
---------------
* This license works on ONE computer only
* Do not share your license key with others
* Sharing will cause your own app to stop working
* Keep your license key safe and confidential

SUPPORT
-------
Email: [email protected]
Phone: +91 XXXXX XXXXX
Website: https://yourwebsite.com
Hours: 9 AM - 6 PM IST (Monday to Saturday)

TROUBLESHOOTING
---------------

Problem: "License key not found"
-> Make sure you entered the key correctly (see above)
-> Copy-paste the key to avoid typos

Problem: "Already activated on another computer"
-> Contact support to transfer your license
-> Email: [email protected]

Problem: "MongoDB not starting"
-> Close any other MongoDB programs
-> Restart your computer and try again

Problem: "Port 8002 already in use"
-> Close any other programs using port 8002
-> Restart the application

======================================================================
Copyright 2025 Your Company Name. All Rights Reserved.

This software is licensed exclusively to {customer_license['customer']}.
Unauthorized copying, distribution, or sharing is prohibited and will
result in immediate license revocation.

For full terms: https://yourwebsite.com/terms
======================================================================
""")
    
    # Create LICENSE.txt (NO SPECIAL CHARACTERS)
    print(f"Creating LICENSE.txt...")
    license_file = customer_folder / "LICENSE.txt"
    with open(license_file, 'w', encoding='utf-8') as f:
        f.write(f"""======================================================================
                SOFTWARE LICENSE AGREEMENT
              TASTE PARADISE RESTAURANT MANAGEMENT
======================================================================

Licensed to: {customer_license['customer']}
License Key: {license_key}
Issue Date: {datetime.now().strftime('%Y-%m-%d')}
Valid Until: {customer_license['expiry_date'][:10]}

======================================================================

IMPORTANT: READ CAREFULLY BEFORE USING THIS SOFTWARE

This License Agreement is between you ("{customer_license['customer']}")
and [Your Company Name] for the TasteParadise Restaurant Management
Software.

1. LICENSE GRANT
----------------
* You are granted ONE (1) license for ONE (1) computer
* This license cannot be transferred without authorization
* This license cannot be shared with others

2. RESTRICTIONS
---------------
You may NOT:
* Use this software on multiple computers
* Share your license key with others
* Copy or distribute the software
* Reverse engineer the software
* Rent, lease, or lend the software

3. ACTIVATION & HARDWARE BINDING
---------------------------------
* License activates on first use
* License binds to your computer's hardware ID
* Cannot be moved to another computer without authorization
* Contact support for license transfers

4. VIOLATION CONSEQUENCES
-------------------------
If you share your license key:
* Your own software will stop working
* License will be immediately revoked
* No refunds will be provided
* Legal action may be taken

5. SUPPORT & UPDATES
--------------------
* Email support for {customer_license.get('duration_days', 365)} days
* Free updates for {customer_license.get('duration_days', 365)} days
* Extended support available separately

6. WARRANTY DISCLAIMER
----------------------
This software is provided "AS IS" without warranty of any kind.
We do not guarantee uninterrupted or error-free operation.

7. LIMITATION OF LIABILITY
--------------------------
[Your Company Name] shall not be liable for any damages arising
from use or inability to use this software.

8. TERMINATION
--------------
* License terminates if you breach any term
* You must destroy all copies upon termination
* Refunds available within 7 days of purchase only

9. CONTACT INFORMATION
----------------------
Email: [email protected]
Phone: +91 XXXXX XXXXX
Website: https://yourwebsite.com

By installing and using this software, you acknowledge that you have
read this agreement and agree to be bound by its terms.

======================================================================
Copyright 2025 [Your Company Name]. All Rights Reserved.
======================================================================
""")
    
    # Create info file for your records
    info_file = customer_folder / "_PACKAGE_INFO.txt"
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write(f"""DISTRIBUTION PACKAGE INFORMATION
================================

Customer: {customer_license['customer']}
Email: {customer_license.get('email', 'N/A')}
Phone: {customer_license.get('phone', 'N/A')}
License Key: {license_key}
Plan: {customer_license['plan']}
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Valid Until: {customer_license['expiry_date'][:10]}

DO NOT INCLUDE THIS FILE IN CUSTOMER PACKAGE!
This is for your internal records only.

Package Size: ~300-500 MB (compressed)
Send via: Google Drive / Dropbox / Email
""")
    
    print(f"\n{'='*70}")
    print(f"SUCCESS: PACKAGE CREATED!")
    print(f"{'='*70}")
    print(f"Location: {customer_folder.absolute()}")
    print(f"Customer: {customer_license['customer']}")
    print(f"License: {license_key}")
    print(f"Valid Until: {customer_license['expiry_date'][:10]}")
    print(f"\nNext Steps:")
    print(f"   1. Zip the folder: {customer_folder.name}.zip")
    print(f"   2. Upload to Google Drive/Dropbox")
    print(f"   3. Send download link to customer")
    print(f"{'='*70}\n")
    
    return True


def main():
    """Interactive package creator"""
    print("\n" + "="*70)
    print(" "*15 + "TASTEPARADISE DISTRIBUTION CREATOR")
    print(" "*20 + "Solution 1: Include Database")
    print("="*70)
    
    # Load licenses
    try:
        with open('licenses_db.json', 'r') as f:
            licenses = json.load(f)
    except FileNotFoundError:
        print("\nERROR: licenses_db.json not found!")
        print("   Run: python license_generator.py to create licenses first")
        return
    
    if not licenses:
        print("\nERROR: No licenses found in database!")
        print("   Run: python license_generator.py to create licenses first")
        return
    
    # Show available licenses
    print("\nAVAILABLE LICENSES:")
    print("-" * 70)
    for i, lic in enumerate(licenses, 1):
        status = "ACTIVATED" if lic.get('activated') else "NOT ACTIVATED"
        print(f"{i}. {lic['customer']}")
        print(f"   Key: {lic['key']}")
        print(f"   Email: {lic.get('email', 'N/A')}")
        print(f"   Plan: {lic['plan'].upper()} | Status: {status}")
        print(f"   Expires: {lic['expiry_date'][:10]}")
        print()
    
    # Create packages
    print("=" * 70)
    print("CREATE DISTRIBUTION PACKAGES:")
    print("  1. Create package for ALL customers")
    print("  2. Create package for SPECIFIC customer")
    print("  3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        # Create for all customers
        print(f"\nCreating packages for {len(licenses)} customers...\n")
        success_count = 0
        
        for lic in licenses:
            if create_customer_package(lic['customer'], lic['key']):
                success_count += 1
        
        print(f"\n{'='*70}")
        print(f"COMPLETED: Created {success_count} out of {len(licenses)} packages")
        print(f"{'='*70}")
        print(f"Check 'distributions/' folder")
        print(f"Zip each customer folder and send")
        print(f"{'='*70}\n")
    
    elif choice == "2":
        # Create for specific customer
        num = input(f"\nEnter customer number (1-{len(licenses)}): ").strip()
        try:
            idx = int(num) - 1
            if 0 <= idx < len(licenses):
                lic = licenses[idx]
                create_customer_package(lic['customer'], lic['key'])
            else:
                print("ERROR: Invalid number!")
        except ValueError:
            print("ERROR: Please enter a valid number!")
    
    elif choice == "3":
        print("\nGoodbye!")
    else:
        print("\nERROR: Invalid choice!")


if __name__ == "__main__":
    main()
